from __future__ import annotations

from uuid import uuid4

from ai_qa_tester.models.contracts import RunComparisonReport, ScenarioRunDelta
from ai_qa_tester.repositories.memory import store


_STATUS_ORDER = {None: 0, 'blocked': 1, 'failed': 2, 'passed': 3}


class RunComparisonService:
    def compare_runs(self, project_id: str, baseline_run_id: str, candidate_run_id: str) -> RunComparisonReport:
        baseline = store.runs.get(baseline_run_id)
        candidate = store.runs.get(candidate_run_id)
        if baseline is None or candidate is None:
            raise KeyError('Run not found')

        baseline_execs = {
            item.scenario_id: item
            for item in store.script_executions.values()
            if item.project_id == project_id and item.run_id == baseline_run_id
        }
        candidate_execs = {
            item.scenario_id: item
            for item in store.script_executions.values()
            if item.project_id == project_id and item.run_id == candidate_run_id
        }

        scenario_ids = sorted(set(baseline.scenario_ids) | set(candidate.scenario_ids) | set(baseline_execs.keys()) | set(candidate_execs.keys()))
        deltas: list[ScenarioRunDelta] = []
        improved_count = 0
        regressed_count = 0
        unchanged_count = 0
        for scenario_id in scenario_ids:
            b_exec = baseline_execs.get(scenario_id)
            c_exec = candidate_execs.get(scenario_id)
            baseline_status = b_exec.status if b_exec else self._status_from_summary(baseline, scenario_id)
            candidate_status = c_exec.status if c_exec else self._status_from_summary(candidate, scenario_id)
            changed = baseline_status != candidate_status
            improved = _STATUS_ORDER[candidate_status] > _STATUS_ORDER[baseline_status]
            regressed = _STATUS_ORDER[candidate_status] < _STATUS_ORDER[baseline_status]
            if improved:
                improved_count += 1
            elif regressed:
                regressed_count += 1
            else:
                unchanged_count += 1
            scenario = store.scenarios.get(scenario_id)
            deltas.append(
                ScenarioRunDelta(
                    scenario_id=scenario_id,
                    title=scenario.title if scenario else None,
                    baseline_status=baseline_status,
                    candidate_status=candidate_status,
                    changed=changed,
                    improved=improved,
                    regressed=regressed,
                )
            )

        summary = {
            'baseline_passed': baseline.summary.get('passed', 0),
            'baseline_failed': baseline.summary.get('failed', 0),
            'baseline_blocked': baseline.summary.get('blocked', 0),
            'candidate_passed': candidate.summary.get('passed', 0),
            'candidate_failed': candidate.summary.get('failed', 0),
            'candidate_blocked': candidate.summary.get('blocked', 0),
            'delta_passed': candidate.summary.get('passed', 0) - baseline.summary.get('passed', 0),
            'delta_failed': candidate.summary.get('failed', 0) - baseline.summary.get('failed', 0),
            'delta_blocked': candidate.summary.get('blocked', 0) - baseline.summary.get('blocked', 0),
            'improved_scenarios': improved_count,
            'regressed_scenarios': regressed_count,
            'unchanged_scenarios': unchanged_count,
        }

        improved = summary['delta_failed'] < 0 or summary['delta_passed'] > 0 or improved_count > regressed_count
        if regressed_count > improved_count or summary['delta_failed'] > 0:
            stability_change = 'regressed'
        elif improved_count > regressed_count or summary['delta_failed'] < 0 or summary['delta_passed'] > 0:
            stability_change = 'improved'
        else:
            stability_change = 'unchanged'

        notes = []
        if stability_change == 'improved':
            notes.append('Candidate run improved automation stability compared with the baseline run.')
        elif stability_change == 'regressed':
            notes.append('Candidate run regressed compared with the baseline run.')
        else:
            notes.append('Candidate run shows no material stability change compared with the baseline run.')

        report = RunComparisonReport(
            id=f'cmp_{uuid4().hex[:8]}',
            project_id=project_id,
            baseline_run_id=baseline_run_id,
            candidate_run_id=candidate_run_id,
            improved=improved,
            stability_change=stability_change,
            summary=summary,
            scenario_deltas=deltas,
            notes=notes,
        )
        store.run_comparisons[report.id] = report
        return report

    @staticmethod
    def _status_from_summary(run, scenario_id: str) -> str | None:
        for item in run.result_details:
            if item.get('scenario_id') == scenario_id:
                return 'failed'
        if scenario_id in run.scenario_ids and run.summary.get('passed', 0) > 0:
            return 'passed'
        return None
