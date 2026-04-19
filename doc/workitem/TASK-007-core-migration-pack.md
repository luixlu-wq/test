# TASK-007 Core Migration Pack

## Type

task

## Description

Create initial migration pack for request/workflow/run/evidence metadata entities.

## Scope

- migration scripts
- rollback scripts
- migration smoke test harness

## Dependencies

- `STORY-004-persistence-core-schema.md`

## Story Link

- `STORY-004-persistence-core-schema.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

3

## Technical Context

- **Migration tool**: Alembic with `env.py` configured for both SQLite and PostgreSQL connection URLs
- **Tables in first migration** (one migration file per logical group):
  - `0001_core_request_workflow.py`: `test_request`, `test_workflow`, `workflow_stage`
  - `0002_case_run_step.py`: `test_case`, `test_run`, `run_step`
  - `0003_evidence_retention.py`: `evidence_item` (with `retention_tier`, `s3_key`, `retention_marker`)
  - `0004_audit_approval.py`: `audit_log`, `approval_task`
- **Index migrations**: included in the same migration file as the table they index; no separate migration for indexes
- **Rollback requirement**: each `downgrade()` function must reverse all DDL changes in the matching `upgrade()`; tested by running `alembic downgrade -1` after each upgrade
- **Smoke test harness**: `tests/integration/test_migrations.py` — runs `alembic upgrade head` + basic INSERT/SELECT + `alembic downgrade base` on ephemeral PostgreSQL; also runs same sequence on SQLite
- **FK cascade DDL**: use `ondelete="CASCADE"` and `ondelete="SET NULL"` as defined in `data model design.md` §34

## Acceptance Criteria

1. `alembic upgrade head` + `alembic downgrade base` cycle passes on both SQLite and PostgreSQL without errors.
2. Primary traceability constraints are enforced: FK from `test_run.workflow_id → test_workflow.id`, `evidence_item.run_id → test_run.id`, `audit_log.correlation_id` indexed.

## Test Cases

- `TC-S2-001` — Full up/down migration cycle passes on both backends

## Definition of Done

- [ ] Four migration files committed; each has a working `downgrade()`
- [ ] All FK indexes and composite indexes created in migrations
- [ ] Smoke test harness in `tests/integration/test_migrations.py`
- [ ] `TC-S2-001` passes in CI Stage 2 (PostgreSQL ephemeral)
- [ ] `alembic current` shows `head` after `upgrade head` in integration environment

## Owner

TBD

## Status

todo
