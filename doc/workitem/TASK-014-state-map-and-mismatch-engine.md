# TASK-014 State Map And Mismatch Engine

## Type

task

## Description

Implement semantic state generation and mismatch detection/classification pipeline.

## Scope

- state map model + generation
- mismatch rules and severity classification
- execution blocking flag output

## Dependencies

- `STORY-007-semantic-state-and-mismatch.md`

## Story Link

- `STORY-007-semantic-state-and-mismatch.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 2

## Story Points

5

## Technical Context

- **State map model**: `knowledge graph schema design.md` §5 — `SemanticStateMap(case_id, snapshot_version, fingerprint, page_states[], transitions[], expected_outcomes[])`; fingerprint = `SHA-256(sorted(visible_elements_list))`
- **Fingerprint stability**: `sorted()` applied to element identifiers before hashing; DOM order must not affect fingerprint; verified by TC-S5-004
- **Mismatch rules**: defined in `api/config/mismatch_rules.yaml`; each rule specifies `mismatch_type`, `condition`, `severity`; engine evaluates all rules against the fused understanding and state map
- **DETECTED_FROM_CHUNK direction**: `(MismatchWarning)-[:DETECTED_FROM_CHUNK]->(ArtifactChunk)` — `knowledge graph schema design.md` §17 fix; mismatch detects FROM conflicting chunks, not the other way around
- **Blocking flag**: `MismatchWarning.blocks_execution = True` when `severity = blocking`; workflow gate reads this flag via a query before allowing `running` transition
- **Severity classification**: `blocking` — contradictory expected outcomes on the same state transition; `warning` — inconsistent labels or partial coverage; `info` — deprecated artifact reference detected
- **Re-run idempotency**: `knowledge graph schema design.md` §17.2 — MERGE on `SemanticStateMap(case_id, snapshot_version)`; existing mismatch nodes reused if content unchanged (checksum comparison)

## Acceptance Criteria

1. State map output stable for same input snapshot: fingerprint identical on two sequential runs with the same artifact content (TC-S5-001, TC-S5-004).
2. Mismatch severity and `blocks_execution` flag generated consistently from rules; `blocking` mismatches have `blocks_execution = True` in the graph node.

## Test Cases

- `TC-S5-001` — State map fingerprint identical on replay
- `TC-S5-003` — Blocking mismatch has `blocks_execution = True`; workflow gate enforces it
- `TCN-S5-001` — Cyclic/self-loop transition set is rejected by state-map validator
- `TCN-S5-002` — Mismatch output missing required source refs fails contract validation
- `TCE-S5-001` — High-cardinality mismatch inputs preserve deterministic severity ordering

## Definition of Done

- [ ] `SemanticStateMapGenerator` produces deterministic fingerprints
- [ ] Mismatch rules loaded from YAML; in-memory for unit tests
- [ ] `blocks_execution` flag set correctly per severity rule
- [ ] `DETECTED_FROM_CHUNK` relationship direction correct in graph writes
- [ ] MERGE semantics verified: no duplicate `SemanticStateMap` or `MismatchWarning` nodes on re-run
- [ ] `TC-S5-001`, `TC-S5-003`, `TCN-S5-001`, `TCN-S5-002`, `TCE-S5-001` pass in `integration` profile

## Owner

TBD

## Status

todo
