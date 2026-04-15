from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.change_impact import ChangeImpactService
from ai_qa_tester.services.connectors import DevOpsConnector
from ai_qa_tester.services.execution import ExecutionService
from ai_qa_tester.services.result_analysis import ResultAnalysisService
from ai_qa_tester.services.sync_pipeline import ingest_work_items, publish_event
from ai_qa_tester.models.contracts import RunStatus, TestRun


@dataclass
class AzureDevOpsWebhookParseResult:
    event_type: str
    changed_external_ids: list[str]
    raw_revision: int | None = None


class AzureDevOpsWebhookService:
    def parse_payload(self, payload: dict[str, Any]) -> AzureDevOpsWebhookParseResult:
        event_type = str(payload.get("eventType") or payload.get("event_type") or "unknown")
        resource = payload.get("resource") or {}
        changed: list[str] = []

        candidates = [
            resource.get("workItemId"),
            resource.get("id"),
            (resource.get("workItem") or {}).get("id"),
            ((resource.get("revision") or {}).get("id")),
        ]
        fields = (resource.get("fields") or {}) if isinstance(resource, dict) else {}
        if isinstance(fields, dict):
            sys_id = fields.get("System.Id")
            if isinstance(sys_id, dict):
                candidates.extend([sys_id.get("newValue"), sys_id.get("oldValue")])
            elif sys_id:
                candidates.append(sys_id)
        revision = resource.get("revision") if isinstance(resource, dict) else None
        if isinstance(revision, dict):
            candidates.append(revision.get("id"))

        for candidate in candidates:
            if candidate is None:
                continue
            value = str(candidate)
            if value.isdigit() and value not in changed:
                changed.append(value)

        return AzureDevOpsWebhookParseResult(
            event_type=event_type,
            changed_external_ids=changed,
            raw_revision=(revision or {}).get("rev") if isinstance(revision, dict) else None,
        )




@dataclass
class AzureDevOpsWebhookValidationResult:
    valid: bool
    reason: str | None = None


class AzureDevOpsWebhookValidator:
    def validate(self, project_id: str, payload: dict[str, Any], headers: dict[str, str], raw_body: bytes) -> AzureDevOpsWebhookValidationResult:
        project = store.projects.get(project_id)
        if not project:
            return AzureDevOpsWebhookValidationResult(valid=False, reason="project_not_found")

        publisher = str(payload.get("publisherId") or payload.get("publisher_id") or "tfs")
        if project.devops_webhook_publisher_id and publisher != project.devops_webhook_publisher_id:
            return AzureDevOpsWebhookValidationResult(valid=False, reason="invalid_publisher")

        subscription_id = headers.get("x-vss-subscriptionid") or headers.get("x-vss-subscription-id")
        if project.devops_webhook_subscription_id and subscription_id != project.devops_webhook_subscription_id:
            return AzureDevOpsWebhookValidationResult(valid=False, reason="invalid_subscription")

        if project.devops_webhook_hmac_secret:
            from ai_qa_tester.services.job_queue import canonicalize_json_bytes, compute_webhook_signature

            signature = headers.get("x-ado-signature") or headers.get("x-hub-signature-256")
            expected = compute_webhook_signature(project.devops_webhook_hmac_secret, canonicalize_json_bytes(payload))
            if signature != expected:
                return AzureDevOpsWebhookValidationResult(valid=False, reason="invalid_signature")

        notification_id = headers.get("x-vss-notificationid") or headers.get("x-vss-notification-id")
        state = store.sync_state.setdefault(project_id, {})
        processed = state.setdefault("processed_notification_ids", [])
        if notification_id and notification_id in processed:
            return AzureDevOpsWebhookValidationResult(valid=False, reason="duplicate_notification")
        if notification_id:
            processed.append(notification_id)

        return AzureDevOpsWebhookValidationResult(valid=True)

class IncrementalSyncService:
    def sync_changed_external_ids(self, project_id: str, changed_external_ids: list[str], trigger_type: str = "ado_webhook", environment: str = "uat", limit: int = 10) -> dict[str, Any]:
        project = store.projects.get(project_id)
        connector = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
        work_items = connector.get_work_items_by_external_ids(changed_external_ids)

        ingest_result = ingest_work_items(project_id, work_items, devops=connector)
        changed_internal_ids = [item.id for item in work_items]
        impact = ChangeImpactService().analyze(project_id, changed_internal_ids) if changed_internal_ids else {
            "changed_work_item_ids": [],
            "related_work_item_ids": [],
            "impacted_artifact_ids": [],
            "impacted_journey_artifact_ids": [],
            "impacted_journeys": [],
            "selected_scenarios": [],
        }
        selected = impact["selected_scenarios"][:limit]
        scenario_ids = [item["scenario_id"] for item in selected]

        run_payload = None
        analysis = None
        if scenario_ids:
            run = TestRun(
                id=f"run_webhook_{len(store.runs)+1}",
                project_id=project_id,
                environment=environment,
                trigger_type=trigger_type,
                status=RunStatus.QUEUED,
                scenario_ids=scenario_ids,
            )
            store.runs[run.id] = run
            executed = ExecutionService().execute(run)
            analysis = ResultAnalysisService().analyze(executed)
            run_payload = executed.model_dump(mode="json")
            publish_event(project_id, "impact.retest_run.created", {"run_id": executed.id, "scenario_ids": scenario_ids}, producer="incremental_sync")

        state = store.sync_state.setdefault(project_id, {})
        state["last_changed_external_ids"] = list(changed_external_ids)
        state["last_internal_ids"] = list(changed_internal_ids)

        return {
            "status": "accepted",
            "changed_external_ids": changed_external_ids,
            "changed_work_item_ids": changed_internal_ids,
            "ingest": ingest_result,
            "impact": impact,
            "run": run_payload,
            "analysis": analysis,
        }
