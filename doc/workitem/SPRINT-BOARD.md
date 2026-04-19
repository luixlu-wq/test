# Sprint Board

This board is derived from `BACKLOG.md` and the implementation plan.

## Team Capacity Placeholders

- Sprint length: 2 weeks
- Backend capacity: `TBD points`
- QA/automation capacity: `TBD points`
- Infra/devops capacity: `TBD points`
- Total capacity: `TBD points`

## Status Legend

- `todo`
- `in_progress`
- `blocked`
- `review`
- `done`

## Sprint 1

### Sprint Goal

Lock contracts and build the platform backbone with durable persistence and auditability.

### Stories

| Story | Status | Owner | Notes |
|---|---|---|---|
| `STORY-001-contract-and-enum-lock.md` | todo | TBD | Canonical schemas and enums |
| `STORY-002-request-trigger-orchestration.md` | todo | TBD | Idempotent orchestration flow |
| `STORY-003-policy-and-audit-foundation.md` | todo | TBD | Policy + audit baseline |
| `STORY-004-persistence-core-schema.md` | todo | TBD | Core migration and repository baseline |

### Tasks

| Task | Parent Story | Status | Owner |
|---|---|---|---|
| `TASK-001-schema-package-and-fixtures.md` | `STORY-001-contract-and-enum-lock.md` | todo | TBD |
| `TASK-002-canonical-enum-constants.md` | `STORY-001-contract-and-enum-lock.md` | todo | TBD |
| `TASK-015-tdr-registry-and-decision-records.md` | `STORY-001-contract-and-enum-lock.md` | todo | TBD |
| `TASK-003-request-dedup-key.md` | `STORY-002-request-trigger-orchestration.md` | todo | TBD |
| `TASK-004-workflow-state-machine.md` | `STORY-002-request-trigger-orchestration.md` | todo | TBD |
| `TASK-005-policy-decision-evaluator.md` | `STORY-003-policy-and-audit-foundation.md` | todo | TBD |
| `TASK-006-audit-correlation-logging.md` | `STORY-003-policy-and-audit-foundation.md` | todo | TBD |
| `TASK-007-core-migration-pack.md` | `STORY-004-persistence-core-schema.md` | todo | TBD |
| `TASK-008-repository-roundtrip-tests.md` | `STORY-004-persistence-core-schema.md` | todo | TBD |

## Sprint 2

### Sprint Goal

Deliver MCP ingestion foundation and understanding/state intelligence with mismatch gates.

### Stories

| Story | Status | Owner | Notes |
|---|---|---|---|
| `STORY-005-mcp-core-set.md` | todo | TBD | Filesystem/doc-parser/browser-reader/trigger MCP |
| `STORY-006-distributed-understanding-pipeline.md` | todo | TBD | Fusion + chunking + provenance |
| `STORY-007-semantic-state-and-mismatch.md` | todo | TBD | State map + mismatch severity/blocking |

### Tasks

| Task | Parent Story | Status | Owner |
|---|---|---|---|
| `TASK-009-filesystem-mcp-and-policy-guard.md` | `STORY-005-mcp-core-set.md` | todo | TBD |
| `TASK-010-document-parser-mcp.md` | `STORY-005-mcp-core-set.md` | todo | TBD |
| `TASK-011-browser-reader-mcp.md` | `STORY-005-mcp-core-set.md` | todo | TBD |
| `TASK-012-trigger-mcp.md` | `STORY-005-mcp-core-set.md` | todo | TBD |
| `TASK-013-understanding-fusion-engine.md` | `STORY-006-distributed-understanding-pipeline.md` | todo | TBD |
| `TASK-014-state-map-and-mismatch-engine.md` | `STORY-007-semantic-state-and-mismatch.md` | todo | TBD |

## Next Queue (Post Sprint 2)

- `STORY-008-graph-rag-foundation.md`
- `STORY-009-agent-runtime-and-prompt-governance.md`
- `STORY-010-test-asset-compiler-and-playwright-hybrid.md`
- `STORY-011-execution-state-and-evidence.md`
- `STORY-012-triage-defect-and-hitl.md`
- `STORY-013-healing-and-playbook-promotion.md`
- `STORY-014-ops-hardening-and-shift-left.md`
