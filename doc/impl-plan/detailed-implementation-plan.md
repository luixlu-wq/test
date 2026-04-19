# AI QA Platform Detailed Implementation Plan

## 1. Purpose

This document turns the architecture and implementation design docs into an executable build plan.

For each step it defines:

1. what to implement
2. environment setup
3. how to test functionality
4. test cases
5. test data
6. assertion standards
7. exit criteria

Source design references:

- `api/doc/arc-design/architectural-design.md`
- `api/doc/impl-design/service design.md`
- `api/doc/impl-design/MCP contract implementation.md`
- `api/doc/impl-design/RAG implementation design.md`
- `api/doc/impl-design/playwrite hybride framework design.md`
- `api/doc/impl-design/data model design.md`
- `api/doc/impl-design/knowledge graph schema design.md`
- `api/doc/impl-design/agent promts design.md`

## 2. Baseline Stack and Environments

### 2.1 Current codebase baseline

- Python package: `ai-qa-tester`
- Services:
  - API service: `ai_qa_tester.api.main:app`
  - Intelligence service: `ai_qa_tester.intelligence.main:app`
  - Worker service: `ai_qa_tester.worker.main:app`
- Existing test framework: `pytest`
- Existing execution mode support in code/tests: simulated and Playwright-backed execution

### 2.2 Environment profiles

1. `local-dev` (default for most implementation)
- SQLite
- local blob store
- local vector store
- in-memory/local queue/event bus fallback

2. `integration`
- PostgreSQL
- object storage (local emulator or cloud)
- vector backend (Qdrant or equivalent)
- service bus enabled

3. `ci`
- ephemeral test DB
- seeded synthetic fixtures only
- no external system credentials

### 2.3 Global setup commands

```powershell
cd api
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev,runner]
python -m playwright install chromium
```

Start services:

```powershell
uvicorn ai_qa_tester.api.main:app --reload --port 8000
uvicorn ai_qa_tester.intelligence.main:app --reload --port 8001
uvicorn ai_qa_tester.worker.main:app --reload --port 8002
```

Run tests:

```powershell
pytest -q
```

### 2.4 Required environment variables (local-dev baseline)

```powershell
$env:AI_QA_ENVIRONMENT="dev"
$env:AI_QA_REPOSITORY_BACKEND="sqlalchemy"
$env:AI_QA_DATABASE_URL="sqlite:///./.local/ai_qa_tester.db"
$env:AI_QA_BLOB_BACKEND="local"
$env:AI_QA_BLOB_ROOT="./.local/blobs"
$env:AI_QA_VECTOR_BACKEND="local"
$env:AI_QA_VECTOR_STORE_PATH="./.local/vectors.json"
$env:AI_QA_EXECUTION_BACKEND="simulated"
$env:AI_QA_PLAYWRIGHT_WORK_ROOT="./.local/playwright_runs"
```

## 3. Global Test Data Strategy

### 3.1 Canonical synthetic project datasets

Create and version these under `api/tests/data/`:

1. `project_login_v1`
- Story: valid login, invalid password, forgot password
- Wireframe image: login and forgot password
- Screenshot set: baseline and drifted versions
- OpenAPI spec: `POST /auth/login`, `POST /auth/forgot-password`
- Known defect note: forgot password link broken

2. `project_registration_v1`
- Multi-step registration flow
- Async state transitions and API dependencies
- 1 known flaky selector sample

3. `project_defect_regression_v1`
- Historical run summaries
- Defect drafts + evidence bundles
- Selector-healing history sample

### 3.2 Test data rules

- Use synthetic or masked data only.
- No production secrets.
- Deterministic fixture seeds for repeatable tests.
- Every test data artifact has stable IDs and source refs.

## 4. Global Assertion Standards

All phases must follow these assertion standards.

### 4.1 Contract assertions

- Every API/MCP response follows schema.
- Required identifiers are present (`requestId`, `runId`, `caseId`, `toolCallId` when applicable).
- Enum values are valid and canonical.

### 4.2 Functional assertions

- Expected side-effects are persisted.
- No unexpected cross-entity mutation.
- Failures return structured error payloads with retryability signals.

### 4.3 Traceability assertions

- Every generated decision links to source refs and evidence refs.
- Retrieval context packs log included references.
- Run outputs map to scenario/test asset IDs.

### 4.4 Determinism assertions

- Same input + same snapshot => same plan/asset selection.
- Regression mode disallows exploratory runtime behavior.
- Non-deterministic fields are explicitly excluded from comparisons.

### 4.5 Security assertions

- Secrets masked in logs and externalized outputs.
- Sensitive fields are not embedded in prompts/context packs.
- Policy violations fail closed.

## 5. Phase-by-Phase Implementation Steps

## Step 0 - Spec Lock and Delivery Guardrails

### What to implement

1. Canonical enum definitions:
- `execution_mode` (`draft`, `diagnostic`, `regression`) as single source of truth.
- lifecycle statuses for request/run/asset/approval.
2. Common envelopes for:
- MCP request/response/error
- agent input/output
- event bus messages
3. Cross-doc alignment checklist and version stamp.

### Environment setup

- Local-dev profile only.
- Add `api/doc/impl-plan/contracts/` for frozen JSON schemas.

### How to test

- Schema validation tests on sample payloads.
- Negative tests for missing required fields and invalid enums.

### Test cases

- `TC-S0-001`: valid MCP request envelope passes schema.
- `TC-S0-002`: invalid `execution_mode` rejected.
- `TC-S0-003`: agent output missing `status` rejected.

### Test data

- `api/tests/data/contracts/valid/*.json`
- `api/tests/data/contracts/invalid/*.json`

### Assertion standards

- Strict schema validation.
- No permissive extra fields for critical envelopes.

### Exit criteria

- Contract schema test suite passes 100%.
- Enum drift eliminated from implementation docs and code constants.

## Step 1 - Platform Backbone (Gateway, Trigger, Orchestration, Policy, Audit)

### What to implement

1. Request ingestion and deduplication path.
2. Trigger ingestion path (manual, webhook, pre-commit).
3. Orchestration state machine with idempotent stage execution.
4. Policy and approval decision service.
5. Audit log writer with correlation IDs.

### Environment setup

- Local-dev plus optional integration DB for workflow persistence.
- Enable service bus toggle only in integration profile.

### How to test

- API endpoint unit tests and workflow service tests.
- End-to-end workflow test from request submission to stage transitions.

### Test cases

- `TC-S1-001`: duplicate request key returns same workflow instance.
- `TC-S1-002`: stage retry is idempotent (no duplicate side-effects).
- `TC-S1-003`: policy requires approval for restricted action.
- `TC-S1-004`: audit record created for each stage transition.

### Test data

- Request payloads:
  - single case (`login-flow`)
  - multi-case (`login-flow`, `registration-flow`)
  - invalid environment

### Assertion standards

- All workflow transitions must be valid graph transitions.
- Every decision includes reason + policy source.

### Exit criteria

- Orchestration can resume interrupted workflows.
- End-to-end backbone tests pass with deterministic state output.

## Step 2 - Data Model and Persistence Foundation

### What to implement

1. Initial migration set for minimum operational tables.
2. Repository abstraction hardening for SQL backend.
3. Persistence integration for request/workflow/run/evidence metadata.
4. Retention job scaffolding for heavy artifacts.

### Environment setup

- Local SQLite first, PostgreSQL in integration profile.
- Create `.local/` folders for DB/blob/vector files.

### How to test

- Migration smoke tests.
- Repository roundtrip tests.
- Transactional integrity tests.

### Test cases

- `TC-S2-001`: migration up/down consistency.
- `TC-S2-002`: request + case + run links persist and query correctly.
- `TC-S2-003`: rollback on partial write keeps integrity.
- `TC-S2-004`: retention policy marks old heavy artifacts for tiering.

### Test data

- Minimal seeded entities:
  - 1 project
  - 2 cases
  - 3 artifacts
  - 1 run
  - 1 evidence bundle

### Assertion standards

- Foreign key and uniqueness constraints enforced.
- No orphan traceability entities.

### Exit criteria

- Persistence tests green in SQLite and PostgreSQL.
- Core tables support end-to-end flow without in-memory fallbacks.

## Step 3 - MCP Core Set (Filesystem, Document Parser, Browser Reader, Trigger)

### What to implement

1. MCP adapter interfaces and shared envelope middleware.
2. Filesystem MCP with policy-safe path constraints.
3. Document Parser MCP for markdown/PDF/docx extraction.
4. Browser Reader MCP read-only ingestion + caching.
5. Trigger MCP for local shift-left entry points.

### Environment setup

- Local-dev with file sandbox path in test fixtures.
- Browser reader can use mocked fetch/session in unit tests.

### How to test

- Contract tests for each MCP operation.
- Policy tests (read-only boundaries, blocked operations).
- Caching behavior tests for browser ingestion.

### Test cases

- `TC-S3-001`: filesystem MCP blocks path escape.
- `TC-S3-002`: parser extracts headings/acceptance criteria from story markdown.
- `TC-S3-003`: browser reader returns normalized snapshot + metadata.
- `TC-S3-004`: trigger MCP emits valid trigger envelope.

### Test data

- `tests/data/cases/login-flow/*`
- HTML snapshots for browser URL capture.

### Assertion standards

- MCP responses contain `toolCallId`, `status`, `audit`.
- No blob payloads in response where refs are required.

### Exit criteria

- MCP contract suite passes.
- Core ingestion MCPs are callable from orchestration path.

## Step 4 - Distributed Understanding Pipeline

### What to implement

1. Artifact normalization pipeline:
- classify, parse, normalize, preserve provenance.
2. Artifact fusion layer:
- map story/wireframe/screenshot/API/rules/expected results.
3. Case understanding summary output.
4. Chunk generation and metadata enrichment for retrieval.

### Environment setup

- Enable local blob + local vector.
- Keep OCR/image tooling installed for wireframe processing.

### How to test

- Service unit tests on normalization and fusion.
- Integration tests through upload + process endpoints.

### Test cases

- `TC-S4-001`: uploaded wireframe yields artifact + extracted visual hints.
- `TC-S4-002`: fused understanding identifies missing acceptance coverage.
- `TC-S4-003`: chunk records include provenance refs and artifact version.
- `TC-S4-004`: ingestion issues reported but workflow remains resumable.

### Test data

- Login wireframe PNG
- Story markdown with acceptance criteria
- OpenAPI yaml
- Known defect markdown

### Assertion standards

- Each fused output references source artifact IDs.
- Conflicts/gaps explicitly represented, never silently dropped.

### Exit criteria

- Understanding outputs are persisted and retrievable.
- Existing wireframe and association tests pass plus new fusion tests.

## Step 5 - Semantic State and Mismatch Detection

### What to implement

1. Semantic state map generation:
- states, transitions, expected outcomes, UI element fingerprints.
2. Mismatch detection service:
- requirement vs state vs artifact contradiction classification.
3. Mismatch severity and execution-blocking signals.

### Environment setup

- No extra infra required for local-dev.
- Ensure state map and mismatch tables/mappings exist.

### How to test

- Deterministic unit tests for state extraction.
- Integration tests for mismatch classification with known conflicting artifacts.

### Test cases

- `TC-S5-001`: state map includes login loading -> authenticated transition.
- `TC-S5-002`: mismatch flagged when wireframe requires captcha but story does not.
- `TC-S5-003`: blocking mismatch prevents execution stage.
- `TC-S5-004`: mismatch summary available for retrieval context.

### Test data

- `project_login_v1` with deliberate conflict variant.
- semantic state expected JSON snapshots.

### Assertion standards

- Mismatch must include severity + source refs + policy flag.
- State map graph must be internally consistent (no unreachable required state).

### Exit criteria

- State map and mismatch outputs feed retrieval and orchestration gates.

## Step 6 - Graph-RAG Foundation

### What to implement

1. Hybrid indexing:
- chunk indexing
- metadata filters (`caseId`, `artifactType`, `sourceType`, `executionMode`)
2. Retrieval search API.
3. Graph linking and one-hop expansion.
4. Context pack builder with bounded context policy.
5. Retrieval logs and context pack logs.

### Environment setup

- Local vector backend for dev.
- Qdrant/search backend in integration profile.

### How to test

- Retrieval relevance tests on known corpus.
- Graph expansion tests.
- Context pack bounds and filtering tests.

### Test cases

- `TC-S6-001`: search top-k contains expected requirement chunks.
- `TC-S6-002`: filter by `caseId` excludes other project noise.
- `TC-S6-003`: graph expansion adds linked test/evidence entities.
- `TC-S6-004`: regression mode context pack excludes non-approved diagnostic artifacts.

### Test data

- Indexed corpus from `project_login_v1`, `project_registration_v1`.
- historical runs/evidence summaries from `project_defect_regression_v1`.

### Assertion standards

- Context pack includes refs, not raw heavy blobs.
- Retrieval logs record query, filters, selected refs, and token size metrics.

### Exit criteria

- Agent runtime can request and consume bounded context packs.

## Step 7 - Agent Runtime and Prompt Governance

### What to implement

1. Role-specific agent runner interfaces:
- intake, understanding, mapping, strategy, authoring, triage, defect, learning.
2. Prompt registry with `promptVersion` and schema version pinning.
3. Structured output validation and retry/fallback strategy.
4. Fact-vs-inference and policy guardrails enforcement.

### Environment setup

- Local model stubs/mocks for tests.
- Optional real model integration behind feature flag.

### How to test

- Contract tests for agent input/output envelopes.
- Guardrail tests for policy boundary violations.
- Deterministic replay tests using stored context packs.

### Test cases

- `TC-S7-001`: agent output failing schema triggers recovery path.
- `TC-S7-002`: low confidence + conflict forces review-required status.
- `TC-S7-003`: prompt metadata persisted with generated assets.
- `TC-S7-004`: regression mode blocks unsupported exploratory suggestion.

### Test data

- Context packs from Step 6.
- Prompt fixtures with valid and invalid model outputs.

### Assertion standards

- No agent action accepted without structured, validated output.
- All generated recommendations include confidence + source refs.

### Exit criteria

- Agent tasks execute through orchestration with validated outputs and audit logs.

## Step 8 - Test Asset Pipeline and Playwright Hybrid Framework

### What to implement

1. Scenario schema and compiler to executable assets.
2. Page/flow/assertion abstraction layers.
3. Runtime adapters:
- retrieval adapter
- context pack consumer
- state map adapter
4. Metadata traceability in generated scripts.

### Environment setup

- Install Playwright browsers.
- Configure `AI_QA_EXECUTION_BACKEND=playwright` for integration tests.

### How to test

- Unit tests for compiler and assertion generation.
- API tests for script generation/bootstrap endpoints.
- Smoke run on sample generated suites.

### Test cases

- `TC-S8-001`: scenario compiles to valid Playwright spec.
- `TC-S8-002`: generated script includes source and state refs metadata.
- `TC-S8-003`: semantic assertions compile to runtime-level assertions.
- `TC-S8-004`: selector profile review promotes approved profile only.

### Test data

- Scenarios produced from login and registration datasets.
- selector profile fixtures with approved/unapproved states.

### Assertion standards

- Generated code must be syntactically valid and deterministic for regression mode.
- No hardcoded sleep-based waits in approved regression assets.

### Exit criteria

- Generated assets run successfully in at least one stable smoke scenario.

## Step 9 - Execution, Evidence, and State Management

### What to implement

1. Execution service orchestration of web/API runners.
2. State management hooks (setup/cleanup/reset).
3. Evidence service:
- screenshot, trace, logs, DOM, request/response snapshots
- evidence summaries and bundles
4. Immutable evidence finalization and retrieval references.

### Environment setup

- Local-dev for simulated execution.
- Integration profile for Playwright + API execution.

### How to test

- Execution integration tests from run creation to result persistence.
- Evidence integrity tests (hash/checksum, immutable finalization).
- State cleanup tests.

### Test cases

- `TC-S9-001`: run executes selected scenarios and persists run steps.
- `TC-S9-002`: failure captures mandatory evidence set.
- `TC-S9-003`: cleanup hook runs even when test fails.
- `TC-S9-004`: evidence bundle generated for triage consumption.

### Test data

- Executable login scenarios.
- Simulated failure scenarios (selector missing, API 500, auth expired).

### Assertion standards

- Every failed step has at least one evidence ref.
- Finalized evidence blobs are immutable.
- Secrets masked in logs and snapshots.

### Exit criteria

- End-to-end run produces traceable run -> step -> evidence linkage.

## Step 10 - Triage, Defect Drafting, HITL

### What to implement

1. Failure classification engine.
2. Confidence scoring + reason generation.
3. Defect draft packet generation with evidence attachments.
4. Human review decision workflow and policy gating.

### Environment setup

- Local-dev with synthetic failure corpus.
- Optional integration with external trackers behind disabled-by-default flags.

### How to test

- Classification unit tests.
- Defect draft API tests.
- HITL workflow tests (approve/reject/reclassify).

### Test cases

- `TC-S10-001`: product defect classification on repeated clean-state failures.
- `TC-S10-002`: test script issue classification for locator break.
- `TC-S10-003`: confidence below threshold creates review task.
- `TC-S10-004`: approved review transitions draft to publish-ready internal state.

### Test data

- Failure bundles labeled by category.
- Historical known defects for similarity linking.

### Assertion standards

- Every triage result includes decision, confidence, reason, evidence refs.
- No auto-submission to external systems in current stage unless explicitly enabled by policy.

### Exit criteria

- Triage and defect drafting flow is reproducible and reviewable end-to-end.

## Step 11 - Healing and Deterministic Playbook Promotion

### What to implement

1. Forensic healing analysis pipeline.
2. Healing event and log persistence.
3. Controlled promotion from diagnostic discoveries to deterministic playbooks.
4. Regression mode enforcement of approved playbooks only.

### Environment setup

- Requires historical execution/evidence fixtures.
- Enable diagnostic mode datasets.

### How to test

- Healing proposal generation tests.
- Playbook promotion/approval tests.
- Regression replay tests using promoted playbooks.

### Test cases

- `TC-S11-001`: healing suggests alternative locator with confidence and rationale.
- `TC-S11-002`: unapproved healing is excluded from regression execution.
- `TC-S11-003`: approved playbook improves run stability versus baseline.
- `TC-S11-004`: healing history retrievable by scenario and state.

### Test data

- Selector drift snapshots across versions.
- Past failed and recovered execution runs.

### Assertion standards

- Healing never silently mutates approved assets.
- Promotion requires explicit approval metadata and provenance.

### Exit criteria

- Diagnostic discoveries can be safely hardened into deterministic regression assets.

## Step 12 - Operational Hardening, SLOs, and Shift-Left

### What to implement

1. Pre-commit and optional watch-mode trigger path.
2. Observability dashboards for:
- workflow duration
- failure class distribution
- flaky selector hotspots
- retrieval quality metrics
3. Retention and cleanup jobs for heavy artifacts.
4. CI quality gates and release checklist.

### Environment setup

- CI profile with isolated storage.
- Add pre-commit hooks and pipeline tasks.

### How to test

- CI pipeline tests.
- SLO alert simulation tests.
- retention job integration tests.

### Test cases

- `TC-S12-001`: pre-commit trigger runs mapped smoke checks.
- `TC-S12-002`: SLO breach emits alert signal/event.
- `TC-S12-003`: retention job tiers old traces but keeps metadata.
- `TC-S12-004`: release blocked when critical contract tests fail.

### Test data

- Synthetic long-history run/evidence metadata.
- simulated CI artifacts.

### Assertion standards

- Operational controls are policy-driven and auditable.
- No cleanup job may delete metadata needed for traceability.

### Exit criteria

- Production-minded MVP is operable with measurable quality gates.

## 6. Test Suite Matrix (Recommended)

1. `tests/unit`
- pure service logic
- parsers/classifiers/scorers

2. `tests/contract`
- API/MCP/agent envelope schemas

3. `tests/integration`
- DB + storage + vector + service boundaries

4. `tests/e2e`
- request -> retrieval -> authoring -> execution -> triage -> review

5. `tests/nonfunctional`
- determinism replay
- load and latency
- retention correctness

## 7. CI/CD Quality Gates

Minimum gates per merge:

1. All unit + contract + integration tests pass.
2. No critical schema drift.
3. Determinism replay suite passes for regression mode.
4. Security checks pass:
- secret masking checks
- policy boundary tests
5. Evidence and traceability completeness threshold met.

## 8. Definition of Done for Production-Minded MVP

MVP is complete only when:

1. End-to-end workflow is functional across all core phases.
2. Every run has requirement/test/evidence/decision traceability.
3. Regression mode behavior is deterministic and policy-safe.
4. HITL decisions are auditable and replayable.
5. Synthetic datasets cover happy path, negative path, and flaky/stability path.
6. CI gates enforce contract integrity and determinism.

## 9. Immediate Next Sprint Plan (First 2 Weeks)

Week 1:

1. Step 0 (spec lock)
2. Step 1 (backbone)
3. Step 2 (persistence baseline)

Week 2:

1. Step 3 (MCP core set)
2. Step 4 (distributed understanding)
3. Step 5 (state + mismatch)

Planned sprint demo artifacts:

1. one successful request flow from intake to indexed understanding
2. one mismatched case showing execution block + review signal
3. one traceable audit trail for the full flow

