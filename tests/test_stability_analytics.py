from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import GeneratedScript, ScriptExecutionResult, TestRun, TestScenario
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.run_comparison import RunComparisonService
from ai_qa_tester.services.stability_analytics import StabilityAnalyticsService


def setup_runs(project_id: str = "proj_test"):
    store.projects.clear()
    store.scenarios.clear()
    store.runs.clear()
    store.script_executions.clear()
    store.run_comparisons.clear()
    store.stability_reports.clear()

    scenario = TestScenario(id="scn_1", project_id=project_id, title="Create project flow", scenario_type="regression", journey="create_project", coverage_reason="stability test")
    store.scenarios[scenario.id] = scenario

    base = TestRun(id="run_base", project_id=project_id, environment="uat", trigger_type="manual", scenario_ids=[scenario.id], summary={"passed":0,"failed":1,"blocked":0}, result_details=[{"scenario_id":scenario.id,"title":scenario.title}])
    cand = TestRun(id="run_new", project_id=project_id, environment="uat", trigger_type="selector_retest", scenario_ids=[scenario.id], summary={"passed":1,"failed":0,"blocked":0}, result_details=[])
    store.runs[base.id] = base
    store.runs[cand.id] = cand

    store.script_executions["exec1"] = ScriptExecutionResult(id="exec1", project_id=project_id, run_id=base.id, script_id="scr1", scenario_id=scenario.id, status="failed", reason="selector failed")
    store.script_executions["exec2"] = ScriptExecutionResult(id="exec2", project_id=project_id, run_id=cand.id, script_id="scr1", scenario_id=scenario.id, status="passed", reason="ok")

    RunComparisonService().compare_runs(project_id, base.id, cand.id)
    return project_id, base.id, cand.id


def test_build_stability_report_tracks_improvement():
    project_id, base_id, cand_id = setup_runs()
    report = StabilityAnalyticsService().build_report(project_id, baseline_run_id=base_id, candidate_run_id=cand_id)
    assert report.improved_comparisons == 1
    assert report.selector_retest_runs == 1
    assert report.pass_rate == 0.5
    assert report.scenario_metrics[0].flaky_score == 1.0


def test_stability_report_api_returns_report():
    client = TestClient(app)
    project_id, base_id, cand_id = setup_runs()
    response = client.post(f"/api/v1/projects/{project_id}/runs/{cand_id}/stability-report", json={"against_run_id": base_id})
    # backward-compatible if request model differs
    if response.status_code == 422:
        response = client.post(f"/api/v1/projects/{project_id}/runs/{cand_id}/stability-report", json={"baseline_run_id": base_id})
    assert response.status_code == 200
    body = response.json()
    assert body["report"]["improved_comparisons"] == 1
