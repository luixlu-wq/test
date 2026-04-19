# AI-Powered QA Platform

## Final Architecture and Design Specification

### Current Scope: Folder + Browser-Readable Sources, Agentic QA, MCP, Hybrid Graph-RAG

---

# 1. Executive Summary

This platform is not just a test generator.

It is a **production-oriented AI QA system** designed for a **local-first, artifact-agnostic workflow**. It uses:

* **Agents** for reasoning, mapping, planning, triage, healing analysis, and learning
* **MCP** as the controlled tool layer
* **Hybrid Graph-RAG** for context retrieval, reuse, and traceability
* **Deterministic execution** for repeatable web/API testing
* **Human-in-the-loop governance** for reliability and trust
* **Artifact fusion** to convert manual assets into executable QA knowledge
* **Forensic-grade evidence** to make every pass/fail decision auditable

The system’s purpose is to:

* ingest requirements and QA artifacts from local case folders and browser-readable URLs
* fuse stories, wireframes, screenshots, defects, APIs, rules, and expected results into a unified QA model
* generate a **semantic state map** that describes pages, controls, states, transitions, validations, and business outcomes
* detect requirement mismatches before test execution
* generate risk-based test strategies
* generate executable tests for web and API applications
* run tests through controlled workers
* analyze failures with evidence and historical context
* support controlled self-healing through forensic comparison
* produce defect-quality outputs
* maintain end-to-end traceability across requirement, state, test, result, evidence, and defect
* improve over time from prior runs and human decisions

This is a practical and professional path that does **not** require direct Figma, Jira, Azure DevOps, or similar API integrations in the current stage.

---

# 2. Strategic Position

## 2.1 Artifact-Agnostic Architecture

The system treats folders and browser-readable sources as the source of truth rather than depending on live third-party APIs.

This is a strategic strength because it makes the platform:

* resilient to API outages and breaking changes
* portable across teams and tooling ecosystems
* easier to audit
* easier to reproduce locally
* safer for enterprise environments with restricted integrations

## 2.2 Visible Truth over Hidden Truth

The system prioritizes:

* visible UI behavior
* documented requirements
* screenshots and wireframes
* browser-observable states
* API request/response behavior
* local evidence files

over hidden implementation metadata.

This increases human auditability and reduces trust dependence on external systems.

## 2.3 Local-First Professional Workflow

The platform is intended to be professional **before** enterprise integrations exist.
It supports:

* manual folder-driven QA design
* browser-readable documentation ingestion
* local git-based shift-left testing
* deterministic local or team-hosted execution
* persistent evidence and healing logs

---

# 3. Scope and Constraints

## 3.1 In Scope for Current Stage

### Primary input sources

* local case folders:

  ```text
  /test/case/<case-name>
  ```
* browser-readable URLs to external systems or documents, when accessible through authenticated browser sessions

### Testing targets

* web applications
* API applications

### AI capabilities

* artifact ingestion
* artifact fusion
* semantic state modeling
* requirement understanding
* requirement mismatch detection
* strategy generation
* test generation
* controlled execution planning
* result analysis
* defect draft generation
* confidence scoring
* human review workflow
* forensic self-healing analysis
* learning from prior runs and reviews

### Runtime characteristics

* deterministic execution
* evidence collection
* auditable AI decisions
* reusable generated assets
* local execution support
* local shift-left integration

---

## 3.2 Explicitly Out of Scope for Current Stage

* direct API integrations to Figma, Jira, Azure DevOps, Linear, etc.
* full autonomous crawler/discovery as a default production feature
* uncontrolled live agent browsing in regression mode
* destructive autonomous actions without approval
* automatic external ticket submission by default
* cloud-mandatory architecture

---

## 3.3 Deferred to Future Stages

* structured Figma ingestion through API
* native Jira/Azure DevOps connectors
* controlled crawler agent
* enterprise PR-based targeted regression service
* advanced design-token-aware visual conformance
* portfolio analytics dashboard

---

# 4. Product Vision

The platform should act as an **AI quality engineer**, not merely as a script generator.

It should:

* understand business intent
* fuse disconnected artifacts into one logical QA model
* identify contradictions and gaps before execution
* connect requirements to states, pages, actions, APIs, and assertions
* generate tests from grounded context
* run them deterministically
* explain why they passed or failed
* produce evidence-rich defects
* learn from failure, healing, and review history

The long-term direction is **Autonomous Quality Engineering**, but the current stage remains:

* controlled
* explainable
* deterministic
* locally operable
* auditable

---

# 5. Key Design Principles

## 5.1 AI as Control Plane, Not Blind Executor

AI should reason, correlate, plan, classify, and propose.
Deterministic tools and runners should execute.

## 5.2 MCP as the Standard Tool Bus

All important capabilities should go through MCP-based tools or MCP-like contracts so the system is modular, replaceable, and governed.

## 5.3 Graph-RAG as the Context Backbone

The system must combine:

* retrieval over chunks and summaries
* graph relationships for traceability and expansion
* bounded context packs for agent prompts

## 5.4 Deterministic Runtime

Approved regression execution must be script-like and repeatable.

## 5.5 Dual Execution Modes

The system should support:

* **Diagnostic Mode** for agentic exploration and timing/state discovery
* **Regression Mode** for locked deterministic execution

## 5.6 Traceability First

Every important decision must be traceable back to:

* artifact
* chunk
* semantic state
* requirement
* test asset
* execution evidence
* defect draft
* review decision

## 5.7 Evidence-Driven Decisions

Pass/fail/defect decisions must be backed by:

* assertions
* screenshots
* traces
* logs
* request/response evidence
* visual diffs
* state transition evidence
* reasoning records

## 5.8 Human-in-the-Loop

Uncertain AI outputs must be reviewable.

## 5.9 Progressive Integration

Use folders and browser-readable sources now.
Add native connectors later.

## 5.10 Local-First Professionalism

The system should be valuable and reliable even when all processing and most data remain local.

---

# 6. High-Level Architecture

The final architecture has six major layers:

## 6.1 Request and Trigger Layer

Receives QA requests from:

* CLI / local UI
* local pre-commit hook
* optional watch mode
* service/API calls

## 6.2 Intake and Fusion Layer

Loads manual assets and converts them into structured QA knowledge.

## 6.3 Knowledge and Context Layer

Maintains:

* artifact records
* retrieval chunks
* semantic state maps
* knowledge graph
* retrieval views
* mismatch warnings

## 6.4 Agentic Control Plane

Specialized agents reason over bounded context packs to:

* understand
* map
* strategize
* author
* triage
* heal
* learn

## 6.5 Deterministic Execution Layer

Runs web/API tests via controlled workers.

## 6.6 Evidence and Governance Layer

Stores:

* evidence packages
* visual diffs
* healing logs
* triage summaries
* defect drafts
* approvals
* learning signals

---

# 7. High-Level Architecture Diagram

```text
+-------------------------------------------------------------+
| Request Gateway / CLI / Local Hook / Optional Watch Mode    |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
| QA Orchestration Service                                    |
| workflow, state, approvals, policy                          |
+----------------------+--------------------------------------+
                       |
       ------------------------------------------------
       |                                              |
       v                                              v
+---------------------------+          +----------------------------+
| Distributed Understanding |          | Agent Runtime             |
| Intake / Understanding /  |          | planning + reasoning      |
| Requirement Mapping       |          +-------------+-------------+
+-------------+-------------+                        |
              |                                      v
              v                        +----------------------------+
+---------------------------------------------------------------+  |
| Knowledge & Context Layer                                     |  |
| - artifact store                                              |  |
| - retrieval chunks                                            |  |
| - semantic state maps                                         |  |
| - requirement mismatch detector                               |  |
| - knowledge graph                                             |  |
| - retrieval / Graph-RAG                                       |<--+
+--------------------------+------------------------------------+
                           |
                           v
+---------------------------------------------------------------+
| Test Asset Service                                            |
| strategies, scenarios, Playwright tests, API specs, fixtures  |
| deterministic playbooks                                       |
+--------------------------+------------------------------------+
                           |
                           v
+---------------------------------------------------------------+
| Execution Grid                                                |
| browser runner / api runner                                   |
+------------------+--------------------------+-----------------+
                   |                          |
                   v                          v
+--------------------------+      +----------------------------+
| Browser Automation MCP   |      | API Runner MCP            |
| Playwright-backed        |      | setup + call + assert     |
+--------------------------+      +----------------------------+
                   |
                   v
+---------------------------------------------------------------+
| Evidence + Triage + Healing Layer                             |
| screenshots, traces, logs, DOM, HAR, visual diffs,            |
| reasoning logs, healing logs, defect packets                  |
+---------------------------------------------------------------+
```

---

# 8. Core End-to-End Flow

## Step 1: Request or trigger

A request can come from:

* manual execution
* CLI
* local pre-commit hook
* optional developer watch mode

## Step 2: Folder and source loading

The system loads:

* `/test/case/<case-name>`
* optional browser-readable URLs

## Step 3: Distributed understanding

The system uses separate agents/services to avoid context stuffing:

* **Intake Agent**: raw ingestion and extraction
* **Case Understanding Agent**: artifact fusion and conflict detection
* **Requirement Mapping Agent**: semantic state map generation and traceability mapping

This refinement is correct and should be adopted.

## Step 4: Semantic state map generation

The system builds a structured technical model of:

* pages
* elements
* states
* transitions
* validations
* business rules
* linked APIs
* expected outcomes

## Step 5: Requirement mismatch detection

Before test generation, the system checks for conflicts such as:

* story vs wireframe mismatch
* screenshot vs expected state mismatch
* business rule with no visible UI/API support
* documented control absent in current UI model

## Step 6: Graph-RAG context building

The retrieval service:

* retrieves relevant chunks and summaries
* expands through graph links
* reranks candidates
* builds bounded context packs for each agent task

## Step 7: Strategy generation

The system chooses:

* priority flows
* test types
* evidence requirements
* setup/cleanup needs
* review thresholds

## Step 8: Test authoring

The system generates:

* scenarios
* Playwright specs
* API specs
* semantic assertions
* fixtures
* reusable modules
* deterministic playbooks

## Step 9: Execution

The system executes through:

* browser workers
* API workers
* deterministic runtime contracts

## Step 10: Healing analysis

If a locator or control changes:

* forensic scan runs
* multi-attribute matching is applied
* healing decision is logged
* persistent update requires governance

## Step 11: Triage and defect drafting

The system:

* classifies failure
* estimates confidence
* uses evidence and history
* drafts defect-quality packets

## Step 12: Learning update

The system stores:

* reusable patterns
* repeated defects
* unstable selectors
* accepted/rejected healing
* human review feedback

---

# 9. Input Model

## 9.1 Folder-Based Case Input

Each case lives under:

```text
/test/case/<case-name>/
```

Recommended structure:

```text
/test/case/login-flow/
  case.yaml
  stories/
    US-101.md
  wireframes/
    login-page.png
  screenshots/
    current-login-screen.png
  defects/
    BUG-120.md
  api/
    openapi.yaml
  rules/
    auth-rules.md
  data/
    users.json
  expected/
    expected-ui.md
  refs/
    urls.yaml
  generated/
    strategy/
    tests/
    evidence/
    healing/
    triage/
    playbooks/
```

### New additions

* `generated/healing/`
* `generated/triage/`
* `generated/playbooks/`

These store:

* healing reports
* triage summaries
* deterministic playbooks exported from diagnostic mode

---

## 9.2 Required `case.yaml`

```yaml
caseName: login-flow
feature: authentication
priority: high
channels:
  - web
  - api
entryUrls:
  - https://uat.example.com/login
criticalFlows:
  - valid login
  - invalid password
  - forgot password
sourceUrls:
  - https://internal-docs.example.com/story/US-101
knownDefects:
  - BUG-120
```

## 9.3 Optional `refs/urls.yaml`

```yaml
documents:
  - type: story_page
    url: https://internal-docs.example.com/story/US-101
    authProfile: corp-sso-session
  - type: defect_page
    url: https://tracker.example.com/bug/BUG-120
    authProfile: corp-sso-session
```

---

# 10. Distributed Understanding Model

This is now the correct intake architecture.

## 10.1 Intake Agent

Responsibilities:

* load folders and browser sources
* extract raw text and metadata
* OCR/vision extraction when needed
* validate presence of required files
* preserve provenance

## 10.2 Case Understanding Agent

Responsibilities:

* merge ingested data
* perform artifact fusion
* identify features, flows, pages, APIs, rules
* identify conflicts and gaps
* create fused case understanding

## 10.3 Requirement Mapping Agent

Responsibilities:

* generate the semantic state map
* connect requirements to pages, elements, states, APIs, and assertions
* create traceability links
* flag mismatches and unsupported links

This separation is correct and should be adopted because it reduces context stuffing and improves precision.

---

# 11. Artifact Fusion and Semantic State Map

## 11.1 Artifact Fusion

Artifact fusion means the system does more than summarize files.
It correlates across:

* stories
* wireframes
* screenshots
* rules
* APIs
* defects
* browser-captured pages

## 11.2 Semantic State Map

The result is a structured JSON-like model describing:

* pages
* interactive elements
* expected visual states
* state transitions
* business logic
* validation rules
* API side effects
* linked requirements
* linked defect history

Example:

```json
{
  "caseName": "login-flow",
  "pages": [
    {
      "name": "Login Page",
      "elements": [
        {
          "name": "Email Input",
          "type": "text_input",
          "required": true
        },
        {
          "name": "Submit Button",
          "type": "button",
          "expectedStates": ["enabled", "disabled_when_invalid"]
        }
      ]
    }
  ],
  "businessRules": [
    "Email is required",
    "Invalid password shows error"
  ],
  "transitions": [
    {
      "from": "Login Page",
      "action": "submit valid credentials",
      "to": "Dashboard"
    }
  ]
}
```

## 11.3 Requirement Mismatch Detection

The system shall flag mismatches like:

* field documented but absent in wireframe/UI
* wireframe control present but story missing
* expected screenshot differs from current visual structure
* business rule exists but no observable UI/API evidence exists

These warnings must be surfaced before execution.

---

# 12. Knowledge and Context Layer

The system uses:

## 12.1 Retrieval Layer

For:

* chunk retrieval
* reusable asset retrieval
* run/defect history retrieval
* evidence summary retrieval

## 12.2 Knowledge Graph

For:

* explicit relationships
* lineage
* graph expansion
* traceability
* coverage analysis

## 12.3 Semantic State Repository

For:

* page/state/element/state-transition modeling
* fingerprint persistence
* state-aware assertions
* requirement mismatch detection

So the real model is:

## Knowledge Graph + Retrieval + Semantic State Model

---

# 13. Agent Architecture

The platform uses these agents:

## 13.1 QA Orchestrator Agent

Coordinates workflow and policies.

## 13.2 Intake Agent

Handles raw ingestion and normalization.

## 13.3 Case Understanding Agent

Performs artifact fusion and conflict analysis.

## 13.4 Requirement Mapping Agent

Builds semantic state map and explicit requirement links.

## 13.5 Risk and Strategy Agent

Prioritizes flows, risks, and evidence requirements.

## 13.6 Test Authoring Agent

Generates:

* scenarios
* Playwright tests
* API tests
* semantic assertions
* fixtures
* reusable modules
* deterministic playbooks

## 13.7 Execution Agent

Schedules and monitors deterministic execution.

## 13.8 Failure Triage Agent

Classifies failures using evidence and history.

## 13.9 Healing Agent

Performs forensic self-healing analysis and creates healing logs.

## 13.10 Defect Drafting Agent

Builds defect-quality packets.

## 13.11 Learning Agent

Stores patterns from runs, healing, and reviews.

---

# 14. MCP Tool Layer

Required current-stage MCP tools:

* Filesystem MCP
* Document Parsing MCP
* Browser Reader MCP
* Retrieval MCP
* Graph Expansion MCP
* Context Pack MCP
* Browser Automation MCP
* API Runner MCP
* Evidence MCP
* State Management MCP
* Test Asset MCP

Future-stage MCP tools:

* Jira/ADO native connectors
* Figma structured reader
* PR diff connector
* crawler connector
* test management sync

---

# 15. Graph-RAG Design

## 15.1 Why plain vector RAG is not enough

The system needs:

* chunk retrieval
* explicit state and requirement links
* reusable asset lookup
* history-aware triage
* graph-based expansion

## 15.2 Runtime Graph-RAG flow

1. retrieval query by agent task
2. candidate retrieval from chunks and summaries
3. graph expansion
4. reranking
5. context pack building
6. bounded agent prompt input

## 15.3 Typical retrieved sources

* requirement chunks
* state map summaries
* rule docs
* API specs
* approved test assets
* prior triage summaries
* known defects
* learning signals

---

# 16. Execution Dual-Mode Design

This Gemini refinement is correct and should be included.

## 16.1 Diagnostic Mode (Agentic)

Purpose:

* initial exploration
* building new tests
* discovering state signals
* handling uncertain async behavior
* investigating failures

Behavior:

* think-observe-act loops allowed
* extra evidence capture
* healing suggestions allowed
* state/timing discovery allowed

## 16.2 Regression Mode (Deterministic)

Purpose:

* repeatable approved suite execution

Behavior:

* strict script execution
* fixed semantics
* bounded waits and state signals
* no uncontrolled exploration
* no broad reasoning loops

## 16.3 Deterministic Playbook Export

When Diagnostic Mode successfully discovers reliable timing and state signals, the system should export them into a **Deterministic Playbook**.

A playbook should include:

* expected page readiness signals
* spinner disappearance checks
* required state assertions
* stable action sequence
* known safe locator strategy

This is a strong improvement and fits the architecture well.

---

# 17. React-Aware Execution Design

## 17.1 Why React requires state-aware execution

React apps are asynchronous and state-driven.

So stable execution should wait for:

* render completion
* loading spinner disappearance
* button enabled state
* route stabilization
* validation render completion
* async API-driven UI update completion

## 17.2 State-aware assertions

Examples:

* component ready
* spinner hidden
* validation shown
* dashboard stable
* modal fully mounted

## 17.3 No sleep-based strategy

Fixed sleeps should not be the primary mechanism.

## 17.4 Preferred implementation

Use Playwright state signals and semantic waits.

---

# 18. Self-Healing Design

## 18.1 Multi-Attribute Fingerprinting

When a key element is first recognized, store a fingerprint based on multiple attributes:

* test id
* role
* text
* CSS classes
* relative position
* nearby labels
* DOM neighborhood
* state map identity
* page context
* expected color/shape grouping where useful

## 18.2 Forensic Scan Logic

If a locator breaks:

1. inspect current DOM
2. compare against stored fingerprint
3. score likely successor elements
4. continue only if confidence/policy allows
5. log the healing decision

## 18.3 Healing Log

Every healing action must produce a persistent log, for example:

```text
Healed "Submit Button"
- previous target: #old-submit
- new target: button.primary[type=submit]
- reason: same role, text family, and DOM neighborhood
- confidence: 0.92
- reviewRequired: true
```

## 18.4 Hardened update process

The AI should not endlessly re-heal the same shift without human governance.
Healing decisions should be reviewable and used to harden future tests.

---

# 19. Test Asset Model

Generated assets include:

* strategy documents
* scenario lists
* Playwright tests
* API specs
* fixtures
* reusable modules
* semantic assertion modules
* deterministic playbooks
* defect packet drafts

Lifecycle states:

* draft
* reviewed
* approved
* active
* deprecated
* retired

---

# 20. Assertion Strategy

## 20.1 Avoid brittle raw assertions

Bad:

```js
expect(button).toHaveId('submit-123')
```

## 20.2 Use semantic or state-aware assertions

Better:

```js
expectFlow("checkout").toCompleteSuccessfully()
expectValidation("email required").toAppear()
expectComponentState("loginForm").toBeReady()
```

## 20.3 Business and state examples

```js
expectPage("dashboard").toBeStable()
expectSpinner("login").toDisappear()
expectBusinessRule("account locks after 5 failures").toHold()
```

These assertions should link back to the semantic state map.

---

# 21. State Management and Deterministic Execution

Every generated test should declare:

```json
{
  "preconditions": ["test user exists", "account is unlocked"],
  "dataSetup": ["seed user profile", "clear prior sessions"],
  "cleanup": ["delete temp record", "logout"]
}
```

State Management responsibilities:

* create clean test accounts
* seed and reset data
* clear prior sessions
* cleanup temporary artifacts
* verify deterministic preconditions

---

# 22. Failure Triage and Confidence Engine

Every important decision should include:

* classification
* confidence
* reason
* evidence refs
* suggested action

Example:

```json
{
  "decision": "draft_defect",
  "confidence": 0.82,
  "reason": "API returned 500, UI showed generic error, same path failed twice in clean state",
  "evidenceRefs": ["trace-1", "screenshot-2", "api-log-7"]
}
```

Failure classes:

* product defect
* test issue
* environment issue
* auth/session issue
* data/setup issue
* flaky/transient issue
* needs human review

---

# 23. Evidence Schema

This is now a required architectural component.

## 23.1 Forensic-grade evidence package

Every run must output:

* semantic trace
* execution steps
* screenshots
* DOM snapshots
* traces
* console logs
* network/HAR
* API request/response evidence
* visual regression diffs where applicable
* healing logs
* reasoning logs
* triage summary

## 23.2 Semantic Trace

A structured map linking:

* user story line
* wireframe region / coordinate
* semantic state entry
* DOM element
* executed step
* evidence ref

This is a strong improvement from Gemini and should be adopted.

## 23.3 Evidence folder layout

```text
/test/case/<case-name>/generated/evidence/<run-id>/
  run-summary.json
  semantic-trace.json
  steps.json
  screenshots/
  dom/
  console/
  network/
  api/
  visual-diff/
  healing/
  triage/
  reasoning/
```

## 23.4 Why this matters

This is what makes the platform professional rather than toy-like.

---

# 24. Human-in-the-Loop Workflow

Review is required for:

* low-confidence pass/fail
* artifact mismatches
* healing with insufficient confidence
* ambiguous root cause
* low-confidence defect creation
* significant deterministic playbook updates

Human actions:

* approve
* reject
* edit defect
* reclassify failure
* approve healing
* mark false positive

These feed the learning layer.

---

# 25. Coverage Intelligence

Track:

* known requirements vs tested
* known states vs tested
* known pages vs tested
* known APIs vs tested
* known defects vs regression coverage
* critical flows vs executed flows
* mismatch warnings unresolved
* playbook coverage

---

# 26. Local Shift-Left Workflow

This Gemini refinement is correct with one adjustment already incorporated.

## 26.1 Local Pre-Commit Hook

Recommended default:

* analyze git diff
* map likely affected cases
* run targeted smoke checks
* block commit or warn depending on policy

## 26.2 Watch Mode

Optional developer-activated mode during active feature work.

## 26.3 Why not default auto-run on save

Too noisy and expensive.
Pre-commit + optional watch mode is the correct design.

---

# 27. Security and Governance

## Guardrails

* approved environments only
* approved credentials only
* secrets isolated from prompts
* action tiering
* audit logs for AI and tool actions
* healing persistence requires review where policy says so

## Action tiers

### Tier 0: Read-only

* read folders
* read browser URLs
* parse docs
* generate strategies
* generate draft tests
* generate defect drafts

### Tier 1: Controlled execution

* log into UAT/test environment
* run web/API tests
* create approved test data
* collect evidence
* update internal run status

### Tier 2: Approval required

* submit external defect
* persist healing into approved asset
* modify sensitive systems
* execute destructive actions
* run in sensitive environments

## Policy Profiles

Policy profiles define which action tiers are permitted for a given request context. They are defined in managed configuration, not in user data.

Each policy profile specifies:

* which environments are accessible
* which action tiers are permitted
* which approval thresholds apply
* which evidence requirements are mandatory
* whether healing persistence is allowed
* whether playbook promotion is allowed

### Profile lifecycle

* profiles are defined in a managed configuration file or policy registry
* profiles are assigned at request submission time by the caller or derived from the environment
* profiles are immutable during a run
* profiles are versioned alongside the platform codebase
* profile applications are recorded in the audit log

Suggested default profiles:

* `read-only` — Tier 0 only, no execution
* `standard-controlled` — Tier 0 and Tier 1, no external submission
* `full-controlled` — All tiers with approval gates for Tier 2 actions
* `local-dev` — All tiers with relaxed approval requirements for local development

### Role definitions

The platform recognizes these actor roles:

| Role | Description | Permitted tiers |
| --- | --- | --- |
| `reader` | Can view runs, evidence, and defect drafts | Tier 0 read only |
| `submitter` | Can submit QA requests and trigger execution | Tier 0 and Tier 1 |
| `reviewer` | Can approve, reject, and reclassify HITL items | Tier 0 and Tier 1 |
| `operator` | Can manage cases, assets, and playbooks | Tier 0 and Tier 1 |
| `admin` | Can perform all actions including Tier 2 where policy allows | All tiers |
| `service` | Internal service identity for agent and worker processes | Scoped to service function |

---

# 28. Identity and Access Model

The platform requires a defined identity model to support multi-user operation, HITL review workflow, and governance.

## 28.1 Identity categories

### Human users

Individuals who interact with the platform through CLI, local UI, or API.

Roles include: reader, submitter, reviewer, operator, admin.

### Service identities

Internal processes that act on behalf of the platform.

Examples:

* orchestration service
* agent runtime
* browser worker
* API runner worker

Service identities must:

* authenticate with scoped credentials
* have permissions bounded to their service function
* never escalate to human-user-level Tier 2 actions without an explicit approval gate

### Agent runtime

Agents are a special class of service identity.

Agents:

* act only through MCP tool contracts
* cannot directly mutate approved assets or persisted healing without a Tier 2 approval gate
* must include their agent name and task ID in all tool calls for audit

## 28.2 Authentication model

The platform supports these authentication mechanisms:

### Local-first mode

* single-user or trusted-team mode
* API key or local token
* no external identity provider required
* suitable for local-dev and small team use

### Integrated mode

* OIDC/OAuth2 compatible
* supports SSO via corporate identity provider
* role assignments via identity provider groups or local role mapping
* deferred to Phase 3 native integrations

The authentication mechanism must be replaceable without requiring service redesign.

## 28.3 Authorization model

Authorization follows a role-based access control model.

Rules:

* every inbound request carries an identity
* the identity resolves to a role
* the role is combined with the request policy profile to determine permitted actions
* all authorization decisions are logged in the audit trail

## 28.4 Credential and session isolation

* test environment credentials must never appear in prompts, logs, or agent context packs
* browser authentication profiles are stored separately from the request payload
* credentials are resolved by the execution service from a managed secrets store
* agents receive only a profile reference, not the raw credential

## 28.5 HITL reviewer identity

When an approval task is created:

* it is assigned to a specific reviewer or a reviewer role group
* the reviewer must authenticate before recording a decision
* decisions are attributed to the reviewer identity in the audit log
* anonymous or unattributed decisions are not permitted

---

# 29. Platform Technology Profile

This section defines the required storage categories and committed technology choices for each category.

Technology choices must satisfy the platform's requirements without creating unnecessary operational complexity. The choices below are the committed defaults. Substitutions require a documented decision and a migration path.

## 29.1 Relational database

**Purpose:** Operational records, workflow state, audit logs, metadata for all domains.

**Required:** Yes — this is the primary system of record.

**Committed choice:**

* Production: PostgreSQL 15+
* Local development: SQLite 3.x via the same ORM abstraction

**Key requirements:**

* ACID transactions
* JSON column support for flexible metadata fields
* Sufficient index support for foreign-key-heavy relational queries

## 29.2 Graph store

**Purpose:** Explicit entity relationships, traceability, graph expansion neighborhoods, lineage queries.

**Required:** Yes — relational joins cannot efficiently support multi-hop traceability at production scale.

**Committed choice:**

* Neo4j Community or Enterprise (self-hosted) as the primary graph store
* For early-stage local development, a graph layer backed by relational adjacency tables is acceptable as a temporary shim, with a defined migration path to Neo4j

**Key requirements:**

* Cypher query language support
* Support for relationship properties such as confidence, createdAt, and sourceRefs
* Uniqueness constraints on node IDs

## 29.3 Vector and retrieval index

**Purpose:** Chunk retrieval, semantic search, hybrid BM25 and dense vector retrieval, retrieval views.

**Required:** Yes for any agent reasoning capability.

**Committed choice:**

* Qdrant (self-hosted) as the primary vector store
* pgvector as an acceptable alternative if a unified PostgreSQL deployment is preferred
* Local development fallback: a JSON-backed local vector store with cosine similarity, acceptable for early iteration only, not for production

**Key requirements:**

* Hybrid retrieval supporting both BM25 keyword search and dense vector search
* Metadata filter support on all indexed chunk fields
* Payload storage per chunk for metadata-only queries

## 29.4 Object storage

**Purpose:** Raw artifact files, screenshots, traces, videos, generated test files, playbook files, evidence blobs.

**Required:** Yes.

**Committed choice:**

* Local filesystem with path-based references for local-dev
* S3-compatible object storage for production: AWS S3, MinIO, or equivalent

**Key requirements:**

* Immutable object writes
* Content-addressable storage preferred for evidence integrity
* Retention lifecycle rules configurable per bucket or path prefix

## 29.5 Event bus

**Purpose:** Asynchronous stage triggering, service-to-service event delivery, workflow advancement.

**Required:** For async workflows. Synchronous in-process fallback is acceptable in local-dev and unit tests.

**Committed choice:**

* Redis Streams as the primary recommended choice for simplicity and low operational overhead
* RabbitMQ as an acceptable alternative
* In-process event dispatcher allowed for local-dev and unit tests only

**Key requirements:**

* At-least-once delivery
* Message persistence for workflow events
* Consumer group support for worker scaling

## 29.6 LLM provider

**Purpose:** Agent reasoning, artifact fusion, test authoring, triage, defect drafting, learning.

**Required:** Yes.

**Committed choice:**

* Claude API (Anthropic) as the primary LLM provider
* Any OpenAI-compatible API endpoint as an acceptable secondary or fallback option
* The LLM provider must be abstracted behind an LLM gateway interface so it can be replaced without agent prompt redesign

**Key requirements:**

* Structured output support via JSON mode or tool-use schema enforcement
* Context window sufficient for typical bounded context packs, minimum 32k tokens
* Streaming support for long-running agent tasks

## 29.7 Embedding model

**Purpose:** Chunk vectorization for the retrieval index.

**Required:** Yes.

**Committed choice:**

* A fixed, versioned embedding model per deployment
* Recommended starting point: `text-embedding-3-small` (OpenAI) or a self-hosted sentence-transformer model
* The embedding model version must be stored alongside each indexed chunk record so that re-embedding can be triggered when the model is upgraded

**Key requirements:**

* Stable output dimensions across the deployment lifetime
* The embedding model must never change without a full re-indexing plan
* Embedding model version is a first-class operational configuration value, not a code constant

## 29.8 Vision and OCR

**Purpose:** Wireframe and screenshot content extraction for distributed understanding.

**Required:** For visual artifact ingestion. Deferrable in early phases if wireframes are provided as annotated text or structured JSON.

**Committed choice:**

* Any multimodal LLM vision capability (Claude Vision or equivalent) for structured field extraction from images
* Tesseract OCR as a lightweight fallback for text-only extraction from screenshots

**Key requirements:**

* Output must be structured text suitable for chunking
* Extraction confidence must be preserved as source quality metadata on the resulting artifact chunk

---

# 30. Non-Functional Requirements

## Reliability

* reproducible runs
* controlled retries
* stable evidence collection
* React-aware state synchronization

### Workflow orchestrator recovery

The orchestration service must support recovery from partial failures without duplicating completed work.

Required behaviors:

* workflow stage state is persisted to durable storage after each stage completes
* if the orchestrator restarts mid-workflow, it resumes from the last completed stage
* stage execution is idempotent — re-executing a completed stage produces the same output and no duplicate side-effects
* partially completed stages are retried from the beginning, not from an arbitrary midpoint
* failed stages produce structured error records that include the failure reason and a retryability classification

Retryability classifications:

* `retryable_transient` — network timeout, temporary resource unavailability; retry automatically
* `retryable_with_backoff` — rate limit or resource contention; retry with exponential backoff
* `not_retryable` — invalid input, policy violation, or unrecoverable state; halt and require human review
* `requires_manual_intervention` — partial progress with unknown state; alert and pause workflow

## Auditability

Every agent decision, tool call, retrieval context, healing action, and review decision must be logged.

## Maintainability

Generated tests, playbooks, healing logs, and evidence packages must be versioned and reviewable.

## Explainability

Important actions should include:

* reasoning summary
* confidence
* evidence refs
* mismatch warnings
* healing explanation where relevant

## Performance

The system should support targeted execution and local smoke tests without requiring full-suite reruns.

## Extensibility

Tool and source integrations should remain replaceable.

---

# 31. Recommended Phased Delivery

## Phase 1 — Current Production-Minded MVP

Build:

* folder ingestion
* browser URL read-only ingestion
* distributed understanding model
* artifact fusion
* semantic state map generation
* requirement mismatch detection
* knowledge graph + retrieval
* orchestrator
* strategy generation
* test authoring
* deterministic web/API execution
* evidence schema + evidence folders
* triage + confidence engine
* defect draft generation
* HITL workflow
* state management
* identity and access model (local-first mode)
* policy profile enforcement

## Phase 2 — Operational Hardening

Add:

* multi-attribute fingerprinting
* healing log workflow
* deterministic playbook export
* reusable asset library
* approval console / local review UI
* local pre-commit smoke tests
* optional watch mode

## Phase 3 — Native Integrations

Add:

* Jira/ADO connectors
* Figma structured integration
* external defect submission
* test management sync
* OIDC/SSO integrated authentication mode

## Phase 4 — Autonomous Expansion

Add:

* controlled crawler agent
* PR-based targeted regression
* richer change impact analysis
* portfolio-level risk optimization

---

# 32. Final Functional Requirements

1. The system shall accept inbound requests containing case names, environment, channels, and optional source URLs.
2. The system shall ingest artifacts from local folders and browser-readable URLs.
3. The system shall use distributed understanding across Intake, Case Understanding, and Requirement Mapping.
4. The system shall fuse artifacts into a semantic state map.
5. The system shall detect requirement mismatches before execution where possible.
6. The system shall map requirements, states, pages, actions, APIs, and assertions into a unified knowledge model.
7. The system shall use Graph-RAG to provide bounded context to agents.
8. The system shall generate risk-based test strategies.
9. The system shall generate executable test assets for web and API testing.
10. The system shall support Diagnostic Mode and Regression Mode.
11. The system shall export deterministic playbooks from successful diagnostic discoveries where appropriate.
12. The system shall execute tests through approved tool interfaces.
13. The system shall collect structured forensic-grade evidence.
14. The system shall support React-aware state-driven waits and assertions.
15. The system shall support controlled self-healing with persistent healing logs.
16. The system shall classify failures and estimate confidence.
17. The system shall support human review before uncertain actions proceed.
18. The system shall generate defect-quality packets and stage them according to policy.
19. The system shall maintain requirement-to-state-to-test-to-result traceability.
20. The system shall support deterministic test state management.
21. The system shall support local shift-left triggers through pre-commit hooks and optional watch mode.
22. The system shall learn from prior runs, healing outcomes, and reviewer decisions.
23. The system shall authenticate all inbound requests and attribute all actions to a verified identity.
24. The system shall enforce role-based access control using defined actor roles and policy profiles.
25. The system shall isolate execution credentials and browser session secrets from agent context packs and audit logs.
26. The system shall support workflow resumption after orchestrator failure without duplicating completed stages.

---

# 33. Final Architecture Position

This final design is stronger than the earlier version because it now clearly includes:

* **distributed understanding** instead of overloaded intake
* **artifact fusion** instead of simple document reading
* **semantic state maps** as first-class QA objects
* **requirement mismatch detection**
* **Graph-RAG** as the context backbone
* **dual execution modes**
* **forensic self-healing** with persistent logs
* **React-aware execution stability**
* **forensic-grade evidence schema**
* **local shift-left git workflow**
* **identity and access model** with role-based authorization and policy profile governance
* **committed technology profile** for relational, graph, vector, object storage, LLM, and embedding layers
* **durable workflow recovery** with idempotent stage execution and retryability classification

It still preserves the strongest parts of the original architecture:

* multi-agent reasoning
* MCP-controlled tooling
* folder + browser-source ingestion
* knowledge graph + retrieval
* deterministic execution
* state management
* confidence scoring
* HITL governance
* evidence-driven triage
* future-ready extensibility

---

# 34. Short Final Summary

The final current-stage design is:

**A local-first, artifact-agnostic, multi-agent QA platform with distributed understanding, artifact fusion, semantic state mapping, hybrid Graph-RAG, deterministic and diagnostic execution modes, React-aware state assertions, forensic self-healing with persistent logs, forensic-grade evidence packaging, confidence-based HITL governance, role-based identity and access control, policy profile governance, committed technology stack across relational, graph, vector, and object storage layers, durable workflow recovery, and progressive integration from case folders and browser-readable URLs.**
