# TASK-012 Trigger MCP

## Type

task

## Description

Implement trigger MCP to support manual, webhook, and shift-left initiation patterns.

## Scope

- trigger envelope ingestion
- orchestration enqueue integration

## Dependencies

- `STORY-005-mcp-core-set.md`

## Story Link

- `STORY-005-mcp-core-set.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 2

## Story Points

2

## Technical Context

- **Operation**: `trigger.dispatch(trigger_type, case_ref, params, requested_by)` — `MCP contract implementation.md` §8
- **Trigger types**: `manual` (UI/API direct), `webhook` (CI/CD push event), `shift_left` (pre-commit hook); each type has a required param subset validated by the envelope schema
- **Enqueue target**: Redis Streams stream `workflow.trigger`; message includes full trigger envelope + `requestId` for dedup linkage with TASK-003
- **Dedup linkage**: `trigger.dispatch` does NOT compute the dedup key itself — it passes the trigger payload to the intake service (STORY-002) which calls `compute_dedup_key`; trigger MCP is fire-and-return-acknowledgement
- **Response**: `{status: "accepted", workflow_id: null, event_id: "<redis_stream_id>"}` — `workflow_id` populated later by orchestration; trigger MCP returns `event_id` for traceability
- **Timeout**: 10 seconds — `MCP contract implementation.md` §4.8
- **Shift-left constraint**: `shift_left` trigger type only permitted in `local-dev` and `integration` profiles; blocked with `POLICY_VIOLATION` in PROD

## Acceptance Criteria

1. Trigger payload validation enforced: missing required fields for the specified `trigger_type` return `SCHEMA_VALIDATION_ERROR` with the field path.
2. Valid trigger dispatch emits a message to Redis Streams `workflow.trigger` stream and returns `{status: "accepted", event_id: "..."}` with the Redis stream message ID.

## Test Cases

- `TC-S3-004` — Valid trigger validated and enqueued; invalid payload returns `SCHEMA_VALIDATION_ERROR`

## Definition of Done

- [ ] `trigger.dispatch` validates per-trigger-type required params
- [ ] Redis Streams publish verified in integration test
- [ ] `shift_left` trigger blocked in PROD profile
- [ ] `TC-S3-004` passes in `integration` profile
- [ ] In `ci` profile: Redis stubbed; validation logic tested without external calls

## Owner

TBD

## Status

todo
