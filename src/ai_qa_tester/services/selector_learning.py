from __future__ import annotations

import re
from uuid import uuid4

from ai_qa_tester.models.contracts import SelectorDefinition, SelectorLearningReport, SelectorLearningSuggestion, SelectorProfile
from ai_qa_tester.repositories.memory import store


class SelectorLearningService:
    FAILURE_PATTERNS = ("locator", "selector", "getby", "toBeVisible", "timeout")

    def _journey_profile(self, project_id: str, journey: str) -> SelectorProfile | None:
        approved = [p for p in store.selector_profiles.values() if p.project_id == project_id and p.journey == journey and p.approved]
        if approved:
            return approved[0]
        drafts = [p for p in store.selector_profiles.values() if p.project_id == project_id and p.journey == journey]
        return drafts[0] if drafts else None

    def _is_selector_failure(self, text: str) -> bool:
        lower = text.lower()
        return any(p.lower() in lower for p in self.FAILURE_PATTERNS)

    def _candidate_selectors(self, profile: SelectorProfile, haystack: str) -> list[SelectorDefinition]:
        hay = haystack.lower()
        found = []
        for selector in profile.selectors:
            bits = [selector.key.lower(), selector.source_label.lower()]
            if any(bit and bit in hay for bit in bits):
                found.append(selector)
        return found or profile.selectors[:2]

    def _suggest_locator(self, journey: str, selector: SelectorDefinition) -> str:
        slug = selector.key.split('__')[-1]
        return f"page.getByTestId('{journey}-{slug}')"

    def analyze_run(self, project_id: str, run_id: str) -> list[SelectorLearningReport]:
        reports: list[SelectorLearningReport] = []
        executions = [e for e in store.script_executions.values() if e.project_id == project_id and e.run_id == run_id and e.status in {'failed', 'blocked'}]
        by_journey: dict[str, list] = {}
        for execution in executions:
            scenario = store.scenarios.get(execution.scenario_id)
            if scenario is None:
                continue
            evidence_text = ' '.join([execution.reason, execution.stderr, execution.stdout, scenario.title, ' '.join(scenario.steps), ' '.join(scenario.expected_results)])
            if not self._is_selector_failure(evidence_text):
                continue
            by_journey.setdefault(scenario.journey, []).append((execution, scenario, evidence_text))

        for journey, items in by_journey.items():
            profile = self._journey_profile(project_id, journey)
            suggestions: list[SelectorLearningSuggestion] = []
            seen: set[str] = set()
            for execution, scenario, evidence_text in items:
                if profile is None:
                    continue
                for selector in self._candidate_selectors(profile, evidence_text):
                    if selector.key in seen:
                        continue
                    seen.add(selector.key)
                    suggestions.append(SelectorLearningSuggestion(
                        selector_key=selector.key,
                        current_locator=selector.locator,
                        suggested_locator=self._suggest_locator(journey, selector),
                        reason=f"Run {run_id} showed likely locator instability for '{selector.source_label}'. Prefer a pinned data-testid locator.",
                        confidence=0.82 if 'timeout' in evidence_text.lower() else 0.74,
                    ))
            if not suggestions:
                continue
            report = SelectorLearningReport(
                id=f"slr_{uuid4().hex[:8]}",
                project_id=project_id,
                run_id=run_id,
                journey=journey,
                profile_id=profile.id if profile else None,
                execution_ids=[execution.id for execution, _, _ in items],
                summary=f"Detected {len(suggestions)} selector improvement suggestion(s) for journey {journey}.",
                suggestions=suggestions,
            )
            store.selector_learning_reports[report.id] = report
            reports.append(report)
        return reports

    def apply_report(self, project_id: str, report_id: str, approve: bool = False, notes: str | None = None) -> SelectorProfile:
        report = store.selector_learning_reports[report_id]
        if report.project_id != project_id:
            raise KeyError(report_id)
        base_profile = store.selector_profiles.get(report.profile_id) if report.profile_id else None
        if base_profile is None:
            raise KeyError(report_id)
        updated_selectors = []
        patch = {s.selector_key: s for s in report.suggestions}
        for selector in base_profile.selectors:
            suggestion = patch.get(selector.key)
            updated_selectors.append(SelectorDefinition(
                key=selector.key,
                locator=suggestion.suggested_locator if suggestion else selector.locator,
                strategy='manual' if suggestion else selector.strategy,
                source_label=selector.source_label,
                element_type=selector.element_type,
            ))
        clone = SelectorProfile(
            id=f"sp_{uuid4().hex[:8]}",
            project_id=project_id,
            name=f"{base_profile.name} learned",
            journey=base_profile.journey,
            page_model_ids=list(base_profile.page_model_ids),
            selectors=updated_selectors,
            source='learned',
            approved=approve,
            status='approved' if approve else 'draft',
            notes=notes or report.summary,
        )
        if approve:
            for other in [sp for sp in store.selector_profiles.values() if sp.project_id == project_id and sp.journey == clone.journey and sp.approved]:
                other.approved = False
                other.status = 'draft'
                store.selector_profiles[other.id] = other
        store.selector_profiles[clone.id] = clone
        report.status = 'applied' if approve else 'proposed'
        store.selector_learning_reports[report.id] = report
        return clone
