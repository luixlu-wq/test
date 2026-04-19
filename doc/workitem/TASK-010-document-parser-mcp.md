# TASK-010 Document Parser MCP

## Type

task

## Description

Implement parser MCP for markdown and structured extraction used in understanding.

## Scope

- parse operation
- heading/criteria extraction
- normalized output model

## Dependencies

- `STORY-005-mcp-core-set.md`

## Story Link

- `STORY-005-mcp-core-set.md` (Primary: Scope + Acceptance Criteria)

## Sprint Candidate

- Sprint 2

## Story Points

2

## Technical Context

- **Operation**: `doc.parse(artifact_ref, content_type)` — `MCP contract implementation.md` §6
- **Supported content types**: `text/markdown`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`; return `UNSUPPORTED_CONTENT_TYPE` for others
- **Output model** (`ParsedDocument`): `artifact_ref`, `content_type`, `headings[]`, `sections[]`, `acceptance_criteria[]`, `tables[]`, `raw_text`, `extracted_images[]` (refs only, not content)
- **Image extraction pipeline** (two-stage): Claude Vision (`claude-sonnet-4-6`) for structural/semantic description + Tesseract OCR v5+ for verbatim text from screenshots/diagrams; combined output stored in `artifact_parse_result.extracted_json` — `RAG implementation design.md` §9.6
- **Acceptance criteria extraction**: Gherkin-style (`Given/When/Then`) and numbered list patterns; linked to the nearest parent heading as context
- **Source artifact metadata**: output must include `source_artifact_id` and `artifact_version` from the input ref; required for provenance tracing in understanding pipeline
- **Timeout**: 30 seconds — `MCP contract implementation.md` §4.8

## Acceptance Criteria

1. Parser extracts headings at all levels (H1–H6), acceptance criteria (numbered and Gherkin patterns), and table content from a markdown test fixture; all items reference the source artifact metadata.
2. Output `ParsedDocument` includes `source_artifact_id` and `artifact_version` from the input ref on every parsed item.

## Test Cases

- `TC-S3-002` — Document Parser extracts expected sections and criteria from markdown fixture with correct source refs

## Definition of Done

- [ ] `doc.parse` operation implemented for markdown and PDF (docx optional for Sprint 2)
- [ ] `ParsedDocument` output model schema-validated before return
- [ ] Source artifact metadata present on every output item
- [ ] Image extraction pipeline stubbed in `ci` profile (no Claude Vision or OCR calls)
- [ ] `TC-S3-002` passes in `integration` profile
- [ ] Unit tests for heading/criteria extraction pass in `ci` profile

## Owner

TBD

## Status

todo
