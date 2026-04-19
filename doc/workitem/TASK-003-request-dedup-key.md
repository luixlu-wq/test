# TASK-003 Request Dedup Key

## Type

task

## Description

Implement request deduplication keying and replay-safe behavior in intake path.

## Scope

- dedup key calculation
- persistence lookup path
- idempotent return semantics

## Dependencies

- `STORY-002-request-trigger-orchestration.md`

## Story Link

- `STORY-002-request-trigger-orchestration.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

3

## Technical Context

- **Dedup key column**: `data model design.md` §3 — `test_request.dedup_key` column; unique constraint; `dedup_key = SHA-256(case_ref || "|" || trigger_source || "|" || canonical_json(normalized_params))`
- **Canonical JSON**: params dict sorted by key, no whitespace; ensures same params in different key order produce the same hash
- **Lookup flow**: on intake, compute key → `SELECT id, workflow_id FROM test_request WHERE dedup_key = ?`; if found, return existing `workflow_id` with `{"status": "existing", "workflow_id": "..."}` and HTTP 200; if not found, insert new row and proceed
- **Race condition**: handle concurrent duplicate submissions with `INSERT ... ON CONFLICT (dedup_key) DO NOTHING` + re-query pattern (PostgreSQL); SQLite uses same upsert fallback
- **Scope boundary**: this task covers only the dedup key computation and DB lookup; workflow creation on first-insert is covered by TASK-004

## Acceptance Criteria

1. Two requests with identical `case_ref`, `trigger_source`, and `normalized_params` (regardless of key order in params dict) produce the same `dedup_key` hash.
2. Second submission returns the existing `workflow_id` immediately without inserting a duplicate `test_request` row.

## Test Cases

- `TC-S1-001` — Duplicate intake returns same `workflow_id`; `test_request` table has exactly 1 row after 2 identical submissions

## Definition of Done

- [ ] `compute_dedup_key(case_ref, trigger_source, params)` function implemented and unit-tested with at least 3 param-ordering variants
- [ ] DB lookup path handles concurrent insert race (ON CONFLICT or equivalent)
- [ ] `TC-S1-001` passes in `integration` profile
- [ ] Unit tests pass in `ci` profile (SQLite, no external calls)

## Owner

TBD

## Status

todo
