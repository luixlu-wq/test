# STORY-010 Test Asset Compiler And Playwright Hybrid

## Type

story

## Description

Implement scenario-to-asset compilation and Playwright hybrid framework integration with trace metadata.

## Scope

- scenario compiler
- script generator integration
- metadata embedding
- selector profile and assertion mapping support

## Dependencies

- `STORY-009-agent-runtime-and-prompt-governance.md`

## Sprint Candidate

- Sprint 4

## Story Points

8

## Technical Context

- **Dual execution modes**: `data model design.md` §17.1 — `diagnostic` (agentic, exploratory) and `regression` (deterministic, compiled asset replay); compiler targets `regression` mode output
- **Playwright hybrid framework**: `playwrite hybride framework design.md` — abstraction layer above raw Playwright; selector profiles (CSS/ARIA/data-testid priority order); assertion helpers with built-in retry and timeout semantics
- **Compiled asset structure**: `test_asset` table (`data model design.md` §16) — `asset_type`, `script_ref` (S3 key), `metadata_ref`, `case_id`, `playbook_id`, `schema_version`; asset is immutable once approved
- **Metadata embedding**: every compiled script includes a header comment block with `case_id`, `playbook_id`, `asset_schema_version`, `generated_by_prompt_version`, `generated_at`; used for traceability and drift detection
- **Regression safety**: compiled regression scripts must not contain `page.waitForTimeout()`, `page.pause()`, or unbounded `waitFor*` loops; compiler rejects these with `UNSAFE_WAIT_PATTERN`
- **Selector profile mapping**: Authoring Agent (`agent prompts design.md` §6) outputs selector candidates ranked by stability; compiler applies the active `selector_profile` (e.g. `aria_first`, `testid_preferred`) to select the final selector
- **Asset compiler validation**: compiled script parsed by Python AST (or Playwright script validator); syntactically invalid output triggers `COMPILE_ERROR` without persisting the asset

## Acceptance Criteria

1. Compiled regression scripts are syntactically valid Playwright Python; invalid output (syntax error) triggers `COMPILE_ERROR` and the asset is not persisted.
2. Every compiled asset has embedded metadata including `case_id`, `playbook_id`, `asset_schema_version`, and `generated_by_prompt_version` in the script header.
3. Regression assets do not contain unsafe wait patterns (`waitForTimeout`, `pause`, unbounded loops); compiler blocks these with `UNSAFE_WAIT_PATTERN` error.

## Test Cases

- `TC-S8-001` — Syntactically valid compiled script passes AST validation and is persisted
- `TC-S8-002` — Metadata header fields present and correct in compiled output
- `TC-S8-003` — Script with `waitForTimeout` rejected with `UNSAFE_WAIT_PATTERN`
- `TC-S8-004` — Selector profile applied: ARIA selector prioritised over CSS when `aria_first` profile active

## Definition of Done

- [ ] Scenario compiler produces valid Playwright Python scripts
- [ ] AST validation runs before persist; `COMPILE_ERROR` on failure
- [ ] Metadata header embedded in every compiled script
- [ ] Unsafe wait pattern detection in place
- [ ] Selector profile mapping applied from active profile
- [ ] `TC-S8-001` through `TC-S8-004` pass; LLM calls stubbed in `ci` profile
- [ ] PR reviewed and merged; CI green

## Owner

TBD

## Status

todo
