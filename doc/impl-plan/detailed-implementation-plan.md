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
- `api/doc/impl-design/agent prompts design.md`

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

### 2.5 Required environment variables — integration profile

```bash
AI_QA_ENVIRONMENT=integration
AI_QA_REPOSITORY_BACKEND=sqlalchemy
AI_QA_DATABASE_URL=postgresql+asyncpg://qa_user:qa_pass@localhost:5432/ai_qa_tester
AI_QA_BLOB_BACKEND=s3
AI_QA_BLOB_BUCKET=ai-qa-tester-integration
AI_QA_BLOB_ENDPOINT=http://localhost:9000        # localstack or minio
AI_QA_VECTOR_BACKEND=qdrant
AI_QA_QDRANT_URL=http://localhost:6333
AI_QA_QDRANT_COLLECTION=ai_qa_tester_integration
AI_QA_EVENT_BUS_BACKEND=redis
AI_QA_REDIS_URL=redis://localhost:6379/0
AI_QA_EXECUTION_BACKEND=playwright
AI_QA_PLAYWRIGHT_WORK_ROOT=./.local/playwright_runs
AI_QA_NEO4J_URL=bolt://localhost:7687
AI_QA_NEO4J_USER=neo4j
AI_QA_NEO4J_PASSWORD=neo4j_pass
AI_QA_EMBEDDING_MODEL=voyage-3-large
AI_QA_VOYAGE_API_KEY=<resolved from secrets manager at runtime>
AI_QA_ANTHROPIC_API_KEY=<resolved from secrets manager at runtime>
```

### 2.6 Required environment variables — CI profile

```bash
AI_QA_ENVIRONMENT=ci
AI_QA_REPOSITORY_BACKEND=sqlalchemy
AI_QA_DATABASE_URL=postgresql+asyncpg://qa_user:qa_pass@localhost:5432/ai_qa_tester_ci
AI_QA_BLOB_BACKEND=local
AI_QA_BLOB_ROOT=/tmp/ai_qa_ci_blobs
AI_QA_VECTOR_BACKEND=local
AI_QA_VECTOR_STORE_PATH=/tmp/ai_qa_ci_vectors.json
AI_QA_EVENT_BUS_BACKEND=memory
AI_QA_EXECUTION_BACKEND=simulated
AI_QA_NEO4J_URL=bolt://localhost:7687
AI_QA_NEO4J_USER=neo4j
AI_QA_NEO4J_PASSWORD=neo4j_ci
AI_QA_EMBEDDING_MODEL=voyage-3-large
AI_QA_VOYAGE_API_KEY=<CI secrets; never committed>
AI_QA_ANTHROPIC_API_KEY=<CI secrets; never committed>
AI_QA_LLM_STUB_MODE=true           # stubs LLM calls in unit/contract/integration tests
AI_QA_SKIP_EXTERNAL_CALLS=true     # blocks any real outbound network in CI
```

CI must never reach external APIs except in explicitly tagged integration test jobs. `AI_QA_LLM_STUB_MODE=true` and `AI_QA_SKIP_EXTERNAL_CALLS=true` are mandatory for all test types except the designated integration test job.

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

## Step 0 - Spec Lock, TDRs, and Delivery Guardrails

### What to implement

1. **Technology Decision Records (TDRs)** — one record per committed technology choice. These are the foundational decisions that every subsequent step depends on. TDRs must be created and merged before Step 1 begins.

   Required TDRs (stored under `api/doc/tdr/`):

   | TDR ID   | Decision                                                    | Rationale reference                          |
   | -------- | ----------------------------------------------------------- | -------------------------------------------- |
   | TDR-001  | PostgreSQL 15+ as the relational store (system of record)  | Arch doc Section 29 — Platform Technology Profile |
   | TDR-002  | Neo4j as the graph store                                   | Arch doc Section 29; KG schema design Section 16 |
   | TDR-003  | Qdrant as the primary vector store; pgvector as fallback   | Arch doc Section 29; RAG design Section 11.3 |
   | TDR-004  | Redis Streams as the event bus                             | Arch doc Section 29 |
   | TDR-005  | `voyage-3-large` as the embedding model                    | RAG design Section 11.3 |
   | TDR-006  | Claude API (`claude-sonnet-4-6` default) as the LLM        | Arch doc Section 29; Agent prompts design Section 17 |
   | TDR-007  | Claude Vision + Tesseract OCR for visual extraction        | Arch doc Section 29; RAG design Section 9.6 |
   | TDR-008  | S3-compatible object store for evidence and artifacts      | Arch doc Section 29 |
   | TDR-009  | Transactional Outbox for cross-store consistency           | Service design Section 7.4 |
   | TDR-010  | Choreography-based Saga for multi-stage workflow compensation | Service design Section 7.4 |

   Each TDR must contain: decision statement, context, alternatives considered, consequences, and date of decision.

2. Canonical enum definitions:
   - `execution_mode` (`draft`, `diagnostic`, `regression`) as single source of truth.
   - lifecycle statuses for request/run/asset/approval.
3. Common envelopes for:
   - MCP request/response/error
   - agent input/output
   - event bus messages
4. Cross-doc alignment checklist and version stamp.

### Environment setup

- Local-dev profile only.
- Add `api/doc/tdr/` for Technology Decision Records.
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

## 6. Step Effort Estimates

Estimates use story points on the Fibonacci scale (1, 2, 3, 5, 8, 13). One point ≈ half a day of focused implementation work for a single engineer. These are complexity estimates, not time guarantees.

| Step | Title                                          | Points | Key complexity driver                                                 |
| ---- | ---------------------------------------------- | ------ | --------------------------------------------------------------------- |
| 0    | Spec Lock, TDRs, and Delivery Guardrails       | 5      | TDR documentation + enum/envelope schema authoring + validation tests |
| 1    | Platform Backbone                              | 13     | Orchestration state machine + idempotency + policy service + audit    |
| 2    | Data Model and Persistence Foundation          | 8      | Migration set + repository abstraction + PostgreSQL integration        |
| 3    | MCP Core Set                                   | 8      | Four MCPs + shared envelope middleware + policy constraints            |
| 4    | Distributed Understanding Pipeline             | 13     | Artifact normalization + fusion + chunking + metadata enrichment       |
| 5    | Semantic State and Mismatch Detection          | 8      | State map generator + mismatch classifier + severity gates            |
| 6    | Graph-RAG Foundation                           | 13     | Hybrid index + graph linking + context pack builder + retrieval logs  |
| 7    | Agent Runtime and Prompt Governance            | 8      | Prompt registry + structured output validation + guardrails           |
| 8    | Test Asset Pipeline and Playwright Framework   | 8      | Scenario compiler + abstraction layers + generated asset traceability |
| 9    | Execution, Evidence, and State Management      | 8      | Execution orchestration + evidence finalization + state setup/cleanup |
| 10   | Triage, Defect Drafting, HITL                  | 8      | Classification engine + defect packet + approval workflow             |
| 11   | Healing and Deterministic Playbook Promotion   | 8      | Forensic scan + fingerprint comparison + promotion governance         |
| 12   | Operational Hardening, SLOs, Shift-Left        | 5      | Pre-commit hook + observability + retention + CI gates                |
|      | **Total**                                      | **113**| ≈ 57 engineer-days (11–12 weeks solo; 5–6 weeks with 2 engineers)    |

### Sprint allocation guidance

| Sprint | Steps         | Points | Goal                                              |
| ------ | ------------- | ------ | ------------------------------------------------- |
| 1      | 0, 1, 2       | 26     | Contracts locked, backbone running, DB migrated   |
| 2      | 3, 4, 5       | 29     | Ingestion → understanding → state map → mismatch  |
| 3      | 6, 7          | 21     | Graph-RAG + agent runtime operational             |
| 4      | 8, 9          | 16     | Test assets generated and executed                |
| 5      | 10, 11        | 16     | Triage, defects, healing, playbooks               |
| 6      | 12            | 5      | Hardening, SLOs, shift-left, production readiness |

These estimates assume a single experienced full-stack engineer. Add 20% buffer per sprint for integration surprises, environment setup overhead, and review cycles.

## 7. Test Suite Matrix (Recommended)

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

## 8. CI/CD Pipeline

### 8.1 Pipeline structure

The CI/CD pipeline has four stages executed in order. Stages are independent within their tier; a stage failure stops the pipeline.

```
┌─────────────────────────────────────────────────────────────┐
│ Stage 1 — Fast checks (< 3 min)                             │
│   lint + type check                                         │
│   unit tests (AI_QA_LLM_STUB_MODE=true)                    │
│   contract schema tests                                     │
│   secret-masking checks                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │ pass
┌───────────────────────▼─────────────────────────────────────┐
│ Stage 2 — Integration tests (< 10 min)                      │
│   DB migration smoke (PostgreSQL ephemeral)                  │
│   repository roundtrip tests                                │
│   MCP contract tests (stubs for external services)         │
│   policy boundary tests                                     │
│   retrieval + graph expansion tests (local vector/Neo4j)   │
└───────────────────────┬─────────────────────────────────────┘
                        │ pass
┌───────────────────────▼─────────────────────────────────────┐
│ Stage 3 — Determinism and regression gates (< 8 min)        │
│   determinism replay suite (same input → same output)       │
│   regression mode enforcement tests                         │
│   context pack bounds tests                                 │
│   evidence traceability completeness assertions             │
└───────────────────────┬─────────────────────────────────────┘
                        │ pass
┌───────────────────────▼─────────────────────────────────────┐
│ Stage 4 — Deploy (on main branch only)                      │
│   build Docker images                                       │
│   push to registry                                          │
│   deploy to integration environment                         │
│   smoke test against integration environment                │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Trigger conditions

| Event                         | Stages run         | Notes                                         |
| ----------------------------- | ------------------ | --------------------------------------------- |
| Pull request opened / updated | Stages 1, 2, 3     | No deploy; all gates must pass for merge      |
| Push to `main`                | Stages 1, 2, 3, 4  | Full pipeline including deploy                |
| Nightly scheduled run         | Stages 1, 2, 3, 4  | Full integration + smoke against live env     |
| Manual trigger                | Configurable       | Any stage subset can be triggered manually    |

### 8.3 Tooling

| Concern            | Tool                                                       |
| ------------------ | ---------------------------------------------------------- |
| Pipeline runner    | GitHub Actions (primary); adaptable to GitLab CI          |
| Test runner        | `pytest` with `pytest-asyncio` for async service tests    |
| Linting            | `ruff` (Python); `mypy` for type checks                   |
| Secret scanning    | `detect-secrets` pre-commit hook + CI scan step           |
| DB migrations      | Alembic; ephemeral PostgreSQL via Docker service in CI    |
| Graph store in CI  | Neo4j via Docker service (`neo4j:5-community`)            |
| Coverage reporting | `pytest-cov`; fail if coverage drops below 70% on new code|
| Contract validation| JSON Schema via `jsonschema` library                      |

### 8.4 Minimum gates per merge (PR blocking)

All of the following must be green before a PR can merge to `main`:

1. All unit + contract tests pass with `AI_QA_LLM_STUB_MODE=true`.
2. All integration tests pass (PostgreSQL ephemeral, local vector, Neo4j Docker).
3. No schema drift — JSON schema contract tests must pass 100%.
4. Determinism replay suite passes — same context pack + same prompt version → structurally equivalent output.
5. Regression mode enforcement tests pass — no exploratory recommendation leaks into regression mode outputs.
6. Secret masking checks pass — no credential patterns in logs or output fixtures.
7. Policy boundary tests pass — policy violations fail closed, not open.
8. Code coverage does not drop below 70% on modified files.

### 8.5 Release checklist (before Stage 4 deploy)

- [ ] All merge gates green on `main`.
- [ ] TDR registry (`api/doc/tdr/`) has no unresolved items.
- [ ] `api/prompts/registry.yaml` production pointers reviewed.
- [ ] `api/mcp/registry.yaml` MCP versions reviewed.
- [ ] DB migration scripts reviewed and tested up/down.
- [ ] Environment variables checklist (sections 2.4, 2.5, 2.6) confirmed for target environment.
- [ ] No known blocking mismatch warnings in the active sprint's test cases.
- [ ] Smoke test against integration environment passes.

## 9. Definition of Done for Production-Minded MVP

MVP is complete only when:

1. End-to-end workflow is functional across all core phases.
2. Every run has requirement/test/evidence/decision traceability.
3. Regression mode behavior is deterministic and policy-safe.
4. HITL decisions are auditable and replayable.
5. Synthetic datasets cover happy path, negative path, and flaky/stability path.
6. CI gates enforce contract integrity and determinism.

## 10. Immediate Next Sprint Plan (First 2 Weeks)

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

