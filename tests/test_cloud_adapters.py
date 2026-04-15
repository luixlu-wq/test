from pathlib import Path

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.repositories.memory import SQLAlchemyPersistence


def test_sqlalchemy_persistence_roundtrip_sqlite_url(tmp_path):
    settings = get_settings()
    settings.repository_backend = 'sqlalchemy'
    settings.database_url = f"sqlite:///{tmp_path / 'sa.db'}"
    persistence = SQLAlchemyPersistence(settings.resolved_database_url)
    persistence.save_item('ns', 'k1', {'value': 1})
    assert persistence.load_namespace('ns')['k1']['value'] == 1


def test_blob_storage_local_backend_selected(tmp_path, monkeypatch):
    settings = get_settings()
    settings.blob_backend = 'local'
    settings.blob_root = str(tmp_path / 'blobs')
    from ai_qa_tester.services.blob_storage import BlobStorageService

    storage = BlobStorageService()
    saved = storage.save_upload('sample.png', b'abc')
    assert Path(saved).exists()
    assert storage.backend_name == 'local'


def test_vector_store_local_backend_selected(tmp_path):
    settings = get_settings()
    settings.vector_backend = 'local'
    settings.vector_store_path = str(tmp_path / 'vectors.json')
    from ai_qa_tester.services.vector_store import VectorStoreService

    vectors = VectorStoreService()
    vectors.clear()
    vectors.index_document('doc-1', 'create project upload review submit', {'type': 'journey'})
    vectors.index_document('doc-2', 'search business listing results', {'type': 'journey'})
    result = vectors.search_similar('project upload', top_k=1)[0]
    assert result['doc_id'] == 'doc-1'
    assert vectors.backend_name == 'local'
