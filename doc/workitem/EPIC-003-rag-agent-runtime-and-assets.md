# EPIC-003 RAG Agent Runtime And Assets

## Type

epic

## Description

Deliver Graph-RAG foundation, context pack building, agent runtime governance, and scenario-to-asset compiler for deterministic executable outputs.

## Scope

- Step 6, Step 7, Step 8 from implementation plan.
- Hybrid retrieval + graph expansion + context packs.
- Agent runtime with schema-validated structured outputs.
- Prompt versioning and guardrails.
- Test asset generation and Playwright compilation.

## Dependencies

- `EPIC-002-mcp-understanding-and-state.md`

## Acceptance Criteria

1. Retrieval returns bounded context packs with trace refs.
2. Agent outputs are schema-validated and audit-logged.
3. Scenario compiler generates runnable assets with metadata.
4. Regression-safe generated assets avoid uncontrolled runtime behavior.
5. Context-pack budgeting follows mode-specific limits from implementation plan baselines.
6. Negative and edge paths are validated for index readiness, invalid filters, grounding failures, and bounded compiler behavior.

## Test Cases

- `TC-S6-001`, `TC-S6-002`, `TC-S6-003`, `TC-S6-004`
- `TCN-S6-001`, `TCN-S6-002`, `TCE-S6-001`
- `TC-S7-001`, `TC-S7-002`, `TC-S7-003`, `TC-S7-004`
- `TCN-S7-001`, `TCN-S7-002`, `TCE-S7-001`
- `TC-S8-001`, `TC-S8-002`, `TC-S8-003`, `TC-S8-004`
- `TCN-S8-001`, `TCN-S8-002`, `TCE-S8-001`

## Owner

TBD

## Status

todo
