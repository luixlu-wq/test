# STORY-007 Semantic State And Mismatch

## Type

story

## Description

Implement state-map and mismatch services to detect contradictions and enforce execution blocking rules.

## Scope

- semantic state extraction
- transitions and expected outcomes
- mismatch classification and severity
- blocking signal emission

## Dependencies

- `STORY-006-distributed-understanding-pipeline.md`

## Acceptance Criteria

1. State map output deterministic for same input snapshot.
2. Mismatch includes source refs and severity.
3. Blocking mismatch prevents execution stage start.

## Test Cases

- `TC-S5-001`
- `TC-S5-002`
- `TC-S5-003`
- `TC-S5-004`

## Owner

TBD

## Status

todo
