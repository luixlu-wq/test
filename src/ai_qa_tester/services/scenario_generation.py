from __future__ import annotations

from uuid import uuid4

from ai_qa_tester.models.contracts import (
    Artifact,
    Association,
    EntityRef,
    JourneyArtifact,
    ScenarioType,
    TestScenario,
    WorkItem,
)
from ai_qa_tester.repositories.memory import store


class ScenarioGenerator:
    def generate(
        self,
        project_id: str,
        work_item: WorkItem,
        artifact: Artifact | JourneyArtifact,
        association: Association,
    ) -> list[TestScenario]:
        if isinstance(artifact, JourneyArtifact):
            return self._generate_for_journey(project_id, work_item, artifact, association)
        return [self._generate_for_single_artifact(project_id, work_item, artifact, association)]

    def _generate_for_single_artifact(
        self,
        project_id: str,
        work_item: WorkItem,
        artifact: Artifact,
        association: Association,
    ) -> TestScenario:
        journey = str(artifact.metadata.get("journey", "default_journey"))
        step_title = str(artifact.metadata.get("step_title", artifact.title))
        return TestScenario(
            id=f"ts_{uuid4().hex[:8]}",
            project_id=project_id,
            title=f"{work_item.title} - {step_title.lower()} happy path",
            scenario_type=ScenarioType.UI,
            journey=journey,
            priority="high",
            preconditions=["User is authenticated"] + self._comment_preconditions(work_item),
            steps=[
                f"Navigate to the {journey.replace('_', ' ')} page",
                f"Complete the {step_title.lower()} interaction",
                "Continue to the next step or action",
            ],
            expected_results=[
                f"{step_title} is completed successfully",
                "Screen behavior aligns with the design intent",
            ],
            source_refs=[
                EntityRef(type="work_item", id=work_item.id),
                EntityRef(type="artifact", id=artifact.id),
                EntityRef(type="association", id=association.id),
            ],
            coverage_reason="Happy-path scenario generated from approved story-to-design association.",
            confidence=association.confidence,
            review_required=association.status != "approved",
        )

    def _generate_for_journey(
        self,
        project_id: str,
        work_item: WorkItem,
        artifact: JourneyArtifact,
        association: Association,
    ) -> list[TestScenario]:
        source_refs = [
            EntityRef(type="work_item", id=work_item.id),
            EntityRef(type="journey_artifact", id=artifact.id),
            EntityRef(type="association", id=association.id),
        ]
        source_refs.extend(EntityRef(type="artifact", id=step.artifact_id) for step in artifact.steps)

        happy_path = TestScenario(
            id=f"ts_{uuid4().hex[:8]}",
            project_id=project_id,
            title=f"{work_item.title} - end-to-end {artifact.journey_name.replace('_', ' ')} flow",
            scenario_type=ScenarioType.INTEGRATION,
            journey=artifact.journey_name,
            priority="critical" if len(artifact.steps) >= 3 else "high",
            preconditions=["User is authenticated", "Required reference data is available"] + self._comment_preconditions(work_item),
            steps=[f"Complete step {idx + 1}: {step.step_title}" for idx, step in enumerate(artifact.steps)],
            expected_results=[
                f"Journey {artifact.journey_name.replace('_', ' ')} completes successfully",
                "State is preserved across all journey steps",
            ],
            source_refs=source_refs,
            coverage_reason="End-to-end scenario generated from ordered wireframe journey steps.",
            confidence=min(0.99, association.confidence + 0.05),
            review_required=association.status != "approved",
        )

        validation_or_risk = TestScenario(
            id=f"ts_{uuid4().hex[:8]}",
            project_id=project_id,
            title=f"{work_item.title} - validation and risk handling",
            scenario_type=ScenarioType.UI,
            journey=artifact.journey_name,
            priority="high",
            preconditions=["User is on the first actionable step of the journey"],
            steps=self._risk_steps(artifact, work_item),
            expected_results=self._risk_expectations(artifact),
            source_refs=source_refs,
            coverage_reason="Risk-based scenario generated from wireframe journey risk areas.",
            confidence=max(0.6, association.confidence - 0.05),
            review_required=True,
        )

        return [happy_path, validation_or_risk]


    def generate_regressions_from_defect(
        self,
        project_id: str,
        defect: WorkItem,
        story_candidates: list[dict[str, object]],
        journey_candidates: list[dict[str, object]],
        regression_candidates: list[dict[str, object]],
        limit: int = 3,
    ) -> list[dict[str, object]]:
        generated: list[dict[str, object]] = []
        defect_ref = EntityRef(type="work_item", id=defect.id)

        for candidate in regression_candidates[:limit]:
            scenario = store.scenarios.get(str(candidate["scenario_id"]))
            if scenario is None:
                continue
            if not any(ref.type == "work_item" and ref.id == defect.id for ref in scenario.source_refs):
                scenario.source_refs.append(defect_ref)
            scenario.coverage_reason = f"{scenario.coverage_reason} Updated from defect triage evidence.".strip()
            scenario.confidence = min(0.99, max(scenario.confidence, 0.78))
            if defect.comments and not any("Replay the issue described" in step for step in scenario.steps):
                scenario.steps.append("Replay the issue described in the defect repro notes")
            if defect.comments and not any("The defect no longer reproduces" in result for result in scenario.expected_results):
                scenario.expected_results.append("The defect no longer reproduces after the fix")
            store.scenarios[scenario.id] = scenario
            generated.append({"action": "updated", "scenario": scenario})

        existing_journeys = {str(item["scenario"].journey) for item in generated}
        for journey_candidate in journey_candidates:
            if len(generated) >= limit:
                break
            journey_name = str(journey_candidate["journey"])
            if journey_name in existing_journeys:
                continue
            title = f"{defect.title} - {journey_name.replace('_', ' ')} regression"
            story_ref_id = next((str(item.get("work_item_id")) for item in story_candidates if item.get("score", 0) > 0), None)
            source_refs = [defect_ref]
            if story_ref_id:
                source_refs.append(EntityRef(type="work_item", id=story_ref_id))
            entity_type = str(journey_candidate.get("entity_type", "journey"))
            entity_id = str(journey_candidate.get("entity_id", ""))
            if entity_id:
                source_refs.append(EntityRef(type=("journey_artifact" if entity_type == "journey" else entity_type), id=entity_id))
            scenario = TestScenario(
                id=f"ts_{uuid4().hex[:8]}",
                project_id=project_id,
                title=title,
                scenario_type=ScenarioType.REGRESSION,
                journey=journey_name,
                priority="high",
                preconditions=["User is authenticated"] + self._comment_preconditions(defect),
                steps=self._defect_regression_steps(defect, journey_name),
                expected_results=[
                    "The defect no longer reproduces after the fix",
                    f"The {journey_name.replace('_', ' ')} flow completes successfully",
                ],
                source_refs=source_refs,
                coverage_reason="Regression scenario generated from defect triage candidates.",
                confidence=0.82,
                review_required=True,
            )
            store.scenarios[scenario.id] = scenario
            generated.append({"action": "created", "scenario": scenario})
            existing_journeys.add(journey_name)

        return generated[:limit]

    @staticmethod
    def _defect_regression_steps(defect: WorkItem, journey_name: str) -> list[str]:
        comment_blob = ' '.join(defect.comments).lower()
        steps = [f"Navigate to the {journey_name.replace('_', ' ')} flow"]
        if any(term in comment_blob for term in ["upload", "file", "pdf"]):
            steps.append("Upload the representative file or input described in the defect")
        if any(term in comment_blob for term in ["review", "submit"]):
            steps.append("Continue to the review or submit step")
        if any(term in comment_blob for term in ["map", "location", "modal"]):
            steps.append("Open the location or modal step and confirm the expected selection")
        steps.append("Replay the defect path and verify the issue no longer occurs")
        return steps

    @staticmethod
    def _comment_preconditions(work_item: WorkItem) -> list[str]:
        if not work_item.comments:
            return []
        return [f"Context note: {work_item.comments[0][:120]}"]

    @staticmethod
    def _risk_steps(artifact: JourneyArtifact, work_item: WorkItem) -> list[str]:
        risks = artifact.metadata.get("risk_areas", [])
        steps: list[str] = []
        if "field_validation" in risks:
            steps.append("Leave one or more required fields empty and continue")
        if "file_upload" in risks:
            steps.append("Attempt to upload an invalid or missing project definition file")
        if "map_interaction" in risks:
            steps.append("Open the location modal and cancel or confirm without selecting a valid location")
        if "submission" in risks:
            steps.append("Attempt to submit before all required steps are complete")
        if work_item.comments and any(term in " ".join(work_item.comments).lower() for term in ["repro", "error", "fails", "unable"]):
            steps.append("Replay the issue described in the work item comments or repro notes")
        if not steps:
            steps.append("Trigger a representative validation edge case within the journey")
        return steps

    @staticmethod
    def _risk_expectations(artifact: JourneyArtifact) -> list[str]:
        risks = artifact.metadata.get("risk_areas", [])
        results: list[str] = []
        if "field_validation" in risks:
            results.append("Required field validation messages are displayed and progression is blocked")
        if "file_upload" in risks:
            results.append("The file upload error is shown and the invalid file is rejected")
        if "map_interaction" in risks:
            results.append("The modal preserves or rejects location state according to the user action")
        if "submission" in risks:
            results.append("Submission is blocked until the journey is complete")
        if not results:
            results.append("The system handles the validation edge case gracefully")
        return results
