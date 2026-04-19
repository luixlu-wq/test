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

## Acceptance Criteria

1. Fused understanding links to source artifacts.
2. Missing/conflicting inputs are captured in warnings.
3. Retrieval chunks are generated with metadata and refs.

## Test Cases

- `TC-S4-001`
- `TC-S4-002`
- `TC-S4-003`
- `TC-S4-004`

## Owner

TBD

## Status

todo
