from __future__ import annotations

from uuid import uuid4

from ai_qa_tester.models.contracts import (
    Artifact,
    Association,
    AssociationDecision,
    AssociationEvidence,
    EntityRef,
    JourneyArtifact,
    WorkItem,
    WorkItemType,
)
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.vector_store import VectorStoreService, vector_store


class AssociationService:
    def __init__(self, vector_backend: VectorStoreService | None = None) -> None:
        self.vector_store = vector_backend or vector_store

    def associate_work_item_to_artifact(self, project_id: str, work_item: WorkItem, artifact: Artifact | JourneyArtifact) -> Association:
        evidence: list[AssociationEvidence] = []
        confidence = 0.0

        if getattr(artifact, "raw_uri", None) and any(ref.get("value") == artifact.raw_uri for ref in work_item.linked_artifact_refs):
            evidence.append(
                AssociationEvidence(
                    type="direct_reference",
                    strength=1.0,
                    detail="Work item contains artifact URL",
                )
            )
            confidence += 0.65

        semantic_seed = self._semantic_seed(artifact).lower()
        title_tokens = [token for token in work_item.title.lower().split() if len(token) > 2]
        semantic_matches = [token for token in title_tokens if token in semantic_seed]
        if semantic_matches:
            evidence.append(
                AssociationEvidence(
                    type="semantic",
                    strength=0.8,
                    detail=f"Artifact content overlaps work item title tokens: {', '.join(semantic_matches[:4])}",
                )
            )
            confidence += 0.25

        work_item_seed = " ".join(
            [
                work_item.title,
                work_item.description,
                " ".join(work_item.acceptance_criteria),
                " ".join(work_item.tags),
                " ".join(work_item.comments),
                " ".join(ref.get("name", "") for ref in work_item.related_work_item_refs),
            ]
        ).lower()
        artifact_journey = self._journey_name(artifact)
        if artifact_journey and (any(token in artifact_journey for token in title_tokens) or artifact_journey in work_item_seed):
            evidence.append(
                AssociationEvidence(
                    type="journey",
                    strength=0.85,
                    detail=f"Artifact implies user journey: {artifact_journey}",
                )
            )
            confidence += 0.25
        elif artifact_journey and any(term in work_item_seed for term in artifact_journey.split("_")):
            evidence.append(
                AssociationEvidence(
                    type="journey",
                    strength=0.65,
                    detail=f"Artifact journey overlaps work item narrative: {artifact_journey}",
                )
            )
            confidence += 0.1

        retrieval_query = " ".join(
            [
                work_item.title,
                work_item.description,
                " ".join(work_item.acceptance_criteria),
                " ".join(work_item.tags),
                " ".join(work_item.comments),
            ]
        ).strip()
        if retrieval_query:
            vector_hits = self.vector_store.search_similar(
                retrieval_query,
                top_k=5,
                metadata_filters={"project_id": project_id},
            )
            matching_hit = next((hit for hit in vector_hits if hit.get("doc_id") == artifact.id), None)
            if matching_hit:
                score = min(max(float(matching_hit.get("score", 0.0)), 0.0), 1.0)
                evidence.append(
                    AssociationEvidence(
                        type="semantic",
                        strength=score,
                        detail=f"Vector retrieval matched artifact with score {score:.4f}",
                    )
                )
                confidence += min(0.22, score * 0.3)
            elif vector_hits:
                top_hit = vector_hits[0]
                if top_hit.get("metadata", {}).get("journey") == artifact_journey and artifact_journey:
                    score = min(max(float(top_hit.get("score", 0.0)), 0.0), 1.0)
                    evidence.append(
                        AssociationEvidence(
                            type="semantic",
                            strength=round(score * 0.75, 4),
                            detail=f"Vector retrieval found same-journey candidate {top_hit.get('doc_id')} for journey {artifact_journey}",
                        )
                    )
                    confidence += min(0.08, score * 0.1)

        if work_item.comments:
            comment_matches = [comment for comment in work_item.comments if any(token in comment.lower() for token in title_tokens) or any(token in semantic_seed for token in comment.lower().split())]
            if comment_matches:
                evidence.append(
                    AssociationEvidence(
                        type="metadata",
                        strength=0.7,
                        detail="Work item discussion comments reinforce the artifact context",
                    )
                )
                confidence += 0.1

        if work_item.related_work_item_refs:
            relation_types = ", ".join(sorted({ref.get("relation_type", "related") for ref in work_item.related_work_item_refs}))
            evidence.append(
                AssociationEvidence(
                    type="metadata",
                    strength=0.55,
                    detail=f"Work item includes linked relations: {relation_types}",
                )
            )
            confidence += 0.05

        if work_item.tags:
            overlapping_tags = [tag for tag in work_item.tags if tag.lower() in str(getattr(artifact, "metadata", {})).lower()]
            if overlapping_tags:
                evidence.append(
                    AssociationEvidence(
                        type="metadata",
                        strength=0.7,
                        detail=f"Work item tags overlap artifact metadata: {', '.join(overlapping_tags[:4])}",
                    )
                )
                confidence += 0.15

        if isinstance(artifact, JourneyArtifact):
            step_titles = " ".join(step.step_title.lower() for step in artifact.steps)
            if any(token in step_titles for token in title_tokens):
                evidence.append(
                    AssociationEvidence(
                        type="visual",
                        strength=0.75,
                        detail="Journey step titles align with work item language",
                    )
                )
                confidence += 0.12
            if len(artifact.steps) >= 3:
                confidence += 0.08
                evidence.append(
                    AssociationEvidence(
                        type="metadata",
                        strength=0.6,
                        detail=f"Journey artifact contains {len(artifact.steps)} ordered steps",
                    )
                )

        decision = (
            AssociationDecision.ASSOCIATE
            if confidence >= 0.8
            else AssociationDecision.REVIEW if confidence >= 0.45 else AssociationDecision.REJECT
        )
        status = "approved" if decision == AssociationDecision.ASSOCIATE else "proposed"

        target_type = "journey_artifact" if isinstance(artifact, JourneyArtifact) else "artifact"
        return Association(
            id=f"assoc_{uuid4().hex[:8]}",
            project_id=project_id,
            source_entity=EntityRef(type="work_item", id=work_item.id),
            target_entity=EntityRef(type=target_type, id=artifact.id),
            association_type=f"{work_item.type.value}_to_{artifact.artifact_type.value}",
            decision=decision,
            confidence=min(confidence, 0.99),
            evidence=evidence,
            reason_summary="Association generated from direct references, semantic similarity, vector candidate retrieval, metadata overlap, and journey hints.",
            status=status,
        )

    @staticmethod
    def _semantic_seed(artifact: Artifact | JourneyArtifact) -> str:
        metadata = getattr(artifact, "metadata", {})
        parts = [
            artifact.title,
            str(metadata.get("screen_summary", "")),
            str(metadata.get("journey_summary", "")),
            " ".join(metadata.get("extracted_text", [])),
        ]
        if isinstance(artifact, JourneyArtifact):
            parts.append(" ".join(step.step_title for step in artifact.steps))
        return " ".join(parts)



    def retrieve_defect_story_candidates(self, project_id: str, defect: WorkItem, top_k: int = 5) -> list[dict[str, object]]:
        query = self._build_defect_query(defect)
        hits = self.vector_store.search_similar(
            query,
            top_k=max(top_k * 3, top_k),
            metadata_filters={"project_id": project_id, "type": "work_item"},
        )
        candidates: list[dict[str, object]] = []
        defect_related = {str(ref.get("id") or ref.get("external_id") or ref.get("name")) for ref in defect.related_work_item_refs}
        defect_terms = set(self._tokenize(query))
        for hit in hits:
            work_item = store.work_items.get(str(hit.get("doc_id")))
            if work_item is None or work_item.id == defect.id or work_item.type == WorkItemType.DEFECT:
                continue
            reasons: list[str] = [f"Vector similarity {float(hit.get('score', 0.0)):.4f} to defect narrative"]
            score = float(hit.get("score", 0.0))
            if work_item.external_id in defect_related or work_item.id in defect_related:
                score += 0.35
                reasons.append("Explicitly linked to the defect through Azure DevOps relations")
            overlap = defect_terms & set(self._tokenize(' '.join([work_item.title, work_item.description, ' '.join(work_item.tags)])))
            if overlap:
                score += min(0.25, 0.03 * len(overlap))
                reasons.append(f"Keyword overlap: {', '.join(sorted(list(overlap))[:5])}")
            candidates.append({
                "work_item_id": work_item.id,
                "external_id": work_item.external_id,
                "title": work_item.title,
                "type": work_item.type.value,
                "score": round(score, 4),
                "reasons": reasons,
            })
        candidates.sort(key=lambda item: float(item["score"]), reverse=True)
        return candidates[:top_k]

    def retrieve_defect_journey_candidates(self, project_id: str, defect: WorkItem, top_k: int = 5) -> list[dict[str, object]]:
        query = self._build_defect_query(defect)
        hits = self.vector_store.search_similar(
            query,
            top_k=max(top_k * 3, top_k),
            metadata_filters={"project_id": project_id},
        )
        candidates: list[dict[str, object]] = []
        defect_terms = set(self._tokenize(query))
        for hit in hits:
            doc_id = str(hit.get("doc_id"))
            journey = store.journeys.get(doc_id)
            artifact = store.artifacts.get(doc_id)
            if journey is None and artifact is None:
                continue
            if journey is not None:
                journey_name = journey.journey_name
                title = journey.title
                entity_type = "journey"
                ref_id = journey.id
            else:
                journey_name = str(artifact.metadata.get("journey", ""))
                if not journey_name:
                    continue
                title = artifact.title
                entity_type = "artifact"
                ref_id = artifact.id
            score = float(hit.get("score", 0.0))
            reasons = [f"Vector similarity {score:.4f} to defect narrative"]
            if any(token in journey_name for token in defect_terms):
                score += 0.2
                reasons.append(f"Journey name overlaps defect terms: {journey_name}")
            candidates.append({
                "entity_type": entity_type,
                "entity_id": ref_id,
                "journey": journey_name,
                "title": title,
                "score": round(score, 4),
                "reasons": reasons,
            })
        dedup: dict[tuple[str,str], dict[str, object]] = {}
        for candidate in candidates:
            key = (str(candidate["entity_type"]), str(candidate["journey"]))
            existing = dedup.get(key)
            if existing is None or float(candidate["score"]) > float(existing["score"]):
                dedup[key] = candidate
        output = sorted(dedup.values(), key=lambda item: float(item["score"]), reverse=True)
        return output[:top_k]

    def retrieve_defect_regression_candidates(self, project_id: str, defect: WorkItem, top_k: int = 5) -> list[dict[str, object]]:
        story_candidates = self.retrieve_defect_story_candidates(project_id, defect, top_k=top_k)
        journey_candidates = self.retrieve_defect_journey_candidates(project_id, defect, top_k=top_k)
        story_ids = {str(item["work_item_id"]) for item in story_candidates}
        journeys = {str(item["journey"]) for item in journey_candidates}
        candidates: list[dict[str, object]] = []
        for scenario in store.scenarios.values():
            score = 0.0
            reasons: list[str] = []
            source_ids = {ref.id for ref in scenario.source_refs if ref.type == "work_item"}
            if source_ids & story_ids:
                score += 0.8
                reasons.append("Scenario is linked to a candidate story")
            if scenario.journey in journeys:
                score += 0.65
                reasons.append(f"Scenario shares candidate journey {scenario.journey}")
            if defect.comments and any(term in ' '.join(defect.comments).lower() for term in ["repro", "error", "fails", "unable"]) and scenario.scenario_type.value in {"regression", "ui", "integration"}:
                score += 0.1
                reasons.append("Defect contains repro-style context")
            if score <= 0:
                continue
            candidates.append({
                "scenario_id": scenario.id,
                "title": scenario.title,
                "journey": scenario.journey,
                "scenario_type": scenario.scenario_type.value,
                "score": round(score, 4),
                "reasons": reasons,
            })
        candidates.sort(key=lambda item: float(item["score"]), reverse=True)
        return candidates[:top_k]

    @staticmethod
    def _build_defect_query(defect: WorkItem) -> str:
        return ' '.join([defect.title, defect.description, ' '.join(defect.acceptance_criteria), ' '.join(defect.tags), ' '.join(defect.comments)]).strip()

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [token for token in text.lower().replace('_', ' ').split() if len(token) > 2]

    @staticmethod
    def _journey_name(artifact: Artifact | JourneyArtifact) -> str:
        if isinstance(artifact, JourneyArtifact):
            return artifact.journey_name
        return str(artifact.metadata.get("journey", "")).lower()
