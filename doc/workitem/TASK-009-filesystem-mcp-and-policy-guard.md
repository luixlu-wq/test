# TASK-009 Filesystem MCP And Policy Guard

## Type

task

## Description

Implement filesystem MCP read/write operations with policy-safe path checks.

## Scope

- list/read/write operations
- path traversal prevention
- audit details in response envelope

## Dependencies

- `STORY-005-mcp-core-set.md`

## Story Link

- `STORY-005-mcp-core-set.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 2

## Acceptance Criteria

1. Path traversal attempts are blocked.
2. Successful operations return envelope-compliant audit metadata.

## Test Cases

- `TC-S3-001`

## Owner

TBD

## Status

todo
