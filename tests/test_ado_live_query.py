from ai_qa_tester.models.contracts import WorkItemFilter, WorkItemType
import httpx
from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.connectors import DevOpsConnector


def test_build_wiql_includes_filters() -> None:
    connector = DevOpsConnector(base_url="https://dev.azure.com/OPS-GSIC/Business%20Experience/_workitems/recentlyupdated/", pat="token")
    wiql = connector.build_wiql(
        "Business Experience",
        filters=WorkItemFilter(
            state=["Ready for Test"],
            assignee=["qa.user@company.com"],
            type=[WorkItemType.STORY],
            tags=["search"],
            sprint=["Sprint 12"],
            area_path=["Business/Search"],
        ),
    )
    assert "[System.TeamProject] = 'Business Experience'" in wiql
    assert "[System.State] IN ('Ready for Test')" in wiql
    assert "[System.AssignedTo] IN ('qa.user@company.com')" in wiql
    assert "[System.WorkItemType] IN ('User Story', 'Product Backlog Item', 'Story')" in wiql
    assert "[System.IterationPath] CONTAINS 'Sprint 12'" in wiql
    assert "[System.AreaPath] CONTAINS 'Business/Search'" in wiql
    assert "[System.Tags] CONTAINS 'search'" in wiql


def test_live_query_work_items_uses_wiql_and_batch() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith('/_apis/wit/wiql'):
            data = request.read().decode()
            assert 'Ready for Test' in data
            return httpx.Response(200, json={"workItems": [{"id": 101}, {"id": 102}]})
        if request.url.path.endswith('/_apis/wit/workitemsbatch'):
            payload = {
                "value": [
                    {
                        "id": 101,
                        "fields": {
                            "System.WorkItemType": "User Story",
                            "System.Title": "Create project",
                            "System.Description": "Create project description",
                            "Microsoft.VSTS.Common.AcceptanceCriteria": "<ul><li>Upload file</li></ul>",
                            "System.State": "Ready for Test",
                            "System.AssignedTo": {"displayName": "QA User"},
                            "System.Tags": "project;upload",
                            "System.IterationPath": "Sprint 12",
                            "System.AreaPath": "Business/Projects",
                        },
                        "relations": [
                            {
                                "rel": "AttachedFile",
                                "url": "https://dev.azure.com/org/project/_apis/wit/attachments/1",
                                "attributes": {"name": "step-1-upload-project-definition.png"},
                            }
                        ],
                    },
                    {
                        "id": 102,
                        "fields": {
                            "System.WorkItemType": "Bug",
                            "System.Title": "Project upload bug",
                            "System.State": "Active",
                            "System.Tags": "project;bug",
                        },
                        "relations": [],
                    },
                ]
            }
            return httpx.Response(200, json=payload)
        if request.url.path.endswith('/comments'):
            return httpx.Response(200, json={"comments": []})
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client = httpx.Client(transport=httpx.MockTransport(handler), timeout=20.0)
    connector = DevOpsConnector(
        base_url="https://dev.azure.com/OPS-GSIC/Business%20Experience/_workitems/recentlyupdated/",
        pat="token",
        client=client,
    )
    items = connector.query_work_items("proj_01", WorkItemFilter(state=["Ready for Test"], type=[WorkItemType.STORY, WorkItemType.DEFECT]))
    assert len(items) == 2
    assert items[0].external_id == "101"
    assert items[0].acceptance_criteria == ["Upload file"]
    assert items[0].linked_artifact_refs[0]["type"] == "ado_attachment"
    assert items[1].type.value == "defect"


def test_api_query_work_items_uses_saved_project_devops_config(monkeypatch) -> None:
    store.projects.clear()
    store.work_items.clear()
    store.artifacts.clear()
    store.associations.clear()
    store.scenarios.clear()
    store.journeys.clear()

    captured = {}

    def fake_query(self, project_id, filters):
        captured["base_url"] = self.base_url
        captured["pat"] = self.pat
        from ai_qa_tester.models.contracts import WorkItem, WorkItemType
        return [WorkItem(id="wk_900", external_id="900", type=WorkItemType.STORY, title="Configured query")]

    monkeypatch.setattr(DevOpsConnector, "query_work_items", fake_query)
    monkeypatch.setattr(DevOpsConnector, "fetch_attachments_for_work_item", lambda self, project_id, item: [])

    client = TestClient(app)
    create_response = client.post(
        "/api/v1/projects",
        json={
            "name": "Configured Project",
            "devops_url": "https://dev.azure.com/OPS-GSIC/Business%20Experience/_workitems/recentlyupdated/",
            "devops_pat": "secret-pat",
        },
    )
    assert create_response.status_code == 200
    project_id = create_response.json()["id"]

    query_response = client.post(
        f"/api/v1/projects/{project_id}/work-items/query",
        json={"filters": {"state": ["Ready for Test"]}, "sync_mode": "incremental"},
    )
    assert query_response.status_code == 200
    assert captured["base_url"] == "https://dev.azure.com/OPS-GSIC/Business%20Experience/_workitems/recentlyupdated/"
    assert captured["pat"] == "secret-pat"
