# EPIC-002 MCP Understanding And State

## Type

epic

## Description

Implement ingestion and interpretation foundations through MCP core adapters, distributed understanding, semantic state mapping, and mismatch detection.

## Scope

- Step 3, Step 4, Step 5 from implementation plan.
- MCP envelopes and core operations.
- Artifact normalization/fusion.
- Semantic state and transition extraction.
- Mismatch severity and blocking signals.

## Dependencies

- `EPIC-001-spec-and-backbone.md`

## Acceptance Criteria

1. MCP core set is callable through orchestration flow.
2. Fused case understanding persists with provenance refs.
3. Semantic state maps are generated with deterministic structure.
4. Blocking mismatches prevent execution progression.
5. Negative and edge paths are validated for unsupported input, duplicate ingestion, and high-volume determinism.
6. MCP and pipeline failures use machine-checkable error contracts (`errorCode`, `message`, `retryable`, `correlationId`).

## Test Cases

- `TC-S3-001`, `TC-S3-002`, `TC-S3-003`, `TC-S3-004`
- `TCN-S3-001`, `TCN-S3-002`, `TCE-S3-001`
- `TC-S4-001`, `TC-S4-002`, `TC-S4-003`, `TC-S4-004`
- `TCN-S4-001`, `TCN-S4-002`, `TCE-S4-001`
- `TC-S5-001`, `TC-S5-002`, `TC-S5-003`, `TC-S5-004`
- `TCN-S5-001`, `TCN-S5-002`, `TCE-S5-001`

## Owner

TBD

## Status

todo
