# STORY-004 Persistence Core Schema

## Type

story

## Description

Build and validate the first operational data schema required for end-to-end core flow in local and integration environments.

## Scope

- Initial migrations for request/workflow/case/run/evidence metadata.
- Repository roundtrip support.
- retention scaffold for heavy evidence blobs.

## Dependencies

- `STORY-001-contract-and-enum-lock.md`

## Acceptance Criteria

1. Migrations succeed on SQLite and PostgreSQL.
2. Core entity relationships are enforceable and queryable.
3. Retention marker process preserves metadata traceability.

## Test Cases

- `TC-S2-001`
- `TC-S2-002`
- `TC-S2-003`
- `TC-S2-004`

## Owner

TBD

## Status

todo
