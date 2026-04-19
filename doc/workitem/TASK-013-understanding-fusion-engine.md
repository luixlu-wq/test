# TASK-013 Understanding Fusion Engine

## Type

task

## Description

Implement artifact fusion logic that connects parsed sources into a coherent case understanding record.

## Scope

- fusion matching logic
- confidence tagging
- conflict/gap surfacing

## Dependencies

- `STORY-006-distributed-understanding-pipeline.md`

## Story Link

- `STORY-006-distributed-understanding-pipeline.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 2

## Story Points

8

## Technical Context

- **Fusion strategy**: `RAG implementation design.md` §10 — match requirements across source artifacts by requirement ID, semantic similarity (cosine ≥ 0.85), and heading/section label; produce one `FusedRequirement` per matched group with `consensus_value`, `source_refs[]`, `fusion_confidence`
- **Confidence model**: if all sources agree → `fusion_confidence ≥ 0.9`; if partial agreement → weighted by source type priority (spec > design > derived); if single source only → `fusion_confidence = source.confidence * 0.7`
- **Conflict detection**: two sources describe the same requirement with contradictory values (e.g. different expected outcomes) → emit `ingestion_warning(warning_type=conflict, severity=warning, refs=[src_a, src_b])`
- **Gap detection**: required artifact type absent from ingested set → emit `ingestion_warning(warning_type=gap, severity=info, missing_type=...)`
- **Ungrounded fields**: any `case_understanding` field not traceable to at least one source chunk → emit `ingestion_warning(warning_type=ungrounded, field_name=...)` and set `fusion_confidence = 0.0` for that field
- **Output**: `CaseUnderstanding` record persisted to PostgreSQL + Neo4j graph (MERGE on `CaseNode`)
- **LLM use**: Understanding Agent (`agent prompts design.md` §4) called via agent runtime for semantic matching and summary generation; must be stubbed in `ci` profile

## Acceptance Criteria

1. `case_understanding` record contains `source_refs[]` linking each extracted field to at least one source artifact; `fusion_confidence` present for every field.
2. Conflicting sources emit explicit `ingestion_warning` rows with `warning_type = conflict` and refs to both conflicting sources.

## Test Cases

- `TC-S4-002` — Conflict warning emitted for contradictory source values
- `TC-S4-004` — Ungrounded field produces `ungrounded` warning and `fusion_confidence = 0.0`
- `TCN-S4-001` — Empty OCR/visual extraction result is surfaced as low-quality input warning (no fabricated understanding content)
- `TCE-S4-001` — Re-ingesting the same artifact set is idempotent with no duplicate `CaseUnderstanding` entities

## Definition of Done

- [ ] Fusion matching logic handles requirement ID match, semantic match, and label match
- [ ] `FusedRequirement` includes `consensus_value`, `source_refs[]`, `fusion_confidence`
- [ ] `ingestion_warning` rows created for conflict, gap, ungrounded cases
- [ ] `CaseUnderstanding` written to PostgreSQL and Neo4j graph
- [ ] LLM calls stubbed in `ci` profile
- [ ] `TC-S4-002`, `TC-S4-004`, `TCN-S4-001`, `TCE-S4-001` pass in `integration` profile

## Owner

TBD

## Status

todo
