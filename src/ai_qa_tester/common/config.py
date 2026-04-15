from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-qa-tester"
    environment: str = "dev"
    event_bus_enabled: bool = False
    service_bus_enabled: bool = False
    service_bus_connection_string: str | None = None
    service_bus_command_queue: str = "aiqa-commands"
    service_bus_event_topic: str = "aiqa-events"
    service_bus_event_subscription: str = "aiqa-worker"

    # persistence backends
    database_url: str | None = None
    sqlite_path: str = "/mnt/data/ai_qa_tester.db"
    repository_backend: str = "sqlalchemy"

    # blob backends
    blob_backend: str = "local"
    blob_root: str = "/mnt/data/ai_qa_tester_blobs"
    azure_blob_connection_string: str | None = None
    azure_blob_container: str = "ai-qa-artifacts"
    azure_blob_prefix: str = "uploads"

    # vector backends
    vector_backend: str = "local"
    vector_store_path: str = "/mnt/data/ai_qa_tester_vectors.json"
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_collection: str = "ai_qa_vectors"

    # execution backends
    execution_backend: str = "simulated"
    playwright_command: str = "npx playwright test"
    playwright_work_root: str = "/mnt/data/ai_qa_playwright_runs"
    app_base_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_prefix="AI_QA_", extra="ignore")

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"sqlite:///{self.sqlite_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
