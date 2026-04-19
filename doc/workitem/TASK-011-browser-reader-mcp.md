# TASK-011 Browser Reader MCP

## Type

task

## Description

Implement read-only browser URL ingestion operation with snapshot and cache metadata.

## Scope

- fetch/read-only capture
- normalized text/dom/screenshot references
- cache key and reuse behavior

## Dependencies

- `STORY-005-mcp-core-set.md`

## Story Link

- `STORY-005-mcp-core-set.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 2

## Story Points

2

## Technical Context

- **Operation**: `browser.capture_snapshot(url, viewport, options)` — `MCP contract implementation.md` §7
- **Read-only enforcement**: no form submission, no navigation triggered by the MCP; Playwright launched in read-only mode (no `page.click()`, `page.fill()`); return `READ_ONLY_VIOLATION` if operation attempts mutation
- **Output refs**: `text_content` (extracted readable text), `dom_ref` (S3 key for full DOM snapshot), `screenshot_ref` (S3 key for viewport screenshot); refs are pointers into object storage, not inline content
- **Cache key**: `SHA-256(url + "|" + canonical_viewport + "|" + timestamp_bucket)` where `timestamp_bucket = floor(unix_time / cache_ttl_seconds)` (default TTL 300s); cache stored in Redis with key `browser_snapshot:{cache_key}`
- **Cache hit behavior**: return existing refs from Redis cache; `cache_hit: true` in response `auditDetail`; skip Playwright entirely
- **Timeout**: 60 seconds — `MCP contract implementation.md` §4.8; includes page load + screenshot capture
- **Playwright requirement**: `python -m playwright install chromium` (already in global setup — `detailed-implementation-plan.md` §2.3)

## Acceptance Criteria

1. Output includes `text_content`, `dom_ref`, `screenshot_ref` with source URL and viewport metadata in `auditDetail`.
2. Two requests with identical URL, viewport, and timestamp bucket return the same `cache_key` and reuse the cached snapshot without launching Playwright a second time (`cache_hit: true` in response).

## Test Cases

- `TC-S3-003` — Snapshot capture returns normalized refs; second call with same params returns `cache_hit: true`

## Definition of Done

- [ ] `browser.capture_snapshot` implemented with Playwright in read-only mode
- [ ] Cache key computed as specified; Redis cache lookup before Playwright launch
- [ ] `auditDetail` includes `cache_hit`, `url`, `viewport`, `timestamp_bucket`
- [ ] `READ_ONLY_VIOLATION` error returned if mutation operation detected
- [ ] In `ci` profile: Playwright stubbed; cache behavior tested with mock Redis
- [ ] `TC-S3-003` passes in `integration` profile

## Owner

TBD

## Status

todo
