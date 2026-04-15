from __future__ import annotations

import re
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from PIL import Image

from ai_qa_tester.models.contracts import Artifact, ArtifactType, JourneyArtifact, JourneyStep


class ArtifactProcessor:
    def process(self, artifact: Artifact) -> Artifact:
        metadata = dict(artifact.metadata)
        filename = str(metadata.get("filename", artifact.title)).lower()
        preview_text = " ".join(metadata.get("upload_preview_text", []))
        image_context = self._extract_image_context(metadata)
        if image_context:
            metadata["image_context"] = image_context

        if artifact.artifact_type == ArtifactType.SCREENSHOT:
            metadata["extracted_text"] = image_context.get("ocr_lines") or ["Search Business", "Business Name", "Search"]
            metadata["ui_elements"] = self._infer_ui_elements(metadata["extracted_text"], image_context)
            metadata.setdefault("journey", self._infer_journey(filename, metadata["extracted_text"], image_context))

        if artifact.artifact_type == ArtifactType.WIREFRAME:
            extracted_text = self._extract_wireframe_text(filename, preview_text, image_context)
            ui_elements = self._infer_ui_elements(extracted_text, image_context)
            metadata["extracted_text"] = extracted_text
            metadata["ui_elements"] = ui_elements
            metadata["screen_summary"] = self._screen_summary(extracted_text, ui_elements, image_context)
            metadata["journey"] = self._infer_journey(filename, extracted_text, image_context)
            metadata["step_order"] = self._infer_step_order(filename, preview_text, extracted_text)
            metadata["step_title"] = self._infer_step_title(filename, extracted_text, image_context)
            metadata["risk_areas"] = self._infer_risk_areas(extracted_text, image_context)
            metadata["screen_type"] = self._infer_screen_type(extracted_text, image_context)
            metadata["is_journey_step"] = True

        if artifact.artifact_type == ArtifactType.FIGMA_FRAME:
            metadata.setdefault("journey", "business_search")

        artifact.metadata = metadata
        artifact.status = "processed"
        return artifact

    def process_journey(self, journey: JourneyArtifact, step_artifacts: list[Artifact]) -> JourneyArtifact:
        processed_steps = sorted(
            step_artifacts,
            key=lambda item: (
                int(item.metadata.get("step_order", 999)),
                item.title.lower(),
            ),
        )
        inferred_journey = journey.journey_name
        if inferred_journey in {"", "generic_journey"}:
            inferred_journey = self._infer_journey_from_steps(processed_steps)

        steps: list[JourneyStep] = []
        all_labels: list[str] = []
        risk_areas: list[str] = []
        screen_types: list[str] = []
        for index, artifact in enumerate(processed_steps):
            extracted = artifact.metadata.get("extracted_text", [])
            all_labels.extend(extracted)
            risk_areas.extend(artifact.metadata.get("risk_areas", []))
            screen_types.append(str(artifact.metadata.get("screen_type", "screen")))
            steps.append(
                JourneyStep(
                    order=index,
                    artifact_id=artifact.id,
                    step_key=str(artifact.metadata.get("step_title", artifact.title)).lower().replace(" ", "_"),
                    step_title=str(artifact.metadata.get("step_title", artifact.title)),
                    summary=str(artifact.metadata.get("screen_summary", artifact.title)),
                )
            )

        deduped_labels = self._dedupe(all_labels)
        deduped_risks = self._dedupe(risk_areas)
        journey.metadata = {
            **journey.metadata,
            "journey": inferred_journey,
            "extracted_text": deduped_labels,
            "risk_areas": deduped_risks,
            "screen_types": self._dedupe(screen_types),
            "step_count": len(steps),
            "journey_summary": self._journey_summary(inferred_journey, steps, deduped_risks),
        }
        journey.title = journey.title if journey.title != "Wireframe Journey" else inferred_journey.replace("_", " ").title()
        journey.journey_name = inferred_journey
        journey.steps = steps
        journey.step_artifact_ids = [step.artifact_id for step in steps]
        journey.status = "processed"
        return journey

    def _extract_image_context(self, metadata: dict) -> dict:
        path = metadata.get("local_path")
        content_type = str(metadata.get("content_type", "")).lower()
        if not path or ("image" not in content_type and Path(str(path)).suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}):
            return {}

        try:
            image = Image.open(path).convert("RGB")
            rgb = np.array(image)
            gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        except Exception:
            return {}

        height, width = gray.shape
        edges = cv2.Canny(gray, 100, 200)
        edge_density = float(np.count_nonzero(edges)) / float(edges.size or 1)
        dark_ratio = float(np.mean(gray < 70))
        bright_ratio = float(np.mean(gray > 215))

        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([95, 255, 255]))
        red_mask1 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
        red_mask2 = cv2.inRange(hsv, np.array([170, 50, 50]), np.array([180, 255, 255]))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        top_band = green_mask[: max(10, height // 8), :]
        header_green_ratio = float(np.count_nonzero(top_band)) / float(top_band.size or 1)
        red_ratio = float(np.count_nonzero(red_mask)) / float(red_mask.size or 1)

        central = gray[height // 5 : (height * 4) // 5, width // 5 : (width * 4) // 5]
        central_bright_ratio = float(np.mean(central > 215)) if central.size else 0.0
        border = np.concatenate([
            gray[: height // 10, :].flatten(),
            gray[(height * 9) // 10 :, :].flatten(),
            gray[:, : width // 10].flatten(),
            gray[:, (width * 9) // 10 :].flatten(),
        ]) if height > 20 and width > 20 else gray.flatten()
        border_bright_ratio = float(np.mean(border > 215)) if border.size else 0.0
        has_modal = central_bright_ratio > 0.65 and border_bright_ratio < central_bright_ratio - 0.08

        quadrants = {
            "top_left": gray[: height // 2, : width // 2],
            "top_right": gray[: height // 2, width // 2 :],
            "bottom_left": gray[height // 2 :, : width // 2],
            "bottom_right": gray[height // 2 :, width // 2 :],
        }
        textured = {
            name: float(np.count_nonzero(cv2.Canny(q, 80, 180))) / float(q.size or 1)
            for name, q in quadrants.items()
            if q.size
        }
        map_like_region = max(textured, key=textured.get) if textured else None
        has_map_like_region = bool(map_like_region and textured.get(map_like_region, 0.0) > 0.035)

        ocr_lines = self._ocr_lines(image, gray)
        return {
            "dimensions": {"width": width, "height": height},
            "edge_density": round(edge_density, 4),
            "dark_ratio": round(dark_ratio, 4),
            "bright_ratio": round(bright_ratio, 4),
            "header_green_ratio": round(header_green_ratio, 4),
            "has_green_header": header_green_ratio > 0.12,
            "red_ratio": round(red_ratio, 4),
            "has_error_highlight": red_ratio > 0.003,
            "has_modal": has_modal,
            "has_map_like_region": has_map_like_region,
            "map_like_region": map_like_region,
            "ocr_lines": ocr_lines,
        }

    def _ocr_lines(self, image: Image.Image, gray: np.ndarray) -> list[str]:
        lines: list[str] = []
        candidates = [
            image,
            Image.fromarray(cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
        ]
        for candidate in candidates:
            try:
                text = pytesseract.image_to_string(candidate, lang="eng", config="--psm 6")
            except Exception:
                continue
            for raw_line in text.splitlines():
                line = re.sub(r"\s+", " ", raw_line).strip()
                if len(line) < 3:
                    continue
                if re.fullmatch(r"[\W_]+", line):
                    continue
                if line not in lines:
                    lines.append(line)
            if len(lines) >= 12:
                break
        return lines[:20]

    def _extract_wireframe_text(self, filename: str, preview_text: str, image_context: dict) -> list[str]:
        tokens: list[str] = []
        seed = f"{filename} {preview_text}".lower()

        ocr_lines = image_context.get("ocr_lines", [])
        cleaned_ocr = []
        for line in ocr_lines:
            cleaned = re.sub(r"[^A-Za-z0-9 /&:-]", "", line).strip()
            if len(cleaned) >= 3:
                cleaned_ocr.append(cleaned)
        tokens.extend(cleaned_ocr[:12])

        if any(word in seed for word in ["search", "result", "business"]):
            tokens.extend(["Search Business", "Business Name", "Search", "Results"])
        if any(word in seed for word in ["login", "sign in"]):
            tokens.extend(["Sign In", "Username", "Password", "Login"])
        if any(word in seed for word in ["profile", "account"]):
            tokens.extend(["Profile", "Account Name", "Save"])
        if any(word in seed for word in ["project", "definition", "permit", "licence", "license"]):
            tokens.extend(["Project Definition", "Project Name", "Project Description", "Upload Project Definition"])
        if any(word in seed for word in ["before", "begin", "guideline"]):
            tokens.extend(["Before You Begin", "Guidance", "Continue"])
        if any(word in seed for word in ["location", "map"]):
            tokens.extend(["Add Location", "Map", "Confirm", "Cancel"])
        if any(word in seed for word in ["review", "submit", "confirm"]):
            tokens.extend(["Review", "Submit", "Confirm"])

        if image_context.get("has_modal"):
            tokens.append("Modal Dialog")
        if image_context.get("has_map_like_region"):
            tokens.append("Map")
        if image_context.get("has_error_highlight"):
            tokens.append("Validation Error")
        if image_context.get("has_green_header"):
            tokens.append("Wizard Header")

        if not tokens:
            base = Path(filename).stem.replace("_", " ").replace("-", " ").title()
            tokens.extend([base, "Primary Action", "Page Title"])
        return self._dedupe(tokens)

    @staticmethod
    def _infer_ui_elements(extracted_text: list[str], image_context: dict | None = None) -> list[dict[str, str]]:
        elements: list[dict[str, str]] = []
        image_context = image_context or {}
        for text in extracted_text:
            lowered = text.lower()
            if any(keyword in lowered for keyword in ["search", "save", "login", "continue", "submit", "confirm", "cancel", "upload", "choose file"]):
                elements.append({"type": "button", "label": text})
            elif any(keyword in lowered for keyword in ["name", "username", "password", "description", "definition", "email", "address"]):
                elements.append({"type": "input", "label": text})
            elif "map" in lowered:
                elements.append({"type": "map", "label": text})
            elif "error" in lowered:
                elements.append({"type": "alert", "label": text})
            else:
                elements.append({"type": "text", "label": text})
        if image_context.get("has_modal"):
            elements.append({"type": "modal", "label": "Detected modal dialog"})
        return elements

    @staticmethod
    def _screen_summary(extracted_text: list[str], ui_elements: list[dict[str, str]], image_context: dict | None = None) -> str:
        labels = ", ".join(extracted_text[:4])
        controls = ", ".join(sorted({item['type'] for item in ui_elements}))
        image_context = image_context or {}
        flags = []
        if image_context.get("has_modal"):
            flags.append("modal")
        if image_context.get("has_error_highlight"):
            flags.append("validation")
        if image_context.get("has_map_like_region"):
            flags.append("map")
        visual = f" with visual cues [{', '.join(flags)}]" if flags else ""
        return f"Wireframe includes labels [{labels}] and controls [{controls}]{visual}"

    def _infer_journey(self, filename: str, extracted_text: list[str], image_context: dict | None = None) -> str:
        seed = f"{filename} {' '.join(extracted_text)}".lower()
        image_context = image_context or {}
        if "project" in seed and any(term in seed for term in ["upload", "definition", "location", "review"]):
            return "create_project"
        if image_context.get("has_map_like_region") and any(term in seed for term in ["project", "location", "definition"]):
            return "create_project"
        if "search" in seed or "results" in seed:
            return "business_search"
        if "login" in seed or "sign in" in seed:
            return "authentication"
        if "profile" in seed:
            return "profile_management"
        return "generic_journey"

    @staticmethod
    def _infer_step_order(filename: str, preview_text: str, extracted_text: list[str]) -> int:
        seed = f"{filename} {preview_text} {' '.join(extracted_text)}".lower()
        patterns = [
            r"step\s*([0-9]+)",
            r"screen\s*([0-9]+)",
            r"page\s*([0-9]+)",
            r"v([0-9]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, seed)
            if match:
                return int(match.group(1))
        keyword_order = [
            ("before you begin", 0),
            ("before", 0),
            ("upload project definition", 1),
            ("project definition", 1),
            ("location", 2),
            ("map", 2),
            ("review", 3),
            ("submit", 3),
            ("confirmation", 4),
        ]
        for keyword, order in keyword_order:
            if keyword in seed:
                return order
        return 999

    @staticmethod
    def _infer_step_title(filename: str, extracted_text: list[str], image_context: dict | None = None) -> str:
        seed = f"{filename} {' '.join(extracted_text)}".lower()
        image_context = image_context or {}
        if "before you begin" in seed or "before" in seed:
            return "Before you begin"
        if "project definition" in seed or "upload" in seed:
            return "Upload the project definition"
        if "location" in seed or "map" in seed or image_context.get("has_map_like_region"):
            return "Select location"
        if "review" in seed or "submit" in seed or "confirm" in seed:
            return "Review and submit"
        if extracted_text:
            return extracted_text[0]
        return Path(filename).stem.replace("_", " ").replace("-", " ").title()

    @staticmethod
    def _infer_risk_areas(extracted_text: list[str], image_context: dict | None = None) -> list[str]:
        risks: list[str] = []
        seed = " ".join(extracted_text).lower()
        image_context = image_context or {}
        if "upload" in seed:
            risks.append("file_upload")
        if any(term in seed for term in ["required", "name", "description", "definition", "validation error"]):
            risks.append("field_validation")
        if "map" in seed or "location" in seed or image_context.get("has_map_like_region"):
            risks.append("map_interaction")
        if "submit" in seed or "confirm" in seed:
            risks.append("submission")
        if "continue" in seed:
            risks.append("step_navigation")
        if image_context.get("has_modal"):
            risks.append("modal_state")
        return risks or ["generic_ui_flow"]

    @staticmethod
    def _infer_screen_type(extracted_text: list[str], image_context: dict | None = None) -> str:
        seed = " ".join(extracted_text).lower()
        image_context = image_context or {}
        if "before you begin" in seed:
            return "instructions"
        if image_context.get("has_modal"):
            return "modal"
        if "upload" in seed or "project definition" in seed:
            return "form"
        if "map" in seed or "location" in seed or image_context.get("has_map_like_region"):
            return "modal"
        if "review" in seed or "submit" in seed:
            return "review"
        return "screen"

    def _infer_journey_from_steps(self, artifacts: list[Artifact]) -> str:
        combined = " ".join(
            " ".join(artifact.metadata.get("extracted_text", []))
            for artifact in artifacts
        ).lower()
        return self._infer_journey("", combined.split(), {})

    @staticmethod
    def _journey_summary(journey_name: str, steps: list[JourneyStep], risk_areas: list[str]) -> str:
        step_titles = " -> ".join(step.step_title for step in steps)
        risks = ", ".join(risk_areas[:4]) if risk_areas else "none"
        return f"Journey {journey_name} with steps: {step_titles}. Key risk areas: {risks}"

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        deduped: list[str] = []
        for value in values:
            normalized = value.strip()
            if normalized and normalized not in deduped:
                deduped.append(normalized)
        return deduped
