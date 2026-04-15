from __future__ import annotations

from uuid import uuid4

from ai_qa_tester.models.contracts import EventEnvelope, WorkItem
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.association import AssociationService
from ai_qa_tester.services.connectors import AzureDevOpsAttachment, DevOpsConnector, FigmaConnector
from ai_qa_tester.services.event_bus import event_bus
from ai_qa_tester.services.processing import ArtifactProcessor
from ai_qa_tester.services.scenario_generation import ScenarioGenerator
from ai_qa_tester.services.uploads import UploadService
from ai_qa_tester.services.vector_store import vector_store


def publish_event(project_id: str, event_type: str, payload: dict, producer: str = "sync_pipeline") -> EventEnvelope:
    event = EventEnvelope(
        event_id=f"evt_{uuid4().hex[:8]}",
        event_type=event_type,
        project_id=project_id,
        correlation_id=f"corr_{uuid4().hex[:8]}",
        causation_id=f"cmd_{uuid4().hex[:8]}",
        producer=producer,
        payload=payload,
    )
    event_bus.publish(event)
    return event


def process_single_artifact(project_id: str, item: WorkItem, artifact, processor: ArtifactProcessor, associator: AssociationService, generator: ScenarioGenerator) -> tuple[list[str], list[str], list[str]]:
    created_artifacts: list[str] = []
    created_associations: list[str] = []
    created_scenarios: list[str] = []

    processed = processor.process(artifact)
    store.artifacts[processed.id] = processed
    vector_store.index_document(processed.id, " ".join(processed.metadata.get("extracted_text", [])), {"type": "artifact", "project_id": project_id})
    created_artifacts.append(processed.id)

    association = associator.associate_work_item_to_artifact(project_id, item, processed)
    store.associations[association.id] = association
    created_associations.append(association.id)

    for scenario in generator.generate(project_id, item, processed, association):
        store.scenarios[scenario.id] = scenario
        created_scenarios.append(scenario.id)

    return created_artifacts, created_associations, created_scenarios


def group_into_journey(attachments: list[AzureDevOpsAttachment]) -> bool:
    if len(attachments) < 2:
        return False
    names = " ".join(attachment.name.lower() for attachment in attachments)
    return any(token in names for token in ["step-", "step ", "before", "review", "upload", "location"])


def process_attachment_artifacts(project_id: str, item: WorkItem, attachments: list[AzureDevOpsAttachment], uploader: UploadService, processor: ArtifactProcessor, associator: AssociationService, generator: ScenarioGenerator) -> tuple[list[str], list[str], list[str], list[str]]:
    created_artifacts: list[str] = []
    created_associations: list[str] = []
    created_scenarios: list[str] = []
    created_journeys: list[str] = []

    processed_steps = []
    for attachment in attachments:
        artifact = uploader.register_wireframe(
            project_id=project_id,
            filename=attachment.name,
            content_type=attachment.content_type,
            content=attachment.content,
            linked_entity_type="work_item",
            linked_entity_id=item.id,
        )
        artifact.metadata["ado_attachment_url"] = attachment.url
        artifact.metadata["ado_relation_type"] = attachment.relation_type
        artifact.metadata["source_work_item_id"] = attachment.source_work_item_id
        processed = processor.process(artifact)
        store.artifacts[processed.id] = processed
        vector_store.index_document(processed.id, " ".join(processed.metadata.get("extracted_text", [])), {"type": "artifact", "project_id": project_id})
        processed_steps.append(processed)
        created_artifacts.append(processed.id)

    if group_into_journey(attachments):
        journey = uploader.register_journey(
            project_id=project_id,
            journey_name=None,
            artifact_ids=[artifact.id for artifact in processed_steps],
            linked_entity_type="work_item",
            linked_entity_id=item.id,
        )
        processed_journey = processor.process_journey(journey, processed_steps)
        store.journeys[processed_journey.id] = processed_journey
        vector_store.index_document(processed_journey.id, " ".join(processed_journey.metadata.get("extracted_text", [])), {"type": "journey", "project_id": project_id})
        created_journeys.append(processed_journey.id)

        association = associator.associate_work_item_to_artifact(project_id, item, processed_journey)
        store.associations[association.id] = association
        created_associations.append(association.id)

        for scenario in generator.generate(project_id, item, processed_journey, association):
            store.scenarios[scenario.id] = scenario
            created_scenarios.append(scenario.id)
    else:
        for processed in processed_steps:
            association = associator.associate_work_item_to_artifact(project_id, item, processed)
            store.associations[association.id] = association
            created_associations.append(association.id)

            for scenario in generator.generate(project_id, item, processed, association):
                store.scenarios[scenario.id] = scenario
                created_scenarios.append(scenario.id)

    return created_artifacts, created_associations, created_scenarios, created_journeys


def ingest_work_items(project_id: str, work_items: list[WorkItem], devops: DevOpsConnector | None = None) -> dict:
    figma = FigmaConnector()
    uploader = UploadService()
    processor = ArtifactProcessor()
    associator = AssociationService()
    generator = ScenarioGenerator()

    for item in work_items:
        store.work_items[item.id] = item
        vector_store.index_document(
            item.id,
            " ".join([item.title, item.description, " ".join(item.acceptance_criteria), " ".join(item.tags), " ".join(item.comments)]).strip(),
            {"type": "work_item", "project_id": project_id, "journey": None, "work_item_type": item.type.value, "external_id": item.external_id},
        )

    publish_event(project_id, "work_items.ingested", {"work_item_ids": [item.id for item in work_items]})

    created_artifacts: list[str] = []
    created_associations: list[str] = []
    created_scenarios: list[str] = []
    created_journeys: list[str] = []
    for item in work_items:
        figma_urls = [ref["value"] for ref in item.linked_artifact_refs if ref.get("type") == "figma_url"]
        artifacts = figma.fetch_from_urls(project_id, figma_urls)
        for artifact in artifacts:
            art_ids, assoc_ids, scen_ids = process_single_artifact(project_id, item, artifact, processor, associator, generator)
            created_artifacts.extend(art_ids)
            created_associations.extend(assoc_ids)
            created_scenarios.extend(scen_ids)

        if devops:
            attachments = devops.fetch_attachments_for_work_item(project_id, item)
            if attachments:
                att_artifacts, att_associations, att_scenarios, journey_ids = process_attachment_artifacts(project_id, item, attachments, uploader, processor, associator, generator)
                created_artifacts.extend(att_artifacts)
                created_associations.extend(att_associations)
                created_scenarios.extend(att_scenarios)
                created_journeys.extend(journey_ids)
                publish_event(project_id, "work_item.attachments.ingested", {"work_item_id": item.id, "artifact_ids": att_artifacts, "journey_ids": journey_ids})

    return {
        "work_item_ids": [item.id for item in work_items],
        "artifact_ids": created_artifacts,
        "association_ids": created_associations,
        "scenario_ids": created_scenarios,
        "journey_ids": created_journeys,
    }
