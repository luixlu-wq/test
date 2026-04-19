# TASK-001 Schema Package And Fixtures

## Type

task

## Description

Create shared schema module and valid/invalid fixture payloads for MCP, agent, and event envelopes.

## Scope

- schema module under source tree
- fixture sets under `api/tests/data/contracts/`
- helper validators for tests

## Dependencies

- `STORY-001-contract-and-enum-lock.md`

## Story Link

- `STORY-001-contract-and-enum-lock.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

3

## Technical Context

- **Schema package location**: `api/ai_qa_tester/schemas/` — one module per envelope family (mcp, agent, event)
- **MCP envelope fields**: `MCP contract implementation.md` §4.1 — `mcpVersion`, `requestId`, `operation`, `params`, `policyContext`; response adds `result`, `errorCode`, `retryable`
- **Agent output envelope**: `agent prompts design.md` §18 — requires `promptVersion`, `modelId`, `agentId`, `outputSchemaVersion` alongside the structured payload
- **Fixture format**: JSON files; one `valid_*.json` and one `invalid_*.json` per envelope type minimum
- **Validator helper**: wraps `jsonschema.validate()`; used by all contract tests; raises `ContractValidationError` with field path on failure
- **CI profile constraint**: `AI_QA_LLM_STUB_MODE=true`, `AI_QA_SKIP_EXTERNAL_CALLS=true` — no live API calls; fixtures must be fully synthetic

## Acceptance Criteria

1. Fixture files exist for all required envelope types (MCP request, MCP response, MCP error, agent output) with at least one valid and one invalid variant each; the invalid variant triggers schema validation failure on the specific required field removed.
2. `validate_contract(fixture_path, schema_name)` helper callable from any test file; returns `True` on success, raises `ContractValidationError(field=..., message=...)` on failure.

## Test Cases

- `TC-S0-001` — Valid MCP request envelope fixture passes `validate_contract`
- `TC-S0-002` — MCP envelope fixture with missing `requestId` raises `ContractValidationError` pointing to `requestId`

## Definition of Done

- [ ] Schema module importable as `from ai_qa_tester.schemas import mcp, agent, event`
- [ ] All fixture files committed under `api/tests/data/contracts/`
- [ ] `validate_contract` helper covered by unit tests
- [ ] `TC-S0-001` and `TC-S0-002` pass in `ci` profile
- [ ] No hardcoded schema field names outside the schema module

## Owner

TBD

## Status

todo
