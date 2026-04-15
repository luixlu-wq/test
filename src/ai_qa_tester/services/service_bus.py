from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import CommandEnvelope, EventEnvelope

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from azure.servicebus import ServiceBusClient, ServiceBusMessage
except Exception:  # pragma: no cover - optional dependency
    ServiceBusClient = None
    ServiceBusMessage = None


def _json_default(value: Any) -> Any:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value)!r} is not JSON serializable")


@dataclass
class LocalServiceBusStore:
    command_messages: list[dict[str, Any]] = field(default_factory=list)
    event_messages: list[dict[str, Any]] = field(default_factory=list)

    def clear(self) -> None:
        self.command_messages.clear()
        self.event_messages.clear()


class AzureServiceBusTransport:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.service_bus_enabled:
            raise RuntimeError("service bus disabled")
        if not settings.service_bus_connection_string:
            raise RuntimeError("service bus connection string missing")
        if ServiceBusClient is None or ServiceBusMessage is None:
            raise RuntimeError("azure-servicebus package not installed")
        self.settings = settings
        self.client = ServiceBusClient.from_connection_string(settings.service_bus_connection_string)

    def send_command(self, payload: dict[str, Any]) -> None:
        with self.client:
            sender = self.client.get_queue_sender(queue_name=self.settings.service_bus_command_queue)
            with sender:
                sender.send_messages(ServiceBusMessage(json.dumps(payload, default=_json_default)))

    def send_event(self, payload: dict[str, Any]) -> None:
        with self.client:
            sender = self.client.get_topic_sender(topic_name=self.settings.service_bus_event_topic)
            with sender:
                sender.send_messages(ServiceBusMessage(json.dumps(payload, default=_json_default)))


@dataclass
class ServiceBusService:
    local_store: LocalServiceBusStore = field(default_factory=LocalServiceBusStore)

    def _try_transport(self) -> AzureServiceBusTransport | None:
        settings = get_settings()
        if not settings.service_bus_enabled:
            return None
        try:
            return AzureServiceBusTransport()
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("service bus unavailable, falling back to local store", extra={"error": str(exc)})
            return None

    def publish_command(self, command: CommandEnvelope) -> dict[str, Any]:
        payload = command.model_dump(mode="json")
        transport = self._try_transport()
        if transport is not None:
            transport.send_command(payload)
            return {"mode": "azure_service_bus", "message_type": "command", "command_id": command.command_id}
        self.local_store.command_messages.append(payload)
        return {"mode": "local_fallback", "message_type": "command", "command_id": command.command_id}

    def publish_event(self, event: EventEnvelope) -> dict[str, Any]:
        payload = event.model_dump(mode="json")
        transport = self._try_transport()
        if transport is not None:
            transport.send_event(payload)
            return {"mode": "azure_service_bus", "message_type": "event", "event_id": event.event_id}
        self.local_store.event_messages.append(payload)
        return {"mode": "local_fallback", "message_type": "event", "event_id": event.event_id}

    def pop_local_command(self) -> CommandEnvelope | None:
        if not self.local_store.command_messages:
            return None
        return CommandEnvelope.model_validate(self.local_store.command_messages.pop(0))

    def pop_local_event(self) -> EventEnvelope | None:
        if not self.local_store.event_messages:
            return None
        return EventEnvelope.model_validate(self.local_store.event_messages.pop(0))

    def clear(self) -> None:
        self.local_store.clear()


service_bus = ServiceBusService()
