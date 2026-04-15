from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class WorkItemType(str, Enum):
    STORY = "story"
    DEFECT = "defect"
    TASK = "task"


class ArtifactType(str, Enum):
    FIGMA_FRAME = "figma_frame"
    SCREENSHOT = "screenshot"
    WIREFRAME = "wireframe"
    API_SPEC = "api_spec"
    JOURNEY_WIREFRAME = "journey_wireframe"


class AssociationDecision(str, Enum):
    ASSOCIATE = "associate"
    REVIEW = "review"
    REJECT = "reject"


class ScenarioType(str, Enum):
    UI = "ui"
    API = "api"
    INTEGRATION = "integration"
    REGRESSION = "regression"


class RunStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL_SUCCESS = "partial_success"




class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class QueueJob(BaseModel):
    id: str
    project_id: str
    job_type: str
    status: JobStatus = JobStatus.QUEUED
    payload: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None

class EntityRef(BaseModel):
    type: str
    id: str


class WorkItemFilter(BaseModel):
    state: list[str] = Field(default_factory=list)
    assignee: list[str] = Field(default_factory=list)
    type: list[WorkItemType] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    sprint: list[str] = Field(default_factory=list)
    area_path: list[str] = Field(default_factory=list)




class Project(BaseModel):
    id: str
    name: str
    status: str = "active"
    devops_provider: str = "azure_devops"
    figma_enabled: bool = True
    devops_url: str | None = None
    devops_pat: str | None = None
    devops_webhook_secret: str | None = None
    devops_webhook_hmac_secret: str | None = None
    devops_webhook_subscription_id: str | None = None
    devops_webhook_publisher_id: str = "tfs"


class WorkItem(BaseModel):
    id: str
    external_id: str
    source_system: str = "azure_devops"
    type: WorkItemType
    title: str
    description: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)
    state: str = "New"
    assignee: str | None = None
    tags: list[str] = Field(default_factory=list)
    sprint: str | None = None
    area_path: str | None = None
    release: str | None = None
    priority: str | None = None
    severity: str | None = None
    linked_artifact_refs: list[dict[str, str]] = Field(default_factory=list)
    related_work_item_refs: list[dict[str, str]] = Field(default_factory=list)
    comments: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Artifact(BaseModel):
    id: str
    project_id: str
    artifact_type: ArtifactType
    source_type: str
    source_ref: str
    title: str
    raw_uri: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: str = "registered"


class JourneyStep(BaseModel):
    order: int
    artifact_id: str
    step_key: str
    step_title: str
    summary: str = ""


class JourneyArtifact(BaseModel):
    id: str
    project_id: str
    artifact_type: ArtifactType = ArtifactType.JOURNEY_WIREFRAME
    source_type: str = "upload"
    title: str
    journey_name: str
    source_ref: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    step_artifact_ids: list[str] = Field(default_factory=list)
    steps: list[JourneyStep] = Field(default_factory=list)
    status: str = "registered"


class AssociationEvidence(BaseModel):
    type: Literal["direct_reference", "metadata", "semantic", "visual", "journey"]
    strength: float
    detail: str


class Association(BaseModel):
    id: str
    project_id: str
    source_entity: EntityRef
    target_entity: EntityRef
    association_type: str
    decision: AssociationDecision
    confidence: float
    evidence: list[AssociationEvidence] = Field(default_factory=list)
    reason_summary: str
    status: str = "proposed"


class TestScenario(BaseModel):
    id: str
    project_id: str
    title: str
    scenario_type: ScenarioType
    journey: str
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    preconditions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected_results: list[str] = Field(default_factory=list)
    source_refs: list[EntityRef] = Field(default_factory=list)
    coverage_reason: str
    confidence: float = 0.75
    review_required: bool = True
    status: str = "draft"
    version: int = 1




class GeneratedScript(BaseModel):
    id: str
    project_id: str
    scenario_id: str
    framework: str = "playwright"
    language: str = "typescript"
    version: int = 1
    status: str = "generated"
    content: str


class ScriptExecutionResult(BaseModel):
    id: str
    project_id: str
    run_id: str
    script_id: str
    scenario_id: str
    status: Literal["passed", "failed", "blocked"]
    reason: str
    stdout: str = ""
    stderr: str = ""
    evidence_refs: list[str] = Field(default_factory=list)




class SelectorDefinition(BaseModel):
    key: str
    locator: str
    strategy: str = "testid_or_text"
    source_label: str
    element_type: str = "text"


class PageModel(BaseModel):
    id: str
    project_id: str
    name: str
    journey: str
    source_entity: EntityRef
    route_hint: str | None = None
    selectors: list[SelectorDefinition] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    assertions: list[str] = Field(default_factory=list)
    status: str = "generated"



class SelectorProfile(BaseModel):
    id: str
    project_id: str
    name: str
    journey: str
    page_model_ids: list[str] = Field(default_factory=list)
    selectors: list[SelectorDefinition] = Field(default_factory=list)
    source: str = "generated"
    approved: bool = False
    status: str = "draft"
    notes: str | None = None



class SelectorLearningSuggestion(BaseModel):
    selector_key: str
    current_locator: str
    suggested_locator: str
    reason: str
    confidence: float = 0.7


class SelectorLearningReport(BaseModel):
    id: str
    project_id: str
    run_id: str
    journey: str
    profile_id: str | None = None
    execution_ids: list[str] = Field(default_factory=list)
    summary: str = ""
    suggestions: list[SelectorLearningSuggestion] = Field(default_factory=list)
    status: str = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))



class ScenarioRunDelta(BaseModel):
    scenario_id: str
    title: str | None = None
    baseline_status: str | None = None
    candidate_status: str | None = None
    changed: bool = False
    improved: bool = False
    regressed: bool = False


class RunComparisonReport(BaseModel):
    id: str
    project_id: str
    baseline_run_id: str
    candidate_run_id: str
    comparison_type: str = "run_comparison"
    improved: bool = False
    stability_change: str = "unchanged"
    summary: dict[str, int | float | str] = Field(default_factory=dict)
    scenario_deltas: list[ScenarioRunDelta] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))



class StabilityScenarioMetric(BaseModel):
    scenario_id: str
    title: str | None = None
    journey: str | None = None
    total_runs: int = 0
    passed_runs: int = 0
    failed_runs: int = 0
    blocked_runs: int = 0
    pass_rate: float = 0.0
    flaky_score: float = 0.0


class StabilityAnalyticsReport(BaseModel):
    id: str
    project_id: str
    report_type: str = "stability_analytics"
    baseline_run_id: str | None = None
    candidate_run_id: str | None = None
    journey: str | None = None
    total_runs: int = 0
    total_comparisons: int = 0
    improved_comparisons: int = 0
    regressed_comparisons: int = 0
    unchanged_comparisons: int = 0
    selector_retest_runs: int = 0
    pass_rate: float = 0.0
    failed_rate: float = 0.0
    blocked_rate: float = 0.0
    scenario_metrics: list[StabilityScenarioMetric] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class TestRun(BaseModel):
    id: str
    project_id: str
    environment: str
    trigger_type: str
    status: RunStatus = RunStatus.QUEUED
    scenario_ids: list[str] = Field(default_factory=list)
    summary: dict[str, int] = Field(default_factory=dict)
    result_details: list[dict[str, Any]] = Field(default_factory=list)


class DevOpsPublishResult(BaseModel):
    success: bool
    action: str
    target_id: str | None = None
    target_url: str | None = None
    detail: str | None = None


class CommandEnvelope(BaseModel):
    command_id: str
    command_type: str
    project_id: str
    correlation_id: str
    payload: dict[str, Any] = Field(default_factory=dict)


class EventEnvelope(BaseModel):
    event_id: str
    event_type: str
    event_version: int = 1
    project_id: str
    correlation_id: str
    causation_id: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    producer: str
    payload: dict[str, Any] = Field(default_factory=dict)
