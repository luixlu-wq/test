Below is the **rewritten Part 3 — Knowledge Graph Schema**, updated to match the **final architectural design**.

I kept the strongest parts of your previous graph design:

* graph as the traceability backbone
* Graph-RAG support
* chunk grounding
* requirement → test → run → evidence → defect lineage
* reusable asset discovery
* review and learning support

I updated it to fit the final architecture changes in these areas:

* **distributed understanding**
* **semantic state map as a first-class graph concept**
* **UI states and transitions**
* **element fingerprints for forensic self-healing**
* **requirement mismatch warnings**
* **dual execution modes**
* **deterministic playbooks**
* **forensic-grade evidence schema**
* **local shift-left trigger lineage**

Your prior graph schema was already strong on Graph-RAG and traceability. The main gap was that it did not yet model the new architecture’s **state layer**, **mismatch layer**, **healing layer**, and **playbook layer** explicitly enough. 

---

# Part 3 — Knowledge Graph Schema

## AI QA Platform

### Final Architecture-Aligned Version

This section defines the **knowledge graph schema** for your AI-powered QA platform.

The knowledge graph is the **structured traceability and Graph-RAG backbone** of the system.

It is **not**:

* just a document store
* just a vector store
* just a reporting model

Its job is to represent:

* business intent
* source artifacts
* chunk lineage
* fused case understanding
* semantic state maps
* UI states and transitions
* API behavior
* generated tests
* reusable QA assets
* execution history
* forensic evidence
* mismatch warnings
* healing history
* deterministic playbooks
* defects
* review decisions
* learning signals
* retrieval-time expansion paths

This is what allows the system to answer questions like:

* Which test validates this requirement?
* Which state or transition is tied to this user story line?
* Which defects are linked to this screen or state?
* Which API is triggered by this UI transition?
* Which runs failed for this flow in UAT?
* Which evidence supports this defect draft?
* Which requirements still have no effective coverage?
* Which retrieved chunks should expand into linked flows, pages, states, APIs, and approved tests?
* Which reusable assets should the Test Authoring Agent see for this flow?
* Which element fingerprint was used in a healing decision?
* Which diagnostic run produced the deterministic playbook now used in regression mode?

---

# 1. Why the Knowledge Graph Must Match the Final Architecture

A vector database alone can retrieve relevant text, but it cannot reliably model:

* explicit traceability
* semantic state structure
* mismatch relationships
* healing lineage
* playbook lineage
* retrieval-time relationship expansion

Your final architecture needs more than semantic search. It needs to know:

* what a requirement belongs to
* which page, state, and transition it affects
* which test validates it
* which defects came from failed runs
* what evidence supports those failures
* which generated assets were derived from which sources
* which healing decisions came from which unstable UI element
* which diagnostic discoveries were promoted into deterministic playbooks
* which retrieved chunk should expand into which entities during Graph-RAG

That is why the platform should use:

## Knowledge Graph + Retrieval Layer + Semantic State Layer

* **Knowledge Graph** = explicit entities and relationships
* **Retrieval Layer** = semantic and keyword search over chunks and summaries
* **Graph-RAG** = retrieval + graph expansion + reranking + grounded context assembly
* **Semantic State Layer** = formal model of pages, UI states, transitions, fingerprints, and expected outcomes

The graph is the truth layer for:

* structure
* lineage
* traceability
* expansion neighborhoods
* retrieval grounding
* state-awareness
* healing governance
* playbook provenance

---

# 2. Graph Design Goals

The schema should support:

1. traceability from requirement to defect
2. multi-source ingestion from folder and browser URL sources
3. versioning of artifacts and generated assets
4. run history and evidence lineage
5. risk and coverage analysis
6. future support for PR analysis, Figma, Jira, Azure DevOps, and crawler discovery
7. graph traversal queries for reasoning and reporting
8. retrieval-time entity expansion
9. chunk-to-entity grounding
10. reusable asset discovery for authoring
11. historical defect and failure neighborhood lookup
12. semantic state map lineage
13. requirement mismatch modeling
14. element fingerprint and healing lineage
15. deterministic playbook lineage
16. local trigger lineage for shift-left flows

---

# 3. Modeling Principles

## 3.1 Use stable business nodes

Nodes like `Case`, `Requirement`, `SemanticStateMap`, `TestAsset`, `Run`, `DefectDraft`, and `Playbook` should be first-class nodes.

## 3.2 Separate source artifacts from extracted requirements

A markdown file is not the same as the requirement extracted from it.

Example:

* `Artifact: /stories/US-101.md`
* `Requirement: user can login with valid credentials`

## 3.3 Separate fused understanding from raw artifacts

The system should distinguish:

* raw artifacts
* chunks
* fused semantic understanding
* state map entities

## 3.4 Separate execution from design-time assets

A generated Playwright test is a `TestAsset`.
A specific execution is a `Run`.

## 3.5 Preserve provenance

Every extracted or generated node should connect back to:

* source artifact
* chunk
* run
* review
* trigger

## 3.6 Prefer explicit relationships over implicit text meaning

Do not rely on free text alone to express:

* `validates`
* `maps_to`
* `triggers`
* `healed_from`
* `promoted_to_playbook`

## 3.7 Make chunk lineage explicit

Chunks are the bridge between unstructured source content and structured graph entities.

## 3.8 Make state lineage explicit

Semantic states, transitions, and expected outcomes must be explicit graph entities, not buried in JSON only.

## 3.9 Model graph expansion paths intentionally

The graph should make it easy to expand from:

* chunk → requirement
* requirement → flow
* flow → page/state/transition/API
* requirement → scenario/test asset
* run → evidence/defect/history
* unstable element → fingerprint → healing log
* diagnostic run → discovered state signals → deterministic playbook

---

# 4. Top-Level Graph Domains

The graph should be divided conceptually into these domains:

1. **Case Domain**
2. **Artifact Domain**
3. **Retrieval Grounding Domain**
4. **Understanding Domain**
5. **Requirement Domain**
6. **Semantic State Domain**
7. **Application Domain**
8. **Test Domain**
9. **Execution Domain**
10. **Evidence Domain**
11. **Healing Domain**
12. **Playbook Domain**
13. **Defect Domain**
14. **Review / Governance Domain**
15. **Learning Domain**
16. **Trigger Domain**

This expands the earlier graph design with explicit:

* understanding
* semantic state
* healing
* playbook
* trigger domains. 

---

# 5. Core Node Types

---

## 5.1 Case Domain

### `Case`

Represents a top-level QA case.

#### Example properties

```json id="v3c1hz"
{
  "caseId": "CASE-101",
  "name": "login-flow",
  "feature": "authentication",
  "priority": "high",
  "status": "active",
  "createdAt": "2026-04-18T12:00:00Z"
}
```

### `CaseVersion`

Represents a versioned snapshot of the case configuration.

---

## 5.2 Artifact Domain

### `Artifact`

Represents any ingested source artifact.

Possible artifact types:

* story
* wireframe
* screenshot
* defect_doc
* api_spec
* rules_doc
* expected_result_doc
* url_capture
* html_snapshot
* generated_summary
* test_asset_summary
* triage_summary
* defect_summary
* mismatch_summary
* healing_summary
* playbook_summary

#### Example properties

```json id="1p4d1i"
{
  "artifactId": "ART-201",
  "artifactType": "story",
  "sourceType": "folder",
  "sourcePath": "/test/case/login-flow/stories/US-101.md",
  "sourceUrl": null,
  "mimeType": "text/markdown",
  "checksum": "sha256:def456",
  "capturedAt": "2026-04-18T12:10:00Z",
  "version": 1
}
```

### `ArtifactVersion`

Optional version node for evolving source artifacts.

### `SourceLocation`

Represents normalized source locations.

---

## 5.3 Retrieval Grounding Domain

### `ArtifactChunk`

Represents a chunked piece of source or summary content for retrieval and grounding.

#### Example properties

```json id="d2s5w7"
{
  "chunkId": "CHUNK-9001",
  "artifactId": "ART-201",
  "chunkType": "acceptance_criteria",
  "sectionName": "Acceptance Criteria",
  "title": "Valid Login",
  "text": "User can sign in with valid credentials...",
  "orderIndex": 3,
  "retrievalStatus": "indexed",
  "sourceQuality": "high"
}
```

### `RetrievalView`

Represents summarized/indexable views such as:

* approved test asset summary
* triage summary
* defect summary
* evidence summary
* mismatch summary
* playbook summary
* healing summary
* semantic state summary

### `ContextPack`

Optional node for persisted context packs used by agents.

---

## 5.4 Understanding Domain

This is new and important for the final architecture.

### `CaseUnderstanding`

Represents fused case understanding produced from distributed understanding.

It captures:

* merged interpretation of artifacts
* inferred flows/pages/APIs/rules
* structured gaps/conflicts

#### Example properties

```json id="n7lj20"
{
  "understandingId": "UNDERSTAND-1001",
  "caseId": "CASE-101",
  "summary": "Authentication case covering valid login, invalid password, and forgot-password behavior.",
  "version": 1
}
```

### `Conflict`

Represents contradictions or ambiguities discovered during fusion.

Examples:

* wireframe shows CAPTCHA but story omits it
* expected result says redirect but screenshot shows modal

---

## 5.5 Requirement Domain

### `Requirement`

Represents a normalized business/testing requirement extracted from artifacts.

Possible requirement types:

* acceptance_criteria
* business_rule
* flow_step
* validation
* error_behavior
* negative_case
* visual_expectation
* api_expectation

#### Example properties

```json id="3nz3z3"
{
  "requirementId": "REQ-501",
  "requirementType": "acceptance_criteria",
  "text": "User can sign in with valid credentials",
  "priority": "high",
  "criticality": "high",
  "status": "active"
}
```

### `Flow`

Represents a higher-level business flow.

### `FlowStep`

Represents a step within a flow.

### `Rule`

Optional specialized node if you want business rules separate from generic requirements.

---

## 5.6 Semantic State Domain

This is the biggest architectural addition.

### `SemanticStateMap`

Represents the state model for a case or a major slice of a case.

#### Example properties

```json id="jydm8u"
{
  "stateMapId": "STATEMAP-1001",
  "caseId": "CASE-101",
  "name": "login-flow-state-map",
  "version": 1,
  "status": "active"
}
```

### `UIState`

Represents an observable UI state.

Examples:

* login form ready
* loading spinner visible
* validation error displayed
* dashboard stable
* account locked banner shown

#### Example properties

```json id="ezpq73"
{
  "stateId": "STATE-LOGIN-READY",
  "name": "Login Form Ready",
  "stateType": "page_ready",
  "channel": "web"
}
```

### `Transition`

Represents a state transition.

Examples:

* submit valid credentials → dashboard loaded
* submit invalid password → validation error shown

#### Example properties

```json id="t0ehmn"
{
  "transitionId": "TRANS-1001",
  "name": "submit valid credentials",
  "transitionType": "user_action_to_state"
}
```

### `ExpectedOutcome`

Represents the intended resulting state or behavior.

Examples:

* dashboard visible
* error banner shown
* API returns 200
* account is locked after threshold

### `ElementFingerprint`

Represents a multi-attribute fingerprint of a meaningful UI element.

Examples of captured attributes:

* role
* label
* text family
* CSS classes
* DOM neighborhood
* page context
* relative position
* state-map context

#### Example properties

```json id="xgu9zt"
{
  "fingerprintId": "FP-1001",
  "name": "Submit Button Fingerprint",
  "version": 1,
  "stability": "medium"
}
```

### `MismatchWarning`

Represents a detected requirement mismatch or fusion conflict that matters for QA.

Examples:

* story-wireframe mismatch
* state-expectation mismatch
* expected result contradiction

---

## 5.7 Application Domain

### `Page`

Represents a UI page or view.

### `UIElement`

Represents meaningful UI controls or regions.

### `ApiEndpoint`

Represents a backend API endpoint.

### `DataEntity`

Represents domain/business objects or payload entities.

These remain valid from the earlier graph design. 

---

## 5.8 Test Domain

### `TestStrategy`

Represents a generated or reviewed test strategy.

### `TestScenario`

Represents a human-readable test scenario.

### `TestAsset`

Represents an executable or stored test artifact.

Possible types:

* playwright_test
* api_test_spec
* visual_test_spec
* fixture
* reusable_module
* flow_module
* assertion_module

### `Assertion`

Represents a logical assertion.

Examples:

* login completes successfully
* invalid password error is shown
* dashboard stable
* spinner disappears
* account lockout enforced

---

## 5.9 Execution Domain

### `Run`

Represents a single execution of one or more test assets.

### `RunStep`

Represents an execution step within a run.

### `ExecutionContext`

Represents setup/runtime context for a run.

### `ExecutionMode`

Optional explicit node if you want graph queries over:

* diagnostic
* regression

This is useful if mode lineage matters in graph analytics.

### `TriggerEvent`

Represents local shift-left or request entry origin.

Examples:

* pre_commit
* watch_mode
* manual_local
* API request

This is useful for tracing local-first workflow lineage.

---

## 5.10 Evidence Domain

### `Evidence`

Represents any produced evidence artifact.

Possible evidence types:

* screenshot
* trace
* video
* HAR
* DOM snapshot
* console log
* api_request
* api_response
* report_bundle
* semantic_trace
* reasoning_log
* visual_diff

### `EvidenceSummary`

Represents retrieval-friendly evidence summaries.

### `EvidenceBundle`

Represents grouped evidence for triage or defect drafting.

### `SemanticTrace`

Optional explicit node if you want first-class lineage for:

* requirement line
* wireframe region
* DOM element
* executed step
* evidence ref

This aligns strongly with the final evidence schema.

---

## 5.11 Healing Domain

### `HealingEvent`

Represents a healing decision or proposal generated during or after execution.

#### Example properties

```json id="5iqcqo"
{
  "healingEventId": "HEAL-1001",
  "status": "proposed",
  "confidence": 0.92,
  "reason": "Matched role, label family, and DOM neighborhood."
}
```

### `HealingLog`

Represents a persistent logged record of healing activity.

### `InstabilitySignal`

Optional node for recurring UI or selector instability.

---

## 5.12 Playbook Domain

### `DeterministicPlaybook`

Represents a reusable deterministic execution playbook promoted from diagnostic discoveries.

#### Example properties

```json id="m3ah4e"
{
  "playbookId": "PLAYBOOK-1001",
  "name": "login-valid-credentials-playbook",
  "status": "approved",
  "version": 1
}
```

### `StateSignal`

Represents a discovered execution-ready signal.

Examples:

* spinner disappears
* route stable
* banner visible
* button enabled

This is useful for linking diagnostic discovery to deterministic regression behavior.

---

## 5.13 Defect Domain

### `KnownDefect`

Represents an ingested defect from source materials.

### `DefectDraft`

Represents a defect-quality output created by the system.

### `DefectSummary`

Optional retrieval-oriented defect summary.

### `DefectPacketVersion`

Optional version node for edited defect drafts.

---

## 5.14 Review / Governance Domain

### `ApprovalTask`

Represents a human review checkpoint.

### `ReviewDecision`

Represents a human decision.

Examples:

* approve defect
* reject defect
* approve healing
* reject healing
* approve playbook
* reject playbook
* mark false positive

### `PolicyDecision`

Represents an automated governance decision.

---

## 5.15 Learning Domain

### `LearningSignal`

Represents reusable learning outcomes.

Examples:

* selector instability observed
* recurring defect cluster
* repeated mismatch pattern
* rejected auto-healing pattern
* stable playbook pattern

### `Pattern`

Optional node for stable learned patterns.

---

# 6. Core Relationship Types

Below are the most important relationships.

---

## 6.1 Case relationships

```text id="ep8swu"
(Case)-[:HAS_VERSION]->(CaseVersion)
(Case)-[:CONTAINS_ARTIFACT]->(Artifact)
(Case)-[:HAS_UNDERSTANDING]->(CaseUnderstanding)
(Case)-[:HAS_FLOW]->(Flow)
(Case)-[:HAS_PAGE]->(Page)
(Case)-[:HAS_STATE_MAP]->(SemanticStateMap)
(Case)-[:HAS_TEST_STRATEGY]->(TestStrategy)
(Case)-[:HAS_RUN]->(Run)
(Case)-[:HAS_KNOWN_DEFECT]->(KnownDefect)
(Case)-[:HAS_MISMATCH_WARNING]->(MismatchWarning)
```

---

## 6.2 Artifact and grounding relationships

```text id="7iyx0s"
(Artifact)-[:HAS_CHUNK]->(ArtifactChunk)
(Artifact)-[:HAS_RETRIEVAL_VIEW]->(RetrievalView)
(Artifact)-[:DERIVED_REQUIREMENT]->(Requirement)
(Artifact)-[:DESCRIBES_FLOW]->(Flow)
(Artifact)-[:DESCRIBES_PAGE]->(Page)
(Artifact)-[:DESCRIBES_API]->(ApiEndpoint)
(Artifact)-[:CAPTURED_FROM]->(SourceLocation)
```

### Chunk grounding relationships

```text id="72ok5g"
(ArtifactChunk)-[:GROUNDS_REQUIREMENT]->(Requirement)
(ArtifactChunk)-[:GROUNDS_FLOW]->(Flow)
(ArtifactChunk)-[:GROUNDS_PAGE]->(Page)
(ArtifactChunk)-[:GROUNDS_API]->(ApiEndpoint)
(ArtifactChunk)-[:GROUNDS_STATE]->(UIState)
(ArtifactChunk)-[:GROUNDS_MISMATCH]->(MismatchWarning)
(ArtifactChunk)-[:GROUNDS_KNOWN_DEFECT]->(KnownDefect)
```

These are crucial for Graph-RAG expansion.

---

## 6.3 Understanding relationships

```text id="06gb7g"
(CaseUnderstanding)-[:DERIVED_FROM]->(Artifact)
(CaseUnderstanding)-[:IDENTIFIES_FLOW]->(Flow)
(CaseUnderstanding)-[:IDENTIFIES_PAGE]->(Page)
(CaseUnderstanding)-[:IDENTIFIES_API]->(ApiEndpoint)
(CaseUnderstanding)-[:IDENTIFIES_RULE]->(Rule)
(CaseUnderstanding)-[:HAS_CONFLICT]->(Conflict)
```

---

## 6.4 Requirement relationships

```text id="f2a8nf"
(Requirement)-[:BELONGS_TO_FLOW]->(Flow)
(Requirement)-[:RELATES_TO_PAGE]->(Page)
(Requirement)-[:RELATES_TO_API]->(ApiEndpoint)
(Requirement)-[:RELATES_TO_ENTITY]->(DataEntity)
(Requirement)-[:TRIGGERED_BY]->(UIElement)
(Requirement)-[:AFFECTED_BY]->(KnownDefect)
(Requirement)-[:MAPS_TO_STATE]->(UIState)
(Requirement)-[:MAPS_TO_EXPECTED_OUTCOME]->(ExpectedOutcome)
```

---

## 6.5 Semantic state relationships

```text id="htcigj"
(SemanticStateMap)-[:HAS_PAGE]->(Page)
(SemanticStateMap)-[:HAS_STATE]->(UIState)
(SemanticStateMap)-[:HAS_TRANSITION]->(Transition)
(SemanticStateMap)-[:HAS_FINGERPRINT]->(ElementFingerprint)

(Page)-[:HAS_ELEMENT]->(UIElement)
(Page)-[:HAS_STATE]->(UIState)

(UIElement)-[:HAS_FINGERPRINT]->(ElementFingerprint)
(UIElement)-[:TRIGGERS_TRANSITION]->(Transition)

(Transition)-[:FROM_STATE]->(UIState)
(Transition)-[:TO_STATE]->(UIState)
(Transition)-[:EXPECTS_OUTCOME]->(ExpectedOutcome)
(Transition)-[:CALLS_API]->(ApiEndpoint)

(UIState)-[:DISPLAYS_ELEMENT]->(UIElement)
(UIState)-[:SATISFIES_REQUIREMENT]->(Requirement)

(ExpectedOutcome)-[:RELATES_TO_REQUIREMENT]->(Requirement)
```

This is the largest structural addition required by the final architecture.

---

## 6.6 Mismatch relationships

```text id="m4hy0j"
(MismatchWarning)-[:DETECTED_FROM]->(Artifact)
(MismatchWarning)-[:DETECTED_IN_STATE_MAP]->(SemanticStateMap)
(MismatchWarning)-[:RELATES_TO_REQUIREMENT]->(Requirement)
(MismatchWarning)-[:RELATES_TO_PAGE]->(Page)
(MismatchWarning)-[:RELATES_TO_UI_ELEMENT]->(UIElement)
(MismatchWarning)-[:RELATES_TO_API]->(ApiEndpoint)
```

---

## 6.7 Test and reusable asset relationships

```text id="vmjvlq"
(TestStrategy)-[:COVERS_FLOW]->(Flow)
(TestStrategy)-[:COVERS_REQUIREMENT]->(Requirement)
(TestStrategy)-[:USES_STATE_MAP]->(SemanticStateMap)

(TestScenario)-[:VALIDATES_REQUIREMENT]->(Requirement)
(TestScenario)-[:VALIDATES_FLOW]->(Flow)
(TestScenario)-[:VALIDATES_STATE]->(UIState)
(TestScenario)-[:USES_ASSERTION]->(Assertion)

(TestAsset)-[:IMPLEMENTS_SCENARIO]->(TestScenario)
(TestAsset)-[:CONTAINS_ASSERTION]->(Assertion)
(TestAsset)-[:DERIVED_FROM]->(Artifact)
(TestAsset)-[:GENERATED_FROM_STRATEGY]->(TestStrategy)
(TestAsset)-[:USES_PLAYBOOK]->(DeterministicPlaybook)
```

### Retrieval/reuse relationships

```text id="72omdd"
(RetrievalView)-[:SUMMARIZES_TEST_ASSET]->(TestAsset)
(RetrievalView)-[:SUMMARIZES_SCENARIO]->(TestScenario)
(RetrievalView)-[:SUMMARIZES_STATE_MAP]->(SemanticStateMap)
(RetrievalView)-[:SUMMARIZES_PLAYBOOK]->(DeterministicPlaybook)
(TestAsset)-[:REUSES_MODULE]->(TestAsset)
(TestAsset)-[:RELEVANT_TO_FLOW]->(Flow)
(TestAsset)-[:RELEVANT_TO_PAGE]->(Page)
(TestAsset)-[:RELEVANT_TO_STATE]->(UIState)
```

---

## 6.8 Execution relationships

```text id="r3ehz6"
(Run)-[:EXECUTES_TEST_ASSET]->(TestAsset)
(Run)-[:EXECUTES_SCENARIO]->(TestScenario)
(Run)-[:USES_CONTEXT]->(ExecutionContext)
(Run)-[:TRIGGERED_BY]->(TriggerEvent)
(Run)-[:USES_MODE]->(ExecutionMode)
(Run)-[:HAS_STEP]->(RunStep)

(RunStep)-[:IMPLEMENTS_FLOW_STEP]->(FlowStep)
(RunStep)-[:CHECKS_ASSERTION]->(Assertion)
(RunStep)-[:TARGETS_STATE]->(UIState)
(RunStep)-[:USES_FINGERPRINT]->(ElementFingerprint)
```

---

## 6.9 Evidence relationships

```text id="qk560a"
(Run)-[:PRODUCED_EVIDENCE]->(Evidence)
(RunStep)-[:PRODUCED_EVIDENCE]->(Evidence)
(EvidenceBundle)-[:CONTAINS_EVIDENCE]->(Evidence)
(DefectDraft)-[:ATTACHES_EVIDENCE]->(Evidence)
(Evidence)-[:HAS_SUMMARY]->(EvidenceSummary)
(Evidence)-[:HAS_TRACE]->(SemanticTrace)
(EvidenceSummary)-[:SUPPORTS_TRIAGE_OF]->(Run)
(SemanticTrace)-[:LINKS_REQUIREMENT]->(Requirement)
(SemanticTrace)-[:LINKS_STATE]->(UIState)
(SemanticTrace)-[:LINKS_ELEMENT]->(UIElement)
(SemanticTrace)-[:LINKS_RUN_STEP]->(RunStep)
```

This aligns the graph with the final forensic evidence schema.

---

## 6.10 Healing relationships

```text id="f4js9d"
(HealingEvent)-[:RAISED_FROM_RUN]->(Run)
(HealingEvent)-[:RELATES_TO_RUN_STEP]->(RunStep)
(HealingEvent)-[:RELATES_TO_UI_ELEMENT]->(UIElement)
(HealingEvent)-[:USED_FINGERPRINT]->(ElementFingerprint)
(HealingEvent)-[:SUPPORTED_BY_EVIDENCE]->(Evidence)
(HealingLog)-[:LOGS_EVENT]->(HealingEvent)
(LearningSignal)-[:DERIVED_FROM_HEALING]->(HealingEvent)
```

---

## 6.11 Playbook relationships

```text id="lagfnj"
(DeterministicPlaybook)-[:DERIVED_FROM_RUN]->(Run)
(DeterministicPlaybook)-[:USES_SIGNAL]->(StateSignal)
(DeterministicPlaybook)-[:RELEVANT_TO_FLOW]->(Flow)
(DeterministicPlaybook)-[:RELEVANT_TO_STATE]->(UIState)
(DeterministicPlaybook)-[:APPROVED_BY]->(ReviewDecision)
(StateSignal)-[:DISCOVERED_IN_RUN]->(Run)
(StateSignal)-[:RELATES_TO_STATE]->(UIState)
```

---

## 6.12 Defect relationships

```text id="qmy5t1"
(KnownDefect)-[:AFFECTS_REQUIREMENT]->(Requirement)
(KnownDefect)-[:AFFECTS_FLOW]->(Flow)
(KnownDefect)-[:AFFECTS_PAGE]->(Page)
(KnownDefect)-[:AFFECTS_STATE]->(UIState)

(DefectDraft)-[:RAISED_FROM_RUN]->(Run)
(DefectDraft)-[:RELATES_TO_REQUIREMENT]->(Requirement)
(DefectDraft)-[:RELATES_TO_FLOW]->(Flow)
(DefectDraft)-[:RELATES_TO_PAGE]->(Page)
(DefectDraft)-[:RELATES_TO_STATE]->(UIState)
(DefectDraft)-[:SIMILAR_TO]->(KnownDefect)
```

### Defect retrieval relationships

```text id="x7xj1r"
(RetrievalView)-[:SUMMARIZES_DEFECT]->(KnownDefect)
(RetrievalView)-[:SUMMARIZES_DEFECT_DRAFT]->(DefectDraft)
```

---

## 6.13 Review / governance relationships

```text id="02opra"
(ApprovalTask)-[:REVIEWS]->(DefectDraft)
(ApprovalTask)-[:REVIEWS]->(TestAsset)
(ApprovalTask)-[:REVIEWS]->(HealingEvent)
(ApprovalTask)-[:REVIEWS]->(DeterministicPlaybook)

(ReviewDecision)-[:DECIDES]->(ApprovalTask)

(PolicyDecision)-[:APPLIES_TO]->(Run)
(PolicyDecision)-[:APPLIES_TO]->(DefectDraft)
(PolicyDecision)-[:APPLIES_TO]->(TestAsset)
(PolicyDecision)-[:APPLIES_TO]->(HealingEvent)
(PolicyDecision)-[:APPLIES_TO]->(DeterministicPlaybook)
```

---

## 6.14 Learning relationships

```text id="h33u73"
(LearningSignal)-[:OBSERVED_IN_RUN]->(Run)
(LearningSignal)-[:RELATES_TO_TEST_ASSET]->(TestAsset)
(LearningSignal)-[:RELATES_TO_UI_ELEMENT]->(UIElement)
(LearningSignal)-[:RELATES_TO_FLOW]->(Flow)
(LearningSignal)-[:RELATES_TO_STATE]->(UIState)
(ReviewDecision)-[:GENERATES_SIGNAL]->(LearningSignal)
```

---

## 6.15 Trigger relationships

```text id="30jqj8"
(TriggerEvent)-[:INITIATED_REQUEST_FOR]->(Case)
(TriggerEvent)-[:LED_TO_RUN]->(Run)
(TriggerEvent)-[:AFFECTED_ASSET]->(TestAsset)
```

---

## 6.16 Context relationships

Optional but useful.

```text id="3w7n7b"
(ContextPack)-[:INCLUDES_CHUNK]->(ArtifactChunk)
(ContextPack)-[:INCLUDES_ENTITY]->(Requirement)
(ContextPack)-[:INCLUDES_ENTITY]->(Flow)
(ContextPack)-[:INCLUDES_ENTITY]->(Page)
(ContextPack)-[:INCLUDES_ENTITY]->(UIState)
(ContextPack)-[:INCLUDES_ENTITY]->(ApiEndpoint)
(ContextPack)-[:INCLUDES_ENTITY]->(TestAsset)
(ContextPack)-[:INCLUDES_ENTITY]->(DeterministicPlaybook)
(ContextPack)-[:INCLUDES_WARNING]->(MismatchWarning)
```

---

# 7. Recommended Minimal Schema vs Extended Schema

## 7.1 Minimal schema for early implementation

If you want a practical initial graph, start with these nodes:

* `Case`
* `Artifact`
* `ArtifactChunk`
* `Requirement`
* `Flow`
* `Page`
* `UIState`
* `ApiEndpoint`
* `TestScenario`
* `TestAsset`
* `Run`
* `Evidence`
* `KnownDefect`
* `DefectDraft`
* `MismatchWarning`
* `RetrievalView`

And these relationships:

* `CONTAINS_ARTIFACT`
* `HAS_CHUNK`
* `GROUNDS_REQUIREMENT`
* `GROUNDS_STATE`
* `BELONGS_TO_FLOW`
* `RELATES_TO_PAGE`
* `RELATES_TO_API`
* `MAPS_TO_STATE`
* `VALIDATES_REQUIREMENT`
* `VALIDATES_STATE`
* `IMPLEMENTS_SCENARIO`
* `EXECUTES_TEST_ASSET`
* `PRODUCED_EVIDENCE`
* `RAISED_FROM_RUN`
* `ATTACHES_EVIDENCE`
* `SIMILAR_TO`

This is the correct minimal graph for the final architecture.

## 7.2 Extended schema for production-mature design

Add:

* `CaseVersion`
* `CaseUnderstanding`
* `Conflict`
* `FlowStep`
* `UIElement`
* `Transition`
* `ExpectedOutcome`
* `ElementFingerprint`
* `ExecutionContext`
* `ExecutionMode`
* `EvidenceBundle`
* `EvidenceSummary`
* `SemanticTrace`
* `RetrievalView`
* `ApprovalTask`
* `PolicyDecision`
* `HealingEvent`
* `HealingLog`
* `DeterministicPlaybook`
* `StateSignal`
* `LearningSignal`
* `Pattern`
* `TriggerEvent`
* optionally `ContextPack`

This supports:

* Graph-RAG
* semantic state modeling
* self-healing
* policy traceability
* runtime analytics
* learning feedback
* local trigger lineage
* deterministic playbook lifecycle

---

# 8. Example Subgraph: Login Flow with Final Architecture

```text id="6x0pf4"
(Case: login-flow)
  -> CONTAINS_ARTIFACT -> (Artifact: US-101.md)
  -> CONTAINS_ARTIFACT -> (Artifact: login-page.png)
  -> HAS_STATE_MAP -> (SemanticStateMap: login-flow-state-map)
  -> HAS_FLOW -> (Flow: valid login)

(Artifact: US-101.md)
  -> HAS_CHUNK -> (Chunk: CHUNK-9001)

(Chunk: CHUNK-9001)
  -> GROUNDS_REQUIREMENT -> (Requirement: user can sign in with valid credentials)
  -> GROUNDS_FLOW -> (Flow: valid login)
  -> GROUNDS_PAGE -> (Page: Login Page)
  -> GROUNDS_STATE -> (UIState: Login Form Ready)
  -> GROUNDS_API -> (ApiEndpoint: POST /auth/login)

(SemanticStateMap)
  -> HAS_STATE -> (UIState: Login Form Ready)
  -> HAS_TRANSITION -> (Transition: submit valid credentials)

(Transition: submit valid credentials)
  -> TO_STATE -> (UIState: Dashboard Stable)
  -> CALLS_API -> (ApiEndpoint: POST /auth/login)

(TestScenario: valid login succeeds)
  -> VALIDATES_REQUIREMENT -> (Requirement: user can sign in with valid credentials)
  -> VALIDATES_STATE -> (UIState: Dashboard Stable)

(TestAsset: valid-login.spec.ts)
  -> IMPLEMENTS_SCENARIO -> (TestScenario: valid login succeeds)

(Run: RUN-3001)
  -> EXECUTES_TEST_ASSET -> (TestAsset: valid-login.spec.ts)
  -> PRODUCED_EVIDENCE -> (Evidence: screenshot-final)

(HealingEvent: HEAL-1001)
  -> RELATES_TO_UI_ELEMENT -> (UIElement: Submit Button)
  -> USED_FINGERPRINT -> (ElementFingerprint: FP-1001)

(DeterministicPlaybook: PLAYBOOK-1001)
  -> DERIVED_FROM_RUN -> (Run: RUN-3001)
  -> RELEVANT_TO_STATE -> (UIState: Login Form Ready)
```

This now reflects the final architecture’s state map, healing, and playbook layers.

---

# 9. Node Property Standards

## 9.1 Common properties for most nodes

```json id="qt37o6"
{
  "id": "stable-id",
  "type": "logical-type",
  "status": "active|draft|retired|pending|failed",
  "createdAt": "ISO-8601 timestamp",
  "updatedAt": "ISO-8601 timestamp",
  "version": 1
}
```

## 9.2 Provenance properties where relevant

```json id="g77q7o"
{
  "sourceType": "folder|browser_url|generated|system",
  "sourcePath": "/test/case/login-flow/stories/US-101.md",
  "sourceUrl": null,
  "generatedBy": "test-authoring-agent",
  "generatedFromRunId": "RUN-3001"
}
```

## 9.3 Confidence properties where relevant

```json id="cljlwm"
{
  "confidence": 0.84,
  "confidenceReason": "multiple evidence sources support classification"
}
```

## 9.4 Retrieval properties where relevant

For `ArtifactChunk`, `RetrievalView`, `EvidenceSummary`, `MismatchWarning`, `DeterministicPlaybook`:

```json id="jlwmv7"
{
  "retrievalStatus": "indexed",
  "sourceQuality": "high",
  "approvalStatus": "approved",
  "environmentScope": ["UAT"],
  "lastIndexedAt": "2026-04-18T13:00:00Z"
}
```

---

# 10. Relationship Property Standards

Relationships may also carry metadata.

Example:

```text id="4t839z"
(TestScenario)-[:VALIDATES_REQUIREMENT {
  confidence: 0.93,
  createdBy: "requirement-mapping-agent",
  createdAt: "2026-04-18T13:00:00Z",
  sourceRefs: ["CHUNK-9001"]
}]->(Requirement)
```

Useful relationship properties:

* `confidence`
* `createdBy`
* `createdAt`
* `mappingMethod`
* `notes`
* `sourceRefs`

This remains important for AI-generated mappings and graph-grounded retrieval.

---

# 11. Versioning Strategy

Versioning matters because:

* source artifacts change
* state maps evolve
* generated tests evolve
* defect drafts are edited
* healing history accumulates
* playbooks are promoted
* retrieval summaries may be regenerated

## Recommended immutable versioning targets

* artifacts
* semantic state maps
* test assets
* deterministic playbooks
* defect drafts
* retrieval summaries where needed

And optionally connect them with:

```text id="9n6ue4"
(old_version)-[:SUPERSEDED_BY]->(new_version)
```

---

# 12. Coverage Modeling in the Graph

Coverage is still one of the strongest graph use cases.

## Coverage relationships

```text id="4k9f5u"
(TestScenario)-[:VALIDATES_REQUIREMENT]->(Requirement)
(TestScenario)-[:VALIDATES_STATE]->(UIState)
(TestAsset)-[:IMPLEMENTS_SCENARIO]->(TestScenario)
(Run)-[:EXECUTES_TEST_ASSET]->(TestAsset)
```

From these, you can derive:

* requirement has tests
* requirement has executed tests
* requirement has passing coverage
* state has validating coverage
* state transition has validating coverage
* requirement/state has no coverage

This is stronger than the earlier model because it can now measure **state coverage**, not only requirement coverage.

---

# 13. Query Patterns the Graph Must Support

## Requirement traceability

* Which tests validate requirement `REQ-501`?
* Which runs executed those tests?
* Which defects relate to that requirement?

## State traceability

* Which semantic states are linked to `login-flow`?
* Which transitions are validated by approved tests?
* Which expected outcomes remain uncovered?

## Failure analysis

* For failed run `RUN-3001`, what requirement, state, and flow were impacted?
* What evidence was produced?
* Was healing attempted?

## Artifact lineage

* Which requirements came from `US-101.md`?
* Which chunks grounded them?
* Which state-map entries were derived from them?

## Graph-RAG expansion

* For chunk `CHUNK-9001`, which requirements, flows, pages, states, and APIs should expand?
* For requirement `REQ-501`, which approved reusable assets and playbooks are relevant?
* For failed run `RUN-3001`, which similar defect drafts, evidence summaries, and healing logs should triage see?

## Healing and stability

* Which UI elements have repeated instability?
* Which element fingerprints have produced approved healing?
* Which self-healing proposals were rejected by humans?

## Playbook lineage

* Which diagnostic run produced playbook `PLAYBOOK-1001`?
* Which approved tests currently depend on it?

---

# 14. Example Graph Queries

I’ll use Cypher-style examples.

## 14.1 Find all scenarios validating a requirement

```cypher id="y9y6j8"
MATCH (r:Requirement {requirementId: "REQ-501"})<-[:VALIDATES_REQUIREMENT]-(s:TestScenario)
RETURN s;
```

## 14.2 Find all runs and evidence for a requirement

```cypher id="khqlx7"
MATCH (r:Requirement {requirementId: "REQ-501"})<-[:VALIDATES_REQUIREMENT]-(s:TestScenario)
MATCH (t:TestAsset)-[:IMPLEMENTS_SCENARIO]->(s)
MATCH (run:Run)-[:EXECUTES_TEST_ASSET]->(t)
OPTIONAL MATCH (run)-[:PRODUCED_EVIDENCE]->(e:Evidence)
RETURN run, e;
```

## 14.3 Find uncovered requirements in a case

```cypher id="l6zbm3"
MATCH (c:Case {name: "login-flow"})-[:CONTAINS_ARTIFACT]->(:Artifact)-[:HAS_CHUNK]->(ch:ArtifactChunk)-[:GROUNDS_REQUIREMENT]->(r:Requirement)
WHERE NOT EXISTS {
  MATCH (:TestScenario)-[:VALIDATES_REQUIREMENT]->(r)
}
RETURN DISTINCT r;
```

## 14.4 Expand chunk to authoring context

```cypher id="12ngk1"
MATCH (ch:ArtifactChunk {chunkId: "CHUNK-9001"})
OPTIONAL MATCH (ch)-[:GROUNDS_REQUIREMENT]->(r:Requirement)
OPTIONAL MATCH (ch)-[:GROUNDS_FLOW]->(f:Flow)
OPTIONAL MATCH (ch)-[:GROUNDS_STATE]->(st:UIState)
OPTIONAL MATCH (r)<-[:VALIDATES_REQUIREMENT]-(s:TestScenario)
OPTIONAL MATCH (t:TestAsset)-[:IMPLEMENTS_SCENARIO]->(s)
WHERE t.status = "approved"
RETURN ch, r, f, st, s, t;
```

## 14.5 Find similar defect and healing neighborhood for a failed run

```cypher id="gd9mfg"
MATCH (run:Run {runId: "RUN-3001"})-[:EXECUTES_TEST_ASSET]->(t:TestAsset)
MATCH (t)-[:IMPLEMENTS_SCENARIO]->(s:TestScenario)-[:VALIDATES_REQUIREMENT]->(r:Requirement)
OPTIONAL MATCH (d:KnownDefect)-[:AFFECTS_REQUIREMENT]->(r)
OPTIONAL MATCH (dd:DefectDraft)-[:RELATES_TO_REQUIREMENT]->(r)
OPTIONAL MATCH (he:HealingEvent)-[:RAISED_FROM_RUN]->(run)
RETURN run, r, d, dd, he;
```

---

# 15. Recommended Storage Architecture

A **Neo4j + search/vector index hybrid** remains a strong fit.

## Graph store

Use for:

* entities
* relationships
* traceability
* lineage
* impact queries
* graph expansion neighborhoods
* state relationships
* healing lineage
* playbook lineage

## Retrieval/search store

Use for:

* chunk retrieval
* semantic similarity
* hybrid keyword + vector search
* retrieval views
* evidence summaries
* mismatch summaries
* playbook summaries
* healing summaries

The graph and retrieval layers should be linked through shared IDs such as:

* `artifactId`
* `chunkId`
* `requirementId`
* `stateMapId`
* `stateId`
* `testAssetId`
* `runId`
* `playbookId`
* `retrievalViewId`

---

# 16. Graph Update Workflows

The graph is updated by different services.

## Distributed Understanding updates

Creates:

* `Artifact`
* `ArtifactChunk`
* `SourceLocation`
* `CaseUnderstanding`
* basic `Requirement`
* `Page`
* `ApiEndpoint`

## Semantic State Service updates

Creates:

* `SemanticStateMap`
* `UIState`
* `Transition`
* `ExpectedOutcome`
* `ElementFingerprint`

## Mismatch Detection updates

Creates:

* `MismatchWarning`
* mismatch relationships to requirement/page/state/API

## Retrieval preparation updates

Creates:

* `RetrievalView`
* links from summaries to source entities

## Test authoring updates

Creates:

* `TestStrategy`
* `TestScenario`
* `TestAsset`
* `Assertion`
* reusable relevance relationships

## Execution updates

Creates:

* `Run`
* `RunStep`
* `ExecutionContext`
* `TriggerEvent`
* `Evidence`
* optionally `EvidenceSummary`
* optionally `SemanticTrace`

## Healing updates

Creates:

* `HealingEvent`
* `HealingLog`
* instability-related signals

## Playbook updates

Creates:

* `DeterministicPlaybook`
* `StateSignal`

## Triage/defect/review updates

Creates:

* `DefectDraft`
* `ApprovalTask`
* `ReviewDecision`
* `LearningSignal`

---

# 17. Constraints and Integrity Rules

## Recommended uniqueness constraints

Unique by ID for:

* `Case.caseId`
* `Artifact.artifactId`
* `ArtifactChunk.chunkId`
* `CaseUnderstanding.understandingId`
* `Requirement.requirementId`
* `Flow.flowId`
* `Page.pageId`
* `UIState.stateId`
* `Transition.transitionId`
* `ElementFingerprint.fingerprintId`
* `MismatchWarning.mismatchId`
* `ApiEndpoint.apiId`
* `TestScenario.scenarioId`
* `TestAsset.testAssetId`
* `Run.runId`
* `Evidence.evidenceId`
* `HealingEvent.healingEventId`
* `DeterministicPlaybook.playbookId`
* `DefectDraft.defectDraftId`
* `RetrievalView.retrievalViewId`
* `EvidenceSummary.evidenceSummaryId`

## Important integrity expectations

* every `Requirement` should trace back to at least one `Artifact` or `ArtifactChunk`
* every `ArtifactChunk` should belong to exactly one `Artifact`
* every `UIState` should belong to at least one `SemanticStateMap`
* every `Transition` should connect valid states
* every `TestAsset` should implement at least one `TestScenario`
* every `Run` should execute at least one `TestAsset`
* every `DefectDraft` should link to a `Run`
* every `HealingEvent` should link to a `Run` or `RunStep`
* every `DeterministicPlaybook` should trace back to at least one diagnostic `Run`
* every `Evidence` should link to either `Run` or `RunStep`
* every `RetrievalView` should summarize a valid source node

---

# 18. Recommended Initial Schema Choice

For your current stage, I recommend this practical approach:

## Start with these primary nodes

* `Case`
* `Artifact`
* `ArtifactChunk`
* `Requirement`
* `Flow`
* `Page`
* `UIState`
* `SemanticStateMap`
* `ApiEndpoint`
* `TestScenario`
* `TestAsset`
* `Run`
* `Evidence`
* `MismatchWarning`
* `KnownDefect`
* `DefectDraft`
* `RetrievalView`

## Start with these primary relationships

* `CONTAINS_ARTIFACT`
* `HAS_CHUNK`
* `HAS_STATE_MAP`
* `HAS_STATE`
* `GROUNDS_REQUIREMENT`
* `GROUNDS_STATE`
* `GROUNDS_FLOW`
* `GROUNDS_PAGE`
* `GROUNDS_API`
* `MAPS_TO_STATE`
* `BELONGS_TO_FLOW`
* `RELATES_TO_PAGE`
* `RELATES_TO_API`
* `VALIDATES_REQUIREMENT`
* `VALIDATES_STATE`
* `IMPLEMENTS_SCENARIO`
* `EXECUTES_TEST_ASSET`
* `PRODUCED_EVIDENCE`
* `RAISED_FROM_RUN`
* `ATTACHES_EVIDENCE`
* `SIMILAR_TO`

Then expand later with:

* `CaseUnderstanding`
* `Conflict`
* `FlowStep`
* `UIElement`
* `Transition`
* `ExpectedOutcome`
* `ElementFingerprint`
* `HealingEvent`
* `DeterministicPlaybook`
* `StateSignal`
* `ApprovalTask`
* `LearningSignal`
* `ExecutionContext`
* `EvidenceSummary`
* `SemanticTrace`
* `TriggerEvent`
* optionally `ContextPack`

This gives you a practical graph that matches the final architecture without overcomplicating initial implementation.

---

# 19. Final Schema Summary

The knowledge graph should model the platform as a connected system of:

* **Cases** containing **Artifacts**
* Artifacts containing **Chunks**
* Chunks grounding **Requirements**, **Flows**, **Pages**, **States**, **APIs**, and **Known Defects**
* Cases producing **Case Understanding**
* Cases owning **Semantic State Maps**
* State maps containing **UI States**, **Transitions**, and **Fingerprints**
* Requirements being linked to states and outcomes
* Requirements being validated by **Test Scenarios**
* Scenarios being implemented by **Test Assets**
* Assets being summarized by **Retrieval Views**
* Assets being executed in **Runs**
* Runs producing **Evidence**
* Failures and UI shifts generating **Healing Events**
* Diagnostic discoveries becoming **Deterministic Playbooks**
* Failed runs leading to **Defect Drafts**
* Human review producing **Review Decisions**
* Repeated outcomes producing **Learning Signals**

That gives you full traceability from:

## source artifact → chunk → requirement/flow/page/state/API → test → run → evidence/healing → defect/playbook → review → learning

