# STORY-002 Request Trigger Orchestration

## Type

story

## Description

Implement request intake, trigger handling, and orchestrated workflow stage machine with retry/idempotency behavior.

## Scope

- API routes for request/trigger intake.
- Orchestration stage lifecycle persistence.
- Dedup + idempotency controls.

## Dependencies

- `STORY-001-contract-and-enum-lock.md`

## Sprint Candidate

- Sprint 1

## Story Points

8

## Technical Context

- **Intake Agent role**: `agent prompts design.md` §3 — Intake Agent resolves descriptive trigger content into `execution_mode`, `environment_profile`, and case context; sets `source = derived` on resolved fields
- **Dedup key algorithm**: `data model design.md` §3 — `test_request.dedup_key` = stable hash of `(case_ref, trigger_source, normalized_params)`; duplicate intake returns existing `workflow_id` with HTTP 200
- **Workflow stage model**: `data model design.md` §10 — `workflow_stage` table: `stage_name`, `status` (pending/running/done/failed/skipped), `attempt_count`, `started_at`, `completed_at`; max 3 retry attempts before `stage_status = failed`
- **Saga/compensation**: `detailed-implementation-plan.md` TDR-010 — choreography-based saga; each stage emits a completion event consumed by the next stage; rollback path cleans up created resources via compensating actions
- **State machine allowed transitions**: `data model design.md` §6 — `pending → running → done | failed`; `failed → pending` (retry) with `attempt_count` increment; direct `pending → done` blocked
- **Event bus**: Redis Streams — stage completion events published to `workflow.stage.completed` stream; worker service subscribes
- **PROD guard**: `execution_mode = diagnostic` blocked in PROD environment; reject at intake with `POLICY_VIOLATION` error code

## Acceptance Criteria

1. Submitting an identical request twice (same `dedup_key`) returns the same `workflow_id` and HTTP 200 on both calls; no duplicate `workflow_stage` rows are created.
2. Advancing a stage through retry is idempotent: calling the stage transition endpoint a second time with the same `attempt_count` returns the existing stage record unchanged; `attempt_count` does not increment.
3. A paused workflow (stage `status = failed`) can be resumed by re-triggering the failed stage; the stage transitions back to `pending` and re-runs without data loss.

## Test Cases

- `TC-S1-001` — Duplicate request intake returns existing `workflow_id`; DB has exactly one `test_request` and one `test_workflow` row
- `TC-S1-002` — Stage retry increments `attempt_count` by 1 only; no duplicate `workflow_stage` side-effects

## Definition of Done

- [ ] Intake API route (`POST /requests`) implemented with dedup key logic
- [ ] Workflow and stage tables populated correctly on first and duplicate intake
- [ ] Stage state machine enforces allowed transitions; invalid transitions return 422 with `INVALID_TRANSITION` error
- [ ] Retry path tested with at least one injected failure scenario
- [ ] `TC-S1-001` and `TC-S1-002` pass in `integration` profile (PostgreSQL)
- [ ] No `diagnostic` mode requests accepted in `PROD` environment profile
- [ ] Redis Streams event published on stage completion (verified in integration test)
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
