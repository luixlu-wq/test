import httpx
from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import WorkItem, WorkItemFilter, WorkItemType
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.connectors import DevOpsConnector


def test_map_work_item_from_azure_extracts_related_refs() -> None:
    connector = DevOpsConnector()
    work_item = connector.map_work_item_from_azure(
        {
            "id": 654,
            "fields": {
                "System.WorkItemType": "User Story",
                "System.Title": "Create project from template",
                "System.State": "Ready for Test",
            },
            "relations": [
                {
                    "rel": "System.LinkTypes.Related",
                    "url": "https://dev.azure.com/org/project/_apis/wit/workItems/777",
                    "attributes": {"name": "Related"},
                }
            ],
        }
    )
    assert work_item.related_work_item_refs
    assert work_item.related_work_item_refs[0]["work_item_external_id"] == "777"


def test_live_query_enriches_comments() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith('/_apis/wit/wiql'):
            return httpx.Response(200, json={"workItems": [{"id": 101}]})
        if request.url.path.endswith('/_apis/wit/workitemsbatch'):
            return httpx.Response(200, json={
                "value": [
                    {
                        "id": 101,
                        "fields": {
                            "System.WorkItemType": "Bug",
                            "System.Title": "Upload project definition fails",
                            "System.State": "Active",
                        },
                        "relations": [
                            {
                                "rel": "System.LinkTypes.Hierarchy-Reverse",
                                "url": "https://dev.azure.com/org/project/_apis/wit/workItems/202",
                                "attributes": {"name": "Parent"},
                            }
                        ],
                    }
                ]
            })
        if request.url.path.endswith('/_apis/wit/workItems/101/comments'):
            return httpx.Response(200, json={
                "comments": [
                    {"text": "<div>Repro: upload a PDF larger than 10MB and click submit.</div>"},
                    {"text": "<div>Observed error banner on review step.</div>"},
                ]
            })
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client = httpx.Client(transport=httpx.MockTransport(handler), timeout=20.0)
    connector = DevOpsConnector(
        base_url="https://dev.azure.com/OPS-GSIC/Business%20Experience/_workitems/recentlyupdated/",
        pat="token",
        client=client,
    )
    items = connector.query_work_items("proj_01", WorkItemFilter(type=[WorkItemType.DEFECT]))
    assert len(items) == 1
    assert items[0].comments[0].startswith("Repro:")
    assert items[0].related_work_item_refs[0]["relation_type"] == "System.LinkTypes.Hierarchy-Reverse"


def test_context_sync_endpoint_updates_comments(monkeypatch) -> None:
    store.projects.clear()
    store.work_items.clear()

    work_item = WorkItem(
        id="wk_101",
        external_id="101",
        type=WorkItemType.DEFECT,
        title="Upload project definition fails",
        related_work_item_refs=[{"relation_type": "System.LinkTypes.Related", "work_item_external_id": "777", "type": "ado_work_item_relation", "value": "https://example/777"}],
    )
    store.work_items[work_item.id] = work_item

    def fake_sync(self, item):
        item.comments = ["Repro: upload a PDF larger than 10MB and click submit.", "Observed error banner on review step."]
        return item

    monkeypatch.setattr(DevOpsConnector, "sync_work_item_context", fake_sync)

    client = TestClient(app)
    response = client.post("/api/v1/projects/proj_01/work-items/wk_101/context/sync")
    assert response.status_code == 200
    payload = response.json()
    assert payload["comment_count"] == 2
    assert payload["related_work_item_count"] == 1
    assert payload["work_item"]["comments"][0].startswith("Repro:")
