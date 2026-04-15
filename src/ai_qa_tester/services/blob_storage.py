from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from ai_qa_tester.common.config import get_settings


class LocalBlobStorageBackend:
    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save_upload(self, filename: str, content: bytes) -> str:
        suffix = Path(filename).suffix or ".bin"
        path = self.root / f"{uuid4().hex}{suffix}"
        path.write_bytes(content)
        return str(path)

    def exists(self, path: str) -> bool:
        return Path(path).exists()


class AzureBlobStorageBackend:
    def __init__(self, connection_string: str, container: str, prefix: str = "uploads") -> None:
        try:
            from azure.storage.blob import BlobServiceClient
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("azure-storage-blob is required for Azure blob backend") from exc
        self.client = BlobServiceClient.from_connection_string(connection_string)
        self.container = container
        self.prefix = prefix.strip("/")
        self.container_client = self.client.get_container_client(container)
        try:
            self.container_client.create_container()
        except Exception:
            pass

    def save_upload(self, filename: str, content: bytes) -> str:
        blob_name = f"{self.prefix}/{uuid4().hex}-{Path(filename).name}"
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(content, overwrite=True)
        return f"azureblob://{self.container}/{blob_name}"

    def exists(self, path: str) -> bool:
        if not path.startswith("azureblob://"):
            return False
        _, rest = path.split("://", 1)
        container, blob_name = rest.split("/", 1)
        blob_client = self.client.get_blob_client(container=container, blob=blob_name)
        return blob_client.exists()


class BlobStorageService:
    def __init__(self) -> None:
        settings = get_settings()
        backend_name = (settings.blob_backend or "local").lower()
        if backend_name == "azure" and settings.azure_blob_connection_string:
            self.backend = AzureBlobStorageBackend(
                connection_string=settings.azure_blob_connection_string,
                container=settings.azure_blob_container,
                prefix=settings.azure_blob_prefix,
            )
            self.backend_name = "azure"
        else:
            self.backend = LocalBlobStorageBackend(settings.blob_root)
            self.backend_name = "local"

    def save_upload(self, filename: str, content: bytes) -> str:
        return self.backend.save_upload(filename, content)

    def exists(self, path: str) -> bool:
        return self.backend.exists(path)


blob_storage = BlobStorageService()
