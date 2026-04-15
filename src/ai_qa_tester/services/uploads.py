from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

from ai_qa_tester.models.contracts import Artifact, ArtifactType, JourneyArtifact
from ai_qa_tester.services.blob_storage import blob_storage


class UploadService:
    def register_wireframe(
        self,
        project_id: str,
        filename: str,
        content_type: str,
        content: bytes,
        linked_entity_type: str | None = None,
        linked_entity_id: str | None = None,
    ) -> Artifact:
        ext = Path(filename).suffix.lower()
        artifact_type = ArtifactType.WIREFRAME if ext in {".pdf", ".png", ".jpg", ".jpeg", ".webp"} else ArtifactType.SCREENSHOT
        title = Path(filename).stem.replace("_", " ").replace("-", " ").title()
        saved_path = self._persist_upload(filename, content)
        return Artifact(
            id=f"art_{uuid4().hex[:8]}",
            project_id=project_id,
            artifact_type=artifact_type,
            source_type="upload",
            source_ref=f"upload://{filename}",
            raw_uri=None,
            title=title,
            metadata={
                "filename": filename,
                "content_type": content_type,
                "byte_size": len(content),
                "linked_entity_type": linked_entity_type,
                "linked_entity_id": linked_entity_id,
                "upload_preview_text": self._preview_text(filename, content),
                "local_path": saved_path,
            },
            status="registered",
        )

    def register_journey(
        self,
        project_id: str,
        journey_name: str | None,
        artifact_ids: list[str],
        linked_entity_type: str | None = None,
        linked_entity_id: str | None = None,
    ) -> JourneyArtifact:
        title = (journey_name or "Wireframe Journey").replace("_", " ").replace("-", " ").title()
        normalized_name = (journey_name or "generic_journey").strip().lower().replace(" ", "_")
        return JourneyArtifact(
            id=f"jour_{uuid4().hex[:8]}",
            project_id=project_id,
            title=title,
            journey_name=normalized_name,
            source_ref=f"upload-journey://{normalized_name}",
            step_artifact_ids=artifact_ids,
            metadata={
                "linked_entity_type": linked_entity_type,
                "linked_entity_id": linked_entity_id,
                "input_artifact_ids": artifact_ids,
            },
            status="registered",
        )

    @staticmethod
    def _preview_text(filename: str, content: bytes) -> list[str]:
        head = content[:400].decode("utf-8", errors="ignore")
        signals = [filename]
        if head:
            signals.append(head)
        return signals

    @staticmethod
    def _persist_upload(filename: str, content: bytes) -> str:
        ext = Path(filename).suffix or ".bin"
        return blob_storage.save_upload(filename or f"upload{ext}", content)
