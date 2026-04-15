
from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from ai_qa_tester.models.contracts import PageModel, Project, RunStatus, SelectorProfile, TestRun, WorkItemFilter
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.association import AssociationService
from ai_qa_tester.services.connectors import DevOpsConnector
from ai_qa_tester.services.processing import ArtifactProcessor
from ai_qa_tester.services.scenario_generation import ScenarioGenerator
from ai_qa_tester.services.script_generation import ScriptGenerator
from ai_qa_tester.services.execution import ExecutionService
from ai_qa_tester.services.result_analysis import ResultAnalysisService
from ai_qa_tester.services.uploads import UploadService
from ai_qa_tester.services.playwright_assets import PlaywrightAssetService
from ai_qa_tester.services.vector_store import vector_store
from ai_qa_tester.services.sync_pipeline import ingest_work_items, process_attachment_artifacts, publish_event

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


class CreateProjectRequest(BaseModel):
    name: str
    devops_provider: str = "azure_devops"
    figma_enabled: bool = True
    devops_url: str | None = None
    devops_pat: str | None = None
    devops_webhook_secret: str | None = None
    devops_webhook_hmac_secret: str | None = None
    devops_webhook_subscription_id: str | None = None
    devops_webhook_publisher_id: str = "tfs"


class QueryWorkItemsRequest(BaseModel):
    filters: WorkItemFilter
    sync_mode: str = "incremental"


class SelectorOverrideRequest(BaseModel):
    locator: str | None = None
    strategy: str | None = None
    source_label: str | None = None
    element_type: str | None = None


class ReviewSelectorProfileRequest(BaseModel):
    approve: bool = True
    notes: str | None = None
    overrides: dict[str, SelectorOverrideRequest] = {}


@router.post("")
def create_project(request: CreateProjectRequest) -> dict[str, str | bool | None]:
    project_id = f"proj_{uuid4().hex[:8]}"
    project = Project(
        id=project_id,
        name=request.name,
        devops_provider=request.devops_provider,
        figma_enabled=request.figma_enabled,
        devops_url=request.devops_url,
        devops_pat=request.devops_pat,
        devops_webhook_secret=request.devops_webhook_secret,
        devops_webhook_hmac_secret=request.devops_webhook_hmac_secret,
        devops_webhook_subscription_id=request.devops_webhook_subscription_id,
        devops_webhook_publisher_id=request.devops_webhook_publisher_id,
    )
    store.projects[project_id] = project
    return {
        "id": project.id,
        "name": project.name,
        "status": project.status,
        "figma_enabled": project.figma_enabled,
        "devops_url": project.devops_url,
        "devops_webhook_subscription_id": project.devops_webhook_subscription_id,
    }


@router.post("/{project_id}/work-items/query")
def query_work_items(project_id: str, request: QueryWorkItemsRequest) -> dict:
    project = store.projects.get(project_id)
    devops = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
    work_items = devops.query_work_items(project_id, request.filters)
    result = ingest_work_items(project_id, work_items, devops=devops)
    return {
        "job_id": f"job_ingest_{uuid4().hex[:8]}",
        "status": "accepted",
        **result,
    }


@router.post("/{project_id}/work-items/{work_item_id}/context/sync")
def sync_work_item_context(project_id: str, work_item_id: str) -> dict:
    if work_item_id not in store.work_items:
        return {"status": "not_found", "work_item_id": work_item_id}

    item = store.work_items[work_item_id]
    project = store.projects.get(project_id)
    devops = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
    updated = devops.sync_work_item_context(item)
    store.work_items[work_item_id] = updated
    publish_event(
        project_id,
        "work_item.context.synced",
        {
            "work_item_id": updated.id,
            "comment_count": len(updated.comments),
            "related_work_item_count": len(updated.related_work_item_refs),
        },
    )
    return {
        "status": "accepted",
        "work_item": updated.model_dump(mode="json"),
        "comment_count": len(updated.comments),
        "related_work_item_count": len(updated.related_work_item_refs),
    }


@router.post("/{project_id}/work-items/{work_item_id}/attachments/sync")
def sync_work_item_attachments(project_id: str, work_item_id: str) -> dict:
    if work_item_id not in store.work_items:
        return {"status": "not_found", "work_item_id": work_item_id}

    item = store.work_items[work_item_id]
    project = store.projects.get(project_id)
    devops = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
    uploader = UploadService()
    processor = ArtifactProcessor()
    associator = AssociationService()
    generator = ScenarioGenerator()

    attachments = devops.fetch_attachments_for_work_item(project_id, item)
    artifact_ids, association_ids, scenario_ids, journey_ids = process_attachment_artifacts(
        project_id, item, attachments, uploader, processor, associator, generator
    ) if attachments else ([], [], [], [])

    if attachments:
        publish_event(
            project_id,
            "work_item.attachments.ingested",
            {
                "work_item_id": item.id,
                "artifact_ids": artifact_ids,
                "journey_ids": journey_ids,
            },
        )

    return {
        "status": "accepted",
        "work_item_id": work_item_id,
        "attachment_count": len(attachments),
        "artifact_ids": artifact_ids,
        "association_ids": association_ids,
        "scenario_ids": scenario_ids,
        "journey_ids": journey_ids,
    }


@router.post("/{project_id}/artifacts/upload-wireframe")
async def upload_wireframe(
    project_id: str,
    file: UploadFile = File(...),
    linked_entity_type: str | None = Form(default=None),
    linked_entity_id: str | None = Form(default=None),
) -> dict:
    content = await file.read()
    uploader = UploadService()
    processor = ArtifactProcessor()
    artifact = uploader.register_wireframe(
        project_id=project_id,
        filename=file.filename or "wireframe-upload",
        content_type=file.content_type or "application/octet-stream",
        content=content,
        linked_entity_type=linked_entity_type,
        linked_entity_id=linked_entity_id,
    )
    processed = processor.process(artifact)
    store.artifacts[processed.id] = processed
    vector_store.index_document(processed.id, " ".join(processed.metadata.get("extracted_text", [])), {"type": "artifact", "project_id": project_id})
    publish_event(project_id, "artifacts.processed", {"artifact_ids": [processed.id]})
    return {"artifact": processed.model_dump(mode="json")}


@router.post("/{project_id}/artifacts/upload-wireframe-journey")
async def upload_wireframe_journey(
    project_id: str,
    files: list[UploadFile] = File(...),
    journey_name: str | None = Form(default=None),
    linked_entity_type: str | None = Form(default=None),
    linked_entity_id: str | None = Form(default=None),
) -> dict:
    uploader = UploadService()
    processor = ArtifactProcessor()
    associator = AssociationService()
    generator = ScenarioGenerator()

    processed_steps = []
    for upload in files:
        content = await upload.read()
        artifact = uploader.register_wireframe(
            project_id=project_id,
            filename=upload.filename or "wireframe-upload",
            content_type=upload.content_type or "application/octet-stream",
            content=content,
            linked_entity_type=linked_entity_type,
            linked_entity_id=linked_entity_id,
        )
        processed = processor.process(artifact)
        store.artifacts[processed.id] = processed
        vector_store.index_document(processed.id, " ".join(processed.metadata.get("extracted_text", [])), {"type": "artifact", "project_id": project_id})
        processed_steps.append(processed)

    journey = uploader.register_journey(
        project_id=project_id,
        journey_name=journey_name,
        artifact_ids=[artifact.id for artifact in processed_steps],
        linked_entity_type=linked_entity_type,
        linked_entity_id=linked_entity_id,
    )
    processed_journey = processor.process_journey(journey, processed_steps)
    store.journeys[processed_journey.id] = processed_journey
    vector_store.index_document(processed_journey.id, " ".join(processed_journey.metadata.get("extracted_text", [])), {"type": "journey", "project_id": project_id})

    associations: list[str] = []
    scenarios: list[str] = []
    if linked_entity_type == "work_item" and linked_entity_id and linked_entity_id in store.work_items:
        work_item = store.work_items[linked_entity_id]
        association = associator.associate_work_item_to_artifact(project_id, work_item, processed_journey)
        store.associations[association.id] = association
        associations.append(association.id)
        for scenario in generator.generate(project_id, work_item, processed_journey, association):
            store.scenarios[scenario.id] = scenario
            scenarios.append(scenario.id)

    publish_event(
        project_id,
        "wireframe_journey.processed",
        {
            "journey_id": processed_journey.id,
            "artifact_ids": [artifact.id for artifact in processed_steps],
            "association_ids": associations,
            "scenario_ids": scenarios,
        },
    )

    return {
        "journey": processed_journey.model_dump(mode="json"),
        "step_artifacts": [artifact.model_dump(mode="json") for artifact in processed_steps],
        "association_ids": associations,
        "scenario_ids": scenarios,
    }


@router.get("/{project_id}/work-items")
def list_work_items(project_id: str) -> dict:
    items = [item.model_dump(mode="json") for item in store.work_items.values()]
    return {"items": items, "total": len(items)}


@router.get("/{project_id}/associations")
def list_associations(project_id: str, status: str | None = None) -> dict:
    items = [item.model_dump(mode="json") for item in store.associations.values()]
    if status:
        items = [item for item in items if item["status"] == status]
    return {"items": items, "total": len(items)}


@router.get("/{project_id}/journeys")
def list_journeys(project_id: str) -> dict:
    items = [item.model_dump(mode="json") for item in store.journeys.values()]
    return {"items": items, "total": len(items)}


@router.get("/{project_id}/scenarios")
def list_scenarios(project_id: str) -> dict:
    items = [item.model_dump(mode="json") for item in store.scenarios.values()]
    return {"items": items, "total": len(items)}




@router.post("/{project_id}/defects/{work_item_id}/execute-regressions")
def execute_defect_regressions(project_id: str, work_item_id: str, environment: str = "uat", limit: int = 3) -> dict:
    work_item = store.work_items.get(work_item_id)
    if work_item is None:
        return {"status": "not_found", "work_item_id": work_item_id}

    associator = AssociationService()
    generator = ScenarioGenerator()
    script_generator = ScriptGenerator()
    story_candidates = associator.retrieve_defect_story_candidates(project_id, work_item, top_k=limit)
    journey_candidates = associator.retrieve_defect_journey_candidates(project_id, work_item, top_k=limit)
    regression_candidates = associator.retrieve_defect_regression_candidates(project_id, work_item, top_k=limit)
    generated = generator.generate_regressions_from_defect(
        project_id,
        work_item,
        story_candidates=story_candidates,
        journey_candidates=journey_candidates,
        regression_candidates=regression_candidates,
        limit=limit,
    )
    generated_scenarios = [item["scenario"] for item in generated]
    scripts = script_generator.generate_and_store_for_scenarios(project_id, generated_scenarios) if generated_scenarios else []

    from uuid import uuid4
    run = TestRun(
        id=f"run_{uuid4().hex[:8]}",
        project_id=project_id,
        environment=environment,
        trigger_type="defect_retest",
        status=RunStatus.QUEUED,
        scenario_ids=[scenario.id for scenario in generated_scenarios],
    )
    store.runs[run.id] = run
    executed_run, executions = ExecutionService().execute_generated_scripts(run, [script.id for script in scripts])
    analysis = ResultAnalysisService().analyze(executed_run)

    publish_event(
        project_id,
        "defect.regressions.executed",
        {
            "work_item_id": work_item_id,
            "run_id": executed_run.id,
            "scenario_ids": [item["scenario"].id for item in generated],
            "script_ids": [script.id for script in scripts],
            "execution_ids": [execution.id for execution in executions],
        },
    )

    return {
        "status": "accepted",
        "work_item_id": work_item_id,
        "generated": [
            {
                "action": item["action"],
                "scenario": item["scenario"].model_dump(mode="json"),
            }
            for item in generated
        ],
        "scripts": [script.model_dump(mode="json") for script in scripts],
        "run": executed_run.model_dump(mode="json"),
        "executions": [execution.model_dump(mode="json") for execution in executions],
        "analysis": analysis,
    }

@router.get("/{project_id}/scripts")
def list_scripts(project_id: str, scenario_id: str | None = None) -> dict:
    items = [item.model_dump(mode="json") for item in store.scripts.values() if item.project_id == project_id]
    if scenario_id:
        items = [item for item in items if item["scenario_id"] == scenario_id]
    return {"items": items, "total": len(items)}


@router.post("/{project_id}/defects/{work_item_id}/generate-regressions")
def generate_defect_regressions(project_id: str, work_item_id: str, limit: int = 3) -> dict:
    work_item = store.work_items.get(work_item_id)
    if work_item is None:
        return {"status": "not_found", "work_item_id": work_item_id}

    associator = AssociationService()
    generator = ScenarioGenerator()
    story_candidates = associator.retrieve_defect_story_candidates(project_id, work_item, top_k=limit)
    journey_candidates = associator.retrieve_defect_journey_candidates(project_id, work_item, top_k=limit)
    regression_candidates = associator.retrieve_defect_regression_candidates(project_id, work_item, top_k=limit)
    generated = generator.generate_regressions_from_defect(
        project_id,
        work_item,
        story_candidates=story_candidates,
        journey_candidates=journey_candidates,
        regression_candidates=regression_candidates,
        limit=limit,
    )
    generated_scenarios = [item["scenario"] for item in generated]
    scripts = ScriptGenerator().generate_and_store_for_scenarios(project_id, generated_scenarios) if generated_scenarios else []

    publish_event(
        project_id,
        "defect.regressions.generated",
        {
            "work_item_id": work_item_id,
            "scenario_ids": [item["scenario"].id for item in generated],
            "script_ids": [script.id for script in scripts],
            "actions": [item["action"] for item in generated],
        },
    )

    return {
        "status": "accepted",
        "work_item_id": work_item_id,
        "generated": [
            {
                "action": item["action"],
                "scenario": item["scenario"].model_dump(mode="json"),
            }
            for item in generated
        ],
        "scripts": [script.model_dump(mode="json") for script in scripts],
    }


@router.post("/{project_id}/defects/{work_item_id}/triage-candidates")
def get_defect_triage_candidates(project_id: str, work_item_id: str, limit: int = 5) -> dict:
    work_item = store.work_items.get(work_item_id)
    if work_item is None:
        return {"status": "not_found", "work_item_id": work_item_id}

    associator = AssociationService()
    story_candidates = associator.retrieve_defect_story_candidates(project_id, work_item, top_k=limit)
    journey_candidates = associator.retrieve_defect_journey_candidates(project_id, work_item, top_k=limit)
    regression_candidates = associator.retrieve_defect_regression_candidates(project_id, work_item, top_k=limit)

    return {
        "status": "accepted",
        "work_item_id": work_item_id,
        "story_candidates": story_candidates,
        "journey_candidates": journey_candidates,
        "regression_candidates": regression_candidates,
    }


@router.post("/{project_id}/playwright/bootstrap")
def bootstrap_playwright_assets(project_id: str) -> dict:
    service = PlaywrightAssetService()
    page_models = service.build_from_project_artifacts(project_id)
    assets = service.generate_ts_assets(project_id)
    return {
        "status": "accepted",
        "page_models": [item.model_dump(mode="json") for item in page_models],
        "assets": assets,
    }


@router.get("/{project_id}/playwright/page-models")
def list_page_models(project_id: str) -> dict:
    items = [item.model_dump(mode="json") for item in store.page_models.values() if item.project_id == project_id]
    return {"items": items, "total": len(items)}


@router.post("/{project_id}/playwright/selector-profiles/bootstrap")
def bootstrap_selector_profiles(project_id: str) -> dict:
    service = PlaywrightAssetService()
    page_models = service.build_from_project_artifacts(project_id)
    profiles = service.build_selector_profiles(project_id)
    assets = service.generate_ts_assets(project_id)
    return {
        "status": "accepted",
        "page_model_count": len(page_models),
        "profile_count": len(profiles),
        "profiles": profiles,
        "assets": assets,
    }


@router.get("/{project_id}/playwright/selector-profiles")
def list_selector_profiles(project_id: str, approved_only: bool = False) -> dict:
    items = [sp for sp in store.selector_profiles.values() if sp.project_id == project_id]
    if approved_only:
        items = [sp for sp in items if sp.approved]
    return {"items": items, "total": len(items)}


@router.post("/{project_id}/playwright/selector-profiles/{profile_id}/review")
def review_selector_profile(project_id: str, profile_id: str, request: ReviewSelectorProfileRequest) -> dict:
    service = PlaywrightAssetService()
    try:
        profile = service.review_selector_profile(
            project_id,
            profile_id,
            approve=request.approve,
            overrides={k: v.model_dump(exclude_none=True) for k, v in request.overrides.items()},
            notes=request.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Selector profile not found") from exc
    assets = service.generate_ts_assets(project_id)
    return {"status": "accepted", "profile": profile, "assets": assets}
