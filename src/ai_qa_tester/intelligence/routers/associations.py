from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.association import AssociationService

router = APIRouter(prefix="/internal/v1/associations", tags=["associations"])


class GenerateAssociationsRequest(BaseModel):
    project_id: str
    work_item_ids: list[str] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)


@router.post("/generate")
def generate_associations(request: GenerateAssociationsRequest) -> dict:
    service = AssociationService()
    ids: list[str] = []
    for work_item_id in request.work_item_ids:
        work_item = store.work_items.get(work_item_id)
        if work_item is None:
            raise HTTPException(status_code=404, detail=f"Work item not found: {work_item_id}")
        for artifact_id in request.artifact_ids:
            artifact = store.artifacts.get(artifact_id)
            if artifact is None:
                raise HTTPException(status_code=404, detail=f"Artifact not found: {artifact_id}")
            association = service.associate_work_item_to_artifact(request.project_id, work_item, artifact)
            store.associations[association.id] = association
            ids.append(association.id)
    return {"association_ids": ids, "count": len(ids)}
