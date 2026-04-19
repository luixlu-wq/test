# STORY-012 Triage Defect And HITL

## Type

story

## Description

Implement failure classification, confidence scoring, defect draft packet creation, and review gating workflow.

## Scope

- triage classifier
- confidence decision engine
- defect draft generation
- review task and policy gate integration

## Dependencies

- `STORY-011-execution-state-and-evidence.md`

## Acceptance Criteria

1. Triage result includes class, confidence, reason, evidence refs.
2. Low confidence outcomes require review task.
3. External publish path remains policy controlled.

## Test Cases

- `TC-S10-001`
- `TC-S10-002`
- `TC-S10-003`
- `TC-S10-004`

## Owner

TBD

## Status

todo
