from __future__ import annotations

from uuid import uuid4

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import RunStatus, ScriptExecutionResult, TestRun
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.playwright_runner import PlaywrightRunner


class ExecutionService:
    def execute(self, run: TestRun) -> TestRun:
        failed = []
        passed = 0
        for scenario_id in run.scenario_ids:
            scenario = store.scenarios.get(scenario_id)
            if scenario and ('validation' in scenario.title.lower() or scenario.scenario_type.value == 'regression'):
                failed.append({
                    'scenario_id': scenario_id,
                    'title': scenario.title,
                    'reason': 'Simulated mismatch against expected behavior',
                    'journey': scenario.journey,
                })
            else:
                passed += 1
        run.status = RunStatus.COMPLETED
        run.result_details = failed
        run.summary = {'passed': passed, 'failed': len(failed), 'blocked': 0}
        return run

    def execute_generated_scripts(self, run: TestRun, script_ids: list[str]) -> tuple[TestRun, list[ScriptExecutionResult]]:
        settings = get_settings()
        scripts = []
        blocked_missing = 0
        for script_id in script_ids:
            script = store.scripts.get(script_id)
            if script is None or store.scenarios.get(script.scenario_id) is None:
                blocked_missing += 1
                continue
            scripts.append(script)

        if settings.execution_backend == 'playwright' and scripts:
            executions = PlaywrightRunner().execute(run, scripts)
        else:
            executions = self._execute_generated_scripts_simulated(run, scripts)

        passed = 0
        failed = 0
        blocked = blocked_missing
        result_details: list[dict[str, str]] = []
        for execution in executions:
            store.script_executions[execution.id] = execution
            scenario = store.scenarios.get(execution.scenario_id)
            if execution.status == 'passed':
                passed += 1
            elif execution.status == 'failed':
                failed += 1
                result_details.append({
                    'scenario_id': execution.scenario_id,
                    'script_id': execution.script_id,
                    'title': scenario.title if scenario else execution.scenario_id,
                    'reason': execution.reason,
                    'journey': scenario.journey if scenario else '',
                })
            else:
                blocked += 1

        run.status = RunStatus.COMPLETED
        run.summary = {'passed': passed, 'failed': failed, 'blocked': blocked}
        run.result_details = result_details
        store.runs[run.id] = run
        return run, executions

    def _execute_generated_scripts_simulated(self, run: TestRun, scripts: list) -> list[ScriptExecutionResult]:
        executions: list[ScriptExecutionResult] = []
        for script in scripts:
            scenario = store.scenarios.get(script.scenario_id)
            if scenario is None:
                continue

            title_blob = f"{scenario.title} {' '.join(scenario.expected_results)} {' '.join(scenario.steps)}".lower()
            should_fail = any(term in title_blob for term in ['error', 'invalid', 'fail'])
            reason = 'Regression script executed successfully against expected behavior.'
            status = 'passed'
            stderr = ''
            stdout = f"Executed {script.framework} script {script.id} for scenario {scenario.id}"
            if should_fail:
                status = 'failed'
                reason = 'Simulated regression failure from generated script execution.'
                stderr = 'Assertion failed: expected defect path to be fixed.'

            execution = ScriptExecutionResult(
                id=f"exec_{uuid4().hex[:8]}",
                project_id=run.project_id,
                run_id=run.id,
                script_id=script.id,
                scenario_id=scenario.id,
                status=status,
                reason=reason,
                stdout=stdout,
                stderr=stderr,
                evidence_refs=[f"run://{run.id}/script/{script.id}"],
            )
            executions.append(execution)
        return executions
