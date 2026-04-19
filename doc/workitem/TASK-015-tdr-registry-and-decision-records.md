# TASK-015 TDR Registry And Decision Records

## Type

task

## Description

Create and lock the Step-0 Technology Decision Record (TDR) registry required by the implementation plan.

## Scope

- create `api/doc/tdr/` folder
- add required TDR files `TDR-001` through `TDR-010`
- add checklist validation to ensure required sections exist in every TDR

## Dependencies

- `STORY-001-contract-and-enum-lock.md`

## Story Link

- `STORY-001-contract-and-enum-lock.md` (Primary: Step-0 TDR completion requirement)

## Sprint Candidate

- Sprint 1

## Story Points

2

## Technical Context

- **Source of truth**: `api/doc/impl-plan/detailed-implementation-plan.md` Step 0.
- **Required TDR IDs**: `TDR-001`..`TDR-010`.
- **Required sections per TDR**: decision statement, context, alternatives considered, consequences, decision date.
- **Rationale alignment**: each TDR references the relevant architecture/implementation design section for traceability.

## Acceptance Criteria

1. `api/doc/tdr/` contains `TDR-001` through `TDR-010` and each file includes all required sections.
2. Every TDR links back to at least one source design reference section and has an explicit decision date.

## Test Cases

- `TC-S0-004` — TDR inventory check confirms all required IDs exist
- `TCN-S0-004` — Missing required section in any TDR fails checklist validation
- `TCE-S0-003` — Re-running TDR checklist yields deterministic pass/fail output

## Definition of Done

- [ ] TDR directory created and committed
- [ ] TDR-001 to TDR-010 committed with required sections
- [ ] Checklist validator for required TDR fields added to CI/doc checks
- [ ] `TC-S0-004`, `TCN-S0-004`, `TCE-S0-003` pass in `ci` profile

## Owner

TBD

## Status

todo
