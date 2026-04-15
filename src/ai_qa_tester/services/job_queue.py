from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from ai_qa_tester.models.contracts import CommandEnvelope, JobStatus, QueueJob
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.service_bus import service_bus
from ai_qa_tester.services.webhooks import IncrementalSyncService


@dataclass
class JobQueueService:
    def enqueue_incremental_sync(
        self,
        project_id: str,
        changed_external_ids: list[str],
        trigger_type: str,
        environment: str = "uat",
        limit: int = 10,
        source_event: dict | None = None,
    ) -> QueueJob:
        job = QueueJob(
            id=f"job_{uuid4().hex[:10]}",
            project_id=project_id,
            job_type="incremental_sync",
            payload={
                "changed_external_ids": list(changed_external_ids),
                "trigger_type": trigger_type,
                "environment": environment,
                "limit": limit,
                "source_event": source_event or {},
            },
        )
        store.jobs[job.id] = job
        store.job_queue.append(job.id)
        command = CommandEnvelope(
            command_id=f"cmd_{uuid4().hex[:10]}",
            command_type="incremental_sync",
            project_id=project_id,
            correlation_id=f"corr_{uuid4().hex[:8]}",
            payload={"job_id": job.id, **job.payload},
        )
        delivery = service_bus.publish_command(command)
        job.payload["command_delivery_mode"] = delivery["mode"]
        job.payload["command_id"] = command.command_id
        return job

    def process_job(self, job_id: str) -> QueueJob:
        job = store.jobs[job_id]
        if job.status == JobStatus.COMPLETED:
            return job
        job.status = JobStatus.RUNNING
        job.started_at = datetime.now(UTC)
        try:
            if job.job_type == "incremental_sync":
                result = IncrementalSyncService().sync_changed_external_ids(
                    job.project_id,
                    job.payload.get("changed_external_ids", []),
                    trigger_type=job.payload.get("trigger_type", "queued_incremental_sync"),
                    environment=job.payload.get("environment", "uat"),
                    limit=int(job.payload.get("limit", 10)),
                )
            else:
                raise ValueError(f"Unsupported job type: {job.job_type}")
            job.result = result
            job.status = JobStatus.COMPLETED
        except Exception as exc:  # pragma: no cover - defensive
            job.error = str(exc)
            job.status = JobStatus.FAILED
        finally:
            job.completed_at = datetime.now(UTC)
            if job_id in store.job_queue:
                store.job_queue.remove(job_id)
        return job

    def drain(self, limit: int | None = None) -> list[QueueJob]:
        processed: list[QueueJob] = []
        job_ids = list(store.job_queue[: limit or None])
        for job_id in job_ids:
            processed.append(self.process_job(job_id))
        return processed

    def process_next_bus_command(self) -> QueueJob | None:
        command = service_bus.pop_local_command()
        if command is None:
            return None
        job_id = str(command.payload.get("job_id", ""))
        if not job_id or job_id not in store.jobs:
            return None
        return self.process_job(job_id)



def compute_webhook_signature(secret: str, body: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"



def canonicalize_json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
