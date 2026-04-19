# STORY-001 Contract And Enum Lock

## Type

story

## Description

Create and lock canonical contract schemas, enum definitions, and version metadata used by MCP, agents, workflow records, and events.

## Scope

- Shared schema package in source.
- Canonical `execution_mode` and status enums.
- Schema fixtures for valid/invalid payload tests.
- Step-0 TDR registry and required decision records.

## Dependencies

- `EPIC-001-spec-and-backbone.md`

## Sprint Candidate

- Sprint 1

## Story Points

5

## Technical Context

- **MCP envelope schema**: `MCP contract implementation.md` §4 (request/response/error envelope fields, `mcpVersion`, `requestId`, `policyContext`)
- **Execution mode enum**: `data model design.md` §17.1 — values: `diagnostic`, `regression`, `draft`
- **Lifecycle status enums**: `data model design.md` §6/§10/§12 — request/workflow/stage/run lifecycle values are canonicalized in shared constants
- **Schema versioning**: `MCP contract implementation.md` §23 — semantic versioning rules; version stored in `api/mcp/registry.yaml`
- **Agent output envelopes**: `agent prompts design.md` §18 — prompt version + model ID must accompany every agent output persisted to DB
- **Event envelope**: `MCP contract implementation.md` §4 — all MCPs share the same base envelope; contract tests use `api/tests/data/contracts/`

## Acceptance Criteria

1. Canonical enums (`ExecutionMode`, `WorkflowStatus`, `StageStatus`, `RunStatus`, `ArtifactType`, `MismatchSeverity`) defined once in a shared constants module; no duplicate literal definitions remain anywhere in the codebase.
2. Contract fixture files in `api/tests/data/contracts/` cover at minimum: valid MCP request envelope, invalid envelope (missing required field), valid agent output envelope, invalid agent output (wrong type on required field). Each fixture is validated by the schema helper.
3. Schema version metadata (`schemaVersion`) field is present in every MCP request and response envelope fixture and is validated by the contract test suite.
4. Step-0 required TDRs (`TDR-001` to `TDR-010`) exist in `api/doc/tdr/` and are referenced by this story.

## Test Cases

- `TC-S0-001` — Valid MCP request envelope passes schema validation
- `TC-S0-002` — Invalid envelope (missing `requestId`) fails with `SCHEMA_VALIDATION_ERROR`
- `TC-S0-003` — `ExecutionMode` and `WorkflowStatus` constants imported from shared module in at least 3 downstream files
- `TCN-S0-001` — Envelope with malformed timestamp fails strict schema validation
- `TCN-S0-002` — Unknown critical envelope field rejected in strict mode
- `TCE-S0-001` — Repeated validation of same fixture is deterministic

## Definition of Done

- [ ] Shared constants module exists and imports cleanly with no circular dependencies
- [ ] All acceptance criteria pass with automated tests
- [ ] `TC-S0-001`, `TC-S0-002`, `TC-S0-003` pass in `ci` profile (no external calls)
- [ ] `TCN-S0-001`, `TCN-S0-002`, `TCE-S0-001` pass in `ci` profile
- [ ] No duplicate enum literals remain (grep passes `AI_QA_ENUM_AUDIT`)
- [ ] Schema fixture directory committed at `api/tests/data/contracts/`
- [ ] TDR files `TDR-001` through `TDR-010` committed under `api/doc/tdr/`
- [ ] PR reviewed and merged; CI green on all four stages

## Owner

TBD

## Status

todo
