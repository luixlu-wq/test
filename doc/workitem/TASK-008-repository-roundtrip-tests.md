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

## Acceptance Criteria

1. Core entity graph persists and reloads correctly.
2. rollback path leaves no partial entities.

## Test Cases

- `TC-S2-002`
- `TC-S2-003`

## Owner

TBD

## Status

todo
