from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import (
    Association,
    AssociationDecision,
    AssociationEvidence,
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


def _setup_vectors(tmp_path):
    vectors = VectorStoreService()
    vectors.backend_name = "local"
    vectors.local_backend = LocalVectorBackend(str(tmp_path / "vectors.json"))
    vectors.clear()
    return vectors


def test_generate_regressions_updates_existing_and_creates_new(tmp_path):
    store.clear_all()
    vectors = _setup_vectors(tmp_path)

    story = WorkItem(
        id="wk_story", external_id="100", type=WorkItemType.STORY,
        title="Create project upload and review flow",
        description="User uploads a project definition and reviews before submit",
        tags=["create_project", "upload", "review"],
    )
    defect = WorkItem(
        id="wk_defect", external_id="200", type=WorkItemType.DEFECT,
        title="Upload fails on review step",
        description="After upload, review step errors",
        comments=["Repro: upload a pdf then continue to review"],
        related_work_item_refs=[{"id": "wk_story", "external_id": "100"}],
        tags=["upload", "review"],
    )
    journey = JourneyArtifact(
        id="journey_create_project", project_id="proj_01", title="Create Project Journey",
        journey_name="create_project", source_ref="upload://journey/create-project",
        step_artifact_ids=["art_step1"],
        steps=[JourneyStep(order=1, artifact_id="art_step1", step_key="upload", step_title="Upload Project Definition")],
        metadata={"extracted_text": ["Create Project", "Upload Project Definition", "Review and Submit"]},
    )
    assoc = Association(
        id="assoc_story_journey", project_id="proj_01",
        source_entity=EntityRef(type="work_item", id="wk_story"),
        target_entity=EntityRef(type="journey_artifact", id="journey_create_project"),
        association_type="story_to_journey", decision=AssociationDecision.ASSOCIATE, confidence=0.9,
        evidence=[AssociationEvidence(type="journey", strength=0.9, detail="Story matches create_project journey")],
        reason_summary="Story maps to create_project journey", status="approved",
    )
    existing = TestScenario(
        id="scn_existing", project_id="proj_01", title="Create project upload and review regression",
        scenario_type=ScenarioType.REGRESSION, journey="create_project",
        source_refs=[EntityRef(type="work_item", id="wk_story"), EntityRef(type="journey_artifact", id="journey_create_project")],
        coverage_reason="Regression for create project", steps=["Upload file", "Continue to review"],
        expected_results=["Review succeeds"],
    )

    store.projects["proj_01"] = Project(id="proj_01", name="AI QA")
    store.work_items[story.id] = story
    store.work_items[defect.id] = defect
    store.journeys[journey.id] = journey
    store.associations[assoc.id] = assoc
    store.scenarios[existing.id] = existing

    vectors.index_document(story.id, "create project upload review", {"type": "work_item", "project_id": "proj_01", "work_item_type": "story", "external_id": "100"})
    vectors.index_document(journey.id, "create project upload review and submit", {"type": "journey", "project_id": "proj_01", "journey": "create_project"})

    service = AssociationService(vector_backend=vectors)
    story_candidates = service.retrieve_defect_story_candidates("proj_01", defect, top_k=3)
    journey_candidates = service.retrieve_defect_journey_candidates("proj_01", defect, top_k=3)
    regression_candidates = service.retrieve_defect_regression_candidates("proj_01", defect, top_k=3)

    from ai_qa_tester.services.scenario_generation import ScenarioGenerator
    generated = ScenarioGenerator().generate_regressions_from_defect("proj_01", defect, story_candidates, journey_candidates, regression_candidates, limit=2)

    assert generated
    assert generated[0]["action"] == "updated"
    updated = generated[0]["scenario"]
    assert any(ref.type == "work_item" and ref.id == "wk_defect" for ref in updated.source_refs)
    assert any("no longer reproduces" in r.lower() for r in updated.expected_results)


def test_generate_regressions_endpoint_returns_generated(tmp_path):
    store.clear_all()
    vectors = _setup_vectors(tmp_path)

    store.projects["proj_01"] = Project(id="proj_01", name="AI QA")
    story = WorkItem(id="wk_story", external_id="100", type=WorkItemType.STORY, title="Create project upload flow", description="Upload a project definition and continue")
    defect = WorkItem(id="wk_defect", external_id="200", type=WorkItemType.DEFECT, title="Upload error", description="Project definition upload fails on review", comments=["Repro: upload a pdf then continue to review"], related_work_item_refs=[{"id": "wk_story", "external_id": "100"}])
    journey = JourneyArtifact(id="journey_create_project", project_id="proj_01", title="Create Project Journey", journey_name="create_project", source_ref="upload://journey", steps=[JourneyStep(order=1, artifact_id="art1", step_key="upload", step_title="Upload Project Definition")], step_artifact_ids=["art1"], metadata={"extracted_text": ["Create Project", "Upload"]})
    store.work_items[story.id] = story
    store.work_items[defect.id] = defect
    store.journeys[journey.id] = journey
    store.associations["assoc1"] = Association(
        id="assoc1", project_id="proj_01", source_entity=EntityRef(type="work_item", id="wk_story"), target_entity=EntityRef(type="journey_artifact", id="journey_create_project"), association_type="story_to_journey", decision=AssociationDecision.ASSOCIATE, confidence=0.9, evidence=[AssociationEvidence(type="journey", strength=0.9, detail="match")], reason_summary="ok", status="approved"
    )
    vectors.index_document(story.id, "create project upload flow", {"type": "work_item", "project_id": "proj_01", "work_item_type": "story", "external_id": "100"})
    vectors.index_document(journey.id, "create project upload review", {"type": "journey", "project_id": "proj_01", "journey": "create_project"})

    association_module.vector_store = vectors
    client = TestClient(app)
    response = client.post("/api/v1/projects/proj_01/defects/wk_defect/generate-regressions")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["generated"]
    assert payload["generated"][0]["scenario"]["scenario_type"] == "regression"


def test_generate_regressions_endpoint_also_generates_scripts(tmp_path):
    store.clear_all()
    vectors = _setup_vectors(tmp_path)

    store.projects["proj_01"] = Project(id="proj_01", name="AI QA")
    story = WorkItem(id="wk_story", external_id="100", type=WorkItemType.STORY, title="Create project upload flow", description="Upload a project definition and continue")
    defect = WorkItem(id="wk_defect", external_id="200", type=WorkItemType.DEFECT, title="Upload error", description="Project definition upload fails on review", comments=["Repro: upload a pdf then continue to review"], related_work_item_refs=[{"id": "wk_story", "external_id": "100"}])
    journey = JourneyArtifact(id="journey_create_project", project_id="proj_01", title="Create Project Journey", journey_name="create_project", source_ref="upload://journey", steps=[JourneyStep(order=1, artifact_id="art1", step_key="upload", step_title="Upload Project Definition")], step_artifact_ids=["art1"], metadata={"extracted_text": ["Create Project", "Upload"]})
    store.work_items[story.id] = story
    store.work_items[defect.id] = defect
    store.journeys[journey.id] = journey
    store.associations["assoc1"] = Association(
        id="assoc1", project_id="proj_01", source_entity=EntityRef(type="work_item", id="wk_story"), target_entity=EntityRef(type="journey_artifact", id="journey_create_project"), association_type="story_to_journey", decision=AssociationDecision.ASSOCIATE, confidence=0.9, evidence=[AssociationEvidence(type="journey", strength=0.9, detail="match")], reason_summary="ok", status="approved"
    )
    vectors.index_document(story.id, "create project upload flow", {"type": "work_item", "project_id": "proj_01", "work_item_type": "story", "external_id": "100"})
    vectors.index_document(journey.id, "create project upload review", {"type": "journey", "project_id": "proj_01", "journey": "create_project"})

    association_module.vector_store = vectors
    client = TestClient(app)
    response = client.post("/api/v1/projects/proj_01/defects/wk_defect/generate-regressions")
    assert response.status_code == 200
    payload = response.json()
    assert payload["scripts"]
    assert payload["scripts"][0]["framework"] == "playwright"
    assert "@playwright/test" in payload["scripts"][0]["content"]

    list_response = client.get(f"/api/v1/projects/proj_01/scripts?scenario_id={payload['generated'][0]['scenario']['id']}")
    assert list_response.status_code == 200
    assert list_response.json()["total"] >= 1
