# TASK-006 Audit Correlation Logging

## Type

task

## Description

Implement audit logging with request/run/task/tool correlation IDs.

## Scope

- audit event model
- stage and tool invocation log hooks
- query helpers

## Dependencies

- `STORY-003-policy-and-audit-foundation.md`

## Story Link

- `STORY-003-policy-and-audit-foundation.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

2

## Technical Context

- **Audit log table**: `data model design.md` §24 — `audit_log(id, correlation_id, request_id, run_id, action, actor, before_state JSON, after_state JSON, timestamp)`; never hard-deleted
- **Correlation ID source**: `X-Correlation-ID` HTTP header; if absent on inbound request, generate `uuid4()` and attach to response; propagated to all downstream service calls as the same header
- **Hook points**: stage transition (TASK-004), MCP invocation (every `mcp.call()` wrapper), policy decision (TASK-005), approval task state change
- **Write isolation**: audit write must succeed even if the audited action's transaction rolls back — use a separate DB session/connection for audit writes; do NOT wrap in the same transaction
- **Indexes required**: `audit_log(correlation_id)`, `audit_log(request_id)`, `audit_log(run_id)` — see `data model design.md` §35 indexing strategy
- **Query helper**: `AuditLogQuery.by_correlation(correlation_id, limit=100)` returns records in `timestamp ASC` order

## Acceptance Criteria

1. Every workflow stage transition and MCP tool invocation produces an `audit_log` row with a non-null `correlation_id` matching the originating request's `X-Correlation-ID`.
2. `AuditLogQuery.by_correlation(id)` returns correct records in under 200ms for datasets of 10,000+ rows (index must exist).

## Test Cases

- `TC-S1-004` — Stage transition emits audit log; `by_correlation()` returns the row with correct `before_state` / `after_state`
- `TCN-S1-004` — Invalid/failed action path still emits auditable row with correlation ID
- `TCE-S1-004` — Duplicate idempotent event does not produce duplicate audit records while preserving replay traceability

## Definition of Done

- [ ] `audit_log` table migration included in core migration pack (TASK-007)
- [ ] Audit write uses isolated DB session (not wrapped in audited action transaction)
- [ ] Hook registered for: stage transitions, MCP calls, policy decisions, approval state changes
- [ ] Correlation ID middleware generates UUID if header absent and attaches to response
- [ ] `TC-S1-004`, `TCN-S1-004`, `TCE-S1-004` pass in `integration` profile
- [ ] Index existence verified by migration smoke test

## Owner

TBD

## Status

todo
