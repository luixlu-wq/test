from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import GeneratedScript, Project, RunStatus, ScriptExecutionResult, SelectorDefinition, SelectorProfile, TestRun, TestScenario
from ai_qa_tester.repositories.memory import store


def setup_function() -> None:
    store.clear_all()


def _seed() -> None:
    store.projects['proj_01'] = Project(id='proj_01', name='Demo')
    store.scenarios['scn_1'] = TestScenario(
        id='scn_1',
        project_id='proj_01',
        title='Create project continue works',
        scenario_type='regression',
        journey='create_project',
        coverage_reason='test',
        steps=['Click Continue'],
        expected_results=['Next step is shown'],
    )
    store.selector_profiles['sp_1'] = SelectorProfile(
        id='sp_1',
        project_id='proj_01',
        name='create project selectors',
        journey='create_project',
        selectors=[SelectorDefinition(key='create_project__continue', locator="page.getByRole('button', { name: /Continue/i })", source_label='Continue', element_type='button')],
        approved=True,
        status='approved',
    )
    store.runs['run_1'] = TestRun(id='run_1', project_id='proj_01', environment='uat', trigger_type='manual', status=RunStatus.COMPLETED, scenario_ids=['scn_1'])
    store.script_executions['exec_1'] = ScriptExecutionResult(
        id='exec_1', project_id='proj_01', run_id='run_1', script_id='scr_1', scenario_id='scn_1',
        status='failed', reason='Locator timeout waiting for selector', stderr='TimeoutError: waiting for locator Continue', stdout=''
    )


def test_selector_feedback_generates_report() -> None:
    _seed()
    client = TestClient(app)
    resp = client.post('/api/v1/projects/proj_01/runs/run_1/selector-feedback')
    assert resp.status_code == 200
    body = resp.json()
    assert body['total'] == 1
    assert body['reports'][0]['suggestions'][0]['suggested_locator'].startswith("page.getByTestId('create_project-")


def test_apply_selector_feedback_creates_learned_profile() -> None:
    _seed()
    client = TestClient(app)
    report = client.post('/api/v1/projects/proj_01/runs/run_1/selector-feedback').json()['reports'][0]
    resp = client.post(f"/api/v1/projects/proj_01/runs/run_1/selector-feedback/{report['id']}/apply", json={'approve': True, 'notes': 'use stable test id'})
    assert resp.status_code == 200
    body = resp.json()
    assert body['profile']['source'] == 'learned'
    assert body['profile']['approved'] is True
    assert 'getByTestId' in body['profile']['selectors'][0]['locator']
    assert body['regenerated_count'] == 1
    assert body['regenerated_scripts'][0]['scenario_id'] == 'scn_1'


def test_apply_selector_feedback_regenerates_existing_script_version() -> None:
    _seed()
    store.scripts['scr_existing'] = GeneratedScript(
        id='scr_existing',
        project_id='proj_01',
        scenario_id='scn_1',
        framework='playwright',
        language='typescript',
        version=1,
        content='old script',
    )
    client = TestClient(app)
    report = client.post('/api/v1/projects/proj_01/runs/run_1/selector-feedback').json()['reports'][0]
    resp = client.post(f"/api/v1/projects/proj_01/runs/run_1/selector-feedback/{report['id']}/apply", json={'approve': True, 'notes': 'regen with learned selectors'})
    assert resp.status_code == 200
    body = resp.json()
    assert body['regenerated_count'] == 1
    assert body['regenerated_scripts'][0]['id'] == 'scr_existing'
    assert body['regenerated_scripts'][0]['version'] == 2
    assert body['regenerated_scripts'][0]['content'] != 'old script'
    assert 'Create project continue works' in body['regenerated_scripts'][0]['content']


def test_apply_selector_feedback_auto_reruns_regenerated_scripts() -> None:
    _seed()
    store.scripts['scr_existing'] = GeneratedScript(
        id='scr_existing',
        project_id='proj_01',
        scenario_id='scn_1',
        framework='playwright',
        language='typescript',
        version=1,
        content='old script',
    )
    client = TestClient(app)
    report = client.post('/api/v1/projects/proj_01/runs/run_1/selector-feedback').json()['reports'][0]
    resp = client.post(
        f"/api/v1/projects/proj_01/runs/run_1/selector-feedback/{report['id']}/apply",
        json={'approve': True, 'notes': 'approve and rerun', 'auto_rerun': True},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body['rerun'] is not None
    assert body['rerun']['run']['trigger_type'] == 'selector_retest'
    assert body['rerun']['run']['environment'] == 'uat'
    assert body['rerun']['executions']
    assert body['rerun']['comparison']['stability_change'] == 'improved'


def test_compare_runs_endpoint_reports_improvement() -> None:
    _seed()
    store.runs['run_2'] = TestRun(id='run_2', project_id='proj_01', environment='uat', trigger_type='selector_retest', status=RunStatus.COMPLETED, scenario_ids=['scn_1'], summary={'passed': 1, 'failed': 0, 'blocked': 0})
    store.script_executions['exec_2'] = ScriptExecutionResult(
        id='exec_2', project_id='proj_01', run_id='run_2', script_id='scr_2', scenario_id='scn_1',
        status='passed', reason='Execution succeeded', stdout='ok', stderr=''
    )
    client = TestClient(app)
    resp = client.post('/api/v1/projects/proj_01/runs/run_2/compare', json={'against_run_id': 'run_1'})
    assert resp.status_code == 200
    body = resp.json()
    assert body['comparison']['stability_change'] == 'improved'
    assert body['comparison']['summary']['delta_failed'] <= 0
