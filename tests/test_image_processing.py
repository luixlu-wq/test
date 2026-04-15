from io import BytesIO

from PIL import Image, ImageDraw

from ai_qa_tester.models.contracts import ArtifactType
from ai_qa_tester.services.processing import ArtifactProcessor
from ai_qa_tester.services.uploads import UploadService


def _png_bytes(text_lines: list[str], error: bool = False, modal: bool = False) -> bytes:
    image = Image.new("RGB", (900, 1200), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 900, 70), fill=(0, 90, 50))
    if error:
        draw.rectangle((80, 260, 820, 430), outline=(200, 30, 30), width=4)
    if modal:
        draw.rectangle((180, 220, 720, 760), outline=(120, 120, 120), width=3)
    y = 110
    for line in text_lines:
        draw.text((100, y), line, fill=(0, 0, 0))
        y += 70
    if modal:
        draw.rectangle((250, 360, 650, 650), outline=(80, 80, 80), width=2)
        for x in range(270, 631, 20):
            draw.line((x, 380, x, 630), fill=(170, 170, 170), width=1)
        for y_line in range(380, 631, 20):
            draw.line((270, y_line, 630, y_line), fill=(170, 170, 170), width=1)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_image_aware_wireframe_processing_extracts_visual_signals() -> None:
    content = _png_bytes([
        "Step 1 Upload Project Definition",
        "Project Definition",
        "Project Name",
        "Project Description",
        "Upload Project Definition",
        "Continue",
    ], error=True)
    artifact = UploadService().register_wireframe(
        project_id="proj_01",
        filename="wireframe.png",
        content_type="image/png",
        content=content,
    )
    assert artifact.artifact_type == ArtifactType.WIREFRAME
    processed = ArtifactProcessor().process(artifact)
    assert processed.metadata["journey"] == "create_project"
    assert "Project Definition" in " ".join(processed.metadata["extracted_text"])
    assert processed.metadata["image_context"]["has_green_header"] is True
    assert processed.metadata["image_context"]["has_error_highlight"] is True
    assert "field_validation" in processed.metadata["risk_areas"]


def test_image_aware_modal_detection_marks_location_step() -> None:
    content = _png_bytes([
        "Step 2 Add Location",
        "Add Location",
        "Map",
        "Confirm",
        "Cancel",
    ], modal=True)
    artifact = UploadService().register_wireframe(
        project_id="proj_01",
        filename="step-2.png",
        content_type="image/png",
        content=content,
    )
    processed = ArtifactProcessor().process(artifact)
    assert processed.metadata["image_context"]["has_modal"] is True
    assert processed.metadata["screen_type"] == "modal"
    assert processed.metadata["step_title"] == "Select location"
    assert "map_interaction" in processed.metadata["risk_areas"]
