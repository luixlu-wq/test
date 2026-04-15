from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.scenario_generation import ScenarioGenerator

router = APIRouter(prefix="/internal/v1/scenarios", tags=["scenarios"])


class GenerateScenarioRequest(BaseModel):
    project_id: str
    association_ids: list[str] = Field(default_factory=list)


@router.post("/generate")
def generate_scenarios(request: GenerateScenarioRequest) -> dict:
    generator = ScenarioGenerator()
    scenario_ids: list[str] = []
    for association_id in request.association_ids:
        association = store.associations.get(association_id)
        if association is None:
            raise HTTPException(status_code=404, detail=f"Association not found: {association_id}")
        work_item = store.work_items.get(association.source_entity.id)
        artifact = store.artifacts.get(association.target_entity.id)
        if work_item is None or artifact is None:
            raise HTTPException(status_code=404, detail="Traceability graph incomplete for scenario generation")
        for scenario in generator.generate(request.project_id, work_item, artifact, association):
            store.scenarios[scenario.id] = scenario
            scenario_ids.append(scenario.id)
    return {"scenario_ids": scenario_ids, "count": len(scenario_ids)}
