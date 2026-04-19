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

## Sprint Candidate

- Sprint 5

## Story Points

8

## Technical Context

- **Triage Agent**: `agent prompts design.md` §8 — classifies failures as `product_defect`, `test_flakiness`, `environment_issue`, `test_design_gap`; required output fields: `class`, `confidence`, `reason`, `evidence_refs[]`
- **Confidence gate thresholds**: auto-approve if `confidence ≥ 0.85` and class is unambiguous; route to review if `confidence < 0.85` or class is `test_flakiness` (environment sensitivity); block auto-publish if `confidence < 0.60`
- **Defect draft packet**: `data model design.md` §20 — `defect_draft` table: `run_id`, `triage_id`, `title`, `steps_to_reproduce`, `expected_outcome`, `actual_outcome`, `evidence_refs[]`, `suggested_severity`, `status (draft/review/published/rejected)`
- **HITL review task**: low-confidence triage outcome creates `approval_task` with `action_type = triage_review`; defect draft cannot transition to `published` until task is `approved`
- **External publish gate**: `defect_draft.status → published` blocked by policy unless: approval task approved AND `policyContext.allowed_policies` includes `defect_publish`; returns `POLICY_VIOLATION` otherwise
- **Evidence refs in defect**: defect draft must link to finalized evidence items (from STORY-011); unfinalized evidence refs blocked with `EVIDENCE_NOT_FINALIZED`
- **Model constraint**: Triage Agent must use `claude-sonnet-4-6` minimum; `claude-haiku-4-5-20251001` forbidden — `agent prompts design.md` §17

## Acceptance Criteria

1. Triage result includes all four required fields (`class`, `confidence`, `reason`, `evidence_refs[]`); partial triage output fails schema validation and is not persisted.
2. Triage outcome with `confidence < 0.85` or class `test_flakiness` creates an `approval_task` with `action_type = triage_review`; defect draft cannot transition to `published` until the task is `approved`.
3. External publish path is policy-controlled: `defect_draft → published` transition blocked unless both the approval task is `approved` AND `defect_publish` is in `policyContext.allowed_policies`.

## Test Cases

- `TC-S10-001` — Triage output includes all required fields; low-confidence creates approval task
- `TC-S10-002` — Defect draft remains in `review` status until approval task is `approved`
- `TC-S10-003` — External publish blocked by policy without `defect_publish` permission
- `TC-S10-004` — Triage result with unfinalized evidence refs rejected with `EVIDENCE_NOT_FINALIZED`

## Definition of Done

- [ ] Triage Agent integrated; output schema-validated before persist
- [ ] Confidence gate logic implemented with correct thresholds
- [ ] `approval_task` created for low-confidence and `test_flakiness` outcomes
- [ ] Defect draft lifecycle enforces approval gate before publish
- [ ] Policy check on external publish path
- [ ] `TC-S10-001` through `TC-S10-004` pass; LLM calls stubbed in `ci` profile
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
