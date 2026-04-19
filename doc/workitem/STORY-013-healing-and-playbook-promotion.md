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

## Sprint Candidate

- Sprint 5

## Story Points

8

## Technical Context

- **Healing Agent**: `agent prompts design.md` §9 — analyses failed run evidence; proposes selector substitutions, assertion relaxations, or flow path alternatives; output: `healing_suggestion` with `confidence`, `rationale`, `evidence_refs[]`, `suggested_patch`
- **Confidence threshold for auto-promotion**: healing suggestion requires `confidence ≥ 0.85` AND manual approval; no healing patch auto-promotes without approval regardless of confidence — `agent prompts design.md` §9 policy constraint
- **Playbook candidate**: `data model design.md` §19 — `playbook_candidate` table: `case_id`, `source_run_id`, `healing_suggestion_id`, `status (candidate/approved/rejected/promoted)`, `approved_by`, `approved_at`
- **Promotion path**: `candidate → approved` requires `approval_task` with `action_type = playbook_approval` to reach `approved` status; `approved → promoted` copies playbook to `test_asset` table with `asset_type = playbook` and marks as eligible for regression use
- **Regression enforcement**: only `promoted` playbooks eligible for `execution_mode = regression`; candidate or approved-but-not-promoted playbooks blocked with `PLAYBOOK_NOT_PROMOTED`
- **Immutability of approved assets**: promoted playbook asset is immutable (`evidence_finalized`-style write-block via `asset_locked = True`); any modification requires creating a new candidate
- **Fingerprint comparison**: `knowledge graph schema design.md` §5 — healing suggestion compared against current `SemanticStateMap` fingerprint; if fingerprint drifted since the failure run, healing confidence is penalised by 0.15

## Acceptance Criteria

1. Healing suggestions include `confidence`, `rationale`, and `evidence_refs[]`; suggestions without `rationale` fail schema validation.
2. Unapproved healing suggestions (even high-confidence) never mutate `test_asset` rows or any approved asset; write-blocked at the service layer.
3. Only `promoted` playbooks are usable in regression mode; attempting to use a `candidate` or `approved` (not promoted) playbook returns `PLAYBOOK_NOT_PROMOTED`.

## Test Cases

- `TC-S11-001` — Healing suggestion schema-validated; missing `rationale` rejected
- `TC-S11-002` — Unapproved healing cannot modify approved `test_asset` rows
- `TC-S11-003` — Promoted playbook eligible for regression; non-promoted playbook rejected with `PLAYBOOK_NOT_PROMOTED`
- `TC-S11-004` — Approval workflow: `candidate → approved → promoted` lifecycle enforced correctly

## Definition of Done

- [ ] Healing Agent integrated; output schema-validated before persist
- [ ] `playbook_candidate` lifecycle implemented with correct status transitions
- [ ] Approval task required for `candidate → approved` transition
- [ ] Promotion to `test_asset` creates immutable asset record
- [ ] Regression mode gate enforces `promoted` status
- [ ] Fingerprint drift penalty applied to healing confidence
- [ ] `TC-S11-001` through `TC-S11-004` pass; LLM calls stubbed in `ci` profile
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
