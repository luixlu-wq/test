from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.result_analysis import ResultAnalysisService

router = APIRouter(prefix="/internal/v1/results", tags=["results"])


@router.get("/insights/{run_id}")
def get_insights(run_id: str) -> dict:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return ResultAnalysisService().analyze(run)
