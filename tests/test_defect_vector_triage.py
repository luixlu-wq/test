from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import (
    Association,
    AssociationDecision,
    AssociationEvidence,
    ArtifactType,
    EntityRef,
    JourneyArtifact,
    JourneyStep,
    Project,
    ScenarioType,
    TestScenario,
    WorkItem,
    WorkItemType,
)
from ai_qa_tester.repositories.memory import store
import ai_qa_tester.services.association as association_module
from ai_qa_tester.services.association import AssociationService
from ai_qa_tester.services.vector_store import LocalVectorBackend, VectorStoreService


def test_defect_vector_triage_finds_story_journey_and_regression(tmp_path):
    store.clear_all()
    vectors = VectorStoreService()
    vectors.backend_name = "local"
    vectors.local_backend = LocalVectorBackend(str(tmp_path / "vectors.json"))
    vectors.clear()

    story = WorkItem(
        id="wk_story",
        external_id="100",
        type=WorkItemType.STORY,
        title="Create project upload and review flow",
        description="User uploads a project definition and reviews the project before submit",
        acceptance_criteria=["User can upload a project definition", "User can review and submit"],
        tags=["create_project", "upload", "review"],
    )
    defect = WorkItem(
        id="wk_defect",
        external_id="200",
        type=WorkItemType.DEFECT,
        title="Upload fails on review step",
        description="After uploading the project definition, the review step shows an error",
        comments=["Repro: upload a pdf then continue to review; error banner appears"],
        related_work_item_refs=[{"id": "wk_story", "external_id": "100", "name": "Create project upload and review flow"}],
        tags=["upload", "review", "error"],
    )
    journey = JourneyArtifact(
        id="journey_create_project",
        project_id="proj_01",
        title="Create Project Journey",
        journey_name="create_project",
        source_ref="upload://journey/create-project",
        step_artifact_ids=["art_step1"],
        steps=[JourneyStep(order=1, artifact_id="art_step1", step_key="upload", step_title="Upload Project Definition")],
        metadata={"extracted_text": ["Create Project", "Upload Project Definition", "Review and Submit"]},
    )
    assoc = Association(
        id="assoc_story_journey",
        project_id="proj_01",
        source_entity=EntityRef(type="work_item", id="wk_story"),
        target_entity=EntityRef(type="journey_artifact", id="journey_create_project"),
        association_type="story_to_journey",
        decision=AssociationDecision.ASSOCIATE,
        confidence=0.9,
        evidence=[AssociationEvidence(type="journey", strength=0.9, detail="Story matches create_project journey")],
        reason_summary="Story maps to create_project journey",
        status="approved",
    )
    scenario = TestScenario(
        id="scn_create_project_regression",
        project_id="proj_01",
        title="Create project upload and review regression",
        scenario_type=ScenarioType.REGRESSION,
        journey="create_project",
        source_refs=[EntityRef(type="work_item", id="wk_story"), EntityRef(type="journey_artifact", id="journey_create_project")],
        coverage_reason="Regression for create project",
        steps=["Upload file", "Continue to review"],
        expected_results=["Review succeeds"],
    )

    store.projects["proj_01"] = Project(id="proj_01", name="AI QA")
    store.work_items[story.id] = story
    store.work_items[defect.id] = defect
    store.journeys[journey.id] = journey
    store.associations[assoc.id] = assoc
    store.scenarios[scenario.id] = scenario

    vectors.index_document(story.id, " ".join([story.title, story.description, *story.acceptance_criteria, *story.tags]), {"type": "work_item", "project_id": "proj_01", "work_item_type": "story", "external_id": story.external_id})
    vectors.index_document(journey.id, "create project upload project definition review and submit", {"type": "journey", "project_id": "proj_01", "journey": "create_project"})

    service = AssociationService(vector_backend=vectors)
    story_candidates = service.retrieve_defect_story_candidates("proj_01", defect, top_k=3)
    journey_candidates = service.retrieve_defect_journey_candidates("proj_01", defect, top_k=3)
    regression_candidates = service.retrieve_defect_regression_candidates("proj_01", defect, top_k=3)

    assert story_candidates and story_candidates[0]["work_item_id"] == "wk_story"
    assert any("Explicitly linked" in reason for reason in story_candidates[0]["reasons"])
    assert journey_candidates and journey_candidates[0]["journey"] == "create_project"
    assert regression_candidates and regression_candidates[0]["scenario_id"] == "scn_create_project_regression"


def test_defect_triage_endpoint_returns_candidates(tmp_path):
    store.clear_all()
    vectors = VectorStoreService()
    vectors.backend_name = "local"
    vectors.local_backend = LocalVectorBackend(str(tmp_path / "vectors.json"))
    vectors.clear()

    store.projects["proj_01"] = Project(id="proj_01", name="AI QA")
    story = WorkItem(id="wk_story", external_id="100", type=WorkItemType.STORY, title="Create project upload flow", description="Upload a project definition and continue")
    defect = WorkItem(id="wk_defect", external_id="200", type=WorkItemType.DEFECT, title="Upload error", description="Project definition upload fails", related_work_item_refs=[{"id": "wk_story", "external_id": "100"}])
    store.work_items[story.id] = story
    store.work_items[defect.id] = defect
    vectors.index_document(story.id, "create project upload flow", {"type": "work_item", "project_id": "proj_01", "work_item_type": "story", "external_id": "100"})

    association_module.vector_store = vectors
    client = TestClient(app)
    response = client.post("/api/v1/projects/proj_01/defects/wk_defect/triage-candidates")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["story_candidates"][0]["work_item_id"] == "wk_story"
