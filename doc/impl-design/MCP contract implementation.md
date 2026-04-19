# Part 1 â€” MCP Contracts

## AI QA Platform

### Final Architecture-Aligned MCP Implementation

This document defines the **MCP contract layer** for the AI-powered QA platform.

Its role is to create a governed tool bus between:

* the **Agentic Control Plane**
  and
* the **Execution / Evidence / Data Plane**

This is one of the most important implementation boundaries in the system.

## Strategic principle: decoupling intelligence from action

The platform must strictly separate:

* **agents**, which provide reasoning, planning, mapping, and judgment
* **MCP tools**, which provide controlled access to files, browser state, execution, evidence, graph context, test state, and persistence

This separation prevents â€œhallucinated actionsâ€ because no agent can act outside:

* approved operations
* approved schemas
* policy-enforced tool contracts

In practice, this means:

* agents do not directly browse filesystems
* agents do not directly click browsers
* agents do not directly mutate approved assets
* agents do not directly persist healing or playbook promotions
* agents do not directly create hidden side effects

They act through MCP.

---

# 1. MCP design goals

The MCP layer must make all important platform capabilities:

* standardized
* auditable
* permission-controlled
* traceable
* replaceable
* safe for agent use
* compatible with distributed understanding
* compatible with Graph-RAG
* compatible with semantic state maps
* compatible with `draft` (pre-dispatch), `diagnostic`, and `regression` execution semantics

It must support the final architectureâ€™s major ideas:

* manual folder-first ingestion
* browser-readable source ingestion
* semantic state map generation
* mismatch detection
* Graph-RAG context building
* deterministic browser/API execution
* forensic evidence
* forensic self-healing
* deterministic playbook export
* local shift-left triggers

---

# 2. Required MCP set

The current-stage platform requires these **16 MCPs**:

1. **Filesystem MCP**
2. **Document Parser MCP**
3. **Browser Reader MCP**
4. **State Map MCP**
5. **Mismatch Detection MCP**
6. **Retrieval MCP**
7. **Graph Expansion MCP**
8. **Context Pack MCP**
9. **Browser Automation MCP**
10. **API Runner MCP**
11. **Evidence MCP**
12. **Healing MCP**
13. **Playbook MCP**
14. **State Management MCP**
15. **Test Asset MCP**
16. **Trigger MCP**

Deferred MCPs for later stages:

* Figma native MCP
* Jira / Azure DevOps native MCP
* PR diff MCP
* crawler / discovery MCP
* test management sync MCP

---

# 3. Common contract envelope

All MCP tools should use the same request/response/error envelope.

## 3.1 Common request envelope

```json
{
  "requestId": "REQ-1001",
  "runId": "RUN-3001",
  "caseId": "CASE-101",
  "agentId": "strategy-agent",
  "toolCallId": "TOOL-9001",
  "timestamp": "2026-04-18T14:10:00Z",
  "policyProfile": "standard-controlled",
  "executionMode": "diagnostic",
  "payload": {}
}
```

## 3.2 Common response envelope

```json
{
  "toolCallId": "TOOL-9001",
  "mcpVersion": "v1.2.0",
  "status": "success",
  "timestamp": "2026-04-18T14:10:02Z",
  "data": {},
  "warnings": [],
  "audit": {
    "durationMs": 1820,
    "target": "filesystem:/test/case/login-flow",
    "action": "read"
  }
}
```

## 3.3 Common error envelope

```json
{
  "toolCallId": "TOOL-9001",
  "mcpVersion": "v1.2.0",
  "status": "error",
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "case.yaml not found",
    "retryable": false,
    "details": {
      "path": "/test/case/login-flow/case.yaml"
    }
  },
  "audit": {
    "durationMs": 110
  }
}
```

---

# 4. Shared contract conventions

## 4.1 Security fields

Every tool request should support:

* `authProfile`
* `environment`
* `permissionsScope`
* `readOnly`

### Auth profile resolution

The `authProfile` field is a **string key** â€” never a credential value. Credentials are never passed through the MCP envelope or stored in agent inputs.

Resolution flow:

1. The MCP implementation receives `authProfile: "uat-service-account"` in the request.
2. It resolves the key at call time against the platform's **credential store** (environment variable set, secrets manager, or encrypted config â€” determined by the deployment profile: `local-dev` uses env vars; `uat`/`ist`/`prod` use a secrets manager such as AWS Secrets Manager or HashiCorp Vault).
3. The resolved credential is used for the operation and is **never logged, returned, or included in any output payload**.
4. If the `authProfile` key cannot be resolved, the MCP must return `error.code = "AUTH_PROFILE_NOT_FOUND"` â€” it must not silently fall back to unauthenticated access.
5. `permissionsScope` is checked after resolution to ensure the resolved credential is authorized for the requested `environment` and operation type. If scope check fails, return `error.code = "PERMISSION_DENIED"`.

The mapping of `authProfile` key â†’ credential reference lives in `environment_profile.auth_profile` (data model section 32.1). MCPs must not maintain their own credential registries.

## 4.2 Provenance fields

Every tool output should preserve provenance.

For context-producing tools, provenance should support:

* `artifactId`
* `chunkId`
* `requirementRefs`
* `flowRefs`
* `pageRefs`
* `stateRefs`
* `apiRefs`
* `stateMapId`
* `mismatchRefs`
* `playbookRefs`
* `evidenceRefs`

## 4.3 Evidence refs, not blobs

Large artifacts should usually be returned as refs, not inlined raw payloads.

## 4.4 Confidence support

Interpretive tools should return:

* `confidence`
* `confidenceReason`

This is especially important for:

* browser page interpretation
* document extraction
* state map generation
* mismatch detection
* visual comparison
* healing proposals

## 4.5 Forensic score support

Healing-related outputs should also support:

* `forensicScore`
* `reviewThresholdUsed`
* `requiresReview`

This adopts Geminiâ€™s idea, but with the threshold driven by policy rather than hardcoded globally.

## 4.6 Execution mode support

Execution-related tools must respect:

* `draft`
* `diagnostic`
* `regression`

### Draft mode

Used for pre-dispatch preparation only (asset preparation, retrieval/context build, validation).

Rules:

* execution MCPs (`Browser Automation MCP`, `API Runner MCP`) must reject direct run attempts in `draft` mode
* preparation MCPs may process draft inputs
* transitioning from `draft` to runnable state is controlled by orchestration + policy

### Diagnostic mode

May allow:

* richer evidence
* exploratory state discovery
* healing analysis
* playbook export candidates

### Regression mode

Must remain:

* deterministic
* bounded
* non-exploratory
* approval-aware

## 4.7 Visual anchor convention

This is an important refinement.

UI-seeing tools should support a shared **visual anchor** concept.

A visual anchor may contain:

* approximate coordinates or region
* nearby labels/text
* layout neighborhood
* semantic role guess
* linked state-map identity
* linked fingerprint ref where available

This should be used consistently by:

* Browser Reader MCP
* Healing MCP
* optionally Evidence MCP

That creates one visual language between:

* what the system â€œseesâ€ while reading requirements
* what the system â€œseesâ€ while healing runtime UI shifts

## 4.8 Timeout contracts

Every MCP operation must have a defined timeout. If the operation does not complete within the timeout, the MCP returns `error.code = â€œTIMEOUTâ€` with `retryable: true`. The caller (Agent Runtime Service or Orchestration Service) is responsible for retry logic â€” the MCP does not retry internally.

| MCP                    | Default timeout | Notes                                                                          |
| ---------------------- | --------------- | ------------------------------------------------------------------------------ |
| Filesystem MCP         | 5s              | File I/O; abnormal if exceeded                                                 |
| Document Parser MCP    | 30s             | Large PDFs or complex DOCX may approach limit                                  |
| Browser Reader MCP     | 45s             | Page render + screenshot + extraction; JavaScript-heavy pages may need full 45s |
| State Map MCP          | 60s             | Multi-artifact fusion can be slow                                               |
| Mismatch Detection MCP | 30s             |                                                                                |
| Retrieval MCP          | 10s             | If exceeded, likely index or query issue                                        |
| Graph Expansion MCP    | 10s             | Bounded traversal should be fast; timeout indicates runaway query               |
| Context Pack MCP       | 15s             | Combines retrieval + expansion + assembly                                       |
| Browser Automation MCP | 120s            | Per `execute_steps` call; individual step timeout managed inside the operation  |
| API Runner MCP         | 30s             | Per `execute_request`; includes network roundtrip                              |
| Evidence MCP           | 20s             | Storage write; large artifacts may approach limit                               |
| Healing MCP            | 30s             | DOM scan + fingerprint comparison                                               |
| Playbook MCP           | 15s             |                                                                                |
| State Management MCP   | 45s             | Data seeding/reset operations may require DB roundtrips                         |
| Test Asset MCP         | 10s             |                                                                                |
| Trigger MCP            | 15s             | Graph impact analysis is the slow part                                          |

Callers must not assume completion before the timeout expires. Long-running operations (Browser Automation, State Map, State Management) should be treated as async-capable: the MCP may return a job ID immediately and expose a polling or callback mechanism in a future version.

## 4.9 Error codes and retryability

The `error.code` field in the common error envelope uses string codes from the following registry. Each code carries a fixed `retryable` value unless overridden by context.

### Universal codes (all MCPs)

| Code                      | Retryable | Meaning                                                                    |
| ------------------------- | --------- | -------------------------------------------------------------------------- |
| `TIMEOUT`                 | true      | Operation did not complete within the defined timeout window               |
| `AUTH_PROFILE_NOT_FOUND`  | false     | The `authProfile` key could not be resolved from the credential store      |
| `PERMISSION_DENIED`       | false     | Resolved credential lacks the required scope for this operation            |
| `INVALID_INPUT`           | false     | Request payload failed schema validation                                   |
| `POLICY_BLOCKED`          | false     | Policy profile rejected the operation (e.g. diagnostic mode in PROD env)  |
| `ENVIRONMENT_NOT_FOUND`   | false     | The specified `environment` is not registered in `environment_profile`     |
| `INTERNAL_ERROR`          | true      | Unexpected internal failure; safe to retry with backoff                    |
| `RATE_LIMITED`            | true      | Downstream resource is rate-limiting; retry after `retryAfterMs`          |

### MCP-specific codes

| MCP                    | Code                         | Retryable | Meaning                                                          |
| ---------------------- | ---------------------------- | --------- | ---------------------------------------------------------------- |
| Filesystem MCP         | `FILE_NOT_FOUND`             | false     | Specified path does not exist                                    |
| Filesystem MCP         | `PATH_NOT_ALLOWED`           | false     | Path is outside approved case root or generated/ directory       |
| Filesystem MCP         | `WRITE_REJECTED`             | false     | Write attempted to a non-generated/ path                         |
| Document Parser MCP    | `UNSUPPORTED_FORMAT`         | false     | File type not in supported list                                  |
| Document Parser MCP    | `PARSE_FAILED`               | false     | Document could not be parsed; may indicate corrupt file          |
| Browser Reader MCP     | `PAGE_NOT_REACHABLE`         | true      | URL returned connection error; retry may resolve transient issue |
| Browser Reader MCP     | `AUTH_FAILED`                | false     | Authentication to the target URL failed                          |
| Browser Reader MCP     | `DOMAIN_NOT_APPROVED`        | false     | Target URL domain is not in the approved domain list             |
| State Map MCP          | `STATE_MAP_NOT_FOUND`        | false     | Requested `stateMapId` does not exist                            |
| State Map MCP          | `ARTIFACT_REF_MISSING`       | false     | One or more artifact refs not found in store                     |
| Mismatch Detection MCP | `NO_ARTIFACTS_TO_COMPARE`    | false     | Fewer than two artifact refs provided for comparison             |
| Retrieval MCP          | `INDEX_NOT_READY`            | true      | Index is being built; retry after delay                          |
| Retrieval MCP          | `NO_RESULTS`                 | false     | Search returned zero candidates; not an error, just empty        |
| Graph Expansion MCP    | `NODE_NOT_FOUND`             | false     | Seed node ID not found in the graph                              |
| Graph Expansion MCP    | `DEPTH_EXCEEDED`             | false     | `maxDepth` exceeded the per-policy cap                           |
| Browser Automation MCP | `SESSION_NOT_FOUND`          | false     | `sessionId` does not correspond to an active session             |
| Browser Automation MCP | `STEP_ASSERTION_FAILED`      | false     | An assertion step failed; this is a test result, not an error    |
| Browser Automation MCP | `STATE_SIGNAL_TIMEOUT`       | true      | `wait_for_state_signal` timed out; may retry if transient        |
| API Runner MCP         | `ENDPOINT_UNREACHABLE`       | true      | HTTP connection failed; retry may resolve                        |
| API Runner MCP         | `ASSERTION_FAILED`           | false     | API response did not match expected assertion                    |
| Evidence MCP           | `STORAGE_WRITE_FAILED`       | true      | Object storage write failed; safe to retry                       |
| Evidence MCP           | `EVIDENCE_NOT_FOUND`         | false     | Requested `evidenceId` does not exist                            |
| Healing MCP            | `FINGERPRINT_NOT_FOUND`      | false     | `fingerprintRef` not found                                       |
| Healing MCP            | `NO_CANDIDATE_FOUND`         | false     | Forensic scan found no plausible replacement; not an error       |
| Playbook MCP           | `PLAYBOOK_NOT_FOUND`         | false     | `playbookId` not found                                           |
| Playbook MCP           | `PROMOTION_BLOCKED`          | false     | Policy blocked playbook promotion (review required)              |
| State Management MCP   | `PRECONDITION_FAILED`        | false     | Verified preconditions were not met; run cannot proceed          |
| State Management MCP   | `SETUP_FAILED`               | true      | Data seeding failed; may retry if transient DB issue             |
| Test Asset MCP         | `ASSET_NOT_FOUND`            | false     | `testAssetId` not found                                          |
| Test Asset MCP         | `STATUS_TRANSITION_INVALID`  | false     | Requested status transition not allowed by lifecycle rules       |
| Trigger MCP            | `NO_AFFECTED_CASES`          | false     | No cases were affected by the changed files; trigger is a no-op  |

The `retryable: true` codes should be retried with **exponential backoff** (base 1s, max 30s, max 3 attempts) unless the error payload includes a `retryAfterMs` field, in which case that value takes precedence.

---

# 5. Filesystem MCP

## Purpose

Provide safe access to local case folders and generated asset storage.

## Responsibilities

* list case files
* read files
* write generated artifacts
* validate folder structure
* fetch metadata/checksum

## Operations

* `fs.list_case_files`
* `fs.read_file`
* `fs.write_generated_asset`
* `fs.validate_case_structure`

## Example: `fs.list_case_files`

```json
{
  "payload": {
    "caseName": "login-flow",
    "rootPath": "/test/case/login-flow",
    "recursive": true,
    "includeMetadata": true
  }
}
```

## Policy constraints

* read allowed in Tier 0
* write only to approved `generated/` directories
* no delete in current stage

## Why it matters

This MCP is the foundation for local data sovereignty and folder-first operation.

---

# 6. Document Parser MCP

## Purpose

Convert raw documents into structured content for ingestion, fusion, state-map generation, and RAG.

## Responsibilities

* parse documents into structured sections
* extract entities
* extract requirements, rules, expected results, steps
* support chunk-ready outputs
* preserve source references

## Supported sources

* markdown
* txt
* yaml/json
* docx
* pdf
* html snapshots
* test templates

## Operations

* `doc.parse_document`
* `doc.chunk_document`
* `doc.extract_requirements`
* `doc.extract_chunk_metadata`

## Policy constraints

* read-only
* no mutation of source docs
* parser output must preserve provenance

## Why it matters

This is one of the two foundation MCPs you should build first.

---

# 7. Browser Reader MCP

## Purpose

Read browser-accessible external sources before native integrations exist.

## Responsibilities

* open authenticated URLs
* render page
* extract visible text
* capture DOM snapshot
* capture screenshot
* return structured page summary
* normalize content for RAG
* provide visible-truth evidence for artifact fusion
* produce visual anchors where useful

## Operations

* `browser.read_page`
* `browser.extract_structured_page`
* `browser.normalize_page_for_rag`
* `browser.capture_visual_reference`
* `browser.extract_visual_anchors`

## Example: `browser.extract_visual_anchors`

```json
{
  "data": {
    "pageRef": "PAGE-301",
    "anchors": [
      {
        "anchorId": "VA-1001",
        "name": "Submit Button",
        "region": {"x": 420, "y": 580, "w": 140, "h": 44},
        "nearbyText": ["Password", "Forgot password?"],
        "semanticRole": "submit_login",
        "stateMapElementRef": "EL-1001"
      }
    ]
  }
}
```

## Policy constraints

* read-only in current stage
* no destructive or submit-style actions
* approved domains only
* authenticated sessions must use approved profiles

## Why it matters

This separates **reading** from **automation**, which is correct and important.

---

# 8. State Map MCP

## Purpose

Generate and manage the **semantic state map** from fused artifacts.

## Responsibilities

* build page/state/element models
* derive expected states and transitions
* link requirements to states
* link states to likely APIs and validations
* return machine-usable semantic maps

## Operations

* `state_map.generate`
* `state_map.get`
* `state_map.list_by_case`
* `state_map.link_requirements`

## Example: `state_map.generate`

```json
{
  "payload": {
    "caseId": "CASE-101",
    "artifactRefs": ["ART-201", "ART-205", "ART-210"],
    "sourceRefs": ["CHUNK-9001", "CHUNK-9002"],
    "mode": "fused"
  }
}
```

## Policy constraints

* preserve source refs
* no mutation of approved state maps without versioning
* confidence required when inference is indirect

## Why it matters

This is the â€œcommon knowledgeâ€ layer that keeps understanding, mapping, and execution synchronized.

---

# 9. Mismatch Detection MCP

## Purpose

Detect requirement mismatches across fused artifacts before execution.

## Responsibilities

* compare story vs wireframe
* compare wireframe vs screenshot
* compare requirement vs state map
* compare expected result vs observable UI/API evidence
* surface warnings before generation or execution

## Operations

* `mismatch.detect`
* `mismatch.validate_before_execution`

## Example: `mismatch.detect`

```json
{
  "payload": {
    "caseId": "CASE-101",
    "stateMapId": "STATEMAP-1001",
    "artifactRefs": ["ART-201", "ART-205", "ART-210"]
  }
}
```

## Policy constraints

* read-only
* blocking behavior must be policy-governed
* every mismatch must include source refs

## Why it matters

This prevents test generation from silently drifting on contradictory inputs.

---

# 10. Retrieval MCP

## Purpose

Provide hybrid search over indexed QA knowledge.

## Responsibilities

* search artifact chunks
* search approved test asset summaries
* search prior run summaries
* search known defects and defect drafts
* search state-map summaries
* search mismatch summaries
* search healing summaries where allowed
* search playbook summaries where allowed
* apply metadata filters
* support keyword, vector, and hybrid retrieval

## Operations

* `retrieval.search`
* `retrieval.search_by_refs`
* `retrieval.index_chunks`
* `retrieval.delete_or_reindex_refs`
* `retrieval.search_state_aware`

## Policy constraints

* agent-facing search is read-only
* indexing only from approved ingestion paths
* case/environment/policy boundaries must be enforced

## Why it matters

This is the search front-end of Graph-RAG.

---

# 11. Graph Expansion MCP

## Purpose

Provide bounded graph traversal to enrich retrieval and support impact analysis.

## Responsibilities

* expand retrieved refs into linked entities
* traverse bounded relationship sets
* support lineage lookup
* support impact analysis
* expand requirement â†” state â†” page â†” API â†” test neighborhoods
* avoid unbounded graph walks

## Operations

* `graph.expand_context`
* `graph.trace_lineage`
* `graph.find_related_entities`
* `graph.expand_state_context`
* `graph.impact_analysis`

## Example: `graph.impact_analysis`

```json
{
  "payload": {
    "changedRefs": [
      "src/components/LoginForm.tsx",
      "src/pages/login.tsx"
    ],
    "maxDepth": 2
  }
}
```

## Policy constraints

* max depth enforced
* relationship allowlist enforced
* traversal should be case-aware where possible

## Why it matters

This is how Trigger MCP reduces noise using graph-backed impact analysis.

---

# 12. Context Pack MCP

## Purpose

Build task-specific grounded context packs for agents.

## Responsibilities

* combine search and graph expansion results
* rerank selected context
* enforce task-specific limits
* format agent-ready context
* preserve source refs, state refs, mismatch refs, conflicts, gaps, and playbook refs

## Operations

* `context.build_pack`
* `context.build_pack_from_refs`
* `context.log_pack`
* `context.build_pack_for_mode`

## Policy constraints

* bounded pack size
* sensitive content masking/filtering
* regression packs should favor approved assets and approved playbooks

## Why it matters

This is the final bounded input into agent prompts.

---

# 13. Browser Automation MCP

## Purpose

Execute web UI tests in a controlled browser runtime.

## Responsibilities

* launch browser sessions
* navigate
* interact
* assert states
* capture evidence
* return structured step results
* respect execution mode

## Operations

* `web.start_session`
* `web.execute_steps`
* `web.assert_state`
* `web.capture_artifacts`
* `web.end_session`
* `web.wait_for_state_signal`
* `web.capture_visual_diff`

## Example: `web.wait_for_state_signal`

```json
{
  "payload": {
    "sessionId": "WEB-SESSION-001",
    "signalType": "spinner_disappeared",
    "targetRef": "STATE-login-loading-complete",
    "timeoutMs": 10000
  }
}
```

## Policy constraints

* approved environments only
* approved auth profiles only
* destructive actions may require escalation
* regression mode must remain deterministic

## Why it matters

This is the execution-side counterpart to State Map MCP.

---

# 14. API Runner MCP

## Purpose

Execute API integration tests with controlled auth, assertions, and evidence.

## Responsibilities

* call endpoints
* manage auth/session
* validate responses
* support setup/cleanup
* capture evidence
* support linkage to semantic state expectations where relevant

## Operations

* `api.start_context`
* `api.execute_request`
* `api.assert_response`
* `api.end_context`

## Policy constraints

* secrets masked in outputs
* approved domains only
* write/delete actions governed by policy

## Why it matters

This gives the platform first-class API QA alongside web QA.

---

# 15. Evidence MCP

## Purpose

Store and retrieve forensic-grade execution evidence in a normalized way.

## Responsibilities

* persist screenshots
* persist traces/videos
* persist logs
* persist request/response snapshots
* issue evidence refs
* retrieve bundles
* create retrieval-friendly evidence summaries
* support semantic trace output
* support reasoning log output
* support visual diff output

## Operations

* `evidence.store`
* `evidence.get`
* `evidence.bundle_run`
* `evidence.summarize_for_retrieval`
* `evidence.write_semantic_trace`
* `evidence.write_reasoning_log`
* `evidence.store_visual_diff`

## Semantic Trace

The semantic trace is a first-class forensic artifact. It is the chain-of-evidence record that links a requirement through the execution to the observed outcome.

### `evidence.write_semantic_trace` payload

```json
{
  "payload": {
    "runId": "RUN-3001",
    "runStepId": "RUNSTEP-1001",
    "caseId": "CASE-101",
    "trace": {
      "requirementRef": "REQ-501",
      "requirementText": "User can sign in with valid credentials",
      "flowRef": "FLOW-1001",
      "pageRef": "PAGE-301",
      "stateRef": "STATE-LOGIN-READY",
      "transitionRef": "TRANS-1001",
      "targetStateRef": "STATE-DASHBOARD-STABLE",
      "executedAction": {
        "actionType": "click",
        "targetLocator": "getByRole('button', { name: 'Sign in' })",
        "fingerprintRef": "FPV-1002"
      },
      "observedOutcome": {
        "outcomeType": "state_reached",
        "stateRef": "STATE-DASHBOARD-STABLE",
        "confidence": 0.97,
        "evidenceRefs": ["EV-1001", "EV-1002"]
      },
      "verdict": "pass",
      "notes": "State signal 'route_stable' observed within 320ms of click."
    }
  }
}
```

### Semantic trace fields

| Field                                | Required | Notes                                                                          |
| ------------------------------------ | -------- | ------------------------------------------------------------------------------ |
| `runId`                              | Yes      |                                                                                |
| `runStepId`                          | Yes      | The step this trace covers                                                     |
| `trace.requirementRef`               | Yes      | The requirement being validated by this step                                   |
| `trace.requirementText`              | Yes      | Snapshot of requirement text at time of execution                              |
| `trace.flowRef`                      | No       | Flow containing this step                                                      |
| `trace.pageRef`                      | No       | Page the action occurred on                                                    |
| `trace.stateRef`                     | No       | UI state before the action                                                     |
| `trace.transitionRef`                | No       | Transition being exercised                                                     |
| `trace.targetStateRef`               | No       | Expected state after the action                                                |
| `trace.executedAction.actionType`    | Yes      | `navigate`, `fill`, `click`, `assert`, `wait_for_state_signal`, `api_call`     |
| `trace.executedAction.targetLocator` | No       | Playwright locator or API endpoint used                                        |
| `trace.executedAction.fingerprintRef`| No       | Fingerprint version used for locator resolution                                |
| `trace.observedOutcome.outcomeType`  | Yes      | `state_reached`, `assertion_passed`, `assertion_failed`, `state_not_reached`   |
| `trace.observedOutcome.confidence`   | No       | Confidence that the observed outcome matches the expected outcome               |
| `trace.observedOutcome.evidenceRefs` | Yes      | At least one screenshot or DOM snapshot evidence ref must be included          |
| `trace.verdict`                      | Yes      | `pass`, `fail`, `skip`                                                         |
| `trace.notes`                        | No       | Free text â€” e.g. state signal timing, healing decision notes                  |

A semantic trace record must be written for every `RunStep` where `action_type = "assert"` or `action_type = "wait_for_state_signal"`. It is optional but recommended for `click` and `fill` steps on critical paths.

## Policy constraints

* evidence immutable once finalized
* reasoning logs must avoid secrets
* large artifacts returned by ref, not embedded

## Why it matters

This is what makes failures explainable, not just executable.

---

# 16. Healing MCP

## Purpose

Provide controlled forensic self-healing analysis and persistent healing logs.

## Responsibilities

* analyze broken locators/interactions
* compare element fingerprints
* use visual anchors where available
* perform forensic scan against current DOM
* generate healing proposals
* persist healing logs
* support human hardening workflow

## Operations

* `healing.generate_fingerprint`
* `healing.forensic_scan`
* `healing.write_log`
* `healing.list_history`

## Example: `healing.forensic_scan`

```json
{
  "payload": {
    "sessionId": "WEB-SESSION-001",
    "originalTarget": "button[type='submit']",
    "fingerprintRef": "FP-1001",
    "stateMapId": "STATEMAP-1001",
    "visualAnchorRefs": ["VA-1001"]
  }
}
```

## Example response

```json
{
  "data": {
    "proposedTarget": "getByRole('button', { name: 'Sign in' })",
    "confidence": 0.92,
    "forensicScore": 0.92,
    "confidenceReason": "Matched role, text family, DOM neighborhood, page context, and visual anchor.",
    "requiresReview": true,
    "reviewThresholdUsed": 0.95
  }
}
```

## `healing.write_log` should persist

* original target
* proposed target
* fingerprint ref
* forensic score
* threshold used
* requiresReview
* policy profile
* evidence refs

## Policy constraints

* healing must not silently rewrite approved tests
* persistent updates require governance
* threshold is policy-driven, not universally hardcoded

## Why it matters

This is the controlled human-in-the-loop gate for self-healing.

---

# 17. Playbook MCP

## Purpose

Store and export deterministic playbooks discovered in diagnostic mode.

## Responsibilities

* capture discovered state signals
* store stable wait conditions
* store safe action sequences
* export deterministic playbooks for regression use
* support governed promotion

## Operations

* `playbook.export_from_run`
* `playbook.get`
* `playbook.promote`
* `playbook.list_by_case`

## Policy constraints

* only successful or sufficiently reviewed diagnostic discoveries may be promoted
* regression mode should prefer approved playbooks

## Why it matters

This is how exploratory diagnostic knowledge becomes deterministic regression knowledge.

---

# 18. State Management MCP

## Purpose

Keep execution deterministic through controlled data and state lifecycle.

## Responsibilities

* verify preconditions
* create/reset test users
* seed data
* reset supported resources
* cleanup temporary state

## Operations

* `state.verify_preconditions`
* `state.setup_data`
* `state.cleanup_data`

## Policy constraints

* approved environments only
* safe actions only in current stage
* all state changes auditable

## Why it matters

Without this MCP, deterministic testing is not credible.

---

# 19. Test Asset MCP

## Purpose

Persist generated tests and related assets as governed artifacts.

## Responsibilities

* store draft tests
* version assets
* fetch approved asset versions
* promote lifecycle state
* attach metadata
* provide retrieval-friendly summaries
* link tests to playbooks, state maps, and healing history where relevant

## Operations

* `asset.create_test_asset`
* `asset.get_asset`
* `asset.update_status`
* `asset.list_assets_for_case`
* `asset.summarize_for_retrieval`
* `asset.link_playbook`
* `asset.link_state_map`

## Policy constraints

* promotion governed
* approved assets must preserve lineage

## Why it matters

This is the governance layer for generated QA assets.

---

# 20. Trigger MCP

## Purpose

Support local deterministic triggers such as pre-commit and watch mode.

## Responsibilities

* accept local trigger events
* classify trigger source
* map changed files to likely cases
* use graph-assisted impact analysis where available
* request targeted smoke execution
* preserve local workflow audit trail

## Operations

* `trigger.pre_commit`
* `trigger.watch_mode`
* `trigger.manual_local`

## Example: updated `trigger.pre_commit`

```json
{
  "payload": {
    "triggerSource": "pre_commit",
    "gitDiffFiles": [
      "src/components/LoginForm.tsx",
      "src/pages/login.tsx"
    ],
    "environment": "LOCAL"
  }
}
```

## Example response

```json
{
  "data": {
    "requestId": "REQ-LOCAL-1001",
    "affectedCases": ["login-flow"],
    "affectedPages": ["PAGE-301"],
    "affectedFlows": ["FLOW-1001"],
    "impactAnalysisMethod": "graph_assisted",
    "recommendedAction": "targeted_smoke_test"
  }
}
```

## Policy constraints

* watch mode opt-in
* pre-commit bounded by smoke scope unless policy expands it
* local triggers still respect environment and action restrictions

## Why it matters

This is the shift-left entry point for local-first workflow.

---

# 21. Audit and observability requirements

Every MCP tool must emit:

* request ID
* run ID
* case ID when applicable
* agent ID
* action name
* target
* start/end timestamps
* duration
* result status
* warnings
* policy decision outcome

RAG-related tools should also emit:

* query text or query hash
* filters
* selected refs
* candidate count
* context pack size

Healing / playbook / state-map tools should also emit:

* stateMapId
* mismatchIds if relevant
* fingerprintRef if relevant
* visualAnchorRefs if relevant
* healingLogRef if created
* playbookRef if created
* executionMode
* forensicScore if healing was evaluated

---

# 22. Policy matrix

| Tool                   | Read Only |                   Write | External Mutation | Current Stage |
| ---------------------- | --------: | ----------------------: | ----------------: | ------------- |
| Filesystem MCP         |       Yes |                 Limited |                No | Yes           |
| Document Parser MCP    |       Yes |                      No |                No | Yes           |
| Browser Reader MCP     |       Yes |                      No |                No | Yes           |
| State Map MCP          |       Yes |                     Yes |                No | Yes           |
| Mismatch Detection MCP |       Yes |                      No |                No | Yes           |
| Retrieval MCP          |       Yes | Limited indexing writes |                No | Yes           |
| Graph Expansion MCP    |       Yes |                      No |                No | Yes           |
| Context Pack MCP       |       Yes |                      No |                No | Yes           |
| Browser Automation MCP |        No |                     Yes |  In test app only | Yes           |
| API Runner MCP         |        No |                     Yes |  In test app only | Yes           |
| Evidence MCP           |        No |                     Yes |                No | Yes           |
| Healing MCP            |       Yes |                     Yes |                No | Yes           |
| Playbook MCP           |       Yes |                     Yes |                No | Yes           |
| State Management MCP   |        No |                     Yes |  In test env only | Yes           |
| Test Asset MCP         |        No |                     Yes |                No | Yes           |
| Trigger MCP            |       Yes |                     Yes |                No | Yes           |

---

# 23. MCP versioning strategy

MCP contracts must be versioned so that changes to operation schemas do not silently break calling services.

## 23.1 Version field

Every MCP operation response includes a `mcpVersion` field in the response envelope alongside `toolCallId` and `timestamp`:

```json
{
  "toolCallId": "TOOL-9001",
  "mcpVersion": "v1.2.0",
  "status": "success",
  "timestamp": "...",
  "data": {}
}
```

The `mcpVersion` is also stored in `tool_invocation_log.tool_version` (data model section 24.2).

## 23.2 Versioning scheme

MCP contracts use **semantic versioning**: `vMAJOR.MINOR.PATCH`.

| Increment | When to use                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------- |
| `PATCH`   | Internal fix â€” no change to request or response schema. Callers need not update.                       |
| `MINOR`   | New optional request fields or new optional response fields added. Backward-compatible. Callers may ignore new fields. |
| `MAJOR`   | Required request fields added, response fields removed or renamed, operation behavior semantically changed. Callers must update. |

## 23.3 Operation-level contracts

Each operation within an MCP is independently versioned. The MCP version declared in the envelope is the version of the highest-versioned operation in that MCP. Callers that only use lower-versioned operations are not affected by a `MINOR` bump driven by a different operation.

## 23.4 Breaking change protocol

When a `MAJOR` version is required:

1. The new version of the operation is added alongside the old version using an explicit `operationVersion` field in the request payload: `"operationVersion": "v2"`.
2. The old version is supported for one full sprint cycle before deprecation.
3. Deprecation is signaled by a `warnings` entry in the response: `"OPERATION_DEPRECATED: use operationVersion v2"`.
4. After the deprecation window, the old version returns `error.code = "OPERATION_VERSION_RETIRED"` with `retryable: false`.

## 23.5 Version registry

The canonical version for each MCP is declared in `api/mcp/registry.yaml`:

```yaml
mcps:
  filesystem:
    version: "1.0.0"
  document-parser:
    version: "1.0.0"
  browser-reader:
    version: "1.1.0"
  state-map:
    version: "1.0.0"
  evidence:
    version: "1.2.0"
  healing:
    version: "1.0.0"
  # ... remaining MCPs
```

The Agent Runtime Service reads this registry at startup. If a service calls an MCP at a version higher than the registered version, it must fail fast with a startup error rather than discovering the mismatch at call time.

---

# 24. Build order

The recommended first build steps are:

1. **Filesystem MCP**
2. **Document Parser MCP**
3. **Trigger MCP**

Then:
4. Browser Reader MCP
5. State Map MCP
6. Mismatch Detection MCP
7. Retrieval + Graph Expansion + Context Pack MCPs
8. Browser Automation + API Runner MCPs
9. Evidence MCP
10. Healing MCP
11. Playbook MCP
12. State Management MCP
13. Test Asset MCP

That build order is correct for the final architecture.

---

# 25. Final summary

This MCP layer is the governed â€œlanguage of qualityâ€ for the platform.

It gives you:

* **local-first data sovereignty** through Filesystem MCP
* **artifact fusion support** through Document Parser + Browser Reader + State Map MCP
* **state-aware React testing** through State Map MCP + Browser Automation MCP
* **Graph-RAG context building** through Retrieval + Graph Expansion + Context Pack MCPs
* **forensic evidence** through Evidence MCP and Semantic Trace
* **controlled self-healing** through Healing MCP
* **deterministic regression promotion** through Playbook MCP
* **deterministic test setup/cleanup** through State Management MCP
* **governed asset lifecycle** through Test Asset MCP
* **shift-left local execution** through Trigger MCP

