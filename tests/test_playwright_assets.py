from fastapi.testclient import TestClient

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import Artifact, ArtifactType, Project, TestScenario
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.playwright_assets import PlaywrightAssetService
from ai_qa_tester.services.script_generation import ScriptGenerator


def setup_function() -> None:
    store.clear_all()


def test_build_page_model_and_generate_assets() -> None:
    artifact = Artifact(
        id='art_1',
        project_id='proj_01',
        artifact_type=ArtifactType.WIREFRAME,
        source_type='upload',
        source_ref='upload://art_1',
        title='Upload Project Definition',
        metadata={
            'journey': 'create_project',
            'step_title': 'Upload the project definition',
            'ui_elements': [
                {'type': 'input', 'label': 'Project Name'},
                {'type': 'button', 'label': 'Upload Project Definition'},
                {'type': 'button', 'label': 'Continue'},
            ],
            'extracted_text': ['Project Definition', 'Project Name', 'Continue'],
        },
        status='processed',
    )
    store.artifacts[artifact.id] = artifact
    service = PlaywrightAssetService()
    page_models = service.build_from_project_artifacts('proj_01')
    assert page_models
    assets = service.generate_ts_assets('proj_01')
    assert 'selectors.ts' in assets
    assert 'UploadProjectDefinitionPage' in assets['pageModels.ts']


def test_script_generator_uses_page_model_imports() -> None:
    artifact = Artifact(
        id='art_1',
        project_id='proj_01',
        artifact_type=ArtifactType.WIREFRAME,
        source_type='upload',
        source_ref='upload://art_1',
        title='Upload Project Definition',
        metadata={
            'journey': 'create_project',
            'step_title': 'Upload the project definition',
            'ui_elements': [
                {'type': 'input', 'label': 'Project Name'},
                {'type': 'button', 'label': 'Continue'},
            ],
            'extracted_text': ['Project Name', 'Continue'],
        },
        status='processed',
    )
    store.artifacts[artifact.id] = artifact
    scenario = TestScenario(
        id='scn_1',
        project_id='proj_01',
        title='Create project regression',
        scenario_type='regression',
        journey='create_project',
        coverage_reason='test',
        steps=['Open form'],
        expected_results=['Success'],
    )
    content = ScriptGenerator().generate_playwright('proj_01', scenario)
    assert "from '../support/pageModels'" in content
    assert 'pageModel.assertLoaded' in content


def test_playwright_bootstrap_endpoint_returns_assets() -> None:
    client = TestClient(app)
    store.projects['proj_01'] = Project(id='proj_01', name='Demo')
    artifact = Artifact(
        id='art_1',
        project_id='proj_01',
        artifact_type=ArtifactType.WIREFRAME,
        source_type='upload',
        source_ref='upload://art_1',
        title='Before you begin',
        metadata={
            'journey': 'create_project',
            'step_title': 'Before you begin',
            'ui_elements': [
                {'type': 'button', 'label': 'Continue'},
            ],
            'extracted_text': ['Before you begin', 'Continue'],
        },
        status='processed',
    )
    store.artifacts[artifact.id] = artifact
    resp = client.post('/api/v1/projects/proj_01/playwright/bootstrap')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'accepted'
    assert 'selectors.ts' in body['assets']
