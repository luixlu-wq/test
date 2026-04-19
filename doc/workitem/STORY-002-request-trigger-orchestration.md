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

## Acceptance Criteria

1. Duplicate request returns same workflow identity.
2. Stage retry is idempotent.
3. Workflow can pause/resume safely.

## Test Cases

- `TC-S1-001`
- `TC-S1-002`

## Owner

TBD

## Status

todo
