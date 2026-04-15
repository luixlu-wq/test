from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import Artifact, ArtifactType, WorkItem, WorkItemType
from ai_qa_tester.services.association import AssociationService
from ai_qa_tester.services.processing import ArtifactProcessor
from ai_qa_tester.services.scenario_generation import ScenarioGenerator


def test_upload_wireframe_processes_artifact() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/projects/proj_01/artifacts/upload-wireframe",
        files={"file": ("business-search-wireframe.png", b"search results business name", "image/png")},
        data={"linked_entity_type": "work_item", "linked_entity_id": "wk_demo"},
    )
    assert response.status_code == 200
    artifact = response.json()["artifact"]
    assert artifact["artifact_type"] == "wireframe"
    assert artifact["status"] == "processed"
    assert artifact["metadata"]["journey"] == "business_search"
    assert artifact["metadata"]["extracted_text"]
    assert artifact["metadata"]["ui_elements"]


def test_wireframe_can_generate_association_and_scenario() -> None:
    work_item = WorkItem(
        id="wk_1",
        external_id="ADO-1",
        type=WorkItemType.STORY,
        title="Search registered business",
        description="As a user, I want to search registered businesses.",
        acceptance_criteria=["User can search by business name", "Matching results are displayed"],
        tags=["search", "business"],
    )
    artifact = Artifact(
        id="art_1",
        project_id="proj_01",
        artifact_type=ArtifactType.WIREFRAME,
        source_type="upload",
        source_ref="upload://business-search-wireframe.png",
        title="Business Search Wireframe",
        metadata={"filename": "business-search-wireframe.png", "upload_preview_text": ["Search Business Business Name Results"]},
    )
    processed = ArtifactProcessor().process(artifact)
    association = AssociationService().associate_work_item_to_artifact("proj_01", work_item, processed)
    assert association.confidence >= 0.45
    scenarios = ScenarioGenerator().generate("proj_01", work_item, processed, association)
    assert scenarios
    assert scenarios[0].journey == "business_search"
