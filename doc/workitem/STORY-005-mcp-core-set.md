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

## Sprint Candidate

- Sprint 2

## Story Points

8

## Technical Context

- **MCP envelope standard**: `MCP contract implementation.md` §4 — all MCPs share: `mcpVersion`, `requestId`, `operation`, `params`, `policyContext` (request); `result`, `errorCode`, `retryable`, `warnings`, `auditDetail` (response)
- **Timeout contracts**: `MCP contract implementation.md` §4.8 — Filesystem 5s, Document Parser 30s, Browser Reader 60s, Trigger MCP 10s; all emit `TIMEOUT` with `retryable: true`
- **Error codes**: `MCP contract implementation.md` §4.9 — universal codes: `SCHEMA_VALIDATION_ERROR`, `POLICY_VIOLATION`, `TIMEOUT`, `AUTH_PROFILE_NOT_FOUND`; per-MCP codes defined in §§5–8
- **Filesystem MCP**: `MCP contract implementation.md` §5 — operations: `fs.list`, `fs.read`, `fs.write`; path traversal blocked (`..` components rejected with `PATH_TRAVERSAL_BLOCKED`); `auditDetail` includes `resolved_path`, `operation_type`
- **Document Parser MCP**: `MCP contract implementation.md` §6 — operations: `doc.parse`; extracts headings, acceptance criteria, tables; output normalized to `ParsedDocument` model; two-stage vision pipeline for images: Claude Vision (`claude-sonnet-4-6`) + Tesseract OCR v5+ (`RAG implementation design.md` §9.6)
- **Browser Reader MCP**: `MCP contract implementation.md` §7 — `browser.capture_snapshot`: read-only; returns `text_content`, `dom_ref`, `screenshot_ref`; cache key = `SHA-256(url + viewport + timestamp_bucket)`
- **Trigger MCP**: `MCP contract implementation.md` §8 — `trigger.dispatch`: accepts `trigger_type` (manual/webhook/shift_left), validates envelope, enqueues to Redis Streams `workflow.trigger` stream
- **Policy guard**: every MCP checks `policyContext` via `PolicyEvaluator` before executing; `POLICY_VIOLATION` returned without executing the operation

## Acceptance Criteria

1. All four MCPs validate their request envelopes against the shared schema; malformed requests return `SCHEMA_VALIDATION_ERROR` with the offending field path before any operation executes.
2. Filesystem MCP blocks path traversal attempts (`..` in any path component) with `PATH_TRAVERSAL_BLOCKED` error; legitimate read operations return `auditDetail` with `resolved_path`.
3. Browser Reader MCP returns read-only snapshots with deterministic cache behavior: two requests with the same URL, viewport, and timestamp bucket return the same `cache_key` and reuse the cached snapshot.

## Test Cases

- `TC-S3-001` — Filesystem MCP blocks traversal; valid read returns audit metadata
- `TC-S3-002` — Document Parser MCP extracts headings and criteria from markdown fixture
- `TC-S3-003` — Browser Reader returns snapshot with cache key; second call with same params hits cache
- `TC-S3-004` — Trigger MCP validates payload and enqueues workflow kickoff event to Redis Streams

## Definition of Done

- [ ] All four MCPs implement the shared envelope middleware
- [ ] Policy guard fires before any MCP operation; `POLICY_VIOLATION` tested
- [ ] Timeout enforcement in place for all MCPs (timeout values from §4.8)
- [ ] `TC-S3-001` through `TC-S3-004` pass in `integration` profile
- [ ] Contract tests pass for all MCPs in `ci` profile (stubs for external services)
- [ ] No credential storage in MCP code; credentials resolved via auth profile mechanism
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
