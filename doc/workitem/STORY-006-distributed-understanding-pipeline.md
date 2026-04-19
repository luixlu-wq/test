# STORY-006 Distributed Understanding Pipeline

## Type

story

## Description

Build the artifact ingestion/fusion/normalization pipeline and produce structured case understanding with provenance.

## Scope

- artifact classification and normalization
- fusion summary generation
- retrieval-ready chunk generation
- ingestion warning handling

## Dependencies

- `STORY-005-mcp-core-set.md`
- `STORY-004-persistence-core-schema.md`

## Sprint Candidate

- Sprint 2

## Story Points

13

## Technical Context

- **Distributed Understanding Model**: `RAG implementation design.md` §3 — anti-hallucination pipeline; all LLM claims grounded in source artifact chunks; provenance chain: artifact → parse_result → chunks → graph nodes
- **Artifact classification**: `data model design.md` §5 — `ArtifactType`: `spec`, `design`, `requirement`, `screenshot`, `har`, `log`, `playbook`; classifier uses file extension + MIME type + content heuristics
- **Normalization pipeline**: `RAG implementation design.md` §9 — parse (via Document Parser MCP or Browser Reader MCP) → extract structured fields → assign `artifact_version` → store `artifact_parse_result`
- **Fusion engine** (TASK-013): `RAG implementation design.md` §10 — matches requirements across multiple source artifacts; builds `case_understanding` record with `fusion_confidence`, linked `source_refs[]`
- **Conflict/gap surfacing**: conflicts between sources → `ingestion_warning` rows with `warning_type = conflict`; missing expected artifact types → `warning_type = gap`; both linked to `case_id`
- **Chunk generation**: `RAG implementation design.md` §11 — chunks of 256–512 tokens with 10% overlap; each chunk stores `model_version`, `artifact_ref`, `section_ref`, `chunk_index`; `voyage-3-large` 1024-dim embeddings
- **Graph writes**: `knowledge graph schema design.md` §17.1 — MERGE semantics for all graph writes; idempotent; no cross-service graph transactions
- **Provenance requirement**: every `case_understanding` field must trace to at least one source artifact chunk via `source_refs[]`

## Acceptance Criteria

1. Fused `case_understanding` record contains `source_refs[]` linking every extracted field to at least one source artifact; a field with no traceable source is surfaced as an `ingestion_warning` with `warning_type = ungrounded`.
2. Missing or conflicting inputs are captured as `ingestion_warning` rows: missing required artifact type → `gap`, contradictory values across sources → `conflict`; both are queryable by `case_id`.
3. Retrieval-ready chunks are generated with `model_version`, `artifact_ref`, `section_ref`, and `chunk_index` metadata; chunks are vector-indexed and retrievable by `case_id` filter.

## Test Cases

- `TC-S4-001` — Fusion produces `case_understanding` with complete `source_refs`
- `TC-S4-002` — Conflicting artifacts produce `conflict` warnings; missing artifact produces `gap` warning
- `TC-S4-003` — Chunks generated with required metadata; retrievable by `case_id`
- `TC-S4-004` — Ungrounded field in understanding produces `ungrounded` ingestion warning
- `TCN-S4-001` — OCR empty-result input produces explicit low-quality warning without fabricated extraction
- `TCN-S4-002` — Conflicting artifact versions create explicit conflict records with source refs
- `TCE-S4-001` — Duplicate artifact ingestion is idempotent and does not duplicate entities

## Definition of Done

- [ ] Artifact classifier correctly categorises all supported `ArtifactType` values
- [ ] Fusion engine produces `case_understanding` with `fusion_confidence` and `source_refs`
- [ ] `ingestion_warning` rows created for conflicts, gaps, and ungrounded fields
- [ ] Chunks indexed in vector store with required metadata fields
- [ ] Graph nodes written with MERGE semantics (no duplicate nodes on re-ingestion)
- [ ] `TC-S4-001` through `TC-S4-004`, `TCN-S4-001`, `TCN-S4-002`, `TCE-S4-001` pass in `integration` profile
- [ ] LLM calls stubbed in `ci` profile (`AI_QA_LLM_STUB_MODE=true`)
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
