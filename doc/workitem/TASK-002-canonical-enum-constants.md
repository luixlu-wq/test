# TASK-002 Canonical Enum Constants

## Type

task

## Description

Define and apply canonical constants for execution mode and major lifecycle status enums.

## Scope

- constants module
- replacement of duplicated literals in services/tests

## Dependencies

- `TASK-001-schema-package-and-fixtures.md`

## Story Link

- `STORY-001-contract-and-enum-lock.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

2

## Technical Context

- **ExecutionMode values**: `data model design.md` §17.1 — `diagnostic` (agentic exploration, PROD-blocked), `regression` (deterministic replay), `draft` (pre-dispatch; must not be picked up by Execution Service until `status = pending`)
- **WorkflowStatus / StageStatus / RunStatus**: `data model design.md` §6 — lifecycle columns on `test_workflow`, `workflow_stage`, `test_run` tables
- **MismatchSeverity**: `knowledge graph schema design.md` §7.6 — `blocking`, `warning`, `info`
- **ArtifactType**: `data model design.md` §5 — `spec`, `design`, `requirement`, `screenshot`, `har`, `log`, `playbook`
- **Constants module**: `api/ai_qa_tester/constants/enums.py` — Python `StrEnum` (or plain string constants) so values are JSON-serialisable without `.value` access
- **Audit rule**: after this task, a CI lint check should grep for inline string literals matching enum values and fail the build if found outside the constants module

## Acceptance Criteria

1. All enum definitions consolidated in `api/ai_qa_tester/constants/enums.py`; no conflicting or duplicate definitions remain in service or test files (verified by grep in CI).
2. All test files that previously used raw string literals for status/mode values now import from the constants module.

## Test Cases

- `TC-S0-002` — CI grep audit finds zero enum literals outside constants module
- `TCN-S0-003` — Unknown enum literal in fixture is rejected by schema validator
- `TCE-S0-002` — Enum serialization/deserialization is deterministic across repeated runs

## Definition of Done

- [ ] `enums.py` defines `ExecutionMode`, `WorkflowStatus`, `StageStatus`, `RunStatus`, `ArtifactType`, `MismatchSeverity`
- [ ] All service and test files updated to import from constants module
- [ ] Grep-based CI audit step passes (no stray literals)
- [ ] `TC-S0-002`, `TCN-S0-003`, `TCE-S0-002` pass in `ci` profile

## Owner

TBD

## Status

todo
