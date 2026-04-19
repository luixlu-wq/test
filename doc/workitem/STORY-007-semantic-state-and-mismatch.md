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

## Sprint Candidate

- Sprint 2

## Story Points

8

## Technical Context

- **Semantic State Map**: `knowledge graph schema design.md` §5 — first-class QA object; `SemanticStateMap` node linked to `PageNode`, `UIStateNode`, `TransitionNode`, `FingerprintNode`; deterministic fingerprint = `SHA-256(sorted(visible_elements))`
- **State map generation inputs**: `case_understanding` (requirements, expected outcomes), `ParsedDocument` (UI state descriptions), screenshot analysis (via Claude Vision if available); output is deterministic for same input snapshot
- **Mismatch types**: `knowledge graph schema design.md` §7.6 — `CONTRADICTS`, `SUPERSEDES`, `GROUNDS_MISMATCH`; `MismatchWarning` node; `(MismatchWarning)-[:DETECTED_FROM_CHUNK]->(ArtifactChunk)`
- **Severity levels**: `blocking` (halts execution stage start), `warning` (surfaced in context pack but does not block), `info` (logged only)
- **Blocking signal**: on `blocking` mismatch, workflow stage transition to `running` is rejected with `BLOCKED_BY_MISMATCH`; the mismatch `id` and `severity` included in the error payload
- **Determinism requirement**: same input snapshot (same artifact versions and content hashes) must produce bit-identical state map output; verified by replay test
- **Graph writes**: MERGE on `UIStateNode(fingerprint)` and `SemanticStateMap(case_id, snapshot_version)` — `knowledge graph schema design.md` §17.2

## Acceptance Criteria

1. State map output is deterministic: running the state map generator twice on the same input snapshot (same artifact content hashes) produces identical output with the same `fingerprint` values.
2. Mismatch detection output includes `source_refs` (the conflicting artifact chunks), `severity` (`blocking`/`warning`/`info`), and `mismatch_type`; partial mismatch records are rejected by schema validation.
3. A `blocking` severity mismatch prevents the execution stage from transitioning to `running`; the stage status remains `pending` and the error response includes the mismatch `id`.

## Test Cases

- `TC-S5-001` — State map generator produces identical output on two runs of the same snapshot
- `TC-S5-002` — Mismatch includes complete `source_refs`, `severity`, `mismatch_type`
- `TC-S5-003` — Blocking mismatch prevents execution stage start; error includes mismatch `id`
- `TC-S5-004` — State map fingerprint stable for same set of visible elements regardless of DOM order
- `TCN-S5-001` — Cyclic/self-loop transition input is rejected by state validator
- `TCN-S5-002` — Mismatch output missing source refs is rejected by output contract validation
- `TCE-S5-001` — High-volume mismatch set preserves deterministic severity ordering

## Definition of Done

- [ ] `SemanticStateMapGenerator.generate(case_id, snapshot_version)` produces deterministic output
- [ ] `MismatchDetector` emits `MismatchWarning` nodes with all required fields
- [ ] Blocking signal wired into workflow stage state machine (TASK-004)
- [ ] `TC-S5-001` through `TC-S5-004`, `TCN-S5-001`, `TCN-S5-002`, `TCE-S5-001` pass in `integration` profile
- [ ] Graph MERGE semantics verified (no duplicate nodes on re-run)
- [ ] LLM calls stubbed in `ci` profile
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
