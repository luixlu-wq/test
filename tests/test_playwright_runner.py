
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import EntityRef, GeneratedScript, TestRun, TestScenario
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.execution import ExecutionService
from ai_qa_tester.services.playwright_runner import PlaywrightRunner
from ai_qa_tester.services.script_generation import ScriptGenerator


def setup_function() -> None:
    get_settings.cache_clear()
    store.projects.clear()
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()
    store.scripts.clear()
    store.runs.clear()
    store.script_executions.clear()


def test_playwright_runner_blocks_when_command_missing(monkeypatch):
    monkeypatch.setenv('AI_QA_EXECUTION_BACKEND', 'playwright')
    monkeypatch.setenv('AI_QA_PLAYWRIGHT_COMMAND', 'definitely-not-installed-playwright')
    runner = PlaywrightRunner()
    run = TestRun(id='run_1', project_id='proj_01', environment='uat', trigger_type='manual')
    script = GeneratedScript(id='scr_1', project_id='proj_01', scenario_id='scn_1', content='test')
    results = runner.execute(run, [script])
    assert results[0].status == 'blocked'
    assert 'not available' in results[0].reason.lower()


def test_execution_service_uses_playwright_backend(monkeypatch, tmp_path):
    monkeypatch.setenv('AI_QA_EXECUTION_BACKEND', 'playwright')
    monkeypatch.setenv('AI_QA_PLAYWRIGHT_WORK_ROOT', str(tmp_path))
    monkeypatch.setenv('AI_QA_PLAYWRIGHT_COMMAND', 'echo playwright-test')

    # fake command resolution
    monkeypatch.setattr('shutil.which', lambda cmd: '/usr/bin/echo')

    def fake_run(cmd, cwd, env, capture_output, text, timeout):
        tests_dir = Path(cwd) / 'tests'
        assert tests_dir.exists()
        assert any(p.suffix == '.ts' for p in tests_dir.iterdir())
        return SimpleNamespace(returncode=0, stdout='ok', stderr='')

    monkeypatch.setattr('subprocess.run', fake_run)

    scenario = TestScenario(
        id='scn_ok',
        project_id='proj_01',
        title='Create project happy path',
        scenario_type='integration',
        journey='create_project',
        steps=['Open page', 'Submit form'],
        expected_results=['Success'],
        source_refs=[EntityRef(type='work_item', id='wk_1')],
        coverage_reason='happy path',
        review_required=False,
    )
    store.scenarios[scenario.id] = scenario
    script = ScriptGenerator().generate_and_store_for_scenarios('proj_01', [scenario])[0]
    run = TestRun(id='run_1', project_id='proj_01', environment='uat', trigger_type='manual', scenario_ids=[scenario.id])

    updated, executions = ExecutionService().execute_generated_scripts(run, [script.id])
    assert updated.summary['passed'] == 1
    assert executions[0].status == 'passed'
    assert executions[0].stdout == 'ok'
