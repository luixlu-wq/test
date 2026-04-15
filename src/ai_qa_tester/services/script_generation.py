from __future__ import annotations

import re
from uuid import uuid4

from ai_qa_tester.models.contracts import GeneratedScript, PageModel, ScenarioType, TestScenario
from ai_qa_tester.repositories.memory import store
from ai_qa_tester.services.playwright_assets import PlaywrightAssetService


def _slug(value: str) -> str:
    value = re.sub(r'[^a-zA-Z0-9]+', '_', value.strip().lower())
    return re.sub(r'_+', '_', value).strip('_') or 'item'


def _class_name(value: str) -> str:
    tokens = [t for t in _slug(value).split('_') if t not in {'the', 'a', 'an'}]
    return ''.join(part.capitalize() for part in tokens) + 'Page'


class ScriptGenerator:
    def _page_model_for_scenario(self, project_id: str, scenario: TestScenario) -> PageModel | None:
        asset_service = PlaywrightAssetService()
        candidates = [p for p in store.page_models.values() if p.project_id == project_id and p.journey == scenario.journey]
        if candidates:
            return candidates[0]
        built = asset_service.build_from_project_artifacts(project_id)
        for page in built:
            if page.journey == scenario.journey:
                return page
        return built[0] if built else None

    def generate_playwright(self, project_id: str, scenario: TestScenario) -> str:
        title = scenario.title.replace("'", "\\'")
        page_model = self._page_model_for_scenario(project_id, scenario)
        if page_model is not None:
            class_name = _class_name(page_model.name)
            action_calls: list[str] = []
            for action in page_model.actions[:3]:
                action_calls.append(f"  await pageModel.{_slug(action)}();")
            if not action_calls:
                action_calls.append("  await page.waitForLoadState('networkidle');")
            assertion = "  await pageModel.assertLoaded();\n"
            if scenario.scenario_type == ScenarioType.REGRESSION:
                assertion += "  await expect(page.getByText(/error|failed|invalid/i)).not.toBeVisible();\n"
            elif scenario.scenario_type == ScenarioType.INTEGRATION:
                assertion += "  await expect(page).toHaveURL(/.+/);\n"
            return (
                "import { test, expect } from '@playwright/test';\n"
                "import { %s } from '../support/pageModels';\n\n"
                "test('%s', async ({ page }) => {\n"
                "  await page.goto(process.env.APP_BASE_URL ?? 'http://localhost:3000');\n"
                "  const pageModel = new %s(page);\n"
                "  await pageModel.assertLoaded();\n"
                "%s\n"
                "%s});\n"
            ) % (class_name, title, class_name, "\n".join(action_calls), assertion)

        steps_comment = "\n".join([f"  // Step {i+1}: {step}" for i, step in enumerate(scenario.steps[:6])])
        if scenario.scenario_type == ScenarioType.REGRESSION:
            assertion = "  await expect(page.getByText(/error|failed|invalid/i)).not.toBeVisible();\n"
        elif scenario.scenario_type == ScenarioType.INTEGRATION:
            assertion = "  await expect(page).toHaveURL(/.+/);\n"
        else:
            assertion = "  await expect(page.getByRole('heading').first()).toBeVisible();\n"
        return (
            "import { test, expect } from '@playwright/test';\n\n"
            "test('%s', async ({ page }) => {\n"
            "  await page.goto(process.env.APP_BASE_URL ?? 'http://localhost:3000');\n"
            "%s\n"
            "  // TODO: Replace placeholders with real selectors or page objects.\n"
            "  await page.waitForLoadState('networkidle');\n"
            "%s});\n"
        ) % (title, steps_comment, assertion)

    def generate_and_store_for_scenarios(self, project_id: str, scenarios: list[TestScenario]) -> list[GeneratedScript]:
        generated: list[GeneratedScript] = []
        for scenario in scenarios:
            existing = next((s for s in store.scripts.values() if s.project_id == project_id and s.scenario_id == scenario.id and s.framework == 'playwright' and s.language == 'typescript'), None)
            content = self.generate_playwright(project_id, scenario)
            if existing:
                existing.version += 1
                existing.content = content
                existing.status = 'generated'
                store.scripts[existing.id] = existing
                generated.append(existing)
                continue
            script = GeneratedScript(
                id=f"scr_{uuid4().hex[:8]}",
                project_id=project_id,
                scenario_id=scenario.id,
                framework='playwright',
                language='typescript',
                content=content,
            )
            store.scripts[script.id] = script
            generated.append(script)
        return generated
