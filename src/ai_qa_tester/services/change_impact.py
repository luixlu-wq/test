from __future__ import annotations

from dataclasses import dataclass, field

from ai_qa_tester.models.contracts import Artifact, JourneyArtifact, TestScenario, WorkItem
from ai_qa_tester.repositories.memory import store


@dataclass
class ImpactReason:
    scenario_id: str
    reasons: list[str] = field(default_factory=list)
    score: float = 0.0


class ChangeImpactService:
    def analyze(self, project_id: str, changed_work_item_ids: list[str]) -> dict:
        scenario_reasons: dict[str, ImpactReason] = {}
        impacted_journeys: set[str] = set()
        related_work_item_ids: set[str] = set()
        artifact_ids: set[str] = set()
        journey_artifact_ids: set[str] = set()

        changed_items = [store.work_items[item_id] for item_id in changed_work_item_ids if item_id in store.work_items]

        for item in changed_items:
            # collect related work item refs
            for rel in item.related_work_item_refs:
                work_item_external_id = rel.get("work_item_external_id")
                if work_item_external_id:
                    related_work_item_ids.update(
                        candidate.id
                        for candidate in store.work_items.values()
                        if candidate.external_id == work_item_external_id
                    )

            # direct scenario links from source_refs
            for scenario in store.scenarios.values():
                reasons: list[str] = []
                score = 0.0
                if any(ref.type == "work_item" and ref.id == item.id for ref in scenario.source_refs):
                    reasons.append(f"Directly linked to changed work item {item.id}")
                    score += 5.0
                if item.sprint and scenario.journey and item.sprint.lower().replace(" ", "_") in scenario.journey:
                    reasons.append(f"Journey name overlaps sprint hint from {item.id}")
                    score += 0.5
                if self._comment_or_title_matches_scenario(item, scenario):
                    reasons.append(f"Comment/title keywords overlap with scenario {scenario.id}")
                    score += 2.0
                if reasons:
                    impacted_journeys.add(scenario.journey)
                    self._add_reason(scenario_reasons, scenario.id, reasons, score)

            # association-driven selection
            for association in store.associations.values():
                if association.source_entity.type == "work_item" and association.source_entity.id == item.id:
                    target_type = association.target_entity.type
                    target_id = association.target_entity.id
                    if target_type == "artifact":
                        artifact_ids.add(target_id)
                    elif target_type == "journey_artifact":
                        journey_artifact_ids.add(target_id)

        # related work item scenarios
        for related_id in related_work_item_ids:
            for scenario in store.scenarios.values():
                if any(ref.type == "work_item" and ref.id == related_id for ref in scenario.source_refs):
                    impacted_journeys.add(scenario.journey)
                    self._add_reason(
                        scenario_reasons,
                        scenario.id,
                        [f"Linked via related work item {related_id}"],
                        3.0,
                    )

        # artifact and journey artifacts drive additional scenario selection
        for scenario in store.scenarios.values():
            reasons: list[str] = []
            score = 0.0
            source_ref_ids = {ref.id for ref in scenario.source_refs}
            if artifact_ids.intersection(source_ref_ids):
                reasons.append("Linked to impacted artifact")
                score += 3.0
            if journey_artifact_ids.intersection(source_ref_ids):
                reasons.append("Linked to impacted journey artifact")
                score += 4.0
            if scenario.journey in impacted_journeys:
                reasons.append(f"Shares impacted journey {scenario.journey}")
                score += 1.5
            if reasons:
                self._add_reason(scenario_reasons, scenario.id, reasons, score)

        selected = sorted(
            [
                {
                    "scenario_id": reason.scenario_id,
                    "title": store.scenarios[reason.scenario_id].title,
                    "journey": store.scenarios[reason.scenario_id].journey,
                    "priority": store.scenarios[reason.scenario_id].priority,
                    "score": round(reason.score, 2),
                    "reasons": reason.reasons,
                }
                for reason in scenario_reasons.values()
            ],
            key=lambda item: (-item["score"], item["scenario_id"]),
        )

        return {
            "changed_work_item_ids": changed_work_item_ids,
            "related_work_item_ids": sorted(related_work_item_ids),
            "impacted_artifact_ids": sorted(artifact_ids),
            "impacted_journey_artifact_ids": sorted(journey_artifact_ids),
            "impacted_journeys": sorted(impacted_journeys),
            "selected_scenarios": selected,
        }

    def _add_reason(self, bucket: dict[str, ImpactReason], scenario_id: str, reasons: list[str], score: float) -> None:
        current = bucket.setdefault(scenario_id, ImpactReason(scenario_id=scenario_id))
        for reason in reasons:
            if reason not in current.reasons:
                current.reasons.append(reason)
        current.score += score

    def _comment_or_title_matches_scenario(self, item: WorkItem, scenario: TestScenario) -> bool:
        haystack = " ".join([item.title, item.description, *item.comments]).lower()
        scenario_text = " ".join([scenario.title, scenario.journey, *scenario.steps, *scenario.expected_results]).lower()
        keywords = {token for token in haystack.replace("_", " ").split() if len(token) > 4}
        if not keywords:
            return False
        return any(keyword in scenario_text for keyword in keywords)
