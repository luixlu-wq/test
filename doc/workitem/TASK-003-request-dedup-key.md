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

## Acceptance Criteria

1. Duplicate requests reuse existing workflow identity.
2. No duplicate downstream workflow creation.

## Test Cases

- `TC-S1-001`

## Owner

TBD

## Status

todo
