from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request
from pydantic import BaseModel, Field

from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.job_queue import JobQueueService
from ai_qa_tester.services.webhooks import (
    AzureDevOpsWebhookService,
    AzureDevOpsWebhookValidator,
    IncrementalSyncService,
)

router = APIRouter(prefix="/api/v1/projects/{project_id}", tags=["webhooks"])


class IncrementalSyncRequest(BaseModel):
    changed_external_ids: list[str] = Field(default_factory=list)
    environment: str = "uat"
    limit: int = 10
    trigger_type: str = "incremental_sync"


@router.post("/sync/incremental")
def incremental_sync(project_id: str, request: IncrementalSyncRequest) -> dict:
    if not request.changed_external_ids:
        raise HTTPException(status_code=400, detail="changed_external_ids is required")
    return IncrementalSyncService().sync_changed_external_ids(
        project_id,
        request.changed_external_ids,
        trigger_type=request.trigger_type,
        environment=request.environment,
        limit=request.limit,
    )


@router.post("/webhooks/azure-devops")
async def receive_azure_devops_webhook(
    project_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    x_webhook_token: str | None = Header(default=None, alias="X-Webhook-Token"),
    x_vss_subscriptionid: str | None = Header(default=None, alias="X-VSS-SubscriptionId"),
    x_vss_notificationid: str | None = Header(default=None, alias="X-VSS-NotificationId"),
    x_ado_signature: str | None = Header(default=None, alias="X-Ado-Signature"),
) -> dict:
    project = store.projects.get(project_id)
    if project and project.devops_webhook_secret and x_webhook_token != project.devops_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook token")

    raw_body = await request.body()
    payload = await request.json()
    headers = {
        "x-vss-subscriptionid": x_vss_subscriptionid or "",
        "x-vss-notificationid": x_vss_notificationid or "",
        "x-ado-signature": x_ado_signature or "",
    }
    validation = AzureDevOpsWebhookValidator().validate(project_id, payload, headers, raw_body)
    if not validation.valid:
        if validation.reason == "duplicate_notification":
            return {"status": "ignored", "reason": validation.reason}
        raise HTTPException(status_code=401, detail=validation.reason or "invalid_webhook")

    parsed = AzureDevOpsWebhookService().parse_payload(payload)
    job = JobQueueService().enqueue_incremental_sync(
        project_id=project_id,
        changed_external_ids=parsed.changed_external_ids,
        trigger_type=f"ado_webhook:{parsed.event_type}",
        source_event={
            "event_type": parsed.event_type,
            "raw_revision": parsed.raw_revision,
            "notification_id": x_vss_notificationid,
            "subscription_id": x_vss_subscriptionid,
        },
    )
    background_tasks.add_task(JobQueueService().process_job, job.id)
    return {
        "status": "accepted",
        "mode": "queued",
        "event_type": parsed.event_type,
        "changed_external_ids": parsed.changed_external_ids,
        "raw_revision": parsed.raw_revision,
        "job_id": job.id,
    }


@router.get("/jobs/{job_id}")
def get_job(project_id: str, job_id: str) -> dict:
    job = store.jobs.get(job_id)
    if not job or job.project_id != project_id:
        raise HTTPException(status_code=404, detail="job_not_found")
    return {"job": job.model_dump(mode="json")}


@router.post("/jobs/{job_id}/process")
def process_job(project_id: str, job_id: str) -> dict:
    job = store.jobs.get(job_id)
    if not job or job.project_id != project_id:
        raise HTTPException(status_code=404, detail="job_not_found")
    processed = JobQueueService().process_job(job_id)
    return {"job": processed.model_dump(mode="json")}


@router.post("/jobs/drain")
def drain_jobs(project_id: str, limit: int = 10) -> dict:
    processed = [
        job.model_dump(mode="json")
        for job in JobQueueService().drain(limit=limit)
        if job.project_id == project_id
    ]
    return {"processed_jobs": processed, "count": len(processed)}


@router.post("/jobs/process-next-command")
def process_next_command(project_id: str) -> dict:
    processed = JobQueueService().process_next_bus_command()
    if not processed or processed.project_id != project_id:
        return {"status": "idle"}
    return {"status": "processed", "job": processed.model_dump(mode="json")}
