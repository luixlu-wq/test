from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import EntityRef, JobStatus, Project, TestScenario, WorkItem, WorkItemType
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.event_bus import event_bus
from ai_qa_tester.services.service_bus import service_bus
from ai_qa_tester.services.job_queue import canonicalize_json_bytes, compute_webhook_signature
from ai_qa_tester.services.webhooks import AzureDevOpsWebhookService


def setup_function() -> None:
    store.projects.clear()
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()
    store.runs.clear()
    store.jobs.clear()
    store.job_queue.clear()
    store.sync_state.clear()
    event_bus.clear()
    service_bus.clear()


def test_parse_azure_devops_webhook_payload_extracts_changed_id() -> None:
    payload = {
        "eventType": "workitem.updated",
        "resource": {
            "workItemId": 123,
            "revision": {"id": 123, "rev": 7},
        },
    }
    parsed = AzureDevOpsWebhookService().parse_payload(payload)
    assert parsed.event_type == "workitem.updated"
    assert parsed.changed_external_ids == ["123"]
    assert parsed.raw_revision == 7


def test_incremental_sync_endpoint_fetches_exact_changed_ids(monkeypatch) -> None:
    client = TestClient(app)
    store.projects["proj_01"] = Project(id="proj_01", name="Demo")

    def fake_get(self, external_ids):
        assert external_ids == ["123"]
        return [
            WorkItem(
                id="wk_123",
                external_id="123",
                type=WorkItemType.STORY,
                title="Create project upload flow",
                description="Upload project definition and review submission",
                comments=["review step validation"],
            )
        ]

    monkeypatch.setattr("ai_qa_tester.services.connectors.DevOpsConnector.get_work_items_by_external_ids", fake_get)

    store.scenarios["scn_seed"] = TestScenario(
        id="scn_seed",
        project_id="proj_01",
        title="Create project review validation",
        scenario_type="integration",
        journey="create_project",
        steps=["Upload project definition", "Review and submit"],
        expected_results=["Project is submitted successfully"],
        source_refs=[EntityRef(type="work_item", id="wk_123")],
        coverage_reason="seeded regression",
        review_required=False,
    )

    response = client.post(
        "/api/v1/projects/proj_01/sync/incremental",
        json={"changed_external_ids": ["123"], "environment": "uat", "limit": 5},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["changed_work_item_ids"] == ["wk_123"]
    assert payload["impact"]["selected_scenarios"]
    assert payload["run"]["trigger_type"] == "incremental_sync"
    assert store.sync_state["proj_01"]["last_changed_external_ids"] == ["123"]


def test_webhook_endpoint_validates_token_signature_and_queues_job(monkeypatch) -> None:
    client = TestClient(app)
    store.projects["proj_secure"] = Project(
        id="proj_secure",
        name="Secure",
        devops_webhook_secret="secret-token",
        devops_webhook_hmac_secret="hmac-secret",
        devops_webhook_subscription_id="sub-123",
    )

    def fake_get(self, external_ids):
        return [
            WorkItem(
                id="wk_456",
                external_id="456",
                type=WorkItemType.DEFECT,
                title="Upload review defect",
                description="Review step fails after upload",
            )
        ]

    monkeypatch.setattr("ai_qa_tester.services.connectors.DevOpsConnector.get_work_items_by_external_ids", fake_get)

    payload = {"eventType": "workitem.updated", "resource": {"workItemId": 456}, "publisherId": "tfs"}

    unauthorized = client.post(
        "/api/v1/projects/proj_secure/webhooks/azure-devops",
        json=payload,
    )
    assert unauthorized.status_code == 401

    bad_sig = client.post(
        "/api/v1/projects/proj_secure/webhooks/azure-devops",
        headers={
            "X-Webhook-Token": "secret-token",
            "X-VSS-SubscriptionId": "sub-123",
            "X-Ado-Signature": "sha256=bad",
        },
        json=payload,
    )
    assert bad_sig.status_code == 401

    signature = compute_webhook_signature("hmac-secret", canonicalize_json_bytes(payload))
    response = client.post(
        "/api/v1/projects/proj_secure/webhooks/azure-devops",
        headers={
            "X-Webhook-Token": "secret-token",
            "X-VSS-SubscriptionId": "sub-123",
            "X-VSS-NotificationId": "notif-1",
            "X-Ado-Signature": signature,
        },
        json=payload,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "accepted"
    assert body["mode"] == "queued"
    job_id = body["job_id"]
    assert job_id in store.jobs
    assert store.jobs[job_id].status in {JobStatus.QUEUED, JobStatus.COMPLETED}

    job_resp = client.get(f"/api/v1/projects/proj_secure/jobs/{job_id}")
    assert job_resp.status_code == 200


def test_duplicate_notification_is_ignored() -> None:
    client = TestClient(app)
    store.projects["proj_secure"] = Project(id="proj_secure", name="Secure")
    payload = {"eventType": "workitem.updated", "resource": {"workItemId": 456}, "publisherId": "tfs"}

    first = client.post(
        "/api/v1/projects/proj_secure/webhooks/azure-devops",
        headers={"X-VSS-NotificationId": "notif-dup"},
        json=payload,
    )
    assert first.status_code == 200

    second = client.post(
        "/api/v1/projects/proj_secure/webhooks/azure-devops",
        headers={"X-VSS-NotificationId": "notif-dup"},
        json=payload,
    )
    assert second.status_code == 200
    assert second.json()["status"] == "ignored"


def test_process_next_command_endpoint_executes_local_bus_message(monkeypatch) -> None:
    client = TestClient(app)
    store.projects["proj_01"] = Project(id="proj_01", name="Demo")

    def fake_get(self, external_ids):
        return [
            WorkItem(
                id="wk_789",
                external_id="789",
                type=WorkItemType.STORY,
                title="Create project upload flow",
                description="Upload project definition and submit",
            )
        ]

    monkeypatch.setattr("ai_qa_tester.services.connectors.DevOpsConnector.get_work_items_by_external_ids", fake_get)

    payload = {"eventType": "workitem.updated", "resource": {"workItemId": 789}, "publisherId": "tfs"}
    response = client.post("/api/v1/projects/proj_01/webhooks/azure-devops", json=payload)
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    assert store.jobs[job_id].status in {JobStatus.QUEUED, JobStatus.COMPLETED}

    processed = client.post("/api/v1/projects/proj_01/jobs/process-next-command")
    assert processed.status_code == 200
    assert processed.json()["status"] in {"processed", "idle"}
