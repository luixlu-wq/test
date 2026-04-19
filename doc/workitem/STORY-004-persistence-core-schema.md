# STORY-004 Persistence Core Schema

## Type

story

## Description

Build and validate the first operational data schema required for end-to-end core flow in local and integration environments.

## Scope

- Initial migrations for request/workflow/case/run/evidence metadata.
- Repository roundtrip support.
- Retention scaffold for heavy evidence blobs.

## Dependencies

- `STORY-001-contract-and-enum-lock.md`

## Sprint Candidate

- Sprint 1

## Story Points

8

## Technical Context

- **Target databases**: PostgreSQL 15+ (integration/production), SQLite (local-dev/ci) — `data model design.md` §1
- **Core tables in scope** (first migration pack): `test_request`, `test_workflow`, `workflow_stage`, `test_case`, `test_run`, `run_step`, `evidence_item`, `audit_log`, `approval_task` — `data model design.md` §§3, 10, 11, 12, 13, 24, 22
- **Migration tooling**: Alembic — `detailed-implementation-plan.md` §8 CI/CD pipeline; up + down migrations required for every migration file
- **FK cascade rules**: `data model design.md` §34 — `test_run → test_workflow` (SET NULL on workflow delete), `evidence_item → run_step` (CASCADE on run delete for blob cleanup); audit trail records never cascade-deleted
- **Soft delete policy**: `data model design.md` §34 — operational records use `deleted_at` column (never physically deleted); blob retention uses `retention_marker` flag; audit records: hard-delete forbidden
- **Index strategy**: `data model design.md` §35 — all FK columns indexed; composite indexes on `(test_run.workflow_id, status)`, `(evidence_item.run_id, artifact_type)`, `(audit_log.correlation_id)`
- **Retention scaffold**: `evidence_item.retention_tier` column (`hot`, `warm`, `cold`); tier transition job is out of scope here but column must exist from first migration

## Acceptance Criteria

1. All Alembic migrations (`upgrade` and `downgrade`) execute cleanly on both SQLite (local-dev) and PostgreSQL (integration) without errors; downgrade returns the schema to the pre-migration state with no residual tables or indexes.
2. Core entity relationships are enforceable and queryable: inserting a `test_run` row with a non-existent `workflow_id` raises a FK violation; querying runs by `workflow_id` uses the index (no full-table scan on PostgreSQL `EXPLAIN ANALYZE`).
3. `evidence_item.retention_tier` column exists from the initial migration; metadata for retained items is preserved even after blob deletion (blob `s3_key` set to null, `retention_marker = true`, metadata row remains).

## Test Cases

- `TC-S2-001` — Up migration creates all required tables; down migration removes them cleanly
- `TC-S2-002` — FK violation raised on orphaned `test_run` insert
- `TC-S2-003` — Repository roundtrip: create → read → update relationships for `test_request → test_workflow → test_run → evidence_item`
- `TC-S2-004` — Retention marker preserved after blob null-out; metadata row queryable

## Definition of Done

- [ ] All migration files committed with both `upgrade` and `downgrade` paths
- [ ] Migration smoke test passes on PostgreSQL ephemeral (CI Stage 2)
- [ ] `TC-S2-001` through `TC-S2-004` pass in `integration` profile
- [ ] FK indexes and composite indexes present (verified by migration test)
- [ ] `retention_tier` column exists from day 1
- [ ] Soft-delete (`deleted_at`) columns on all operational tables
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
