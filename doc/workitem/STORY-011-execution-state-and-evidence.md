# STORY-011 Execution State And Evidence

## Type

story

## Description

Implement deterministic run execution, state setup/cleanup, and forensic evidence collection/finalization.

## Scope

- execution service runner orchestration
- state management integration
- evidence collector, summary, bundle generation
- immutable evidence finalize workflow

## Dependencies

- `STORY-010-test-asset-compiler-and-playwright-hybrid.md`

## Sprint Candidate

- Sprint 4

## Story Points

8

## Technical Context

- **Execution service**: `data model design.md` §12 — `test_run` lifecycle: `pending → running → passed | failed | error`; `run_step` records one row per script step with `step_index`, `action`, `assertion_result`, `evidence_refs[]`
- **State setup/cleanup**: before run: restore `SemanticStateMap` baseline (DB seeding or API setup sequence); after run: cleanup script runs on pass AND fail paths; cleanup failure logged as `cleanup_warning` but does not override run result
- **Evidence collector**: collects during run — screenshots, DOM snapshots, network HAR, console logs; each item stored as `evidence_item` with `artifact_type`, `s3_key`, `retention_tier = hot`, `run_step_id`
- **Semantic trace**: `MCP contract implementation.md` §15 — `evidence.write_semantic_trace` called for every `assert` and `wait_for_state_signal` step; 15-field payload including `requirementRef`, `flowRef`, `executedAction`, `observedOutcome`, `verdict`
- **Evidence finalization**: after run completes, `EvidenceFinalizer.finalize(run_id)` computes SHA-256 hash of evidence bundle manifest, stores in `test_run.evidence_hash`; sets `evidence_finalized = True`; finalized evidence is immutable (write-blocked)
- **Immutability enforcement**: any attempt to write to `evidence_item` where `test_run.evidence_finalized = True` raises `EVIDENCE_IMMUTABILITY_VIOLATION`
- **Evidence bundle**: ZIP archive of all evidence refs stored at `evidence_bundle/{run_id}/bundle.zip` in object storage; manifest JSON included in bundle

## Acceptance Criteria

1. `run_step` records and `evidence_item` refs are persisted for every executed step; a run with 0 `run_step` records is considered an execution error.
2. Cleanup script executes on both pass and fail paths; cleanup failure is logged as `cleanup_warning` but does not change the run `status`.
3. Finalized evidence is immutable: after `evidence_finalized = True` is set, any write attempt to associated `evidence_item` rows returns `EVIDENCE_IMMUTABILITY_VIOLATION`; the SHA-256 `evidence_hash` is verifiable against the bundle manifest.

## Test Cases

- `TC-S9-001` — `run_step` and `evidence_item` rows persisted for every step
- `TC-S9-002` — Cleanup executes on fail path; run result not overridden by cleanup failure
- `TC-S9-003` — Finalized evidence rejects writes with `EVIDENCE_IMMUTABILITY_VIOLATION`
- `TC-S9-004` — `evidence_hash` matches SHA-256 of bundle manifest contents
- `TCN-S9-001` — Worker crash mid-run transitions run to recoverable failed state with partial evidence markers
- `TCN-S9-002` — Evidence storage write failure triggers retry and preserves run-step status consistency
- `TCE-S9-001` — Rerun on same run id is blocked or idempotently resumed per policy

## Definition of Done

- [ ] Execution runner orchestrates step dispatch, evidence collection, and semantic trace writing
- [ ] State setup/cleanup scripts execute in correct order
- [ ] `EvidenceFinalizer.finalize(run_id)` sets `evidence_finalized = True` and computes `evidence_hash`
- [ ] Write-block enforced for finalized evidence
- [ ] `TC-S9-001` through `TC-S9-004`, `TCN-S9-001`, `TCN-S9-002`, `TCE-S9-001` pass in `integration` profile
- [ ] Playwright calls stubbed in `ci` profile
- [ ] Negative-path tests use deterministic failpoints (worker crash, blob write timeout)
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
