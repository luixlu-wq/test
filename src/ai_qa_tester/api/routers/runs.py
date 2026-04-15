from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_qa_tester.models.contracts import RunStatus, TestRun
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.connectors import DevOpsConnector
from ai_qa_tester.services.execution import ExecutionService
from ai_qa_tester.services.result_analysis import ResultAnalysisService
from ai_qa_tester.services.selector_learning import SelectorLearningService
from ai_qa_tester.services.script_generation import ScriptGenerator
from ai_qa_tester.services.run_comparison import RunComparisonService
from ai_qa_tester.services.stability_analytics import StabilityAnalyticsService

router = APIRouter(prefix="/api/v1/projects/{project_id}/runs", tags=["runs"])


class CreateRunRequest(BaseModel):
    environment: str
    scenario_ids: list[str] = Field(default_factory=list)
    script_ids: list[str] = Field(default_factory=list)
    trigger_type: str = "manual"


class PublishSummaryRequest(BaseModel):
    work_item_id: str


class PublishTraceabilityRequest(BaseModel):
    work_item_id: str
    text: str


class CreateBugFromRunRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    work_item_id: str | None = None


@router.post("")
def create_run(project_id: str, request: CreateRunRequest) -> dict:
    scenario_ids = list(request.scenario_ids)
    if request.script_ids and not scenario_ids:
        scenario_ids = [store.scripts[script_id].scenario_id for script_id in request.script_ids if script_id in store.scripts]
    run = TestRun(
        id=f"run_{uuid4().hex[:8]}",
        project_id=project_id,
        environment=request.environment,
        trigger_type=request.trigger_type,
        status=RunStatus.QUEUED,
        scenario_ids=scenario_ids,
    )
    store.runs[run.id] = run

    execution_service = ExecutionService()
    if request.script_ids:
        executed, executions = execution_service.execute_generated_scripts(run, request.script_ids)
        analysis = ResultAnalysisService().analyze(executed)
        return {"run": executed.model_dump(mode="json"), "executions": [item.model_dump(mode="json") for item in executions], "analysis": analysis}

    executed = execution_service.execute(run)
    analysis = ResultAnalysisService().analyze(executed)
    return {"run": executed.model_dump(mode="json"), "analysis": analysis}


@router.get("/{run_id}")
def get_run(project_id: str, run_id: str) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run.model_dump(mode="json")


@router.post('/{run_id}/publish-summary')
def publish_run_summary(project_id: str, run_id: str, request: PublishSummaryRequest) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail='Run not found')
    project = store.projects.get(project_id)
    connector = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
    if not connector.base_url or not connector.pat:
        return {'status': 'skipped', 'reason': 'Azure DevOps config missing'}
    payload = connector.publish_run_summary_comment(request.work_item_id, run.id, run.summary, run.scenario_ids)
    return {'status': 'published', 'work_item_id': request.work_item_id, 'comment': payload}


@router.post('/{run_id}/publish-traceability')
def publish_traceability(project_id: str, run_id: str, request: PublishTraceabilityRequest) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail='Run not found')
    project = store.projects.get(project_id)
    connector = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
    if not connector.base_url or not connector.pat:
        return {'status': 'skipped', 'reason': 'Azure DevOps config missing'}
    payload = connector.publish_traceability_comment(request.work_item_id, request.text)
    return {'status': 'published', 'work_item_id': request.work_item_id, 'comment': payload}


@router.post('/{run_id}/create-bug')
def create_bug_from_run(project_id: str, run_id: str, request: CreateBugFromRunRequest) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail='Run not found')
    project = store.projects.get(project_id)
    connector = DevOpsConnector(base_url=project.devops_url if project else None, pat=project.devops_pat if project else None)
    if not connector.base_url or not connector.pat:
        return {'status': 'skipped', 'reason': 'Azure DevOps config missing'}

    failed_titles = [item.get('title', item.get('scenario_id', 'unknown scenario')) for item in run.result_details]
    title = request.title or f'AI QA failure for run {run.id}'
    description = request.description or (
        f'Generated from AI QA run {run.id} in {run.environment}. ' 
        f'Failed scenarios: {", ".join(failed_titles) if failed_titles else "none"}.'
    )
    related = store.work_items.get(request.work_item_id) if request.work_item_id else None
    repro = [f"Re-run scenario: {name}" for name in failed_titles] or ['Review AI QA run evidence.']
    payload = connector.upsert_bug_from_failed_run(
        run_id=run.id,
        title=title,
        description=description,
        repro_steps=repro,
        area_path=related.area_path if related else None,
        iteration_path=related.sprint if related else None,
        related_work_item_id=related.external_id if related else request.work_item_id,
    )
    return {'status': payload.get('action', 'created'), 'bug': payload.get('bug'), 'dedup': payload}


@router.get("/{run_id}/executions")
def get_run_executions(project_id: str, run_id: str) -> dict:
    executions = [item.model_dump(mode="json") for item in store.script_executions.values() if item.project_id == project_id and item.run_id == run_id]
    return {"items": executions, "total": len(executions)}




class CompareRunsRequest(BaseModel):
    against_run_id: str



class StabilityReportRequest(BaseModel):
    baseline_run_id: str | None = None
    against_run_id: str | None = None
    candidate_run_id: str | None = None
    journey: str | None = None

class ApplySelectorLearningRequest(BaseModel):
    approve: bool = False
    notes: str | None = None
    regenerate_scripts: bool = True
    auto_rerun: bool = False
    environment: str | None = None


@router.post("/{run_id}/compare")
def compare_run(project_id: str, run_id: str, request: CompareRunsRequest) -> dict:
    run = store.runs.get(run_id)
    against = store.runs.get(request.against_run_id)
    if run is None or against is None:
        raise HTTPException(status_code=404, detail="Run not found")
    report = RunComparisonService().compare_runs(project_id, request.against_run_id, run_id)
    return {"status": "accepted", "comparison": report.model_dump(mode="json")}


@router.get("/{run_id}/comparisons")
def list_run_comparisons(project_id: str, run_id: str) -> dict:
    items = [
        item.model_dump(mode="json")
        for item in store.run_comparisons.values()
        if item.project_id == project_id and (item.baseline_run_id == run_id or item.candidate_run_id == run_id)
    ]
    return {"items": items, "total": len(items)}


@router.post("/{run_id}/selector-feedback")
def get_selector_feedback(project_id: str, run_id: str) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    reports = SelectorLearningService().analyze_run(project_id, run_id)
    return {"status": "accepted", "run_id": run_id, "reports": [r.model_dump(mode="json") for r in reports], "total": len(reports)}


@router.post("/{run_id}/selector-feedback/{report_id}/apply")
def apply_selector_feedback(project_id: str, run_id: str, report_id: str, request: ApplySelectorLearningRequest) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    try:
        profile = SelectorLearningService().apply_report(project_id, report_id, approve=request.approve, notes=request.notes)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Selector learning report not found") from exc

    regenerated = []
    rerun_payload = None
    if request.regenerate_scripts and request.approve:
        scenarios = [s for s in store.scenarios.values() if s.project_id == project_id and s.journey == profile.journey]
        regenerated = ScriptGenerator().generate_and_store_for_scenarios(project_id, scenarios)

    if request.auto_rerun and request.approve and regenerated:
        rerun = TestRun(
            id=f"run_{uuid4().hex[:8]}",
            project_id=project_id,
            environment=request.environment or run.environment,
            trigger_type='selector_retest',
            status=RunStatus.QUEUED,
            scenario_ids=[script.scenario_id for script in regenerated],
        )
        store.runs[rerun.id] = rerun
        executed_run, executions = ExecutionService().execute_generated_scripts(rerun, [script.id for script in regenerated])
        analysis = ResultAnalysisService().analyze(executed_run)
        comparison = RunComparisonService().compare_runs(project_id, run.id, executed_run.id)
        stability_report = StabilityAnalyticsService().build_report(project_id, baseline_run_id=run.id, candidate_run_id=executed_run.id)
        rerun_payload = {
            "run": executed_run.model_dump(mode="json"),
            "executions": [item.model_dump(mode="json") for item in executions],
            "analysis": analysis,
            "comparison": comparison.model_dump(mode="json"),
            "stability_report": stability_report.model_dump(mode="json"),
        }

    return {
        "status": "accepted",
        "profile": profile.model_dump(mode="json"),
        "regenerated_scripts": [script.model_dump(mode="json") for script in regenerated],
        "regenerated_count": len(regenerated),
        "rerun": rerun_payload,
    }


@router.post("/{run_id}/stability-report")
def create_stability_report(project_id: str, run_id: str, request: StabilityReportRequest) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    report = StabilityAnalyticsService().build_report(
        project_id,
        baseline_run_id=request.baseline_run_id or request.against_run_id or run_id,
        candidate_run_id=request.candidate_run_id,
        journey=request.journey,
    )
    return {"status": "accepted", "report": report.model_dump(mode="json")}


@router.get("/{run_id}/stability-reports")
def list_stability_reports(project_id: str, run_id: str) -> dict:
    items = [
        item.model_dump(mode="json")
        for item in store.stability_reports.values()
        if item.project_id == project_id and (item.baseline_run_id == run_id or item.candidate_run_id == run_id)
    ]
    return {"items": items, "total": len(items)}
