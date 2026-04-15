from pathlib import Path

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import Artifact, ArtifactType, Project
from ai_qa_tester.repositories.memory import PersistedMap, SQLitePersistence, store
from ai_qa_tester.services.blob_storage import blob_storage
from ai_qa_tester.services.vector_store import vector_store


def test_sqlite_persisted_map_roundtrip(tmp_path):
    db_path = tmp_path / 'repo.db'
    persistence = SQLitePersistence(str(db_path))
    projects = PersistedMap(persistence, 'projects_test', Project)
    project = Project(id='proj_test', name='Persistent Project')
    projects[project.id] = project

    reloaded = PersistedMap(persistence, 'projects_test', Project)
    assert reloaded['proj_test'].name == 'Persistent Project'


def test_blob_storage_and_vector_index(tmp_path, monkeypatch):
    settings = get_settings()
    blob_root = tmp_path / 'blobs'
    vector_path = tmp_path / 'vectors.json'
    monkeypatch.setattr(settings, 'blob_root', str(blob_root))
    monkeypatch.setattr(settings, 'vector_store_path', str(vector_path))

    # rebuild lightweight services bound to patched settings
    from ai_qa_tester.services.blob_storage import BlobStorageService
    from ai_qa_tester.services.vector_store import VectorStoreService

    storage = BlobStorageService()
    path = storage.save_upload('create-project.png', b'fake-bytes')
    assert Path(path).exists()

    vectors = VectorStoreService()
    vectors.clear()
    vectors.index_document('art_1', 'create project upload definition validation map', {'type': 'artifact'})
    vectors.index_document('art_2', 'search business results listing table', {'type': 'artifact'})
    results = vectors.search_similar('project upload validation', top_k=1)
    assert results[0]['doc_id'] == 'art_1'


def test_global_store_persists_project_record():
    store.projects.clear()
    project = Project(id='proj_global', name='Global Persistent Project')
    store.projects[project.id] = project
    # access again through the global store object
    assert store.projects['proj_global'].name == 'Global Persistent Project'
