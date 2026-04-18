Below is the **rewritten Part 2 — Service Design**, updated to fit the **final architectural design**.

I kept the strongest parts of your previous service design:

* clear separation between orchestration, agent runtime, retrieval, graph, execution, and evidence
* explicit Graph-RAG ownership
* deterministic execution boundary
* policy and observability separation

I updated it to reflect the final architecture changes in these areas:

* **distributed understanding** instead of a single broad ingestion/intake flow
* **semantic state map** as a first-class service concern
* **requirement mismatch detection**
* **dual execution modes**: diagnostic vs regression
* **forensic self-healing** and persistent healing logs
* **deterministic playbook export**
* **forensic-grade evidence schema**
* **local shift-left triggers** such as pre-commit hook and optional watch mode

Your prior service design was already strong on RAG, Retrieval Service, Knowledge Graph Service, and deterministic execution. The main gap was that it did not yet promote **artifact fusion**, **state-map generation**, **healing**, **playbooks**, and **local triggers** into explicit service responsibilities. 

---

# Part 2 — Service Design

## AI QA Platform

### Final Architecture-Aligned Version

This section defines the **service-by-service implementation design** for the AI-powered QA platform.

It translates the architecture into deployable components with clear responsibilities, interfaces, ownership boundaries, and runtime behavior.

This version updates the earlier service design so it now fully matches the final architecture with:

* folder-based case ingestion
* browser-readable URL ingestion
* distributed understanding
* semantic state maps
* mismatch detection
* hybrid Graph-RAG
* deterministic and diagnostic execution modes
* forensic self-healing
* forensic-grade evidence
* local shift-left triggers
* no direct Jira/Figma/Azure DevOps API integration yet

---

# 1. Service Design Goals

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

# 2. Top-Level Service Map

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

This is the main structural change from the earlier service design: the final architecture now deserves explicit service ownership for **distributed understanding**, **semantic state maps**, **mismatch detection**, **healing**, **playbooks**, and **local triggers**. 

---

# 3. High-Level Runtime Topology

```text id="k9y7n8"
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
| intake + artifact fusion + requirement mapping prep          |
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
| graph expansion + hybrid retrieval + context packs           |
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
| screenshots, traces, logs, semantic trace, visual diffs     |
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

# 4. Core Service Design Principles

## 4.1 Distributed Understanding Ownership

The final architecture requires understanding to be split across separate responsibilities:

* **Distributed Understanding Service** handles raw intake, normalization, and artifact fusion
* **Semantic State Service** produces semantic state maps
* **Mismatch Detection Service** compares fused artifacts and states to detect pre-run warnings

This is better than overloading one ingestion service.

## 4.2 Graph-RAG Ownership Split

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
* reranking
* context packs
* retrieval policy
* retrieval logs

### Knowledge Graph Service

Owns:

* explicit entities and relationships
* state-map linkage
* requirement/test/evidence lineage
* bounded graph expansion APIs

### Agent Runtime Service

Consumes grounded context packs instead of assembling raw context itself.

## 4.3 Dual Execution Ownership

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

---

# 5. Service-by-Service Design

---

## 5.1 Request Gateway Service

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

### Example input

```json id="d43kff"
{
  "cases": ["login-flow", "business-registration"],
  "env": "UAT",
  "channels": ["web", "api"],
  "policyProfile": "standard-controlled",
  "sourceUrls": [
    "https://internal-docs.example.com/story/US-101"
  ]
}
```

### Example output

```json id="saapco"
{
  "requestId": "REQ-1001",
  "status": "accepted"
}
```

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

## 5.2 Trigger Service

### Purpose

Handle local shift-left triggers such as pre-commit hooks, optional watch mode, and manual local execution.

### Responsibilities

* receive local trigger events
* classify trigger type
* inspect changed files or trigger metadata
* map changed files to likely cases
* create bounded smoke-test requests
* send derived request to Request Gateway / Orchestration
* preserve local trigger audit trail

### Trigger types

* `pre_commit`
* `watch_mode`
* `manual_local`

### Inputs

* git diff file list
* trigger source
* environment
* optional developer-selected case scope

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

---

## 5.3 QA Orchestration Service

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

### Updated internal state machine

```text id="4r9cz4"
PENDING
-> VALIDATING_INPUT
-> INGESTING_ARTIFACTS
-> FUSING_ARTIFACTS
-> BUILDING_STATE_MAP
-> DETECTING_MISMATCHES
-> INDEXING_AND_LINKING
-> BUILDING_CONTEXT
-> GENERATING_STRATEGY
-> GENERATING_TESTS
-> PREPARING_STATE
-> EXECUTING
-> FINALIZING_EVIDENCE
-> ANALYZING_HEALING
-> ANALYZING_RESULTS
-> DRAFTING_DEFECTS
-> EXPORTING_PLAYBOOK (optional)
-> WAITING_APPROVAL (optional)
-> COMPLETED / FAILED / PARTIAL
```

### Persistence

Stores:

* workflow state
* timestamps per stage
* retry counts
* blocking errors
* linked run IDs
* approval checkpoints

### Events consumed

* `qa.request.accepted`
* `qa.trigger.translated`
* `understanding.completed`
* `state_map.completed`
* `mismatch.detected`
* `retrieval.context_pack.ready`
* `execution.completed`
* `triage.completed`
* `approval.decision.recorded`

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

* should support resumable workflows
* must be idempotent per stage
* must preserve causal ordering between mismatch detection and execution

---

## 5.4 Distributed Understanding Service

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

### This service replaces the earlier single broad ingestion interpretation path.

### Inputs

* case names
* folder roots
* source URLs
* ingestion policy
* auth profiles

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

* should support re-ingestion if files change
* should keep immutable snapshots when required
* chunk quality strongly affects downstream RAG quality

---

## 5.5 Semantic State Service

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

### Inputs

* fused artifacts
* requirement refs
* page and API refs
* screenshots and wireframe interpretations

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
* generated state maps must preserve source refs
* should support later linkage to visual diff and playbook export

---

## 5.6 Mismatch Detection Service

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

### Inputs

* fused artifacts
* semantic state maps
* expected-result docs
* known rules and requirements

### Outputs

* mismatch warnings
* severity classifications
* policy escalation flags
* mismatch summaries for retrieval

### Events produced

* `mismatch.detected`
* `mismatch.blocking_detected`
* `mismatch.completed`

### Non-functional notes

* should be deterministic and explainable
* all mismatches must include source refs
* should run before authoring and before execution

---

## 5.7 Knowledge Graph Service

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

### Entities handled

* case
* artifact
* requirement
* page
* UI element
* UI state
* transition
* API endpoint
* defect
* test asset
* run
* evidence
* defect draft
* review decision
* learning signal
* playbook
* mismatch warning

### Example graph operations

* upsert artifact node
* link requirement to state/page/API
* link state to test/assertion
* link run to evidence and defect
* link playbook to originating diagnostic run
* link healing event to unstable element

### Non-functional notes

* graph queries should be fast for lineage and impact lookup
* traversal depth should be bounded and policy-aware
* graph must remain separate from retrieval engine responsibilities

---

## 5.8 Retrieval Service

### Purpose

Provide full Graph-RAG runtime capabilities for agent reasoning.

### Responsibilities

* index chunks and retrieval views
* support hybrid retrieval
* retrieve candidate context by query and filters
* call Knowledge Graph Service for expansion
* rerank retrieved items
* build task-specific context packs
* enforce retrieval policies
* log retrieval queries and selected context
* include state-map refs, mismatch warnings, playbook refs, and healing history where appropriate

### Inputs

* retrieval mode / task type
* query intent
* case ID
* stage context
* graph expansion policy
* filters such as:

  * current case only
  * include history or not
  * approved-only assets
  * include mismatch warnings
  * include healing logs
  * include playbooks
  * execution mode awareness

### Outputs

* ranked context candidates
* graph-expanded context
* final metadata-rich context pack

### Retrieval modes

* understanding
* mapping
* strategy
* authoring
* triage
* defect drafting
* learning

### Updated internal subcomponents

* candidate retriever
* graph expansion orchestrator
* reranker
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

* should support low latency
* retrieval output must be bounded and stage-aware
* should prefer approved/high-quality sources when relevant

---

## 5.9 Agent Runtime Service

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

The final architecture no longer treats intake as one overloaded step. Agent Runtime must respect distributed understanding boundaries.

### Inputs

* workflow stage request
* run context
* artifact references
* retrieval context pack
* state map refs
* mismatch refs
* policy constraints

### Outputs

* case summary
* requirement mappings
* semantic mapping proposals
* strategy
* generated test assets
* triage output
* healing assessment
* defect draft
* learning updates

### Internal components

* prompt builder
* context pack consumer / validator
* agent registry
* tool invocation adapter
* response validator
* confidence estimator

### Persistence

* ephemeral run memory
* optional persisted reasoning summary
* agent execution metadata

### Events produced

* `agent.output.generated`
* `agent.tool.called`
* `agent.step.failed`

### Non-functional notes

* can be stateless if context is externalized
* must not store secrets in raw prompt logs
* must preserve used source refs for audit

---

## 5.10 Test Asset Service

### Purpose

Manage generated and reviewed QA assets as governed artifacts.

### Responsibilities

* store strategy docs
* store test scenarios
* store Playwright tests
* store API specs
* store semantic assertion modules
* store reusable flow modules
* store deterministic playbooks linkage
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

### Outputs

* asset IDs
* version IDs
* reusable asset summaries for retrieval
* playbook links

### Non-functional notes

* strong versioning from day one
* immutable past versions
* must retain context-pack lineage for generated versions

---

## 5.11 Execution Service

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

### Inputs

* approved/draft test assets
* target environment
* execution mode
* state setup requirements
* evidence policy
* optional playbook refs

### Outputs

* run record
* step results
* execution status
* evidence refs

### Internal subcomponents

* run planner
* mode selector
* worker dispatcher
* session tracker
* timeout/retry manager
* result aggregator

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
* must isolate web and API run types cleanly

---

## 5.12 Browser Worker Service

### Purpose

Run web UI tests in isolated browser sessions.

### Responsibilities

* launch browser
* load environment base URL
* authenticate with approved profile
* execute Playwright-backed steps
* perform state-aware waits
* capture screenshot/video/trace/console/network
* support diagnostic or regression mode behavior

### Inputs

* browser execution spec
* session config
* evidence config
* credentials profile
* state-map refs
* optional playbook refs

### Outputs

* per-step status
* session result
* evidence refs
* runtime logs

### Non-functional notes

* can scale horizontally
* state-aware waiting is required for React-style async UIs
* regression mode must not behave like uncontrolled agent exploration

---

## 5.13 API Runner Worker Service

### Purpose

Run API scenario tests in isolated runtime contexts.

### Responsibilities

* manage auth context
* run request chains
* validate responses
* capture request/response evidence
* return structured assertion outcomes

### Inputs

* API scenario definition
* auth profile
* headers/body templates
* assertion set

### Outputs

* response summaries
* assertion outcomes
* evidence refs
* runtime logs

### Non-functional notes

* stateless between runs
* can reuse context within one run only
* must mask secrets in logs

---

## 5.14 Evidence Service

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

### Outputs

* evidenceRef
* bundle refs
* evidence summaries

### Non-functional notes

* evidence must be immutable once finalized
* retention policy configurable
* only summaries, not heavy raw blobs, should normally feed retrieval

---

## 5.15 Healing Service

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

### Inputs

* failed step result
* DOM snapshot
* screenshot
* fingerprint ref
* state-map ref
* execution mode
* policy profile

### Outputs

* healing proposal
* confidence
* healing log ref
* escalation recommendation

### Non-functional notes

* must not silently mutate approved tests
* persistent update requires governance
* should support reuse of prior healing history

---

## 5.16 Playbook Service

### Purpose

Export, store, and manage deterministic playbooks derived from successful diagnostic execution.

### Responsibilities

* capture discovered state signals
* record reliable waits and state transitions
* export deterministic playbooks
* version and govern playbooks
* link playbooks to assets and scenarios
* provide playbook summaries for retrieval

### Inputs

* diagnostic run results
* state signals
* evidence
* approval status if needed

### Outputs

* playbook ref
* playbook summary
* promotion status

### Non-functional notes

* only stable or approved diagnostic discoveries should become regression playbooks
* playbooks should be versioned and reviewable

---

## 5.17 State Management Service

### Purpose

Provide deterministic environment and data preparation.

### Responsibilities

* verify preconditions
* setup test data
* reset supported resources
* cleanup temporary data
* record state actions for audit

### Non-functional notes

* must be heavily policy-controlled
* action catalog should be declarative where possible
* state mutations should remain minimal and explicit

---

## 5.18 Triage & Confidence Service

### Purpose

Analyze execution results and produce structured failure classification with confidence.

### Responsibilities

* combine evidence from web/API runs
* classify failure type
* score evidence quality
* estimate confidence
* recommend next action
* use retrieval support when needed
* include healing context and reasoning logs when relevant

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
* reasoning summary
* suggested action
* supporting refs

### Non-functional notes

* confidence calculation should be explainable
* classification taxonomy must be stable
* should downgrade to review if evidence is incomplete

---

## 5.19 Defect Draft Service

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

### Outputs

* defectDraftId
* draft content
* approval requirement flag

### Current-stage boundary

Internal draft only.
No automatic external ticket submission yet.

---

## 5.20 Policy & Approval Service

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

## 5.21 Audit & Observability Service

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

* avoid storing raw secrets or sensitive bodies
* retrieval and context-pack logging remain critical
* healing and playbook logs should be first-class observable records

---

# 6. Service Interaction Flow

## 6.1 Main synchronous vs asynchronous split

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

---

## 6.2 Primary end-to-end flow

```text id="etiofi"
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

---

# 7. Service Boundaries and Why They Matter

## 7.1 Orchestration vs Agent Runtime

* Orchestration = workflow engine
* Agent Runtime = reasoning engine

## 7.2 Distributed Understanding vs Semantic State Service

* Distributed Understanding = ingest and fuse artifacts
* Semantic State Service = turn fused meaning into state models

## 7.3 Semantic State Service vs Mismatch Detection

* State Service = produces state truth model
* Mismatch Detection = compares truth sources and flags conflicts

## 7.4 Knowledge Graph vs Retrieval

* Graph = explicit relationships
* Retrieval = search + expansion + reranking + context packs

## 7.5 Execution vs Workers

* Execution Service plans and coordinates
* Workers actually run web/API sessions

## 7.6 Healing vs Triage

* Healing analyzes recoverable UI shifts
* Triage explains overall test failure cause

## 7.7 Diagnostic vs Regression

* Diagnostic = discovery
* Regression = deterministic enforcement

This separation is now a core architectural requirement.

---

# 8. Suggested Deployment Shape

## 8.1 Core services

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

## 8.2 Worker pools

* Browser worker pool
* API runner worker pool

## 8.3 Shared stores

* relational DB
* graph DB
* vector/retrieval index
* object storage
* queue/event bus

---

# 9. Service Storage Responsibilities

| Service                   | Primary Storage                         |
| ------------------------- | --------------------------------------- |
| Request Gateway           | relational DB                           |
| Trigger Service           | relational DB / audit log               |
| QA Orchestration          | relational DB / workflow store          |
| Distributed Understanding | relational DB + object storage          |
| Semantic State Service    | relational DB + graph links             |
| Mismatch Detection        | relational DB                           |
| Knowledge Graph           | graph DB                                |
| Retrieval                 | vector/search index + retrieval logs    |
| Agent Runtime             | ephemeral + audit store                 |
| Test Asset                | relational DB + object storage          |
| Execution                 | relational DB                           |
| Browser Worker            | ephemeral session artifacts             |
| API Runner Worker         | ephemeral execution artifacts           |
| Evidence                  | object storage + metadata DB            |
| Healing                   | relational DB + object storage for logs |
| Playbook                  | relational DB + object storage          |
| State Management          | relational DB / action log              |
| Triage & Confidence       | relational DB                           |
| Defect Draft              | relational DB + object storage          |
| Policy & Approval         | relational DB                           |
| Audit & Observability     | log/trace/metrics stores                |

---

# 10. Failure Handling Strategy by Service

## Request Gateway

* reject invalid requests fast
* idempotency key support recommended

## Trigger Service

* degrade gracefully on bad git diff or file mapping
* allow manual override path

## Distributed Understanding

* isolate artifact-level failures
* continue partial ingestion where policy allows

## Semantic State Service

* surface incomplete state maps as warnings
* version partially generated outputs if useful

## Mismatch Detection

* classify blockers vs non-blocking warnings
* never silently suppress mismatches

## Retrieval

* return bounded partial context if some sources fail
* log retrieval degradation

## Agent Runtime

* validate output shape before returning
* fail fast if required context pack is missing or malformed

## Execution

* distinguish infra failure vs test failure
* preserve evidence even on crash

## Healing

* never silently convert low-confidence healing into success
* escalate when confidence is weak

## Triage

* downgrade to human review if evidence is incomplete

## Playbook

* never auto-promote unstable discoveries into regression baseline

---

# 11. Scalability Strategy

## Horizontal scale candidates

* Request Gateway
* Trigger Service
* Distributed Understanding
* Retrieval
* Agent Runtime
* Browser workers
* API workers

## State-heavy services

* Orchestration
* Policy & Approval
* Knowledge Graph
* Semantic State Service
* Evidence metadata
* Audit

## Early bottlenecks

* browser workers
* LLM/agent runtime latency
* retrieval index quality
* graph expansion latency
* evidence volume
* visual diff generation

---

# 12. Security Design Across Services

## Authentication and identity

Each service should authenticate with service-to-service identity.

## Authorization

* policy service decides action rights
* workers run only with approved profiles
* browser URL ingestion limited to approved domains
* retrieval may be filtered by environment, asset status, or approval state
* regression mode must not use unapproved playbooks or healing updates

## Secret handling

* credentials referenced by profile
* no raw secrets in prompts
* no secret values in logs/evidence unless masked and approved

## Environment controls

* UAT/test environments only by default
* stronger approval for sensitive environments
* local trigger workflows still obey policy

---

# 13. Recommended Initial Build Order

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
16. Evidence Service
17. State Management

## Phase D — Intelligence and hardening

18. Agent Runtime
19. Healing Service
20. Triage & Confidence
21. Defect Draft
22. Playbook Service

This build order better matches the final architecture than the earlier RAG-only sequence. 

---

# 14. Minimal MVP vs Production-Minded MVP

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

This is the recommended target.

---

# 15. Final Service Summary

The final recommended service decomposition is:

1. **Request Gateway Service** — receives and validates inbound requests
2. **Trigger Service** — handles local pre-commit, watch mode, and manual local triggers
3. **QA Orchestration Service** — controls lifecycle and workflow state
4. **Distributed Understanding Service** — ingests and fuses folder/URL artifacts
5. **Semantic State Service** — creates semantic state maps, transitions, and fingerprints
6. **Mismatch Detection Service** — detects requirement and artifact conflicts before execution
7. **Knowledge Graph Service** — stores explicit QA relationships and supports bounded graph expansion
8. **Retrieval Service** — provides full Graph-RAG runtime: hybrid search, expansion, reranking, context packs
9. **Agent Runtime Service** — hosts specialized reasoning agents and consumes grounded context packs
10. **Test Asset Service** — manages strategies, tests, reusable modules, and governed versions
11. **Execution Service** — coordinates diagnostic and regression execution
12. **Browser Worker Service** — runs web tests with state-aware waits
13. **API Runner Worker Service** — runs API tests
14. **Evidence Service** — persists forensic-grade evidence, semantic trace, and summaries
15. **Healing Service** — performs forensic self-healing analysis and manages healing logs
16. **Playbook Service** — exports and governs deterministic playbooks from diagnostic discoveries
17. **State Management Service** — prepares and cleans deterministic test state
18. **Triage & Confidence Service** — classifies failures with confidence
19. **Defect Draft Service** — creates defect-quality packets
20. **Policy & Approval Service** — governs risky and uncertain actions
21. **Audit & Observability Service** — captures logs, traces, metrics, RAG logs, mismatch logs, healing logs, and playbook logs

This service design now fully fits the final architecture:

* distributed understanding
* semantic state maps
* mismatch detection
* Graph-RAG
* dual execution modes
* forensic healing
* deterministic playbooks
* forensic-grade evidence
* local shift-left triggers 

