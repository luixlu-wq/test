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

## Story Points

2

## Technical Context

- **Operations**: `fs.list(path)`, `fs.read(path)`, `fs.write(path, content)` — `MCP contract implementation.md` §5
- **Path traversal prevention**: normalize path → resolve against allowed root → reject if resolved path escapes root directory; reject any component containing `..`, `~`, or null bytes; return `PATH_TRAVERSAL_BLOCKED` (retryable: false)
- **Allowed root**: configured via `AI_QA_FS_ALLOWED_ROOT` env var; not configurable at runtime; no credential storage in MCP
- **Audit detail fields**: `resolved_path` (normalized, absolute), `operation_type` (read/write/list), `file_size_bytes` (for read/write), `item_count` (for list)
- **Timeout**: 5 seconds — `MCP contract implementation.md` §4.8; returns `TIMEOUT` with `retryable: true`
- **Write policy**: `fs.write` only permitted when `policyContext.allowed_policies` includes `fs_write`; blocked with `POLICY_VIOLATION` otherwise

## Acceptance Criteria

1. Path traversal attempts (`../../etc/passwd`, paths with null bytes, paths escaping the allowed root) are blocked and return `PATH_TRAVERSAL_BLOCKED` without touching the filesystem.
2. Successful read/write/list operations return an envelope with `auditDetail` containing `resolved_path`, `operation_type`, and relevant size/count metadata.

## Test Cases

- `TC-S3-001` — Traversal attempt blocked; valid read returns complete `auditDetail`
- `TCN-S3-001` — Unsupported filesystem operation returns structured error contract without side effects
- `TCE-S3-001` — Large file read respects configured limits and emits overflow warning metadata

## Definition of Done

- [ ] All three operations implemented with shared envelope middleware
- [ ] Path normalization + root-escape check covers `..`, `~`, null bytes, and symlink escapes
- [ ] `policyContext` checked before any file I/O
- [ ] `TC-S3-001`, `TCN-S3-001`, `TCE-S3-001` pass in `integration` profile
- [ ] Unit tests for path normalization edge cases pass in `ci` profile
- [ ] Error payload contract validated: `errorCode`, `message`, `retryable`, `correlationId`

## Owner

TBD

## Status

todo
