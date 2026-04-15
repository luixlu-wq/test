from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.script_generation import ScriptGenerator

router = APIRouter(prefix="/internal/v1/scripts", tags=["scripts"])


class GenerateScriptsRequest(BaseModel):
    scenario_ids: list[str] = Field(default_factory=list)


@router.post("/generate")
def generate_scripts(request: GenerateScriptsRequest) -> dict:
    generator = ScriptGenerator()
    scenarios = []
    for scenario_id in request.scenario_ids:
        scenario = store.scenarios.get(scenario_id)
        if scenario is None:
            raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")
        scenarios.append(scenario)
    generated = generator.generate_and_store_for_scenarios(scenarios[0].project_id if scenarios else "", scenarios)
    return {"scripts": [script.model_dump(mode="json") for script in generated]}
