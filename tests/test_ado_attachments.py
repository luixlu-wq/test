
from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

from ai_qa_tester.api.main import app
from ai_qa_tester.models.contracts import WorkItem, WorkItemType
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.connectors import AzureDevOpsAttachment, DevOpsConnector


def _png_bytes(lines: list[str], modal: bool = False, error: bool = False) -> bytes:
    image = Image.new("RGB", (900, 1200), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 900, 70), fill=(0, 90, 50))
    y = 110
    for line in lines:
        draw.text((100, y), line, fill=(0, 0, 0))
        y += 70
    if modal:
        draw.rectangle((180, 220, 720, 760), outline=(120, 120, 120), width=3)
        draw.rectangle((250, 360, 650, 650), outline=(80, 80, 80), width=2)
    if error:
        draw.rectangle((80, 260, 820, 430), outline=(200, 30, 30), width=4)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_map_work_item_from_azure_extracts_attachment_refs() -> None:
    connector = DevOpsConnector()
    work_item = connector.map_work_item_from_azure(
        {
            "id": 321,
            "fields": {
                "System.WorkItemType": "Bug",
                "System.Title": "Create project flow broken",
                "System.State": "Active",
                "System.Tags": "project;upload",
                "Microsoft.VSTS.Common.AcceptanceCriteria": "<ul><li>User can upload file</li><li>User can submit</li></ul>",
            },
            "relations": [
                {
                    "rel": "AttachedFile",
                    "url": "https://dev.azure.com/org/project/_apis/wit/attachments/abc?fileName=step-1-upload-project-definition.png",
                    "attributes": {"name": "step-1-upload-project-definition.png"},
                }
            ],
        }
    )
    assert work_item.type == WorkItemType.DEFECT
    assert work_item.linked_artifact_refs
    assert work_item.linked_artifact_refs[0]["type"] == "ado_attachment"
    assert work_item.acceptance_criteria == ["User can upload file", "User can submit"]


def test_sync_work_item_attachments_builds_journey(monkeypatch) -> None:
    store.work_items.clear()
    store.artifacts.clear()
    store.journeys.clear()
    store.associations.clear()
    store.scenarios.clear()

    work_item = WorkItem(
        id="wk_create_project",
        external_id="ADO-777",
        type=WorkItemType.STORY,
        title="Create project flow",
        description="As a user, I want to create a project and upload the project definition.",
        acceptance_criteria=[
            "User can review before starting",
            "User can upload project definition",
            "User can select location and submit",
        ],
        tags=["project", "upload", "location"],
        linked_artifact_refs=[
            {"type": "ado_attachment", "value": "https://example/step-0.png", "name": "step-0-before-you-begin.png"},
            {"type": "ado_attachment", "value": "https://example/step-1.png", "name": "step-1-upload-project-definition.png"},
            {"type": "ado_attachment", "value": "https://example/step-2.png", "name": "step-2-select-location.png"},
            {"type": "ado_attachment", "value": "https://example/step-3.png", "name": "step-3-review-submit.png"},
        ],
    )
    store.work_items[work_item.id] = work_item

    attachments = [
        AzureDevOpsAttachment(
            name="step-0-before-you-begin.png",
            url="https://example/step-0.png",
            content_type="image/png",
            content=_png_bytes(["Step 0 Before you begin", "Continue"]),
            source_work_item_id=work_item.id,
        ),
        AzureDevOpsAttachment(
            name="step-1-upload-project-definition.png",
            url="https://example/step-1.png",
            content_type="image/png",
            content=_png_bytes(["Step 1 Upload Project Definition", "Project Definition", "Upload"], error=True),
            source_work_item_id=work_item.id,
        ),
        AzureDevOpsAttachment(
            name="step-2-select-location.png",
            url="https://example/step-2.png",
            content_type="image/png",
            content=_png_bytes(["Step 2 Add Location", "Map", "Confirm"], modal=True),
            source_work_item_id=work_item.id,
        ),
        AzureDevOpsAttachment(
            name="step-3-review-submit.png",
            url="https://example/step-3.png",
            content_type="image/png",
            content=_png_bytes(["Step 3 Review Submit", "Submit"]),
            source_work_item_id=work_item.id,
        ),
    ]

    monkeypatch.setattr(DevOpsConnector, "fetch_attachments_for_work_item", lambda self, project_id, item: attachments)

    client = TestClient(app)
    response = client.post("/api/v1/projects/proj_01/work-items/wk_create_project/attachments/sync")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["attachment_count"] == 4
    assert payload["journey_ids"]

    journeys = client.get("/api/v1/projects/proj_01/journeys").json()["items"]
    assert len(journeys) == 1
    journey = journeys[0]
    assert journey["journey_name"] == "create_project"
    assert journey["steps"][0]["step_title"] == "Before you begin"
    assert "map_interaction" in journey["metadata"]["risk_areas"]

    scenarios = client.get("/api/v1/projects/proj_01/scenarios").json()["items"]
    assert any(item["journey"] == "create_project" for item in scenarios)
    assert any("end-to-end" in item["title"].lower() for item in scenarios)
