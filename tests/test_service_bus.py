from ai_qa_tester.models.contracts import CommandEnvelope, EventEnvelope
from ai_qa_tester.services.event_bus import event_bus
from ai_qa_tester.services.service_bus import service_bus


def setup_function() -> None:
    event_bus.clear()


def test_local_fallback_command_and_event_buffers() -> None:
    command = CommandEnvelope(
        command_id="cmd_1",
        command_type="incremental_sync",
        project_id="proj_01",
        correlation_id="corr_1",
        payload={"job_id": "job_1", "changed_external_ids": ["123"]},
    )
    event = EventEnvelope(
        event_id="evt_1",
        event_type="work_items.ingested",
        project_id="proj_01",
        correlation_id="corr_1",
        causation_id="cmd_1",
        producer="test",
        payload={"work_item_ids": ["wk_1"]},
    )

    cmd_result = service_bus.publish_command(command)
    evt_result = service_bus.publish_event(event)

    assert cmd_result["mode"] == "local_fallback"
    assert evt_result["mode"] == "local_fallback"
    assert service_bus.pop_local_command() is not None
    assert service_bus.pop_local_event() is not None


def test_event_bus_records_and_falls_back_locally() -> None:
    event = EventEnvelope(
        event_id="evt_2",
        event_type="results.analyzed",
        project_id="proj_01",
        correlation_id="corr_2",
        causation_id="cmd_2",
        producer="test",
        payload={"run_id": "run_1"},
    )
    event_bus.publish(event)
    assert event_bus.published_events[0].event_id == "evt_2"
