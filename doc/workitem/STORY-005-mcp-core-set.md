# STORY-005 MCP Core Set

## Type

story

## Description

Implement the minimum MCP tool surface needed for current-stage ingestion and triggering.

## Scope

- Filesystem MCP
- Document Parser MCP
- Browser Reader MCP
- Trigger MCP
- shared request/response/error envelopes

## Dependencies

- `EPIC-001-spec-and-backbone.md`

## Acceptance Criteria

1. MCP operations enforce schema and policy constraints.
2. Filesystem MCP path traversal is blocked.
3. Browser Reader supports read-only snapshots and cache.

## Test Cases

- `TC-S3-001`
- `TC-S3-002`
- `TC-S3-003`
- `TC-S3-004`

## Owner

TBD

## Status

todo
