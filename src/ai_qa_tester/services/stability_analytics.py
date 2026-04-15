from __future__ import annotations

from collections import defaultdict
from uuid import uuid4

from ai_qa_tester.models.contracts import StabilityAnalyticsReport, StabilityScenarioMetric
from ai_qa_tester.repositories.memory import store


class StabilityAnalyticsService:
    def build_report(self, project_id: str, baseline_run_id: str | None = None, candidate_run_id: str | None = None, journey: str | None = None) -> StabilityAnalyticsReport:
        runs = [r for r in store.runs.values() if r.project_id == project_id]
        if journey:
            runs = [r for r in runs if any((store.scenarios.get(sid) and store.scenarios[sid].journey == journey) for sid in r.scenario_ids)]

        comparisons = [c for c in store.run_comparisons.values() if c.project_id == project_id]
        if journey:
            comparisons = [c for c in comparisons if any((store.scenarios.get(d.scenario_id) and store.scenarios[d.scenario_id].journey == journey) for d in c.scenario_deltas)]
        if baseline_run_id or candidate_run_id:
            comparisons = [c for c in comparisons if (baseline_run_id is None or c.baseline_run_id == baseline_run_id) and (candidate_run_id is None or c.candidate_run_id == candidate_run_id)]

        execs = [e for e in store.script_executions.values() if e.project_id == project_id]
        if journey:
            execs = [e for e in execs if (store.scenarios.get(e.scenario_id) and store.scenarios[e.scenario_id].journey == journey)]
        if baseline_run_id or candidate_run_id:
            allowed = {rid for rid in [baseline_run_id, candidate_run_id] if rid}
            execs = [e for e in execs if e.run_id in allowed]

        scenario_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"passed":0,"failed":0,"blocked":0,"total":0})
        scenario_statuses: dict[str, list[str]] = defaultdict(list)
        for e in execs:
            stats = scenario_stats[e.scenario_id]
            stats["total"] += 1
            if e.status in ("passed","failed","blocked"):
                stats[e.status] += 1
            scenario_statuses[e.scenario_id].append(e.status)

        metrics = []
        for scenario_id, stats in scenario_stats.items():
            scenario = store.scenarios.get(scenario_id)
            statuses = scenario_statuses[scenario_id]
            switches = sum(1 for i in range(1, len(statuses)) if statuses[i] != statuses[i-1])
            flaky_score = switches / max(1, len(statuses)-1) if len(statuses) > 1 else 0.0
            metrics.append(StabilityScenarioMetric(
                scenario_id=scenario_id,
                title=scenario.title if scenario else None,
                journey=scenario.journey if scenario else None,
                total_runs=stats["total"],
                passed_runs=stats["passed"],
                failed_runs=stats["failed"],
                blocked_runs=stats["blocked"],
                pass_rate=stats["passed"] / max(1, stats["total"]),
                flaky_score=flaky_score,
            ))
        metrics.sort(key=lambda m: (m.flaky_score, 1-m.pass_rate, m.failed_runs), reverse=True)

        total_execs = len(execs)
        total_passed = sum(1 for e in execs if e.status == "passed")
        total_failed = sum(1 for e in execs if e.status == "failed")
        total_blocked = sum(1 for e in execs if e.status == "blocked")
        selector_retest_runs = sum(1 for r in runs if r.trigger_type == 'selector_retest')
        improved = sum(1 for c in comparisons if c.stability_change == 'improved')
        regressed = sum(1 for c in comparisons if c.stability_change == 'regressed')
        unchanged = sum(1 for c in comparisons if c.stability_change == 'unchanged')

        notes = []
        if metrics:
            top_flaky = metrics[0]
            notes.append(f"Most unstable scenario: {top_flaky.title or top_flaky.scenario_id} (flaky_score={top_flaky.flaky_score:.2f}).")
        if improved > regressed:
            notes.append("Recent reruns show net stability improvement.")
        elif regressed > improved:
            notes.append("Recent reruns show net stability regression.")
        else:
            notes.append("Recent reruns are neutral overall.")

        report = StabilityAnalyticsReport(
            id=f"sar_{uuid4().hex[:8]}",
            project_id=project_id,
            baseline_run_id=baseline_run_id,
            candidate_run_id=candidate_run_id,
            journey=journey,
            total_runs=len(runs),
            total_comparisons=len(comparisons),
            improved_comparisons=improved,
            regressed_comparisons=regressed,
            unchanged_comparisons=unchanged,
            selector_retest_runs=selector_retest_runs,
            pass_rate=total_passed / max(1, total_execs),
            failed_rate=total_failed / max(1, total_execs),
            blocked_rate=total_blocked / max(1, total_execs),
            scenario_metrics=metrics,
            notes=notes,
        )
        store.stability_reports[report.id] = report
        return report
