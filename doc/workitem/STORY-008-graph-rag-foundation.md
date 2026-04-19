# STORY-008 Graph RAG Foundation

## Type

story

## Description

Build indexing, retrieval, graph expansion, and bounded context pack generation for grounded agent reasoning.

## Scope

- hybrid indexing
- search and filtering
- one-hop graph expansion
- context pack builder
- retrieval/context logs

## Dependencies

- `STORY-007-semantic-state-and-mismatch.md`

## Sprint Candidate

- Sprint 3

## Story Points

13

## Technical Context

- **Hybrid retrieval pipeline**: `RAG implementation design.md` §14 — vector search (Qdrant/pgvector) → graph expansion (Neo4j one-hop) → reranking → context pack assembly
- **Embedding model**: `voyage-3-large` (Voyage AI, 1024-dim, 16k tokens) — `RAG implementation design.md` §11.3; model version stored on every chunk; `text-embedding-3-large` tagged fallback
- **Reranking weights**: `RAG implementation design.md` §16.2 — 9 signals; key weights: `same_case_boost` 0.20 (second-highest, prevents cross-case pollution), `semantic_similarity` 0.22 (highest), `blocking_mismatch_penalty` -0.15
- **Graph expansion**: `knowledge graph schema design.md` §8 — one-hop expansion from matched chunks along `GROUNDS`, `RELATES_TO`, `TRANSITIONS_TO`, `DETECTED_FROM` relationships; max 50 additional nodes per query
- **Context pack**: `RAG implementation design.md` §17 — 18,000-token RAG envelope; per-section budget: Facts 800, Requirements 4000, State refs 2000, Assets 3000, History 3000, Mismatches 1500, Evidence 2000, Gaps 700 = 17,000 + 1,000 buffer; never truncate blocking mismatches
- **Regression policy**: context pack excludes unapproved diagnostic results when `execution_mode = regression`; approved results included via `APPROVED_BY` graph relationship
- **Retrieval log**: every context pack generation logged to `retrieval_log` table with `query_vector_ref`, `top_k`, `reranking_scores[]`, `context_pack_token_count`, `truncation_applied`

## Acceptance Criteria

1. Retrieval supports filter-based narrowing by `case_id` and `artifact_type`; returning chunks from outside the specified case is a test failure.
2. Context pack token count stays within the 18,000-token envelope; blocking mismatches are never truncated even when the envelope is at capacity (lower-priority sections shrink first).
3. Regression execution context excludes unapproved diagnostic results: a context pack requested with `execution_mode = regression` must not contain chunks from diagnostic runs that have not been through the approval workflow.

## Test Cases

- `TC-S6-001` — Retrieval with `case_id` filter returns only chunks from that case
- `TC-S6-002` — Context pack at capacity shrinks non-critical sections before blocking mismatches
- `TC-S6-003` — Regression context pack excludes unapproved diagnostic content
- `TC-S6-004` — One-hop graph expansion adds related nodes up to 50-node cap

## Definition of Done

- [ ] Vector index populated with `voyage-3-large` embeddings for all chunks
- [ ] Graph expansion follows only allowed relationship types; capped at 50 nodes
- [ ] Reranking weights applied; configurable via `api/config/reranking_weights.yaml`
- [ ] Context pack respects 18,000-token budget with per-section allocation
- [ ] Blocking mismatch chunks never truncated
- [ ] Regression policy enforced on context pack assembly
- [ ] Retrieval log written for every context pack generation
- [ ] `TC-S6-001` through `TC-S6-004` pass in `integration` profile
- [ ] Vector/graph calls stubbed in `ci` profile
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
