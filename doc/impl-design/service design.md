I agree with most of Gemini’s comments. The best updates are:

* make the **distributed understanding split** even more explicit as a deliberate anti-hallucination design
* make **reranking** in Retrieval Service a required internal subcomponent, not just an optional implementation detail
* strengthen **Browser Worker** so state-aware assertions and React-ready signals are clearly native runtime behavior
* strengthen **Triage & Confidence Service** so confidence scoring and reasoning-backed explanation are explicit first-class outputs
* reinforce **Playbook Service** as the hardening layer between diagnostic discovery and deterministic regression
* emphasize **Evidence Service schema** as a core dependency for fast debugging and reliable HITL review

I did **not** change the architecture shape dramatically, because the service design was already strong. The comments mostly sharpen and clarify the existing design rather than replace it. The original Part 2 already had the right service boundaries, Graph-RAG ownership, execution split, and forensic evidence direction. 

Below is the **rewritten Part 2 — Service Design**, updated with the comments I think are correct.

---

# Part 2 — Service Design

## AI QA Platform

### Final Architecture-Aligned Version

#### Updated with review refinements

This section defines the **service-by-service implementation design** for the AI-powered QA platform.

It translates the architecture into deployable components with clear responsibilities, interfaces, ownership boundaries, and runtime behavior.

This version matches the final architecture with:

* folder-based case ingestion
* browser-readable URL ingestion
* distributed understanding
* semantic state maps
* requirement mismatch detection
* hybrid Graph-RAG
* deterministic and diagnostic execution modes
* forensic self-healing
* forensic-grade evidence
* local shift-left triggers
* no direct Jira/Figma/Azure DevOps API integration yet

---

# 1. Service design goals

The service design must achieve these goals:

1. keep AI reasoning separate from deterministic execution
2. make all important actions auditable
3. support incremental expansion later
4. avoid tight coupling between agents and external systems
5. allow future addition of native connectors without redesign
6. make **Graph-RAG a first-class subsystem**
7. make **semantic state modeling a first-class subsystem**
8. support both **diagnostic** and **regression** execution modes
9. support production concerns:

   * retries
   * observability
   * policy enforcement
   * state isolation
   * artifact versioning
   * retrieval grounding
   * context traceability
   * healing governance
   * evidence reproducibility

---

# 2. Strategic service design win

The most important service-level decision is the **strict separation of distributed understanding responsibilities**.

Instead of one overloaded “intake” or “analysis” service, the design deliberately separates:

* **Distributed Understanding Service** for ingestion, normalization, artifact fusion, and case understanding
* **Semantic State Service** for generating semantic state maps, transitions, and fingerprints
* **Mismatch Detection Service** for identifying contradictions and unsupported expectations before authoring or execution

## Why this works

This avoids **context stuffing**, which is one of the main causes of hallucination and low-precision QA reasoning.

It means:

* one service focuses on what was ingested
* another focuses on the state model implied by those artifacts
* another focuses on where those sources disagree

That is the right service split for multimodal local QA.

---

# 3. Top-level service map

The platform should be split into the following core services:

1. **Request Gateway Service**
2. **Trigger Service**
3. **QA Orchestration Service**
4. **Distributed Understanding Service**
5. **Semantic State Service**
6. **Mismatch Detection Service**
7. **Knowledge Graph Service**
8. **Retrieval Service**
9. **Agent Runtime Service**
10. **Test Asset Service**
11. **Execution Service**
12. **Browser Worker Service**
13. **API Runner Worker Service**
14. **Evidence Service**
15. **Healing Service**
16. **Playbook Service**
17. **State Management Service**
18. **Triage & Confidence Service**
19. **Defect Draft Service**
20. **Policy & Approval Service**
21. **Audit & Observability Service**

Supporting infrastructure:

* object storage
* relational database
* graph database and/or graph layer
* vector index / retrieval index
* queue / event bus

This core service map remains correct. 

---

# 4. High-level runtime topology

```text id="c26j4d"
+-------------------------------------------------------------+
| Request Gateway / CLI / Local UI                            |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| Trigger Service                                              |
| pre-commit / watch mode / manual local trigger              |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| QA Orchestration Service                                     |
| workflow, state machine, approvals, policy checkpoints       |
+-------------+----------------------+-------------------------+
              |                      |
              |                      v
              |         +-------------------------------+
              |         | Policy & Approval Service     |
              |         +-------------------------------+
              |
              v
+-------------------------------------------------------------+
| Distributed Understanding Service                            |
| intake + normalization + artifact fusion + case understanding|
+-------------+----------------------+-------------------------+
              |                      |
              v                      v
+----------------------------+   +-----------------------------+
| Semantic State Service     |   | Mismatch Detection Service  |
| state maps, UI states,     |   | requirement mismatch rules  |
| transitions, fingerprints  |   | and pre-run warnings        |
+-------------+--------------+   +--------------+--------------+
              |                                 |
              +----------------+----------------+
                               |
                               v
+-------------------------------------------------------------+
| Knowledge & Context Layer                                    |
| Knowledge Graph Service + Retrieval Service                  |
| graph expansion + hybrid retrieval + reranking + context pack|
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| Agent Runtime Service                                        |
| strategy / authoring / triage / learning agents             |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| Test Asset Service                                           |
| scenarios, tests, assertions, reusable assets               |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| Execution Service                                            |
| diagnostic mode / regression mode planning                  |
+-------------+--------------------------+--------------------+
              |                          |
              v                          v
+---------------------------+  +-----------------------------+
| Browser Worker Service    |  | API Runner Worker Service   |
+-------------+-------------+  +-------------+---------------+
              |                              |
              +---------------+--------------+
                              |
                              v
+-------------------------------------------------------------+
| Evidence Service                                             |
| screenshots, traces, logs, semantic trace, visual diffs,     |
| reasoning logs, bundles                                      |
+----------------------------+--------------------------------+
                             |
               +-------------+-------------+
               |                           |
               v                           v
+----------------------------+   +-----------------------------+
| Healing Service            |   | Triage & Confidence Service |
| forensic scan, healing log |   | failure classification      |
+-------------+--------------+   +-------------+---------------+
              |                                |
              v                                v
+----------------------------+   +-----------------------------+
| Playbook Service           |   | Defect Draft Service        |
| export deterministic       |   | defect-quality packets      |
| playbooks from diagnostics |   +-----------------------------+
+----------------------------+
```

---

# 5. Core service design principles

## 5.1 Distributed understanding ownership

The final architecture requires understanding to be split across separate responsibilities:

* **Distributed Understanding Service** handles raw intake, normalization, artifact fusion, and case understanding
* **Semantic State Service** produces semantic state maps
* **Mismatch Detection Service** compares fused artifacts and states to detect pre-run warnings

This is not just a style choice. It is a reliability choice.

## 5.2 Graph-RAG ownership split

### Distributed Understanding Service

Produces structured inputs for RAG:

* parsed artifacts
* normalized artifact summaries
* retrieval chunks
* metadata

### Retrieval Service

Owns the runtime side of Graph-RAG:

* search
* graph expansion orchestration
* **reranking**
* context packs
* retrieval policy
* retrieval logs

### Knowledge Graph Service

Owns:

* explicit entities and relationships
* state-map linkage
* requirement/test/evidence lineage
* bounded graph expansion APIs
* impact lookup

### Agent Runtime Service

Consumes grounded context packs instead of assembling raw context itself.

## 5.3 Dual execution ownership

### Diagnostic Mode

Allows:

* richer evidence
* state-signal discovery
* healing analysis
* exploratory but bounded reasoning

### Regression Mode

Allows:

* deterministic approved asset execution
* locked playbook-based waits and actions
* no uncontrolled exploration

### Playbook Service

Bridges the two by exporting stable discoveries from diagnostic mode into reusable deterministic playbooks.

This is one of the strongest parts of the design and should remain explicit.

---

# 6. Service-by-service design

---

## 6.1 Request Gateway Service

### Purpose

Entry point for all inbound QA requests from UI, CLI, or API.

### Responsibilities

* receive new QA requests
* validate request schema
* authenticate caller
* assign request ID
* normalize request payload
* persist initial request record
* pass request to orchestration

### Internal responsibilities

* schema validation
* deduplication prevention
* request classification
* priority tagging

### Persistence

Stores:

* request record
* caller identity
* submission time
* normalized payload
* initial status

### Events produced

* `qa.request.accepted`

### Non-functional notes

* stateless HTTP service
* horizontally scalable
* should not perform heavy reasoning

---

## 6.2 Trigger Service

### Purpose

Handle local shift-left triggers such as pre-commit hooks, optional watch mode, and manual local execution.

### Responsibilities

* receive local trigger events
* classify trigger type
* inspect changed files or trigger metadata
* map changed files to likely cases
* use graph-assisted impact analysis when available
* create bounded smoke-test requests
* send derived request to Request Gateway / Orchestration
* preserve local trigger audit trail

### Trigger types

* `pre_commit`
* `watch_mode`
* `manual_local`

### Outputs

* derived QA request
* affected case list
* recommended smoke scope

### Events produced

* `qa.trigger.received`
* `qa.trigger.translated`

### Non-functional notes

* watch mode should be opt-in
* pre-commit should be bounded by policy
* should not bypass request normalization

This aligns well with the shift-left design and should stay.

---

## 6.3 QA Orchestration Service

### Purpose

Central workflow coordinator for the whole QA lifecycle.

### Responsibilities

* manage request state machine
* schedule stages in order
* invoke service and agent tasks
* apply retry and timeout rules
* coordinate approvals
* maintain run-level workflow context
* manage mode transitions between diagnostic and regression logic
* produce final summary

### Main workflow stages

1. request accepted
2. case validation
3. ingestion
4. artifact fusion
5. semantic state generation
6. mismatch detection
7. graph/index update
8. context build request
9. strategy generation
10. test generation
11. state preparation
12. execution
13. evidence finalization
14. healing analysis
15. triage
16. defect drafting
17. playbook export if applicable
18. approval handling
19. completion

### Events produced

* `workflow.stage.started`
* `workflow.stage.completed`
* `retrieval.context_pack.requested`
* `execution.run.requested`
* `healing.analysis.requested`
* `triage.requested`
* `defect.draft.requested`
* `playbook.export.requested`

### Non-functional notes

* resumable workflows
* idempotent stages
* preserve causal ordering between mismatch detection and execution

---

## 6.4 Distributed Understanding Service

### Purpose

Perform raw ingestion, artifact classification, artifact fusion, and structured case understanding.

### Responsibilities

* read case folders
* validate folder structure
* read browser-readable URLs
* call document parsing tools
* classify artifacts
* normalize artifacts
* fuse related artifacts
* create structured case understanding
* produce retrieval-ready chunks and summaries
* preserve provenance

### Why this service matters

This service is the operational home of **Artifact Fusion**.

It is not just a parser wrapper.
It merges:

* text artifacts
* visual artifacts
* browser-captured pages
* rule documents
* defects
* expected-result material

into a coherent case understanding that downstream services can trust.

### Outputs

* normalized artifact records
* parsed content
* fused case understanding
* retrieval-ready chunks
* enriched metadata
* source metadata
* ingestion issues

### Internal stages

1. folder discovery
2. file listing
3. document parsing
4. browser capture
5. artifact classification
6. artifact normalization
7. artifact fusion
8. retrieval chunk generation
9. metadata enrichment
10. handoff to Semantic State Service and Retrieval Service

### Persistence

Stores:

* artifact metadata
* raw parse output
* normalized summaries
* chunk records
* fusion summaries
* warnings/errors

### Events produced

* `artifact.ingested`
* `artifact.normalized`
* `artifact.fused`
* `artifact.chunked`
* `understanding.completed`

### Non-functional notes

* support re-ingestion if files change
* keep immutable snapshots when required
* chunk quality strongly affects downstream retrieval

---

## 6.5 Semantic State Service

### Purpose

Generate and manage semantic state maps for each case.

### Responsibilities

* create page/state/element models
* model expected UI states
* model transitions and validations
* link requirements to states
* link states to likely APIs and assertions
* maintain state map versions
* maintain element fingerprints for forensic healing
* expose state-map lookups for execution and retrieval

### Outputs

* semantic state maps
* state refs
* transition refs
* element fingerprints
* state-map summaries for retrieval

### Internal components

* state map builder
* UI state modeler
* transition modeler
* fingerprint generator
* version manager

### Persistence

Stores:

* state maps
* page/element/state relationships
* element fingerprints
* state-map summaries

### Events produced

* `state_map.generated`
* `state_map.updated`
* `state_map.completed`

### Non-functional notes

* state maps should be versioned
* preserve source refs
* support later linkage to visual diff and playbook export

This service should continue to be the technical “common knowledge” layer for the platform.

---

## 6.6 Mismatch Detection Service

### Purpose

Detect requirement mismatches across fused artifacts and semantic state maps before execution.

### Responsibilities

* compare story vs wireframe
* compare wireframe vs screenshot
* compare requirement vs state map
* compare expected result vs visible state/API evidence
* classify mismatch severity
* surface warnings and possible execution blockers
* provide mismatch data to retrieval and agents

### Outputs

* mismatch warnings
* severity classifications
* policy escalation flags
* mismatch summaries for retrieval

### Events produced

* `mismatch.detected`
* `mismatch.blocking_detected`
* `mismatch.completed`

### Trigger mechanism

The Mismatch Detection Service is triggered by the **QA Orchestration Service** immediately after the Semantic State Service emits `state_map.completed`. It runs as a mandatory pre-authoring gate and is not triggered directly by upstream services.

Trigger flow:

1. Semantic State Service emits `state_map.completed`
2. Orchestrator dispatches `mismatch.detection.requested`
3. Mismatch Detection Service runs full analysis across all fused artifacts and the new state map
4. Service emits either `mismatch.completed` (no blockers) or `mismatch.blocking_detected` (blockers found)
5. If blocking mismatches exist, the Orchestration Service halts the workflow at the authoring gate
6. An approval task is created and routed to a reviewer
7. The reviewer resolves or explicitly overrides the blocking mismatch
8. The Orchestration Service resumes the workflow

Non-blocking mismatches do not halt the workflow. They are included in the context pack delivered to all downstream agents and must be acknowledged in agent reasoning output.

### Non-functional notes

* deterministic and explainable
* all mismatches must include source refs
* must complete before authoring stage begins; this is enforced by the Orchestration Service, not by this service itself
* blocking severity is determined by the Mismatch Detection Service; the enforcement gate is owned by the Orchestration Service

This is one of the most important reliability services in the whole system.

---

## 6.7 Knowledge Graph Service

### Purpose

Store the structured relationships that power traceability and retrieval-time graph expansion.

### Responsibilities

* persist entities and relationships
* support traversal queries
* maintain requirement-to-test lineage
* store case knowledge graph
* support update/version operations
* provide bounded graph expansion APIs for Retrieval Service
* provide impact lookup and traceability neighborhood queries
* store semantic state map relationships
* store healing and playbook lineage where relevant

### Non-functional notes

* graph queries should be fast for lineage and impact lookup
* traversal depth should be bounded and policy-aware
* graph must remain separate from retrieval engine responsibilities

---

## 6.8 Retrieval Service

### Purpose

Provide full Graph-RAG runtime capabilities for agent reasoning.

### Responsibilities

* index chunks and retrieval views
* support hybrid retrieval
* retrieve candidate context by query and filters
* call Knowledge Graph Service for expansion
* **rerank retrieved items**
* build task-specific context packs
* enforce retrieval policies
* log retrieval queries and selected context
* include state-map refs, mismatch warnings, playbook refs, and healing history where appropriate

### Reviewer refinement adopted

The review is correct: reranking should not be treated as optional.

In a folder-first system, artifacts can be noisy, redundant, incomplete, or unevenly structured.
So the Retrieval Service should have a dedicated internal **Reranking Engine**.

### Updated internal subcomponents

* candidate retriever
* graph expansion orchestrator
* **reranker**
* context pack builder
* retrieval policy engine
* retrieval query logger

### Example use cases

* get requirements and mismatch warnings for login-flow
* get approved reusable login assets for authoring
* get similar historical failures for triage
* get healing history for unstable submit button
* get playbook refs for regression execution

### Non-functional notes

* support low latency
* retrieval output must be bounded and stage-aware
* prefer approved/high-quality sources when relevant

This is the context backbone of the platform and should be treated as such.

---

## 6.9 Agent Runtime Service

### Purpose

Host the multi-agent reasoning layer.

### Responsibilities

* execute agent prompts and workflows
* manage agent memory for a run
* coordinate agent-to-agent handoff
* call MCP tools when needed
* consume task-specific context packs from Retrieval Service
* return structured outputs
* provide reasoning summaries and confidence where applicable

### Agents hosted

* Intake Agent
* Case Understanding Agent
* Requirement Mapping Agent
* Risk & Strategy Agent
* Test Authoring Agent
* Failure Triage Agent
* Healing Agent
* Defect Drafting Agent
* Learning Agent

### Important correction

Agent Runtime must respect distributed understanding boundaries.
It should not collapse all upstream understanding into one generalized reasoning step.

### Non-functional notes

* can be stateless if context is externalized
* must not store secrets in raw prompt logs
* must preserve used source refs for audit

---

## 6.10 Test Asset Service

### Purpose

Manage generated and reviewed QA assets as governed artifacts.

### Responsibilities

* store strategy docs
* store test scenarios
* store Playwright tests
* store API specs
* store semantic assertion modules
* store reusable flow modules
* store deterministic playbook linkage
* version assets
* track asset lifecycle
* provide latest approved assets and playbooks

### Asset lifecycle

* draft
* reviewed
* approved
* active
* deprecated
* retired

### Non-functional notes

* strong versioning from day one
* immutable past versions
* must retain context-pack lineage for generated versions

---

## 6.11 Execution Service

### Purpose

Coordinate deterministic and diagnostic execution of generated tests.

### Responsibilities

* create execution plan
* determine execution mode
* dispatch jobs to browser/API workers
* collect step results
* enforce timeout/retry policy
* attach run metadata
* trigger healing analysis when needed
* request playbook export when diagnostic discoveries are promotable

### Outputs

* run record
* step results
* execution status
* evidence refs

### Events produced

* `execution.run.started`
* `execution.step.completed`
* `execution.run.completed`
* `execution.run.failed`
* `healing.analysis.requested`
* `playbook.export.requested`

### Non-functional notes

* regression mode must remain deterministic
* diagnostic mode may allow richer evidence and discovery
* web and API execution must remain cleanly isolated

This service remains one of the strongest parts of the design.

---

## 6.12 Browser Worker Service

### Purpose

Run web UI tests in isolated browser sessions.

### Responsibilities

* launch browser
* load environment base URL
* authenticate with approved profile
* execute Playwright-backed steps
* perform **state-aware waits natively**
* implement **state-aware assertions natively**
* capture screenshot/video/trace/console/network
* support diagnostic or regression mode behavior

### Reviewer refinement adopted

The review is correct: the Browser Worker must not rely on naive URL changes or fixed sleeps as its primary runtime model.

It should natively support **React-ready / state-aware runtime signals**, such as:

* component mount completion
* spinner disappearance
* button enabled state
* validation message visibility
* route stabilization
* async render completion

### Outputs

* per-step status
* session result
* evidence refs
* runtime logs

### Non-functional notes

* horizontally scalable
* state-aware waiting is required for React-style async UIs
* regression mode must not behave like uncontrolled agent exploration

This is a real implementation requirement, not just a nice-to-have.

---

## 6.13 API Runner Worker Service

### Purpose

Run API scenario tests in isolated runtime contexts.

### Responsibilities

* manage auth context
* run request chains
* validate responses
* capture request/response evidence
* return structured assertion outcomes

### Non-functional notes

* stateless between runs
* can reuse context within one run only
* must mask secrets in logs

---

## 6.14 Evidence Service

### Purpose

Central storage and indexing for forensic-grade run evidence.

### Responsibilities

* persist screenshots
* persist video/trace/HAR/DOM/logs
* persist request/response evidence
* create semantic trace
* create reasoning logs
* store visual diffs
* index evidence metadata
* create retrieval-friendly evidence summaries
* bundle evidence for triage and defect drafting

### Evidence types

* screenshot
* video
* trace
* DOM snapshot
* console log
* network/HAR
* API request snapshot
* API response snapshot
* visual diff
* semantic trace
* reasoning log
* report bundle

### Reviewer refinement adopted

The review is correct: the **Evidence Service schema** is one of the most important things to stabilize early.

This service should become the debugging backbone for the rest of implementation because it lets you inspect:

* what the platform saw
* what the platform believed
* what the platform did
* why the platform concluded pass/fail/defect

### Outputs

* evidenceRef
* bundle refs
* evidence summaries

### Non-functional notes

* evidence immutable once finalized
* retention policy configurable
* only summaries, not heavy raw blobs, should normally feed retrieval

---

## 6.15 Healing Service

### Purpose

Perform forensic self-healing analysis and manage persistent healing logs.

### Responsibilities

* generate multi-attribute element fingerprints
* analyze locator and interaction failures
* perform forensic scan of current DOM
* compute likely successor targets
* estimate confidence
* create persistent healing logs
* surface repeated instability patterns
* feed approved healing knowledge into future runs

### Outputs

* healing proposal
* confidence
* healing log ref
* escalation recommendation

### Non-functional notes

* must not silently mutate approved tests
* persistent update requires governance
* should support reuse of prior healing history

This remains correct and should stay tightly separated from Triage.

---

## 6.16 Playbook Service

### Purpose

Export, store, and manage deterministic playbooks derived from successful diagnostic execution.

### Responsibilities

* capture discovered state signals
* record reliable waits and state transitions
* export deterministic playbooks
* version and govern playbooks
* link playbooks to assets and scenarios
* provide playbook summaries for retrieval

### Reviewer refinement adopted

The review is correct: this service is the **hardening layer** between AI exploration and stable automation.

When diagnostic mode discovers:

* stable selectors
* stable state signals
* stable transition timing
* repeatable safe execution paths

this service should export them into a deterministic playbook so regression mode does not have to “rethink” the same problem.

### Outputs

* playbook ref
* playbook summary
* promotion status

### Non-functional notes

* only stable or approved diagnostic discoveries should become regression playbooks
* playbooks should be versioned and reviewable

---

## 6.17 State Management Service

### Purpose

Provide deterministic environment and data preparation, including parallel run isolation when multiple runs execute concurrently against the same environment.

### Responsibilities

* verify preconditions before execution begins
* create scoped test accounts and data sets for each run
* seed required data states declared by the test scenario
* reset resources to a known clean state
* clean up run-scoped data after completion (pass or fail)
* enforce isolation boundaries between concurrent runs
* record all state actions in the audit log with run ID, environment, and actor identity

### Parallel run isolation

When multiple runs execute against the same environment simultaneously, data collisions and session bleed-through must be prevented.

Isolation strategies, applied in priority order:

1. **Tenant or namespace isolation** — each run receives a unique namespace prefix or scoped test tenant where the environment supports it (preferred)
2. **Account-per-run isolation** — each run creates a dedicated scoped test account (e.g. `testuser-RUN-3001@test.example.com`)
3. **Sequential execution gate** — if the environment cannot support parallel data isolation, a concurrency limit of 1 is enforced for that environment profile; subsequent runs queue until the prior run releases

The isolation strategy for each environment is declared in the environment profile configuration and enforced by this service before execution begins. The Execution Service may not dispatch a run until this service confirms isolation is established.

### Action catalog

State management actions must be defined in a declarative action catalog, not as ad-hoc scripts.

Each action in the catalog declares:

* `name` — stable identifier
* `preconditions` — what must be true before the action runs
* `inputs` — parameters the orchestrator provides per run
* `side_effects` — what the action changes in the environment
* `cleanup_action` — the paired teardown action reference
* `policy_tier` — Tier 1 for standard setup, Tier 2 for sensitive or destructive mutations

### Data lifecycle contract

Each run that uses State Management must follow this four-phase contract:

1. **Setup** — called before execution; creates isolated data and verifies preconditions
2. **Verification** — confirms setup succeeded and the environment is in the expected state; blocks execution if verification fails
3. **Cleanup** — called after execution completes regardless of pass or fail; removes run-scoped data and releases any locks or reservations
4. **Audit** — records all actions taken with timestamps, run ID, environment ID, and actor identity

Cleanup must execute even if the run fails or is cancelled partway through. Cleanup failures are flagged as warnings attached to the run record.

### Non-functional notes

* all Tier 2 state mutations require an explicit approval gate before execution
* the service must not assume that environment state is clean between runs
* the service must support idempotent setup — re-running setup for the same run ID must produce the same state without duplication
* concurrency limits and isolation assignments must be persisted so they survive orchestrator restarts

---

## 6.18 Triage & Confidence Service

### Purpose

Analyze execution results and produce structured failure classification with confidence.

### Responsibilities

* combine evidence from web/API runs
* classify failure type
* score evidence quality
* estimate confidence
* explain **why** the conclusion was reached
* recommend next action
* use retrieval support when needed
* include healing context and reasoning logs when relevant

### Reviewer refinement adopted

This service should explicitly prioritize **confidence scoring** as a first-class output.

If it concludes a run failed, it should explain:

* what facts were observed
* how those facts support the classification
* which reasoning logs were used
* which evidence refs support the conclusion

This makes HITL review much faster.

### Inputs

* run result
* evidence bundle
* state-map refs
* linked requirements
* linked historical failures
* retrieval context pack
* healing logs if any

### Outputs

* triage classification
* confidence score
* confidence reason
* reasoning summary
* suggested action
* supporting refs

### Non-functional notes

* confidence calculation should be explainable
* classification taxonomy must be stable
* should downgrade to review if evidence is incomplete

This is a key production-quality service, not just a convenience layer.

---

## 6.19 Defect Draft Service

### Purpose

Generate internal defect-quality packets.

### Responsibilities

* create structured defect draft
* attach evidence bundle
* generate repro steps
* link to requirement/story/run
* include visual diffs, semantic trace, and reasoning refs where useful
* stage draft for approval if needed
* retrieve similar prior defect drafts for drafting assistance

### Current-stage boundary

Internal draft only.
No automatic external ticket submission yet.

---

## 6.20 Policy & Approval Service

### Purpose

Enforce action policy and support human-in-the-loop checkpoints.

### Responsibilities

* evaluate whether an action is allowed
* decide whether approval is needed
* persist approval tasks
* record reviewer decisions
* unblock workflows after decisions

### Example controlled decisions

* allow execution in UAT?
* allow persistent self-healing update?
* allow playbook promotion?
* allow use of draft assets in regression mode?
* allow mismatch override?

### Non-functional notes

* decisions should be deterministic
* approval log is auditable and immutable

---

## 6.21 Audit & Observability Service

### Purpose

Provide centralized audit trail, metrics, tracing, and operational visibility.

### Responsibilities

* collect audit records from all services
* collect metrics and traces
* expose dashboards and search
* support incident/debugging workflows
* support compliance reporting
* capture Graph-RAG observability
* capture state-map, mismatch, healing, and playbook observability

### Audit examples

* who submitted request
* which trigger created the request
* what artifacts were fused
* what mismatches were found
* what context pack was used by which agent
* what healing action was proposed
* what playbook was exported
* why approval was required

### Telemetry categories

* request lifecycle metrics
* workflow stage durations
* agent latency
* retrieval latency
* graph expansion latency
* browser/API run latency
* evidence volume
* mismatch counts
* healing frequency
* playbook export rates
* approval wait time
* context pack size metrics

### Non-functional notes

* avoid raw secrets or sensitive bodies
* retrieval and context-pack logging remain critical
* healing and playbook logs should be first-class observable records

---

# 7. Service interaction flow

## 7.1 Synchronous vs asynchronous split

### Synchronous

Use synchronous calls for:

* request submission acknowledgement
* trigger receipt
* basic request validation
* short metadata lookups
* approval decision queries

### Asynchronous

Use async/event-driven flow for:

* ingestion
* fusion
* state-map generation
* mismatch detection
* indexing
* graph registration
* context pack building
* strategy generation
* test generation
* execution
* evidence processing
* healing analysis
* triage
* defect drafting
* playbook export

## 7.2 Primary end-to-end flow

```text id="ht4yc0"
Trigger / Request Gateway
  -> QA Orchestration
    -> Distributed Understanding Service
      -> parse / normalize / fuse / chunk / enrich
    -> Semantic State Service
      -> build state map / fingerprints
    -> Mismatch Detection Service
      -> compare artifacts / state map / expectations
    -> Retrieval Service
      -> index / retrieve / graph expand / rerank / build context pack
    -> Agent Runtime
      -> understand + map + strategy + author
      -> Test Asset Service
    -> State Management
    -> Execution Service
      -> Browser Worker / API Runner Worker
      -> Evidence Service
    -> Healing Service (if needed)
    -> Triage & Confidence
    -> Defect Draft Service
    -> Playbook Service (if diagnostic discoveries qualify)
    -> Policy & Approval if needed
    -> completion summary
```

## 7.3 Inter-service communication protocol

The platform uses a **two-protocol model**: synchronous HTTP for request-response interactions, and an event bus for asynchronous workflow advancement.

### HTTP (synchronous)

Use synchronous HTTP for:

* inbound request submission to Request Gateway
* trigger submission to Trigger Service
* metadata and status lookups
* approval decision submission
* MCP tool calls from agents to service adapters
* direct service-to-service queries within a workflow stage (e.g. Retrieval Service calling Knowledge Graph Service for expansion)

All HTTP APIs use JSON request and response bodies.
Services expose REST-style endpoints.
Internal service-to-service calls use scoped service tokens, not user credentials.

### Event bus (asynchronous)

Use the event bus for:

* workflow stage advancement (Orchestration Service → downstream services)
* stage completion signals (services → Orchestration Service)
* worker dispatch (Execution Service → Browser Worker / API Runner Worker pools)
* evidence finalization signals
* healing analysis triggers
* triage triggers
* playbook export triggers
* learning signal triggers

The committed event bus technology is **Redis Streams** (primary) or RabbitMQ (alternative), as defined in the architecture.

All events use a standard envelope:

```json
{
  "eventType": "string",
  "requestId": "string",
  "workflowId": "string",
  "runId": "string or null",
  "caseId": "string or null",
  "payload": {},
  "issuedAt": "ISO-8601 timestamp",
  "issuedBy": "service-name"
}
```

### No direct cross-service database access

Services must not read or write each other's relational database tables directly.

Cross-service data access must go through:

* the owning service's HTTP API, or
* shared read models published to the retrieval index or object storage

This boundary is what makes services independently deployable and replaceable without requiring schema coordination across teams.

## 7.4 Cross-store consistency and transaction boundaries

The platform writes to multiple stores (relational DB, graph store, vector index, object storage). These stores cannot participate in a single distributed transaction. The design uses the **Transactional Outbox pattern** to maintain consistency across them.

### Transactional Outbox pattern

When a service needs to write to both the relational DB and a secondary store (graph, vector index, or object storage):

1. The service writes the primary record and an outbox entry in the **same local relational transaction**
2. A background outbox processor reads pending outbox entries and writes to the secondary store
3. On success, the outbox entry is marked complete
4. On failure, the outbox processor retries with backoff
5. The relational record is always the source of truth; graph and vector stores are eventually consistent derivatives

This means:

* a graph write failure never causes a relational write to be rolled back or lost
* a vector index failure never blocks a workflow stage from completing
* the outbox table provides a durable, inspectable retry queue for all cross-store writes

### Saga pattern for multi-stage workflows

Long-running workflows that span multiple services use a **choreography-based saga**.

Each workflow stage defines:

* the event that triggers it
* the event it emits on success
* the event it emits on failure
* a compensating action that reverses its side-effects if the saga needs to abort

The QA Orchestration Service tracks saga state and can issue compensation requests if a downstream stage fails unrecoverably. Compensating actions must be idempotent.

### Consistency guarantees by store

| Store | Consistency model | Mechanism |
| --- | --- | --- |
| Relational DB | Strongly consistent within a service | ACID transactions |
| Graph store | Eventually consistent | Transactional Outbox |
| Vector index | Eventually consistent | Transactional Outbox |
| Object storage | Eventually consistent | Idempotent object writes |
| Event bus | At-least-once delivery | Consumer group acknowledgement |

### No distributed transactions (XA)

The platform does not use XA or two-phase commit across services or stores. This is a deliberate choice to keep operational complexity low and services independently deployable.

---

# 8. Service boundaries and why they matter

## 8.1 Orchestration vs Agent Runtime

* Orchestration = workflow engine
* Agent Runtime = reasoning engine

## 8.2 Distributed Understanding vs Semantic State Service

* Distributed Understanding = ingest and fuse artifacts
* Semantic State Service = turn fused meaning into state models

## 8.3 Semantic State Service vs Mismatch Detection

* State Service = produces state truth model
* Mismatch Detection = compares truth sources and flags conflicts

## 8.4 Knowledge Graph vs Retrieval

* Graph = explicit relationships
* Retrieval = search + expansion + reranking + context packs

## 8.5 Execution vs Workers

* Execution Service plans and coordinates
* Workers actually run web/API sessions

## 8.6 Healing vs Triage

* Healing analyzes recoverable UI shifts
* Triage explains overall test failure cause

## 8.7 Diagnostic vs Regression

* Diagnostic = discovery
* Regression = deterministic enforcement

This separation is one of the strongest parts of the service design.

---

# 9. Suggested deployment shape

## 9.1 Core services

* Request Gateway
* Trigger Service
* QA Orchestration
* Distributed Understanding
* Semantic State Service
* Mismatch Detection Service
* Knowledge Graph
* Retrieval Service
* Agent Runtime
* Test Asset Service
* Execution Service
* Evidence Service
* Healing Service
* Playbook Service
* State Management
* Triage & Confidence
* Defect Draft
* Policy & Approval
* Audit & Observability

## 9.2 Worker pools

* Browser worker pool
* API runner worker pool

## 9.3 Shared stores

* relational DB
* graph DB
* vector/retrieval index
* object storage
* queue/event bus

---

# 10. Recommended initial build order

## Phase A — Core workflow backbone

1. Request Gateway
2. Trigger Service
3. QA Orchestration
4. Policy & Approval
5. Audit & Observability

## Phase B — Understanding and context foundation

6. Distributed Understanding Service
7. Semantic State Service
8. Mismatch Detection Service
9. Retrieval index pipeline
10. Knowledge Graph
11. Retrieval Service
12. Test Asset Service

## Phase C — Execution foundation

13. Execution Service
14. Browser Worker
15. API Runner Worker
16. **Evidence Service**
17. State Management

## Phase D — Intelligence and hardening

18. Agent Runtime
19. Healing Service
20. Triage & Confidence
21. Defect Draft
22. Playbook Service

### Refinement from review

This build order is still correct, but one practical note from the review is worth adopting:

Define the **Evidence Service schema early**, even if full evidence features come slightly later in implementation.

That will make debugging the rest of the services much easier.

---

# 11. Minimal MVP vs production-minded MVP

## Minimal MVP

* Request Gateway
* Trigger Service
* Orchestration
* Distributed Understanding
* Semantic State Service
* Retrieval
* Agent Runtime
* Browser Worker
* API Worker
* Evidence
* Test Asset

## Production-minded MVP

Add:

* Mismatch Detection
* Knowledge Graph
* State Management
* Healing
* Triage & Confidence
* Defect Draft
* Playbook
* Policy & Approval
* Audit & Observability

This remains the recommended target.

## Minimum Viable Demo Slice

Before committing to the full production-minded MVP, the team should target a **7-service first demo slice** that demonstrates the core value proposition end-to-end.

The minimum slice is:

1. **Request Gateway** — accepts a request with a case name
2. **QA Orchestration** — drives a simplified workflow through ingestion → context → generation
3. **Distributed Understanding Service** — ingests a case folder and produces fused case understanding with chunks
4. **Retrieval Service** — provides bounded context to the agent using a local in-process vector store (no Qdrant required at this stage)
5. **Agent Runtime** — runs one agent (Test Authoring Agent) against the bounded context
6. **Test Asset Service** — stores and versions the generated test
7. **Evidence Service** (schema only) — records run metadata; no full browser/trace evidence capture yet

This slice demonstrates:

* folder ingestion → artifact fusion → chunk retrieval → agent reasoning → test asset generation

What is deliberately omitted from the demo slice:

* Semantic State Service (no state map generation yet)
* Mismatch Detection Service (no pre-execution gate yet)
* Knowledge Graph Service (no graph store required)
* Browser Worker / API Runner Worker (no live execution yet)
* Healing, Triage, Playbook, Defect Draft services
* Policy & Approval Service (policy is pass-through in demo mode)
* Audit & Observability Service (basic logging only)

The demo slice produces a real, inspectable test file from a real case folder. That is the first meaningful deliverable for any stakeholder review.

---

# 12. Final service summary

The final recommended service decomposition is:

1. **Request Gateway Service** — receives and validates inbound requests
2. **Trigger Service** — handles local pre-commit, watch mode, and manual local triggers
3. **QA Orchestration Service** — controls lifecycle and workflow state
4. **Distributed Understanding Service** — ingests, normalizes, and fuses folder/URL artifacts into case understanding
5. **Semantic State Service** — creates semantic state maps, transitions, and fingerprints
6. **Mismatch Detection Service** — detects requirement and artifact conflicts before execution
7. **Knowledge Graph Service** — stores explicit QA relationships and supports bounded graph expansion and impact lookup
8. **Retrieval Service** — provides full Graph-RAG runtime: hybrid search, expansion, **reranking**, and context packs
9. **Agent Runtime Service** — hosts specialized reasoning agents and consumes grounded context packs
10. **Test Asset Service** — manages strategies, tests, reusable modules, and governed versions
11. **Execution Service** — coordinates diagnostic and regression execution
12. **Browser Worker Service** — runs web tests with native state-aware waits and state-aware assertions
13. **API Runner Worker Service** — runs API tests
14. **Evidence Service** — persists forensic-grade evidence, semantic trace, visual diffs, reasoning logs, and summaries
15. **Healing Service** — performs forensic self-healing analysis and manages healing logs
16. **Playbook Service** — exports and governs deterministic playbooks from diagnostic discoveries
17. **State Management Service** — prepares and cleans deterministic test state
18. **Triage & Confidence Service** — classifies failures with confidence and evidence-backed explanation
19. **Defect Draft Service** — creates defect-quality packets
20. **Policy & Approval Service** — governs risky and uncertain actions
21. **Audit & Observability Service** — captures logs, traces, metrics, RAG logs, mismatch logs, healing logs, and playbook logs

