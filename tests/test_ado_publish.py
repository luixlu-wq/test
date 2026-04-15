from __future__ import annotations

from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import Project, RunStatus, TestRun, TestScenario, ScenarioType
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.connectors import DevOpsConnector


class StubResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class StubClient:
    def __init__(self, wiql_existing=False):
        self.posts = []
        self.patches = []
        self.wiql_existing = wiql_existing

    def post(self, url, headers=None, json=None):
        self.posts.append((url, headers, json))
        if 'comments' in url:
            return StubResponse({'id': 777, 'text': json['text']})
        if '/wiql' in url:
            if self.wiql_existing:
                return StubResponse({'workItems': [{'id': 1234}]})
            return StubResponse({'workItems': []})
        return StubResponse({})

    def patch(self, url, headers=None, json=None):
        self.patches.append((url, headers, json))
        if '/workitems/1234' in url:
            return StubResponse({'id': 1234, 'url': url})
        return StubResponse({'id': 9001, 'url': url})


def setup_function():
    store.projects.clear()
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()
    store.runs.clear()


def test_connector_publish_comment_and_create_or_update_bug():
    client = StubClient()
    connector = DevOpsConnector(
        base_url='https://dev.azure.com/org/project/_workitems/recentlyupdated/',
        pat='pat',
        client=client,
    )

    comment = connector.publish_traceability_comment('123', 'hello traceability')
    assert comment['id'] == 777
    assert 'comments' in client.posts[0][0]

    bug = connector.create_bug_from_failed_run(
        run_id='run_1',
        title='AI QA failure',
        description='something failed',
        repro_steps=['step 1', 'step 2'],
        area_path='Business/Search',
        iteration_path='Sprint 12',
    )
    assert bug['id'] == 9001
    assert client.patches
    patch_doc = client.patches[0][2]
    assert any(op['path'] == '/fields/System.Title' for op in patch_doc)


def test_connector_upsert_bug_updates_existing_bug():
    client = StubClient(wiql_existing=True)
    connector = DevOpsConnector(
        base_url='https://dev.azure.com/org/project/_workitems/recentlyupdated/',
        pat='pat',
        client=client,
    )

    result = connector.upsert_bug_from_failed_run(
        run_id='run_2',
        title='AI QA failure for run run_2',
        description='validation still fails on upload step',
        repro_steps=['step 1'],
        area_path='Business/Search',
        iteration_path='Sprint 12',
        related_work_item_id='4567',
    )
    assert result['action'] == 'updated'
    assert result['existing_bug_id'] == 1234
    assert client.patches
    assert '/workitems/1234' in client.patches[0][0]



def test_publish_summary_and_create_bug_endpoints(monkeypatch):
    app_client = TestClient(app)
    project = Project(
        id='proj_01',
        name='QA',
        devops_url='https://dev.azure.com/org/project/_workitems/recentlyupdated/',
        devops_pat='pat',
    )
    store.projects[project.id] = project
    store.runs['run_1'] = TestRun(
        id='run_1',
        project_id='proj_01',
        environment='uat',
        trigger_type='manual',
        status=RunStatus.COMPLETED,
        scenario_ids=['scn_1'],
        summary={'passed': 0, 'failed': 1, 'blocked': 0},
        result_details=[{'scenario_id': 'scn_1', 'title': 'Validation on upload', 'reason': 'Mismatch', 'journey': 'create_project'}],
    )

    class FakeConnector:
        def __init__(self, base_url=None, pat=None, client=None):
            self.base_url = base_url
            self.pat = pat

        def publish_run_summary_comment(self, work_item_id, run_id, summary, scenario_ids):
            return {'id': 1, 'text': f'{run_id}:{work_item_id}:{summary["failed"]}'}

        def publish_traceability_comment(self, work_item_id, text):
            return {'id': 2, 'text': text}

        def upsert_bug_from_failed_run(self, **kwargs):
            return {'action': 'updated', 'bug': {'id': 3, 'title': kwargs['title']}, 'existing_bug_id': 3}

    monkeypatch.setattr('ai_qa_tester.api.routers.runs.DevOpsConnector', FakeConnector)

    resp = app_client.post('/api/v1/projects/proj_01/runs/run_1/publish-summary', json={'work_item_id': 'wk_1'})
    assert resp.status_code == 200
    assert resp.json()['status'] == 'published'

    resp2 = app_client.post('/api/v1/projects/proj_01/runs/run_1/publish-traceability', json={'work_item_id': 'wk_1', 'text': 'trace'})
    assert resp2.status_code == 200
    assert resp2.json()['comment']['text'] == 'trace'

    resp3 = app_client.post('/api/v1/projects/proj_01/runs/run_1/create-bug', json={})
    assert resp3.status_code == 200
    assert resp3.json()['status'] == 'updated'
    assert resp3.json()['dedup']['existing_bug_id'] == 3
