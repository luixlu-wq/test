from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import Artifact, ArtifactType
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.processing import ArtifactProcessor
from ai_qa_tester.services.playwright_assets import PlaywrightAssetService


def setup_function():
    store.clear_all()


def test_selector_profile_bootstrap_and_review():
    client = TestClient(app)
    project = client.post('/api/v1/projects', json={'name': 'Selector QA'}).json()
    project_id = project['id']
    artifact = Artifact(
        id='art_1',
        project_id=project_id,
        artifact_type=ArtifactType.WIREFRAME,
        source_type='upload',
        source_ref='upload://wireframe.png',
        title='Create Project',
        metadata={'journey': 'create_project', 'step_title': 'Upload Project Definition', 'upload_path': '/tmp/none'},
    )
    store.artifacts[artifact.id] = artifact
    store.artifacts[artifact.id] = ArtifactProcessor().process(artifact)

    bootstrap = client.post(f'/api/v1/projects/{project_id}/playwright/selector-profiles/bootstrap')
    assert bootstrap.status_code == 200
    body = bootstrap.json()
    assert body['profile_count'] >= 1
    profile = body['profiles'][0]
    first_key = profile['selectors'][0]['key']

    review = client.post(
        f'/api/v1/projects/{project_id}/playwright/selector-profiles/{profile["id"]}/review',
        json={'approve': True, 'notes': 'approved selectors', 'overrides': {first_key: {'locator': "page.getByTestId('approved-selector')"}}},
    )
    assert review.status_code == 200
    reviewed = review.json()['profile']
    assert reviewed['approved'] is True
    assert any(sel['locator'] == "page.getByTestId('approved-selector')" for sel in reviewed['selectors'])
    assert 'approved-selector' in review.json()['assets']['selectors.ts']


def test_generate_ts_assets_prefers_approved_profile():
    client = TestClient(app)
    project_id = client.post('/api/v1/projects', json={'name': 'Selector QA'}).json()['id']
    artifact = Artifact(
        id='art_2',
        project_id=project_id,
        artifact_type=ArtifactType.WIREFRAME,
        source_type='upload',
        source_ref='upload://wireframe2.png',
        title='Review Submit',
        metadata={'journey': 'create_project', 'step_title': 'Review and Submit', 'upload_path': '/tmp/none'},
    )
    store.artifacts[artifact.id] = artifact
    store.artifacts[artifact.id] = ArtifactProcessor().process(artifact)
    service = PlaywrightAssetService()
    profiles = service.build_selector_profiles(project_id)
    key = profiles[0].selectors[0].key
    service.review_selector_profile(project_id, profiles[0].id, True, overrides={key: {'locator': "page.getByRole('button', { name: /approved/i })"}})
    assets = service.generate_ts_assets(project_id)
    assert 'approved' in assets['selectors.ts']
