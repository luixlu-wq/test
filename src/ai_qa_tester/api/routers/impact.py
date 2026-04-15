from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_qa_tester.models.contracts import RunStatus, TestRun
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.change_impact import ChangeImpactService
from ai_qa_tester.services.execution import ExecutionService
from ai_qa_tester.services.result_analysis import ResultAnalysisService

router = APIRouter(prefix="/api/v1/projects/{project_id}/impact", tags=["impact"])


class ImpactAnalysisRequest(BaseModel):
    changed_work_item_ids: list[str] = Field(default_factory=list)
    limit: int = 20


class CreateRetestRunRequest(BaseModel):
    changed_work_item_ids: list[str] = Field(default_factory=list)
    environment: str = "uat"
    trigger_type: str = "impact_retest"
    limit: int = 20


@router.post("/analyze")
def analyze_change_impact(project_id: str, request: ImpactAnalysisRequest) -> dict:
    if not request.changed_work_item_ids:
        raise HTTPException(status_code=400, detail="changed_work_item_ids is required")
    analysis = ChangeImpactService().analyze(project_id, request.changed_work_item_ids)
    analysis["selected_scenarios"] = analysis["selected_scenarios"][: request.limit]
    analysis["status"] = "accepted"
    analysis["job_id"] = f"job_impact_{uuid4().hex[:8]}"
    return analysis


@router.post("/retest-run")
def create_retest_run(project_id: str, request: CreateRetestRunRequest) -> dict:
    if not request.changed_work_item_ids:
        raise HTTPException(status_code=400, detail="changed_work_item_ids is required")
    impact = ChangeImpactService().analyze(project_id, request.changed_work_item_ids)
    selected = impact["selected_scenarios"][: request.limit]
    scenario_ids = [item["scenario_id"] for item in selected]
    run = TestRun(
        id=f"run_{uuid4().hex[:8]}",
        project_id=project_id,
        environment=request.environment,
        trigger_type=request.trigger_type,
        status=RunStatus.QUEUED,
        scenario_ids=scenario_ids,
    )
    store.runs[run.id] = run
    executed = ExecutionService().execute(run)
    analysis = ResultAnalysisService().analyze(executed)
    return {
        "impact": impact,
        "run": executed.model_dump(mode="json"),
        "analysis": analysis,
    }
