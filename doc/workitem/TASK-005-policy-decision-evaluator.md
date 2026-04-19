# TASK-005 Policy Decision Evaluator

## Type

task

## Description

Implement policy evaluator for action authorization, escalation requirements, and decision rationale output.

## Scope

- policy rules format
- decision API/service
- rationale fields

## Dependencies

- `STORY-003-policy-and-audit-foundation.md`

## Story Link

- `STORY-003-policy-and-audit-foundation.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 1

## Story Points

3

## Technical Context

- **Policy profile table**: `data model design.md` §32.1 — `environment_profile` rows define `allowed_modes`, `allowed_policies`; evaluator reads the active profile for the current environment
- **Decision output fields** (all required): `action` (the operation being evaluated), `decision` (`allow` | `deny` | `review`), `reason` (human-readable string), `threshold` (numeric confidence or severity threshold applied), `policy_source` (profile name + rule ID)
- **Deny conditions**: mode blocked by profile (`diagnostic` in PROD), action type not in `allowed_policies`, caller RBAC role insufficient
- **Review conditions**: action confidence below auto-approve threshold (e.g. healing patch confidence < 0.85), destructive action class, first-time playbook promotion
- **Policy rules storage**: loaded from `api/config/policy_rules.yaml` at startup; hot-reloadable without restart
- **Error codes**: `POLICY_VIOLATION` (deny), `APPROVAL_REQUIRED` (review) — both defined in `MCP contract implementation.md` §4.9

## Acceptance Criteria

1. `PolicyEvaluator.evaluate(action, context)` returns a dict with all five required fields; any missing field raises `PolicyDecisionIncompleteError`.
2. The threshold value and policy source (profile + rule ID) are traceable: calling `explain(decision_id)` returns the exact rule that produced the decision.

## Test Cases

- `TC-S1-003` — Policy evaluator returns complete decision struct for allowed, denied, and review-required actions

## Definition of Done

- [ ] `PolicyEvaluator` implemented with `evaluate()` and `explain()` methods
- [ ] All five decision fields present and schema-validated in every return
- [ ] Policy rules loaded from YAML; unit tests use in-memory rule fixtures (no file I/O dependency)
- [ ] `TC-S1-003` passes in `ci` profile (no external calls required)
- [ ] Edge cases tested: unknown action type, missing profile, PROD + diagnostic mode

## Owner

TBD

## Status

todo
