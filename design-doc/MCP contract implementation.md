Below is the **rewritten Part 1 — MCP Contracts**, updated to match the **final architectural design**.

I kept the strong parts of your previous MCP design, especially:

* common contract envelope
* clear policy boundaries
* RAG-aware retrieval contracts
* evidence and asset governance

I updated it to reflect the architecture changes in these areas:

* **distributed understanding** instead of a single overloaded intake path
* **semantic state map** as a first-class output
* **requirement mismatch detection**
* **dual execution modes**: diagnostic vs regression
* **forensic self-healing**
* **persistent healing log**
* **deterministic playbook export**
* **forensic-grade evidence schema**
* **local trigger support** such as pre-commit hooks and optional watch mode

Your earlier MCP document was already strong on Graph-RAG, Retrieval MCP, Graph Expansion MCP, and Context Pack MCP. The main gap was that it did not yet expose the new architecture’s **state map**, **mismatch**, **healing**, **playbook**, and **local trigger** capabilities as first-class contracts. 

---

# Part 1 — MCP Contracts

## AI QA Platform

### Final Architecture-Aligned Version

This section defines the **tool contracts** between the agent layer and the execution/integration layer.

The goal of MCP in this system is to make every external or operational capability:

* standardized
* auditable
* replaceable
* permission-controlled
* safe for agent use
* compatible with **distributed understanding**
* compatible with **hybrid Graph-RAG**
* compatible with **deterministic and diagnostic execution modes**

In this architecture, agents should not directly perform raw file access, graph traversal, browser actions, API execution, state reset, healing persistence, evidence storage, or local trigger orchestration.
They should call MCP tools through well-defined contracts.

This updated version explicitly adds or strengthens:

* **State Map MCP**
* **Mismatch Detection MCP**
* **Healing MCP**
* **Playbook MCP**
* **Trigger MCP**
* stronger Evidence MCP for forensic-grade outputs

---

# 1. MCP Design Principles

## 1.1 Purpose

MCP contracts provide a standard interface for the platform to:

* read artifacts
* parse and chunk documents
* open browser-readable URLs
* normalize manual assets
* generate semantic state maps
* detect requirement mismatches
* index retrievable content
* search relevant context
* expand graph-linked context
* build task-specific context packs
* execute browser tests
* execute API tests
* manage test state
* store and retrieve forensic evidence
* analyze healing opportunities
* write healing logs
* export deterministic playbooks
* manage generated test assets
* support local triggers such as pre-commit and watch mode

---

## 1.2 Contract Style

Each MCP tool contract should define:

* **tool name**
* **purpose**
* **allowed actions**
* **input schema**
* **output schema**
* **error schema**
* **policy constraints**
* **audit metadata**
* **provenance requirements**
* **traceability requirements**
* **execution-mode relevance**, where applicable

---

## 1.3 Common Contract Envelope

All MCP tools should use a common request/response structure.

### Common request envelope

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

### Common response envelope

```json
{
  "toolCallId": "TOOL-9001",
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

### Common error envelope

```json
{
  "toolCallId": "TOOL-9001",
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

# 2. Shared Contract Conventions

## 2.1 Security fields

Every tool request should support:

* `authProfile`
* `environment`
* `permissionsScope`
* `readOnly`

Example:

```json
{
  "environment": "UAT",
  "authProfile": "qa-automation-user",
  "permissionsScope": ["read:files", "execute:web"],
  "readOnly": true
}
```

---

## 2.2 Provenance fields

Every tool output should preserve provenance.

```json
{
  "sourceType": "folder",
  "sourcePath": "/test/case/login-flow/stories/US-101.md",
  "sourceUrl": null,
  "capturedAt": "2026-04-18T14:12:00Z"
}
```

For RAG-aware and state-aware tools, provenance should also support:

* `artifactId`
* `chunkId`
* `requirementRefs`
* `flowRefs`
* `pageRefs`
* `apiRefs`
* `stateMapId`
* `evidenceRefs`

---

## 2.3 Evidence references

When a tool creates evidence, it should return references instead of raw blobs whenever possible:

```json
{
  "evidenceRefs": [
    "evidence://RUN-3001/screenshot-01",
    "evidence://RUN-3001/trace-01"
  ]
}
```

---

## 2.4 Confidence support

Tools that perform interpretation should return confidence when relevant:

```json
{
  "confidence": 0.87,
  "confidenceReason": "DOM title, button labels, and layout strongly matched expected login page"
}
```

This is especially important for:

* browser page interpretation
* document extraction
* state map generation
* mismatch detection
* healing proposals
* retrieval reranking
* visual comparison

---

## 2.5 Traceability support

All context-producing tools should return stable refs rather than only free text.

Example:

```json
{
  "sourceRefs": [
    "ART-201:CHUNK-9001",
    "REQ-501",
    "FLOW-1001",
    "STATE-LOGIN-01"
  ]
}
```

---

## 2.6 Execution mode support

Execution-related tools must respect:

* `diagnostic`
* `regression`

### Rules

* **diagnostic** may allow exploratory reasoning, healing proposal generation, richer evidence, and state discovery
* **regression** must remain bounded, deterministic, and non-exploratory

---

# 3. MCP Tool Set for Current Stage

For the current stage, the platform should have these MCP contracts:

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

This expands your prior contract set to match the final architecture. 

---

# 4. Filesystem MCP

## 4.1 Purpose

Provide safe access to local case folders and generated asset storage.

## 4.2 Responsibilities

* list case files
* read files
* write generated artifacts
* verify folder structure
* fetch metadata/checksum

---

## 4.3 Operations

### A. `fs.list_case_files`

#### Request

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

#### Response

```json
{
  "data": {
    "files": [
      {
        "path": "/test/case/login-flow/case.yaml",
        "type": "file",
        "size": 1024,
        "mimeType": "application/x-yaml",
        "checksum": "sha256:abc123"
      },
      {
        "path": "/test/case/login-flow/stories/US-101.md",
        "type": "file",
        "size": 5420,
        "mimeType": "text/markdown",
        "checksum": "sha256:def456"
      }
    ]
  }
}
```

### B. `fs.read_file`

### C. `fs.write_generated_asset`

### D. `fs.validate_case_structure`

These remain valid.

---

## 4.4 Policy constraints

* read allowed in Tier 0
* write only to approved `generated/` paths
* no delete in current stage

---

# 5. Document Parser MCP

## 5.1 Purpose

Convert raw documents into structured content for knowledge ingestion, state-map generation, and RAG preparation.

## 5.2 Supported source types

* markdown
* txt
* yaml/json
* docx
* pdf
* html snapshots
* test case templates

---

## 5.3 Responsibilities

* parse documents into structured sections
* extract entities
* extract acceptance criteria, rules, steps, expected results
* support chunk-ready outputs
* preserve source references

---

## 5.4 Operations

### A. `doc.parse_document`

### B. `doc.chunk_document`

### C. `doc.extract_requirements`

### D. `doc.extract_chunk_metadata`

These remain valid from the previous version.

---

## 5.5 Policy constraints

* read-only
* no mutation of source docs
* parser must preserve source references

---

# 6. Browser Reader MCP

## 6.1 Purpose

Read browser-accessible external sources before native integrations exist.

This is the temporary bridge for:

* Azure DevOps URLs
* Jira URLs
* internal docs pages
* design preview pages
* wiki pages

---

## 6.2 Responsibilities

* open authenticated URLs
* render page
* extract visible text
* capture DOM snapshot
* capture screenshot
* return structured page summary
* produce retrieval-ready normalized content
* provide visible-truth evidence for fusion and state mapping

---

## 6.3 Operations

### A. `browser.read_page`

### B. `browser.extract_structured_page`

### C. `browser.normalize_page_for_rag`

These remain valid.

### D. `browser.capture_visual_reference`

New optional operation.

Purpose:

* capture wireframe-comparable or screenshot-comparable visual references for evidence and visual diff

#### Example response

```json
{
  "data": {
    "visualRef": "evidence://RUN-3001/visual-reference-login-page",
    "pageName": "Login Page"
  }
}
```

---

## 6.4 Policy constraints

* strictly read-only in current stage
* no clicking submit/update/delete actions
* only allowed domains
* authenticated sessions must use approved profiles

---

# 7. State Map MCP

This is a new first-class tool family required by the architectural change.

## 7.1 Purpose

Generate and manage the **semantic state map** from fused artifacts.

## 7.2 Responsibilities

* build page/state/element models
* derive expected states and transitions
* link requirements to states
* link states to likely APIs and validations
* return machine-usable semantic maps

---

## 7.3 Operations

### A. `state_map.generate`

#### Request

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

#### Response

```json
{
  "data": {
    "stateMapId": "STATEMAP-1001",
    "pages": [
      {
        "pageRef": "PAGE-301",
        "name": "Login Page",
        "elements": [
          {
            "elementRef": "EL-1001",
            "name": "Submit Button",
            "type": "button",
            "expectedStates": ["enabled", "disabled_when_invalid"]
          }
        ]
      }
    ],
    "transitions": [
      {
        "fromPageRef": "PAGE-301",
        "action": "submit valid credentials",
        "toPageRef": "PAGE-302"
      }
    ],
    "sourceRefs": ["CHUNK-9001", "CHUNK-9002"]
  }
}
```

---

### B. `state_map.get`

### C. `state_map.list_by_case`

### D. `state_map.link_requirements`

Purpose:

* bind requirement refs to state-map nodes

---

## 7.4 Policy constraints

* generated state maps must preserve source refs
* no mutation of approved state maps without versioning
* confidence should be included when map inference is indirect

---

# 8. Mismatch Detection MCP

This is a new first-class tool family required by the architectural change.

## 8.1 Purpose

Detect **requirement mismatches** across fused artifacts before execution.

## 8.2 Responsibilities

* compare story vs wireframe
* compare wireframe vs screenshot
* compare requirement vs state map
* compare expected result vs visible UI/API evidence
* surface warnings before test generation or execution

---

## 8.3 Operations

### A. `mismatch.detect`

#### Request

```json
{
  "payload": {
    "caseId": "CASE-101",
    "stateMapId": "STATEMAP-1001",
    "artifactRefs": ["ART-201", "ART-205", "ART-210"]
  }
}
```

#### Response

```json
{
  "data": {
    "mismatches": [
      {
        "mismatchId": "MM-1001",
        "type": "story_wireframe_conflict",
        "summary": "Wireframe shows CAPTCHA but story does not mention it.",
        "severity": "medium",
        "sourceRefs": ["ART-201:CHUNK-9005", "ART-205"],
        "confidence": 0.91
      }
    ]
  }
}
```

---

### B. `mismatch.validate_before_execution`

Purpose:

* check if unresolved mismatches should block execution or require review

---

## 8.4 Policy constraints

* mismatch detection is read-only
* blocking decisions must be policy-governed
* every mismatch must include source refs

---

# 9. Retrieval MCP

## 9.1 Purpose

Provide hybrid search over indexed QA knowledge.

## 9.2 Responsibilities

* search artifact chunks
* search approved test asset summaries
* search prior run summaries
* search known defects and defect drafts
* search state-map summaries
* search healing logs and playbook summaries where allowed
* apply metadata filters
* support keyword, vector, and hybrid retrieval

---

## 9.3 Operations

### A. `retrieval.search`

### B. `retrieval.search_by_refs`

### C. `retrieval.index_chunks`

### D. `retrieval.delete_or_reindex_refs`

These remain valid.

### E. `retrieval.search_state_aware`

New optional operation.

Purpose:

* retrieve content with state-map filters

#### Example request

```json
{
  "payload": {
    "queryText": "invalid password validation on login page",
    "filters": {
      "caseId": "CASE-101",
      "pageRefs": ["PAGE-301"],
      "stateMapId": "STATEMAP-1001"
    }
  }
}
```

---

## 9.4 Policy constraints

* read-only for agent-facing search
* indexing allowed only from approved ingestion pipeline
* filters must enforce case/environment/policy boundaries

---

# 10. Graph Expansion MCP

## 10.1 Purpose

Provide bounded graph traversal to enrich retrieval and state-aware mappings.

## 10.2 Responsibilities

* expand retrieved refs into linked entities
* traverse bounded relationship sets
* support lineage and impact lookup
* expand requirement ↔ state ↔ page ↔ API ↔ test relationships
* avoid unbounded graph walks

---

## 10.3 Operations

### A. `graph.expand_context`

### B. `graph.trace_lineage`

### C. `graph.find_related_entities`

These remain valid.

### D. `graph.expand_state_context`

New optional operation.

Purpose:

* expand from state-map refs into linked requirements, elements, pages, APIs, and approved assets

---

## 10.4 Policy constraints

* max depth must be enforced
* relationship allowlist must be respected
* traversal should be case-aware when possible

---

# 11. Context Pack MCP

## 11.1 Purpose

Build task-specific grounded context packs for agents.

## 11.2 Responsibilities

* combine search results and graph expansion
* rerank selected context
* enforce task-specific limits
* format context into agent-ready structure
* preserve source refs, mismatch warnings, and gaps/conflicts

---

## 11.3 Operations

### A. `context.build_pack`

This remains valid, but now should be able to include:

* state-map refs
* mismatch warnings
* playbook refs
* healing history refs

### B. `context.build_pack_from_refs`

### C. `context.log_pack`

### D. `context.build_pack_for_mode`

New optional operation.

Purpose:

* build different packs for `diagnostic` vs `regression`

---

## 11.4 Policy constraints

* pack size limits must be enforced
* sensitive content must be filtered or masked
* agent-specific retrieval policies must be respected
* regression packs should favor approved assets and stable refs

---

# 12. Browser Automation MCP

## 12.1 Purpose

Execute web UI tests in a controlled browser runtime.

## 12.2 Responsibilities

* launch browser session
* navigate
* perform actions
* assert states
* capture evidence
* return structured step results
* respect execution mode

---

## 12.3 Operations

### A. `web.start_session`

Add:

* `executionMode`
* `stateMapId`
* `playbookRef` optional

### B. `web.execute_steps`

### C. `web.assert_state`

Should support:

* semantic assertions
* state-aware assertions
* React-aware readiness checks

### D. `web.capture_artifacts`

### E. `web.end_session`

### F. `web.wait_for_state_signal`

New operation.

Purpose:

* wait for state-aware signals instead of naive sleeps

#### Example request

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

### G. `web.capture_visual_diff`

New optional operation.

Purpose:

* compare actual UI against manual wireframe or baseline image

---

## 12.4 Policy constraints

* only approved environments
* only approved auth profiles
* destructive actions may require escalation
* regression mode must remain deterministic
* diagnostic mode may allow richer reasoning loops within policy

---

# 13. API Runner MCP

## 13.1 Purpose

Execute API integration tests with controlled auth, assertions, and evidence.

## 13.2 Responsibilities

* call endpoints
* manage auth/session
* validate response
* support setup/cleanup
* capture evidence
* support linkage to semantic state expectations where relevant

---

## 13.3 Operations

### A. `api.start_context`

### B. `api.execute_request`

### C. `api.assert_response`

### D. `api.end_context`

These remain valid.

---

## 13.4 Policy constraints

* secrets masked in outputs
* only approved domains
* write/delete API actions governed by policy

---

# 14. Evidence MCP

## 14.1 Purpose

Store and retrieve forensic-grade execution evidence in a normalized way.

## 14.2 Responsibilities

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

---

## 14.3 Operations

### A. `evidence.store`

### B. `evidence.get`

### C. `evidence.bundle_run`

### D. `evidence.summarize_for_retrieval`

These remain valid.

### E. `evidence.write_semantic_trace`

New operation.

Purpose:

* write trace from requirement line → state-map node → DOM element → executed step → evidence

### F. `evidence.write_reasoning_log`

New operation.

Purpose:

* persist plain-text explanation of why an AI decision was made

### G. `evidence.store_visual_diff`

New operation.

Purpose:

* persist visual comparison artifact

---

## 14.4 Policy constraints

* evidence must be immutable once finalized for a run
* reasoning logs must avoid leaking secrets
* heavy binary artifacts should be referenced, not embedded

---

# 15. Healing MCP

This is a new first-class tool family.

## 15.1 Purpose

Provide controlled forensic self-healing analysis and persistent healing logs.

## 15.2 Responsibilities

* analyze broken locators/interactions
* compare element fingerprints
* perform forensic scan against current DOM
* generate healing proposals
* persist healing logs
* support human hardening workflow

---

## 15.3 Operations

### A. `healing.generate_fingerprint`

Purpose:

* record multi-attribute fingerprint for important elements

### B. `healing.forensic_scan`

#### Request

```json
{
  "payload": {
    "sessionId": "WEB-SESSION-001",
    "originalTarget": "button[type='submit']",
    "fingerprintRef": "FP-1001",
    "stateMapId": "STATEMAP-1001"
  }
}
```

#### Response

```json
{
  "data": {
    "proposedTarget": "getByRole('button', { name: 'Sign in' })",
    "confidence": 0.92,
    "confidenceReason": "Matched role, text family, DOM neighborhood, and page context.",
    "requiresReview": true
  }
}
```

### C. `healing.write_log`

#### Example response

```json
{
  "data": {
    "healingLogRef": "HEALLOG-1001",
    "path": "/test/case/login-flow/generated/healing/HEALLOG-1001.json"
  }
}
```

### D. `healing.list_history`

Purpose:

* retrieve prior healing events for repeated shifts

---

## 15.4 Policy constraints

* healing must not silently rewrite approved tests
* persistent updates require governance
* regression mode may use only approved healing outcomes or bounded fallback rules

---

# 16. Playbook MCP

This is a new first-class tool family.

## 16.1 Purpose

Store and export **deterministic playbooks** discovered in diagnostic mode.

## 16.2 Responsibilities

* capture discovered state signals
* store stable wait conditions
* store safe action sequence
* export deterministic playbook for regression use

---

## 16.3 Operations

### A. `playbook.export_from_run`

#### Request

```json
{
  "payload": {
    "runId": "RUN-3001",
    "caseId": "CASE-101",
    "scenarioId": "SCN-2001"
  }
}
```

#### Response

```json
{
  "data": {
    "playbookRef": "PLAYBOOK-1001",
    "summary": "Deterministic login playbook exported from diagnostic run."
  }
}
```

### B. `playbook.get`

### C. `playbook.promote`

Purpose:

* mark playbook as approved for regression use

### D. `playbook.list_by_case`

---

## 16.4 Policy constraints

* only successful or sufficiently reviewed diagnostic discoveries may be promoted
* regression mode should prefer approved playbooks

---

# 17. State Management MCP

## 17.1 Purpose

Keep execution deterministic through controlled data and state lifecycle.

## 17.2 Responsibilities

* create/reset test users
* seed data
* reset known resources
* cleanup artifacts
* verify preconditions

These remain valid.

---

## 17.3 Operations

### A. `state.verify_preconditions`

### B. `state.setup_data`

### C. `state.cleanup_data`

---

## 17.4 Policy constraints

* only approved environments
* only safe/setup cleanup actions in current stage
* all state changes must be auditable

---

# 18. Test Asset MCP

## 18.1 Purpose

Persist generated tests and related assets as governed artifacts.

## 18.2 Responsibilities

* store draft tests
* version test assets
* fetch latest approved asset
* promote asset state
* attach metadata
* provide retrieval-friendly summaries of reusable assets
* link tests to playbooks, state maps, and healing history where relevant

---

## 18.3 Operations

### A. `asset.create_test_asset`

### B. `asset.get_asset`

### C. `asset.update_status`

### D. `asset.list_assets_for_case`

### E. `asset.summarize_for_retrieval`

These remain valid.

### F. `asset.link_playbook`

New optional operation.

### G. `asset.link_state_map`

New optional operation.

---

# 19. Trigger MCP

This is a new first-class tool family required by the local shift-left architecture.

## 19.1 Purpose

Support local deterministic triggers such as pre-commit and watch mode.

## 19.2 Responsibilities

* accept local trigger events
* classify trigger source
* map changed files to likely cases
* request targeted smoke execution
* preserve local workflow audit trail

---

## 19.3 Operations

### A. `trigger.pre_commit`

#### Request

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

#### Response

```json
{
  "data": {
    "requestId": "REQ-LOCAL-1001",
    "affectedCases": ["login-flow"],
    "recommendedAction": "targeted_smoke_test"
  }
}
```

### B. `trigger.watch_mode`

Purpose:

* developer-activated watch trigger

### C. `trigger.manual_local`

Purpose:

* local manual run without external API request path

---

## 19.4 Policy constraints

* watch mode should be opt-in
* pre-commit should use bounded smoke scope unless policy expands it
* local triggers must still respect environment and action restrictions

---

# 20. Audit and Observability Requirements for All MCP Tools

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

For RAG-related tools, also emit:

* query text or query hash
* filters
* selected refs
* candidate count
* context pack size

For healing/playbook/state-map tools, also emit:

* stateMapId
* mismatchIds if relevant
* fingerprintRef if relevant
* healingLogRef if created
* playbookRef if created
* executionMode

---

# 21. Policy Matrix by Tool

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

# 22. Contract Versioning

Every tool contract should include a version:

```json
{
  "tool": "context.build_pack",
  "version": "2.0"
}
```

Versioning matters because:

* prompts depend on contract shape
* execution modes may evolve
* retrieval behavior may evolve
* multiple backends may coexist

---

# 23. Example End-to-End MCP Usage Flow

For `login-flow`, a typical architecture-aligned sequence would be:

1. `trigger.pre_commit` or manual request entry
2. `fs.validate_case_structure`
3. `fs.list_case_files`
4. `doc.parse_document`
5. `doc.chunk_document`
6. `browser.read_page` for external story/bug URL
7. `browser.normalize_page_for_rag`
8. `state_map.generate`
9. `mismatch.detect`
10. `retrieval.index_chunks`
11. `context.build_pack` for case understanding
12. `context.build_pack` for requirement mapping
13. `context.build_pack` for strategy
14. `asset.create_test_asset` for generated strategy
15. `state.verify_preconditions`
16. `state.setup_data`
17. `web.start_session`
18. `web.wait_for_state_signal`
19. `web.execute_steps`
20. `web.assert_state`
21. `api.execute_request` if API validation is needed
22. `healing.forensic_scan` if locator breaks
23. `healing.write_log` if healing applied or proposed
24. `evidence.bundle_run`
25. `evidence.write_semantic_trace`
26. `evidence.write_reasoning_log`
27. `evidence.summarize_for_retrieval`
28. `playbook.export_from_run` if diagnostic discovery should be hardened
29. `context.build_pack` for triage if needed
30. `asset.create_test_asset` for final generated/updated test
31. `state.cleanup_data`

---

# 24. Final MCP Contract Summary

The current-stage MCP layer should include:

## Required now

* **Filesystem MCP**
* **Document Parser MCP**
* **Browser Reader MCP**
* **State Map MCP**
* **Mismatch Detection MCP**
* **Retrieval MCP**
* **Graph Expansion MCP**
* **Context Pack MCP**
* **Browser Automation MCP**
* **API Runner MCP**
* **Evidence MCP**
* **Healing MCP**
* **Playbook MCP**
* **State Management MCP**
* **Test Asset MCP**
* **Trigger MCP**

## Deferred

* Figma native MCP
* Jira/ADO native MCP
* PR diff MCP
* crawler MCP
* test management sync MCP

---

# 25. Final Recommendation

Before implementation, standardize these contracts around:

* a single JSON envelope
* strong audit metadata
* explicit policy fields
* evidence refs instead of raw large payloads
* contract versioning from day one
* source refs in RAG outputs
* state-map refs in state-aware outputs
* bounded context pack outputs
* retrieval and graph-expansion logging
* persistent healing logs
* deterministic playbook export support
