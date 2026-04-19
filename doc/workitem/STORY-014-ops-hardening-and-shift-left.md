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

## Sprint Candidate

- Sprint 6

## Story Points

5

## Technical Context

- **Shift-left trigger**: pre-commit hook calls `trigger.dispatch(trigger_type=shift_left, ...)`; only permitted in `local-dev` and `integration` profiles (PROD blocked via policy — `MCP contract implementation.md` §4.9); runs targeted smoke checks on changed files
- **Watch mode**: filesystem watcher (`watchdog` or equivalent) monitors `api/` for changes; on spec/requirement file change, triggers understanding re-ingestion for affected cases; debounced to avoid thrashing (minimum 30s between re-ingestions for same case)
- **Retention job**: `data model design.md` §34 + §35 — background job runs daily; transitions `evidence_item.retention_tier`: `hot → warm` after 30 days, `warm → cold` after 90 days; cold items have `s3_key` set to null but metadata row preserved; job logs to `audit_log` with `action = retention_tier_transition`
- **SLO metrics** (target SLOs for MVP):
  - Retrieval P95 latency <= 1200ms on canonical top-k integration corpus
  - Understanding pipeline end-to-end < 120s per case
  - Triage classification < 30s per run
- **CI quality gates**: `detailed-implementation-plan.md` §8 — 9 PR merge gates including negative/edge reliability (failpoints + limits); all must pass before merge
- **Determinism gate**: replay same scenario twice with same inputs; assert identical `run_step` results, same `evidence_hash`, and same triage `class`; any divergence fails the determinism gate in CI Stage 3

## Acceptance Criteria

1. Shift-left flow triggers targeted smoke checks on changed files and completes within 60 seconds on a typical spec change.
2. Retention process transitions `evidence_item` tiers correctly (hot → warm → cold) while preserving metadata traceability: after cold transition, `s3_key = null` but all metadata fields (`run_id`, `artifact_type`, timestamps) remain queryable.
3. CI blocks merge on determinism/contract/security failures: a PR introducing a non-deterministic scenario or schema regression cannot be merged (CI Stage 3 or Stage 1 gate respectively).

## Test Cases

- `TC-S12-001` — Shift-left trigger dispatches and completes smoke check within 60s
- `TC-S12-002` — Retention job transitions tiers; cold evidence metadata intact after `s3_key` null-out
- `TC-S12-003` — CI determinism gate fails on non-deterministic scenario (run-step divergence detected)
- `TC-S12-004` — SLO metrics reported; retrieval P95 latency assertion passes on synthetic fixture
- `TCN-S12-001` — Retention policy misconfiguration attempting protected metadata deletion is blocked and audited
- `TCN-S12-002` — CI gate bypass attempt (missing required suite) fails pipeline
- `TCE-S12-001` — High-volume artifact cleanup run remains within timeout budget and integrity guarantees

## Definition of Done

- [ ] Pre-commit hook script committed at `api/scripts/pre-commit-trigger.sh`
- [ ] Watch mode implemented with 30s debounce
- [ ] Retention job implemented with correct tier transition rules and audit logging
- [ ] SLO metrics instrumentation in place (Prometheus-compatible or equivalent)
- [ ] CI Stage 3 determinism gate operational
- [ ] All 9 PR merge gates documented in `detailed-implementation-plan.md` §8 are enforced
- [ ] `TC-S12-001` through `TC-S12-004`, `TCN-S12-001`, `TCN-S12-002`, `TCE-S12-001` pass in appropriate profiles
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
