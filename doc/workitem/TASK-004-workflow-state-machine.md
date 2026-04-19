# TASK-004 Workflow State Machine

## Type

task

## Description

Implement workflow stage state machine with retry safety and resumable execution.

## Scope

- stage transition model
- retry semantics
- resume from persisted state

## Dependencies

- `TASK-003-request-dedup-key.md`

## Story Link

- `STORY-002-request-trigger-orchestration.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

5

## Technical Context

- **Stage status values**: `data model design.md` §10 — `pending`, `running`, `done`, `failed`, `skipped`
- **Allowed transitions**:
  - `pending → running` (stage dispatch)
  - `running → done` (success)
  - `running → failed` (error, `attempt_count < 3`)
  - `failed → pending` (retry trigger; increments `attempt_count`)
  - `running → skipped` (policy gate blocks stage)
  - Blocked: `done → *`, `skipped → *`, `failed → *` when `attempt_count >= 3`
- **Idempotency rule**: transitioning to the current status (e.g. `running → running`) is a no-op that returns the existing row; it does NOT raise an error or increment counters
- **Saga compensation**: `detailed-implementation-plan.md` TDR-010 — on `failed` with `attempt_count >= 3`, emit `workflow.stage.compensation_required` event; downstream handler rolls back partial work
- **Resume semantics**: on server restart, stages with `status = running` and `started_at < NOW() - timeout_threshold` are reset to `pending` by the worker heartbeat process; `attempt_count` is NOT incremented by the reset
- **Audit trail**: every transition writes an `audit_log` row with `action = stage_transition`, `before_status`, `after_status`, `correlation_id`

## Acceptance Criteria

1. All invalid transitions (e.g. `done → running`, `skipped → pending`) are blocked and return a `INVALID_TRANSITION` error with the attempted transition in the error payload.
2. Retrying a stage that already transitioned to `running` (same `attempt_count`) is a no-op; the stage record is returned unchanged and no duplicate side-effects are triggered.

## Test Cases

- `TC-S1-002` — Invalid transition attempt is rejected; valid retry path is idempotent and does not duplicate side-effects

## Definition of Done

- [ ] `StageStateMachine.transition(stage_id, new_status)` implemented with all allowed/blocked transitions
- [ ] Idempotent re-transition returns existing record without error
- [ ] `attempt_count` incremented only on `failed → pending` (retry); not on server restart reset
- [ ] Audit log row written on every non-idempotent transition
- [ ] `TC-S1-002` passes in `integration` profile
- [ ] Unit tests cover all transition edges in `ci` profile

## Owner

TBD

## Status

todo
