from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote, urlparse
from uuid import uuid4

import httpx

from ai_qa_tester.models.contracts import Artifact, ArtifactType, WorkItem, WorkItemFilter, WorkItemType


@dataclass
class AzureDevOpsProjectRef:
    organization: str
    project: str
    base_url: str


@dataclass
class AzureDevOpsAttachment:
    name: str
    url: str
    content_type: str
    content: bytes
    source_work_item_id: str
    relation_type: str = "AttachedFile"


class DevOpsConnector:
    def __init__(self, base_url: str | None = None, pat: str | None = None, client: httpx.Client | None = None) -> None:
        self.base_url = base_url or os.getenv("AI_QA_AZURE_DEVOPS_URL")
        self.pat = pat or os.getenv("AI_QA_AZURE_DEVOPS_PAT")
        self.client = client or httpx.Client(timeout=20.0)

    def query_work_items(self, project_id: str, filters: WorkItemFilter) -> list[WorkItem]:
        if self.base_url and self.pat:
            try:
                return self._query_work_items_live(filters)
            except httpx.HTTPError:
                pass

        return [self._sample_story(filters)]


    def get_work_items_by_external_ids(self, external_ids: list[str]) -> list[WorkItem]:
        if not external_ids:
            return []
        if self.base_url and self.pat:
            try:
                return self._get_work_items_by_external_ids_live(external_ids)
            except httpx.HTTPError:
                pass
        return []

    def _get_work_items_by_external_ids_live(self, external_ids: list[str]) -> list[WorkItem]:
        project_ref = self.parse_project_ref()
        numeric_ids = [int(value) for value in external_ids if str(value).isdigit()]
        if not numeric_ids:
            return []
        all_payloads: list[dict[str, Any]] = []
        for chunk in self._chunk(numeric_ids, 200):
            batch_response = self.client.post(
                f"{project_ref.base_url}/_apis/wit/workitemsbatch?api-version=7.1",
                headers={**self._auth_headers(), "Content-Type": "application/json"},
                json={
                    "ids": chunk,
                    "fields": self._batch_fields(),
                    "$expand": "Relations",
                    "errorPolicy": "Omit",
                },
            )
            batch_response.raise_for_status()
            all_payloads.extend(batch_response.json().get("value", []))
        items = [self.map_work_item_from_azure(payload) for payload in all_payloads]
        return self._enrich_work_items_with_comments(items, project_ref)

    def _sample_story(self, filters: WorkItemFilter) -> WorkItem:
        return WorkItem(
            id=f"wk_{uuid4().hex[:8]}",
            external_id="ADO-1001",
            type=WorkItemType.STORY,
            title="Search registered business",
            description="As a user, I want to search registered businesses.",
            acceptance_criteria=[
                "User can search by business name",
                "Matching results are displayed",
            ],
            state=filters.state[0] if filters.state else "Ready for Test",
            assignee=filters.assignee[0] if filters.assignee else None,
            tags=filters.tags or ["search", "business"],
            sprint=filters.sprint[0] if filters.sprint else "Sprint 1",
            area_path=filters.area_path[0] if filters.area_path else "Business/Search",
            linked_artifact_refs=[{"type": "figma_url", "value": "https://figma.example/file/abc123"}],
        )

    def _query_work_items_live(self, filters: WorkItemFilter) -> list[WorkItem]:
        project_ref = self.parse_project_ref()
        wiql = self.build_wiql(project_ref.project, filters)
        wiql_response = self.client.post(
            f"{project_ref.base_url}/_apis/wit/wiql?api-version=7.1",
            headers={**self._auth_headers(), "Content-Type": "application/json"},
            json={"query": wiql},
        )
        wiql_response.raise_for_status()
        wiql_payload = wiql_response.json()
        work_items = wiql_payload.get("workItems", [])
        if not work_items:
            return []

        ids = [item["id"] for item in work_items if "id" in item]
        all_payloads: list[dict[str, Any]] = []
        for chunk in self._chunk(ids, 200):
            batch_response = self.client.post(
                f"{project_ref.base_url}/_apis/wit/workitemsbatch?api-version=7.1",
                headers={**self._auth_headers(), "Content-Type": "application/json"},
                json={
                    "ids": chunk,
                    "fields": self._batch_fields(),
                    "$expand": "Relations",
                    "errorPolicy": "Omit",
                },
            )
            batch_response.raise_for_status()
            batch_payload = batch_response.json()
            all_payloads.extend(batch_payload.get("value", []))
        items = [self.map_work_item_from_azure(payload) for payload in all_payloads]
        return self._enrich_work_items_with_comments(items, project_ref)

    def fetch_attachments_for_work_item(self, project_id: str, work_item: WorkItem) -> list[AzureDevOpsAttachment]:
        refs = [ref for ref in work_item.linked_artifact_refs if ref.get("type") in {"attachment_url", "ado_attachment"}]
        attachments: list[AzureDevOpsAttachment] = []
        for ref in refs:
            url = ref.get("value") or ref.get("url")
            name = ref.get("name") or self._guess_filename(url)
            if not url:
                continue
            content = self._download_attachment(url)
            attachments.append(
                AzureDevOpsAttachment(
                    name=name,
                    url=url,
                    content_type=ref.get("content_type") or self._guess_content_type(name),
                    content=content,
                    source_work_item_id=work_item.id,
                    relation_type=ref.get("relation_type", "AttachedFile"),
                )
            )
        return attachments

    def parse_project_ref(self, url: str | None = None) -> AzureDevOpsProjectRef:
        raw = url or self.base_url
        if not raw:
            raise ValueError("Azure DevOps URL is required")
        parsed = urlparse(raw)
        path_parts = [unquote(part) for part in parsed.path.strip("/").split("/") if part]
        if parsed.netloc.lower() != "dev.azure.com" or len(path_parts) < 2:
            raise ValueError(f"Unsupported Azure DevOps URL: {raw}")
        organization = path_parts[0]
        project = path_parts[1]
        return AzureDevOpsProjectRef(
            organization=organization,
            project=project,
            base_url=f"https://dev.azure.com/{organization}/{project}",
        )

    def build_wiql(self, team_project: str, filters: WorkItemFilter) -> str:
        clauses = [f"[System.TeamProject] = '{self._escape_wiql(team_project)}'", "[System.IsDeleted] <> True"]
        if filters.state:
            clauses.append(self._in_clause("[System.State]", filters.state))
        if filters.assignee:
            clauses.append(self._in_clause("[System.AssignedTo]", filters.assignee))
        if filters.type:
            expanded_types: list[str] = []
            for work_item_type in filters.type:
                expanded_types.extend(self._azure_type_names(work_item_type))
            clauses.append(self._in_clause("[System.WorkItemType]", expanded_types))
        if filters.sprint:
            clauses.append(self._contains_any_clause("[System.IterationPath]", filters.sprint))
        if filters.area_path:
            clauses.append(self._contains_any_clause("[System.AreaPath]", filters.area_path))
        if filters.tags:
            clauses.append(self._contains_any_clause("[System.Tags]", filters.tags))
        return (
            "SELECT [System.Id] FROM WorkItems WHERE "
            + " AND ".join(clauses)
            + " ORDER BY [System.ChangedDate] DESC"
        )

    def map_work_item_from_azure(self, payload: dict[str, Any]) -> WorkItem:
        fields = payload.get("fields", {})
        relations = payload.get("relations", [])
        item_type = self._normalize_type(fields.get("System.WorkItemType"))
        return WorkItem(
            id=f"wk_{payload.get('id')}",
            external_id=str(payload.get("id")),
            source_system="azure_devops",
            type=item_type,
            title=fields.get("System.Title") or f"Work item {payload.get('id')}",
            description=fields.get("System.Description") or "",
            acceptance_criteria=self._split_acceptance_criteria(fields.get("Microsoft.VSTS.Common.AcceptanceCriteria") or ""),
            state=fields.get("System.State") or "New",
            assignee=self._display_name(fields.get("System.AssignedTo")),
            tags=self._split_tags(fields.get("System.Tags")),
            sprint=fields.get("System.IterationPath"),
            area_path=fields.get("System.AreaPath"),
            release=fields.get("Custom.Release") or fields.get("Release"),
            priority=str(fields.get("Microsoft.VSTS.Common.Priority")) if fields.get("Microsoft.VSTS.Common.Priority") is not None else None,
            severity=fields.get("Microsoft.VSTS.Common.Severity"),
            linked_artifact_refs=self._extract_linked_artifact_refs(relations),
            related_work_item_refs=self._extract_related_work_item_refs(relations),
        )


    def fetch_comments_for_work_item(self, work_item: WorkItem, project_ref: AzureDevOpsProjectRef | None = None) -> list[str]:
        project_ref = project_ref or self.parse_project_ref()
        external_id = work_item.external_id
        response = self.client.get(
            f"{project_ref.base_url}/_apis/wit/workItems/{external_id}/comments?api-version=7.1-preview.4",
            headers=self._auth_headers(),
        )
        if response.status_code == 404:
            return []
        response.raise_for_status()
        payload = response.json()
        comments = payload.get("comments", [])
        return [self._clean_html(comment.get("text", "")) for comment in comments if self._clean_html(comment.get("text", ""))]

    def sync_work_item_context(self, work_item: WorkItem) -> WorkItem:
        if not (self.base_url and self.pat):
            return work_item
        project_ref = self.parse_project_ref()
        work_item.comments = self.fetch_comments_for_work_item(work_item, project_ref)
        return work_item

    def _enrich_work_items_with_comments(self, items: list[WorkItem], project_ref: AzureDevOpsProjectRef) -> list[WorkItem]:
        enriched: list[WorkItem] = []
        for item in items:
            try:
                item.comments = self.fetch_comments_for_work_item(item, project_ref)
            except httpx.HTTPStatusError:
                item.comments = []
            enriched.append(item)
        return enriched

    def _download_attachment(self, url: str) -> bytes:
        headers = self._auth_headers()
        response = self.client.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    def _auth_headers(self) -> dict[str, str]:
        if not self.pat:
            return {}
        token = base64.b64encode(f":{self.pat}".encode("utf-8")).decode("ascii")
        return {"Authorization": f"Basic {token}"}

    @staticmethod
    def _normalize_type(raw_type: str | None) -> WorkItemType:
        value = (raw_type or "").strip().lower()
        if value in {"bug", "defect"}:
            return WorkItemType.DEFECT
        if value in {"task"}:
            return WorkItemType.TASK
        return WorkItemType.STORY

    @staticmethod
    def _azure_type_names(work_item_type: WorkItemType) -> list[str]:
        if work_item_type == WorkItemType.STORY:
            return ["User Story", "Product Backlog Item", "Story"]
        if work_item_type == WorkItemType.DEFECT:
            return ["Bug", "Defect"]
        return ["Task"]

    @staticmethod
    def _split_tags(tags: str | None) -> list[str]:
        if not tags:
            return []
        return [part.strip() for part in str(tags).split(";") if part.strip()]

    @staticmethod
    def _split_acceptance_criteria(text: str) -> list[str]:
        if not text:
            return []
        normalized = (
            text.replace("</li>", "\n")
            .replace("<li>", "")
            .replace("<br>", "\n")
            .replace("<br/>", "\n")
            .replace("<br />", "\n")
        )
        import re
        cleaned = re.sub(r"<[^>]+>", " ", normalized)
        lines = [line.strip(" -•\t") for line in cleaned.splitlines()]
        return [line for line in lines if line]

    @staticmethod
    def _display_name(value: Any) -> str | None:
        if not value:
            return None
        if isinstance(value, dict):
            return value.get("displayName") or value.get("uniqueName")
        return str(value)

    def _extract_linked_artifact_refs(self, relations: list[dict[str, Any]]) -> list[dict[str, str]]:
        refs: list[dict[str, str]] = []
        for relation in relations or []:
            rel = relation.get("rel") or ""
            url = relation.get("url") or ""
            attrs = relation.get("attributes") or {}
            name = attrs.get("name") or self._guess_filename(url)
            if rel == "AttachedFile":
                refs.append(
                    {
                        "type": "ado_attachment",
                        "value": url,
                        "url": url,
                        "name": name,
                        "relation_type": rel,
                        "content_type": self._guess_content_type(name),
                    }
                )
            elif "figma.com" in url:
                refs.append({"type": "figma_url", "value": url})
            elif url:
                refs.append({"type": "external_link", "value": url, "name": name, "relation_type": rel})
        return refs

    def _extract_related_work_item_refs(self, relations: list[dict[str, Any]]) -> list[dict[str, str]]:
        refs: list[dict[str, str]] = []
        for relation in relations or []:
            rel = relation.get("rel") or ""
            url = relation.get("url") or ""
            if not rel or not url or "workItems/" not in url or rel == "AttachedFile":
                continue
            work_item_id = url.rstrip("/").split("/")[-1].split("?")[0]
            attrs = relation.get("attributes") or {}
            refs.append(
                {
                    "type": "ado_work_item_relation",
                    "relation_type": rel,
                    "value": url,
                    "work_item_external_id": work_item_id,
                    "name": attrs.get("name") or rel,
                }
            )
        return refs

    @staticmethod
    def _clean_html(value: str | None) -> str:
        if not value:
            return ""
        import re
        normalized = (
            str(value).replace("</li>", "\n").replace("<li>", "").replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
        )
        cleaned = re.sub(r"<[^>]+>", " ", normalized)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    @staticmethod
    def _guess_filename(url: str | None) -> str:
        if not url:
            return f"attachment-{uuid4().hex[:8]}.bin"
        parsed = urlparse(url)
        name = os.path.basename(parsed.path)
        return name or f"attachment-{uuid4().hex[:8]}.bin"

    @staticmethod
    def _guess_content_type(name: str) -> str:
        lowered = name.lower()
        if lowered.endswith(".png"):
            return "image/png"
        if lowered.endswith(".jpg") or lowered.endswith(".jpeg"):
            return "image/jpeg"
        if lowered.endswith(".webp"):
            return "image/webp"
        if lowered.endswith(".pdf"):
            return "application/pdf"
        return "application/octet-stream"

    @staticmethod
    def _escape_wiql(value: str) -> str:
        return value.replace("'", "''")

    def _in_clause(self, field_name: str, values: list[str]) -> str:
        cleaned = [f"'{self._escape_wiql(value)}'" for value in values if value]
        if not cleaned:
            return "1=1"
        return f"{field_name} IN ({', '.join(cleaned)})"

    def _contains_any_clause(self, field_name: str, values: list[str]) -> str:
        cleaned = [value for value in values if value]
        if not cleaned:
            return "1=1"
        parts = [f"{field_name} CONTAINS '{self._escape_wiql(value)}'" for value in cleaned]
        return "(" + " OR ".join(parts) + ")"

    @staticmethod
    def _chunk(values: list[int], chunk_size: int) -> list[list[int]]:
        return [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]

    @staticmethod
    def _batch_fields() -> list[str]:
        return [
            "System.Id",
            "System.WorkItemType",
            "System.Title",
            "System.Description",
            "System.State",
            "System.AssignedTo",
            "System.Tags",
            "System.IterationPath",
            "System.AreaPath",
            "Microsoft.VSTS.Common.AcceptanceCriteria",
            "Microsoft.VSTS.Common.Priority",
            "Microsoft.VSTS.Common.Severity",
            "Custom.Release",
            "Release",
        ]


    def publish_traceability_comment(self, work_item_id: str, text: str) -> dict[str, Any]:
        project_ref = self.parse_project_ref()
        response = self.client.post(
            f"{project_ref.base_url}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.4",
            headers={**self._auth_headers(), "Content-Type": "application/json"},
            json={"text": text},
        )
        response.raise_for_status()
        return response.json()

    def publish_run_summary_comment(self, work_item_id: str, run_id: str, summary: dict[str, int], scenario_ids: list[str]) -> dict[str, Any]:
        body = (
            f"AI QA run summary for {run_id}: passed={summary.get('passed', 0)}, "
            f"failed={summary.get('failed', 0)}, blocked={summary.get('blocked', 0)}. "
            f"Scenarios: {', '.join(scenario_ids) if scenario_ids else 'none'}."
        )
        return self.publish_traceability_comment(work_item_id, body)

    def create_bug_from_failed_run(
        self,
        run_id: str,
        title: str,
        description: str,
        repro_steps: list[str] | None = None,
        area_path: str | None = None,
        iteration_path: str | None = None,
    ) -> dict[str, Any]:
        project_ref = self.parse_project_ref()
        patch = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
            {"op": "add", "path": "/fields/System.Description", "value": description},
        ]
        if repro_steps:
            patch.append({"op": "add", "path": "/fields/Microsoft.VSTS.TCM.ReproSteps", "value": "<br/>".join(repro_steps)})
        if area_path:
            patch.append({"op": "add", "path": "/fields/System.AreaPath", "value": area_path})
        if iteration_path:
            patch.append({"op": "add", "path": "/fields/System.IterationPath", "value": iteration_path})
        response = self.client.patch(
            f"{project_ref.base_url}/_apis/wit/workitems/$Bug?api-version=7.1",
            headers={**self._auth_headers(), "Content-Type": "application/json-patch+json"},
            json=patch,
        )
        response.raise_for_status()
        payload = response.json()
        if "id" in payload:
            try:
                self.publish_traceability_comment(str(payload["id"]), f"Created automatically from failed AI QA run {run_id}.")
            except Exception:
                pass
        return payload



    def search_existing_bug(
        self,
        title: str,
        area_path: str | None = None,
        iteration_path: str | None = None,
        related_work_item_id: str | None = None,
    ) -> dict[str, Any] | None:
        project_ref = self.parse_project_ref()
        clauses = [
            f"[System.TeamProject] = '{self._escape_wiql(project_ref.project)}'",
            "[System.WorkItemType] = 'Bug'",
            f"[System.Title] = '{self._escape_wiql(title)}'",
            "[System.State] <> 'Closed'",
            "[System.IsDeleted] <> True",
        ]
        if area_path:
            clauses.append(f"[System.AreaPath] = '{self._escape_wiql(area_path)}'")
        if iteration_path:
            clauses.append(f"[System.IterationPath] = '{self._escape_wiql(iteration_path)}'")
        if related_work_item_id:
            clauses.append(f"[System.Description] CONTAINS '{self._escape_wiql(str(related_work_item_id))}'")
        wiql = 'SELECT [System.Id] FROM WorkItems WHERE ' + ' AND '.join(clauses) + ' ORDER BY [System.ChangedDate] DESC'
        response = self.client.post(
            f"{project_ref.base_url}/_apis/wit/wiql?api-version=7.1",
            headers={**self._auth_headers(), "Content-Type": "application/json"},
            json={"query": wiql},
        )
        response.raise_for_status()
        payload = response.json()
        items = payload.get("workItems", [])
        if not items:
            return None
        return items[0]

    def update_bug_from_failed_run(
        self,
        bug_id: str,
        run_id: str,
        summary_text: str,
        repro_steps: list[str] | None = None,
    ) -> dict[str, Any]:
        project_ref = self.parse_project_ref()
        patch = [
            {"op": "add", "path": "/fields/System.History", "value": summary_text},
        ]
        if repro_steps:
            patch.append({
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.ReproSteps",
                "value": "<br/>".join(repro_steps),
            })
        response = self.client.patch(
            f"{project_ref.base_url}/_apis/wit/workitems/{bug_id}?api-version=7.1",
            headers={**self._auth_headers(), "Content-Type": "application/json-patch+json"},
            json=patch,
        )
        response.raise_for_status()
        try:
            self.publish_traceability_comment(str(bug_id), f"Updated automatically from failed AI QA run {run_id}.")
        except Exception:
            pass
        return response.json()

    def upsert_bug_from_failed_run(
        self,
        run_id: str,
        title: str,
        description: str,
        repro_steps: list[str] | None = None,
        area_path: str | None = None,
        iteration_path: str | None = None,
        related_work_item_id: str | None = None,
    ) -> dict[str, Any]:
        existing = self.search_existing_bug(
            title=title,
            area_path=area_path,
            iteration_path=iteration_path,
            related_work_item_id=related_work_item_id,
        )
        if existing and existing.get("id"):
            summary = f"AI QA run {run_id} still reproduces this issue. {description}"
            updated = self.update_bug_from_failed_run(
                bug_id=str(existing["id"]),
                run_id=run_id,
                summary_text=summary,
                repro_steps=repro_steps,
            )
            return {"action": "updated", "bug": updated, "existing_bug_id": existing["id"]}

        created = self.create_bug_from_failed_run(
            run_id=run_id,
            title=title,
            description=description,
            repro_steps=repro_steps,
            area_path=area_path,
            iteration_path=iteration_path,
        )
        return {"action": "created", "bug": created}

class FigmaConnector:
    def fetch_from_urls(self, project_id: str, figma_urls: list[str]) -> list[Artifact]:
        artifacts: list[Artifact] = []
        for url in figma_urls:
            artifacts.append(
                Artifact(
                    id=f"art_{uuid4().hex[:8]}",
                    project_id=project_id,
                    artifact_type=ArtifactType.FIGMA_FRAME,
                    source_type="figma",
                    source_ref=url,
                    title="Business Search Results",
                    raw_uri=url,
                    metadata={
                        "page_name": "Search",
                        "frame_name": "Results",
                        "labels": ["Search", "Results", "Business Name"],
                    },
                    status="processed",
                )
            )
        return artifacts
