# TASK-008 Repository Roundtrip Tests

## Type

task

## Description

Implement persistence roundtrip and integrity tests for key repository operations.

## Scope

- create/read/update links for core entities
- transaction rollback tests

## Dependencies

- `TASK-007-core-migration-pack.md`

## Story Link

- `STORY-004-persistence-core-schema.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

5

## Technical Context

- **Repository pattern**: each entity family has a repository class (`TestRequestRepository`, `TestWorkflowRepository`, `TestRunRepository`, `EvidenceRepository`); no raw SQL in service layer
- **Roundtrip coverage**: create entity → flush/commit → read back → assert all fields preserved; then update a mutable field → commit → read back → assert change persisted
- **Relationship traversal**: load `test_request` → navigate to `test_workflow` → navigate to `test_run` list → navigate to `evidence_item` list; assert lazy-load works correctly without N+1 queries (use `joinedload` or `selectinload`)
- **Rollback test**: wrap INSERT in explicit transaction, raise exception mid-insert, rollback, assert no partial entity in DB — verifies the "no partial entities on failure" requirement
- **Soft-delete test**: call `repository.delete(id)` → verify `deleted_at` is set → verify entity excluded from default query → verify `repository.get_including_deleted(id)` returns it
- **Retention marker test**: set `evidence_item.s3_key = None`, `retention_marker = True` → commit → read back → assert metadata fields (`run_id`, `artifact_type`, timestamps) still intact; `TC-S2-004`

## Acceptance Criteria

1. Full entity graph (`test_request → test_workflow → test_run → evidence_item`) persists and reloads correctly with all foreign key links intact.
2. Transaction rollback path (simulated mid-insert failure) leaves no partial entities in any table; subsequent queries return zero rows for the aborted entity chain.

## Test Cases

- `TC-S2-002` — Entity graph persists and reloads with all FK links
- `TC-S2-003` — Rollback leaves no partial entities; soft-delete excludes entity from default queries
- `TCN-S2-001` — Duplicate unique-key race leaves no orphan rows after rollback
- `TCN-S2-002` — Simulated DB connection loss during transaction produces retry-safe final state
- `TCE-S2-001` — Concurrent writes on same request/run preserve deterministic referential integrity

## Definition of Done

- [ ] Repository classes implemented for all four entity families
- [ ] Roundtrip tests cover create, read, update, soft-delete for each entity
- [ ] Rollback test confirms no partial entities remain after aborted transaction
- [ ] Retention marker test passes (`TC-S2-004` also covered here)
- [ ] N+1 query prevention verified by asserting SQL query count in at least one traversal test
- [ ] `TC-S2-002`, `TC-S2-003`, `TCN-S2-001`, `TCN-S2-002`, `TCE-S2-001` pass in `integration` profile

## Owner

TBD

## Status

todo
