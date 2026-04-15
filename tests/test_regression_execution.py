from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import EntityRef, TestScenario, WorkItem, WorkItemType
from ai_qa_tester.repositories.memory import store


def setup_function() -> None:
    store.projects.clear()
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()
    store.scripts.clear()
    store.runs.clear()
    store.script_executions.clear()


def test_execute_defect_regressions_creates_run_and_script_executions() -> None:
    client = TestClient(app)
    work_item = WorkItem(
        id="wk_defect",
        external_id="200",
        type=WorkItemType.DEFECT,
        title="Create project upload defect",
        description="Upload and review flow fails after fix",
        comments=["Repro: upload project definition then continue to review and confirm error is gone"],
        tags=["upload", "review"],
    )
    story = WorkItem(
        id="wk_story",
        external_id="100",
        type=WorkItemType.STORY,
        title="Create project upload and review flow",
        description="Upload project definition and review before submit",
        tags=["upload", "review"],
    )
    store.work_items[work_item.id] = work_item
    store.work_items[story.id] = story

    existing = TestScenario(
        id="scn_existing",
        project_id="proj_01",
        title="Create project upload and review regression",
        scenario_type="regression",
        journey="create_project",
        steps=["Upload project definition", "Continue to review and submit"],
        expected_results=["The defect no longer reproduces after the fix"],
        source_refs=[EntityRef(type="work_item", id="wk_story")],
        coverage_reason="existing regression",
        review_required=False,
    )
    store.scenarios[existing.id] = existing

    response = client.post("/api/v1/projects/proj_01/defects/wk_defect/execute-regressions")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["run"]["trigger_type"] == "defect_retest"
    assert payload["scripts"]
    assert payload["executions"]
    assert payload["analysis"]["run_id"] == payload["run"]["id"]


def test_create_run_with_script_ids_returns_executions() -> None:
    client = TestClient(app)
    work_item = WorkItem(
        id="wk_story",
        external_id="100",
        type=WorkItemType.STORY,
        title="Create project review flow",
    )
    store.work_items[work_item.id] = work_item
    scenario = TestScenario(
        id="scn_ok",
        project_id="proj_01",
        title="Create project happy path",
        scenario_type="integration",
        journey="create_project",
        steps=["Upload file", "Review", "Submit"],
        expected_results=["Project created successfully"],
        source_refs=[EntityRef(type="work_item", id="wk_story")],
        coverage_reason="happy path",
        review_required=False,
    )
    store.scenarios[scenario.id] = scenario
    from ai_qa_tester.services.script_generation import ScriptGenerator
    script = ScriptGenerator().generate_and_store_for_scenarios("proj_01", [scenario])[0]

    response = client.post(
        "/api/v1/projects/proj_01/runs",
        json={"environment": "uat", "script_ids": [script.id], "trigger_type": "manual"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["run"]["summary"]["passed"] == 1
    assert payload["executions"][0]["script_id"] == script.id
