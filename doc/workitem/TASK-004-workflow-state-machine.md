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

## Acceptance Criteria

1. Invalid transitions are blocked.
2. Retry does not duplicate side-effects.

## Test Cases

- `TC-S1-002`

## Owner

TBD

## Status

todo
