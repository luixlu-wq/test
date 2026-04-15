from __future__ import annotations

import logging
from dataclasses import dataclass, field

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import EventEnvelope
from ai_qa_tester.services.service_bus import service_bus

logger = logging.getLogger(__name__)


@dataclass
class EventBus:
    published_events: list[EventEnvelope] = field(default_factory=list)

    def publish(self, event: EventEnvelope) -> None:
        self.published_events.append(event)
        settings = get_settings()
        mode = "memory_only"
        if settings.event_bus_enabled or settings.service_bus_enabled:
            result = service_bus.publish_event(event)
            mode = result["mode"]
        logger.info("published event", extra={"event": event.model_dump(mode='json'), "delivery_mode": mode})

    def clear(self) -> None:
        self.published_events.clear()
        service_bus.clear()


event_bus = EventBus()
