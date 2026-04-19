# STORY-014 Ops Hardening And Shift Left

## Type

story

## Description

Add operational hardening: shift-left triggers, retention jobs, SLO observability, and CI quality gates.

## Scope

- pre-commit trigger wiring
- watch mode support
- retention jobs
- SLO/quality gate checks in CI

## Dependencies

- `STORY-013-healing-and-playbook-promotion.md`

## Acceptance Criteria

1. Shift-left flow runs targeted smoke checks.
2. Retention process tiers heavy data while preserving metadata.
3. CI blocks merge on determinism/contract/security failures.

## Test Cases

- `TC-S12-001`
- `TC-S12-002`
- `TC-S12-003`
- `TC-S12-004`

## Owner

TBD

## Status

todo
