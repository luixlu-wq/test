from ai_qa_tester.models.contracts import Artifact, ArtifactType, WorkItem, WorkItemType
from ai_qa_tester.services.association import AssociationService
from ai_qa_tester.services.vector_store import LocalVectorBackend, VectorStoreService


def test_vector_candidate_retrieval_boosts_association(tmp_path):
    vectors = VectorStoreService()
    vectors.backend_name = "local"
    vectors.local_backend = LocalVectorBackend(str(tmp_path / "vectors.json"))
    vectors.clear()

    artifact = Artifact(
        id="art_create_project",
        project_id="proj_01",
        artifact_type=ArtifactType.WIREFRAME,
        source_type="upload",
        source_ref="upload://create-project",
        title="Create Project Upload Review",
        metadata={
            "extracted_text": ["Create Project", "Upload Project Definition", "Review and Submit"],
            "journey": "create_project",
        },
    )
    vectors.index_document(
        artifact.id,
        "create project upload project definition review and submit",
        {"type": "artifact", "project_id": "proj_01", "journey": "create_project"},
    )

    service = AssociationService(vector_backend=vectors)
    work_item = WorkItem(
        id="wk_story",
        external_id="123",
        type=WorkItemType.STORY,
        title="Create project upload flow",
        description="User uploads a project definition and reviews before submit",
        acceptance_criteria=["Project definition can be uploaded", "User can review before submit"],
        tags=["project", "upload", "review"],
    )

    assoc = service.associate_work_item_to_artifact("proj_01", work_item, artifact)
    assert any("Vector retrieval matched artifact" in e.detail for e in assoc.evidence)
    assert assoc.confidence >= 0.6


def test_vector_search_can_filter_by_project_metadata(tmp_path):
    vectors = VectorStoreService()
    vectors.backend_name = "local"
    vectors.local_backend = LocalVectorBackend(str(tmp_path / "vectors.json"))
    vectors.clear()

    vectors.index_document("a1", "create project upload", {"type": "artifact", "project_id": "proj_01"})
    vectors.index_document("a2", "create project upload", {"type": "artifact", "project_id": "proj_02"})

    results = vectors.search_similar("create project upload", top_k=5, metadata_filters={"project_id": "proj_01"})
    assert [r["doc_id"] for r in results] == ["a1"]
