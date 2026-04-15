from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app


def test_query_work_items_generates_traceability_chain() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/projects/proj_01/work-items/query",
        json={
            "filters": {
                "state": ["Ready for Test"],
                "assignee": ["qa.user@company.com"],
                "type": ["story"],
                "tags": ["search"],
                "sprint": ["Sprint 12"],
                "area_path": ["Business/Search"],
            },
            "sync_mode": "incremental",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["work_item_ids"]
    assert payload["artifact_ids"]
    assert payload["association_ids"]
    assert payload["scenario_ids"]
