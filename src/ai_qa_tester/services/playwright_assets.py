from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

from ai_qa_tester.models.contracts import Artifact, ArtifactType, EntityRef, JourneyArtifact, PageModel, SelectorDefinition, SelectorProfile
from ai_qa_tester.repositories.memory import store


def _slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", value).strip("_") or "item"


def _class_name(value: str) -> str:
    tokens = [t for t in _slug(value).split('_') if t not in {'the', 'a', 'an'}]
    return ''.join(part.capitalize() for part in tokens) + 'Page'


class PlaywrightAssetService:
    def infer_selectors_from_artifact(self, artifact: Artifact) -> list[SelectorDefinition]:
        selectors: list[SelectorDefinition] = []
        ui_elements = artifact.metadata.get("ui_elements", [])
        seen: set[str] = set()
        for element in ui_elements:
            label = str(element.get("label", "")).strip()
            if not label:
                continue
            key = _slug(label)
            if key in seen:
                continue
            seen.add(key)
            element_type = str(element.get("type", "text"))
            if element_type == 'button':
                locator = f"page.getByRole('button', {{ name: /{re.escape(label)}/i }})"
            elif element_type == 'input':
                locator = f"page.getByLabel(/{re.escape(label)}/i).or(page.getByPlaceholder(/{re.escape(label)}/i))"
            elif element_type == 'map':
                locator = "page.locator('[data-testid*=\"map\"], .map, [aria-label*=\"map\" i]').first()"
            elif element_type == 'modal':
                locator = "page.getByRole('dialog').first()"
            elif element_type == 'alert':
                locator = "page.getByRole('alert').first()"
            else:
                locator = f"page.getByText(/{re.escape(label)}/i).first()"
            selectors.append(SelectorDefinition(key=key, locator=locator, source_label=label, element_type=element_type))
        if not selectors:
            selectors.append(SelectorDefinition(key='page_root', locator="page.locator('body')", source_label='Page Root', element_type='root'))
        return selectors

    def _actions(self, artifact: Artifact) -> list[str]:
        actions: list[str] = []
        for element in artifact.metadata.get('ui_elements', []):
            et = str(element.get('type', 'text'))
            label = str(element.get('label', 'item')).strip()
            if et == 'button':
                actions.append(f"click {label}")
            elif et == 'input':
                actions.append(f"fill {label}")
            elif et == 'map':
                actions.append(f"select {label}")
        return actions or ['wait for page ready']

    def _assertions(self, artifact: Artifact) -> list[str]:
        extracted = artifact.metadata.get('extracted_text', [])
        return [f"see {text}" for text in extracted[:3]] or ['page is visible']

    def build_page_model_for_artifact(self, project_id: str, artifact: Artifact, journey: str | None = None) -> PageModel:
        page = PageModel(
            id=f"pg_{uuid4().hex[:8]}",
            project_id=project_id,
            name=artifact.metadata.get('step_title') or artifact.title,
            journey=journey or str(artifact.metadata.get('journey', 'generic_journey')),
            source_entity=EntityRef(type='artifact', id=artifact.id),
            route_hint='/' + _slug(str(artifact.metadata.get('step_title') or artifact.title)),
            selectors=self.infer_selectors_from_artifact(artifact),
            actions=self._actions(artifact),
            assertions=self._assertions(artifact),
        )
        store.page_models[page.id] = page
        return page

    def build_from_project_artifacts(self, project_id: str) -> list[PageModel]:
        built: list[PageModel] = []
        built_sources = {(p.source_entity.type, p.source_entity.id): p for p in store.page_models.values() if p.project_id == project_id}
        for artifact in store.artifacts.values():
            if artifact.project_id != project_id or artifact.status != 'processed':
                continue
            key = ('artifact', artifact.id)
            if key in built_sources:
                built.append(built_sources[key])
                continue
            built.append(self.build_page_model_for_artifact(project_id, artifact))
        for journey in store.journeys.values():
            if journey.project_id != project_id:
                continue
            for step in journey.steps:
                artifact = store.artifacts.get(step.artifact_id)
                if artifact is None:
                    continue
                key = ('artifact', artifact.id)
                if key in built_sources:
                    continue
                built.append(self.build_page_model_for_artifact(project_id, artifact, journey=journey.journey_name))
        return built



    def build_selector_profiles(self, project_id: str) -> list[SelectorProfile]:
        page_models = [p for p in store.page_models.values() if p.project_id == project_id]
        if not page_models:
            page_models = self.build_from_project_artifacts(project_id)
        profiles: list[SelectorProfile] = []
        by_journey: dict[str, list[PageModel]] = {}
        for page in page_models:
            by_journey.setdefault(page.journey, []).append(page)
        for journey, pages in by_journey.items():
            selectors: list[SelectorDefinition] = []
            for page in pages:
                for sel in page.selectors:
                    profile_key = f"{_slug(page.name)}__{sel.key}"
                    selectors.append(SelectorDefinition(key=profile_key, locator=sel.locator, strategy=sel.strategy, source_label=sel.source_label, element_type=sel.element_type))
            existing = next((sp for sp in store.selector_profiles.values() if sp.project_id == project_id and sp.journey == journey), None)
            if existing:
                existing.page_model_ids = [p.id for p in pages]
                existing.selectors = selectors
                if existing.status == 'rejected':
                    existing.status = 'draft'
                store.selector_profiles[existing.id] = existing
                profiles.append(existing)
                continue
            profile = SelectorProfile(
                id=f"sp_{uuid4().hex[:8]}",
                project_id=project_id,
                name=f"{journey} selectors",
                journey=journey,
                page_model_ids=[p.id for p in pages],
                selectors=selectors,
            )
            store.selector_profiles[profile.id] = profile
            profiles.append(profile)
        return profiles

    def review_selector_profile(self, project_id: str, profile_id: str, approve: bool, overrides: dict[str, dict[str, str]] | None = None, notes: str | None = None) -> SelectorProfile:
        profile = store.selector_profiles[profile_id]
        if profile.project_id != project_id:
            raise KeyError(profile_id)
        if overrides:
            updated: list[SelectorDefinition] = []
            for sel in profile.selectors:
                patch = overrides.get(sel.key, {})
                updated.append(SelectorDefinition(
                    key=sel.key,
                    locator=patch.get('locator', sel.locator),
                    strategy=patch.get('strategy', sel.strategy),
                    source_label=patch.get('source_label', sel.source_label),
                    element_type=patch.get('element_type', sel.element_type),
                ))
            profile.selectors = updated
            profile.source = 'manual'
        profile.approved = approve
        profile.status = 'approved' if approve else 'rejected'
        profile.notes = notes
        if approve:
            for other in [sp for sp in store.selector_profiles.values() if sp.project_id == project_id and sp.journey == profile.journey and sp.id != profile.id and sp.approved]:
                other.approved = False
                other.status = 'draft'
                store.selector_profiles[other.id] = other
        store.selector_profiles[profile.id] = profile
        return profile

    def _approved_profile_selectors(self, project_id: str) -> dict[str, list[SelectorDefinition]]:
        approved = [sp for sp in store.selector_profiles.values() if sp.project_id == project_id and sp.approved]
        out: dict[str, list[SelectorDefinition]] = {}
        for sp in approved:
            out[sp.journey] = sp.selectors
        return out
    def generate_ts_assets(self, project_id: str) -> dict[str, str]:
        page_models = [p for p in store.page_models.values() if p.project_id == project_id]
        if not page_models:
            page_models = self.build_from_project_artifacts(project_id)
        approved_by_journey = self._approved_profile_selectors(project_id)
        selectors_lines = ["export const selectors = {"]
        for page in page_models:
            selectors_lines.append(f"  { _slug(page.name) }: {{")
            selector_defs = approved_by_journey.get(page.journey, page.selectors)
            for sel in selector_defs:
                local_key = sel.key.split('__')[-1]
                selectors_lines.append(f"    {local_key}: ({sel.locator}),")
            selectors_lines.append("  },")
        selectors_lines.append("} as const;\n")

        page_objects = ["import { Page, expect } from '@playwright/test';", "import { selectors } from './selectors';", ""]
        for page in page_models:
            class_name = _class_name(page.name)
            map_key = _slug(page.name)
            page_objects.append(f"export class {class_name} {{")
            page_objects.append("  constructor(private readonly page: Page) {}")
            for action in page.actions[:6]:
                method = _slug(action)
                page_objects.append(f"  async {method}() {{")
                if action.startswith('click '):
                    label = action[6:]
                    sel_key = _slug(label)
                    page_objects.append(f"    await selectors.{map_key}.{sel_key}.click();")
                elif action.startswith('fill '):
                    label = action[5:]
                    sel_key = _slug(label)
                    page_objects.append(f"    await selectors.{map_key}.{sel_key}.fill('TODO');")
                elif action.startswith('select '):
                    label = action[7:]
                    sel_key = _slug(label)
                    page_objects.append(f"    await selectors.{map_key}.{sel_key}.click();")
                else:
                    page_objects.append("    await this.page.waitForLoadState('networkidle');")
                page_objects.append("  }")
            page_objects.append("  async assertLoaded() {")
            first = page.selectors[0]
            page_objects.append(f"    await expect(selectors.{map_key}.{first.key}).toBeVisible();")
            page_objects.append("  }")
            page_objects.append("}\n")
        return {
            'selectors.ts': '\n'.join(selectors_lines),
            'pageModels.ts': '\n'.join(page_objects),
        }
