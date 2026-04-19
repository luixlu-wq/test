# STORY-003 Policy And Audit Foundation

## Type

story

## Description

Implement policy decision evaluation and a complete audit trail for every major action and workflow stage.

## Scope

- Policy decision evaluator.
- Approval task creation path.
- Audit logs with correlation IDs.

## Dependencies

- `STORY-002-request-trigger-orchestration.md`

## Sprint Candidate

- Sprint 1

## Story Points

5

## Technical Context

- **Policy profiles**: `data model design.md` §32.1 — four profiles: `read-only`, `standard-controlled`, `full-controlled`, `local-dev`; PROD sets `allowed_modes = ["regression"]` (blocks `diagnostic`)
- **Policy decision schema**: `MCP contract implementation.md` §4.1 — every MCP operation includes `policyContext`; evaluator returns `{action, decision: allow|deny|review, reason, threshold, policy_source}`
- **Approval task**: `data model design.md` §22 — `approval_task` table: `action_type`, `requested_by`, `status (pending/approved/rejected)`, `policy_decision_id`; created when `decision = review`
- **Audit log schema**: `data model design.md` §24 — `audit_log` table: `id`, `correlation_id`, `request_id`, `run_id`, `action`, `actor`, `before_state`, `after_state`, `timestamp`; never hard-deleted (soft-delete-only policy)
- **Correlation ID propagation**: `detailed-implementation-plan.md` §2 — `X-Correlation-ID` header propagated through all service calls; stored in `audit_log.correlation_id`; `run_id` populated when audit event is within a test run
- **Query requirement**: audit records must be filterable by `correlation_id`, `request_id`, and `run_id` via indexed columns

## Acceptance Criteria

1. Policy decision for any action returns a structured result including `decision` (allow/deny/review), `reason` string, `threshold` value used, and `policy_source` (profile name + rule ID); partial decision objects are rejected by schema validation.
2. Any action with `decision = review` automatically creates an `approval_task` row with `status = pending`; the action is blocked until the task reaches `approved`.
3. Audit log records are emitted for every workflow stage transition and every MCP tool invocation; records are queryable by `correlation_id` and return results in under 200ms on datasets of 10,000+ rows (index-backed).

## Test Cases

- `TC-S1-003` — Policy evaluator returns complete decision struct; `review` decision creates approval task
- `TC-S1-004` — Audit records emitted for stage transition; filtered query by `correlation_id` returns correct records

## Definition of Done

- [ ] `PolicyEvaluator.evaluate(action, context)` returns full decision struct; schema-validated
- [ ] `ApprovalTaskService.create_from_decision(decision)` creates approval task on `review` decisions
- [ ] Audit hook fires on every stage transition and MCP invocation
- [ ] `audit_log` indexed on `correlation_id`, `request_id`, `run_id`
- [ ] `TC-S1-003` and `TC-S1-004` pass in `integration` profile
- [ ] Audit records survive transaction rollback of the audited action (written in separate transaction)
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
