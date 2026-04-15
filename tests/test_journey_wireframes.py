from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import WorkItem, WorkItemType
from ai_qa_tester.repositories.memory import store


def test_upload_wireframe_journey_builds_ordered_steps_and_scenarios() -> None:
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()

    work_item = WorkItem(
        id="wk_create_project",
        external_id="ADO-200",
        type=WorkItemType.STORY,
        title="Create project flow",
        description="As a user, I want to create a project and upload the project definition.",
        acceptance_criteria=[
            "User can review before starting",
            "User can upload a valid project definition",
            "User can select location and submit",
        ],
        tags=["project", "upload", "location"],
    )
    store.work_items[work_item.id] = work_item

    client = TestClient(app)
    response = client.post(
        "/api/v1/projects/proj_01/artifacts/upload-wireframe-journey",
        files=[
            ("files", ("step-1-upload-project-definition.png", b"Step 1 Upload Project Definition Project Name Upload", "image/png")),
            ("files", ("step-2-select-location.png", b"Step 2 Add Location Map Confirm", "image/png")),
            ("files", ("step-0-before-you-begin.png", b"Step 0 Before you begin Continue Guidance", "image/png")),
            ("files", ("step-3-review-submit.png", b"Step 3 Review Submit Confirm", "image/png")),
        ],
        data={"linked_entity_type": "work_item", "linked_entity_id": work_item.id},
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    journey = payload["journey"]
    assert journey["journey_name"] == "create_project"
    assert [step["step_title"] for step in journey["steps"]] == [
        "Before you begin",
        "Upload the project definition",
        "Select location",
        "Review and submit",
    ]
    assert "file_upload" in journey["metadata"]["risk_areas"]
    assert "map_interaction" in journey["metadata"]["risk_areas"]
    assert payload["association_ids"]
    assert payload["scenario_ids"]

    scenarios = client.get("/api/v1/projects/proj_01/scenarios").json()["items"]
    assert len(scenarios) >= 2
    titles = " | ".join(item["title"] for item in scenarios)
    assert "end-to-end" in titles.lower()
    assert any(item["journey"] == "create_project" for item in scenarios)
