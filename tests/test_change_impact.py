from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import (
    Artifact,
    ArtifactType,
    Association,
    AssociationDecision,
    EntityRef,
    TestScenario,
    WorkItem,
    WorkItemType,
)
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.change_impact import ChangeImpactService


def setup_function() -> None:
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()
    store.runs.clear()


def seed_graph() -> None:
    story = WorkItem(
        id="wk_story",
        external_id="100",
        type=WorkItemType.STORY,
        title="Create project with upload and map location",
        description="Create project flow includes upload project definition and choose map location.",
        comments=["Repro note mentions review step validation."],
        related_work_item_refs=[
            {
                "relation_type": "System.LinkTypes.Related",
                "work_item_external_id": "200",
                "type": "ado_work_item_relation",
                "value": "https://example/200",
            }
        ],
    )
    defect = WorkItem(
        id="wk_defect",
        external_id="200",
        type=WorkItemType.DEFECT,
        title="Upload validation banner on review step",
    )
    store.work_items[story.id] = story
    store.work_items[defect.id] = defect

    journey = Artifact(
        id="art_journey",
        project_id="proj_01",
        artifact_type=ArtifactType.JOURNEY_WIREFRAME,
        source_type="upload",
        source_ref="upload://create-project-flow",
        title="Create project journey",
        metadata={"journey_name": "create_project", "risk_areas": ["upload", "validation", "map"]},
        status="processed",
    )
    store.artifacts[journey.id] = journey

    association = Association(
        id="assoc_1",
        project_id="proj_01",
        source_entity=EntityRef(type="work_item", id=story.id),
        target_entity=EntityRef(type="artifact", id=journey.id),
        association_type="story_to_journey_wireframe",
        decision=AssociationDecision.ASSOCIATE,
        confidence=0.91,
        evidence=[],
        reason_summary="Directly linked journey",
        status="approved",
    )
    store.associations[association.id] = association

    direct = TestScenario(
        id="scn_direct",
        project_id="proj_01",
        title="Create project successfully with valid upload and map selection",
        scenario_type="integration",
        journey="create_project",
        steps=["Upload project definition", "Select map location", "Submit"],
        expected_results=["Project created successfully"],
        source_refs=[EntityRef(type="work_item", id=story.id), EntityRef(type="artifact", id=journey.id)],
        coverage_reason="Happy path",
        priority="critical",
        review_required=False,
    )
    related = TestScenario(
        id="scn_related",
        project_id="proj_01",
        title="Show validation banner on review step when upload is invalid",
        scenario_type="regression",
        journey="create_project",
        steps=["Upload invalid file", "Continue to review"],
        expected_results=["Validation banner is shown"],
        source_refs=[EntityRef(type="work_item", id=defect.id)],
        coverage_reason="Defect regression",
        priority="high",
        review_required=False,
    )
    unrelated = TestScenario(
        id="scn_unrelated",
        project_id="proj_01",
        title="Search registered business by name",
        scenario_type="ui",
        journey="business_search",
        steps=["Enter business name"],
        expected_results=["Results displayed"],
        source_refs=[EntityRef(type="work_item", id="wk_other")],
        coverage_reason="Other feature",
        priority="medium",
        review_required=False,
    )
    store.scenarios[direct.id] = direct
    store.scenarios[related.id] = related
    store.scenarios[unrelated.id] = unrelated


def test_change_impact_selects_direct_and_related_scenarios() -> None:
    seed_graph()
    result = ChangeImpactService().analyze("proj_01", ["wk_story"])
    selected_ids = [item["scenario_id"] for item in result["selected_scenarios"]]
    assert selected_ids[:2] == ["scn_direct", "scn_related"]
    assert "create_project" in result["impacted_journeys"]
    assert "wk_defect" in result["related_work_item_ids"]


def test_impact_analysis_endpoint_returns_ranked_retest_candidates() -> None:
    seed_graph()
    client = TestClient(app)
    response = client.post(
        "/api/v1/projects/proj_01/impact/analyze",
        json={"changed_work_item_ids": ["wk_story"], "limit": 5},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["selected_scenarios"][0]["scenario_id"] == "scn_direct"
    assert payload["selected_scenarios"][0]["score"] > payload["selected_scenarios"][1]["score"]


def test_retest_run_endpoint_executes_only_impacted_scenarios() -> None:
    seed_graph()
    client = TestClient(app)
    response = client.post(
        "/api/v1/projects/proj_01/impact/retest-run",
        json={"changed_work_item_ids": ["wk_story"], "environment": "uat", "limit": 2},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["run"]["scenario_ids"] == ["scn_direct", "scn_related"]
    assert payload["run"]["summary"]["failed"] == 1
