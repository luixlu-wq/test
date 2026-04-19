# STORY-009 Agent Runtime And Prompt Governance

## Type

story

## Description

Implement agent runtime orchestration with strict prompt/version governance and structured output validation.

## Scope

- agent execution harness
- prompt registry and version tracking
- output schema validation and fallback handling
- fact vs inference and policy guardrails

## Dependencies

- `STORY-008-graph-rag-foundation.md`

## Sprint Candidate

- Sprint 3

## Story Points

8

## Technical Context

- **Agent roster**: `agent prompts design.md` §2 — 11 agents; all use `claude-sonnet-4-6` by default; `claude-opus-4-6` requires documented justification; `claude-haiku-4-5-20251001` forbidden for triage, healing, defect, playbook agents
- **Prompt registry**: `agent prompts design.md` §18 — semantic versioning (MAJOR.MINOR.PATCH); files at `api/prompts/<agent-name>/v1.0.0.txt`; `registry.yaml` with `production` and `staging` version pointers; promotion requires 80% golden-set pass for MINOR, full manual review for MAJOR
- **Structured output validation**: every agent output validated against its JSON schema before consumption; `OUTPUT_SCHEMA_VALIDATION_ERROR` raised on failure; fallback to `AGENT_PARSE_FAILED` with original raw output preserved for diagnostics
- **Fact vs inference labelling**: `agent prompts design.md` §5 — agent outputs must label each claim as `fact` (grounded in source chunk) or `inference` (agent-derived); `ungrounded_inference` flag triggers review gate
- **Policy guardrails**: actions tagged `policy_restricted` in agent output cannot be auto-executed; require `approval_task` creation (feeds into STORY-003 TASK-005)
- **Prompt metadata storage**: `agent prompts design.md` §18 — `promptVersion`, `modelId`, `agentId`, `outputSchemaVersion` stored with every persisted agent output in DB
- **Token budget**: `RAG implementation design.md` §17.2 — per-agent overrides for RAG envelope; agent runtime passes the appropriate token budget to the context pack builder

## Acceptance Criteria

1. Agent output is schema-validated before any downstream consumption; an output that fails schema validation is quarantined with `OUTPUT_SCHEMA_VALIDATION_ERROR` and does not proceed to the next pipeline stage.
2. Prompt metadata (`promptVersion`, `modelId`, `agentId`) is stored alongside every agent output persisted to the DB; missing metadata fields cause the persist to fail with a clear error.
3. Policy-restricted behaviors in agent output are blocked from auto-execution; the blocked action triggers an `approval_task` with the agent output `id` as context.

## Test Cases

- `TC-S7-001` — Invalid agent output schema triggers quarantine; valid output passes and metadata is persisted
- `TC-S7-002` — Prompt metadata stored with agent output; query by `promptVersion` returns correct records
- `TC-S7-003` — Policy-restricted action in agent output creates `approval_task`; action not executed
- `TC-S7-004` — `ungrounded_inference` flag in agent output triggers review gate

## Definition of Done

- [ ] Agent execution harness wraps all 11 agents with prompt registry lookup + output validation
- [ ] Prompt registry implemented; `registry.yaml` parsed at startup
- [ ] Output schema validation runs before any downstream consumption
- [ ] Prompt metadata stored with every persisted output
- [ ] Policy guardrail fires on `policy_restricted` actions
- [ ] `TC-S7-001` through `TC-S7-004` pass; LLM calls stubbed in `ci` profile
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
