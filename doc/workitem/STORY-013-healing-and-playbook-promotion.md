# STORY-013 Healing And Playbook Promotion

## Type

story

## Description

Implement healing analysis and controlled promotion of approved deterministic playbooks for regression runs.

## Scope

- healing event generation and logging
- playbook candidate generation
- approval-controlled promotion path
- regression mode enforcement for approved playbooks only

## Dependencies

- `STORY-012-triage-defect-and-hitl.md`

## Acceptance Criteria

1. Healing suggestions include confidence and rationale.
2. Unapproved healing never mutates approved assets.
3. Approved playbooks are reusable in regression mode.

## Test Cases

- `TC-S11-001`
- `TC-S11-002`
- `TC-S11-003`
- `TC-S11-004`

## Owner

TBD

## Status

todo
