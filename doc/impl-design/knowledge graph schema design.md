Yes — below is the **full-length rewritten Part 3 — Knowledge Graph Schema**, with the **broader original section coverage restored** and the **Gemini-approved improvements merged in**.

I restored the sections that still fit the requirements and comments, and only changed what genuinely improved the design:

* made **UIState** and **Transition** more explicitly central for path reasoning
* added **versioned fingerprint lineage**
* strengthened **MismatchWarning** for pre-execution governance
* added **confidence on Evidence → DefectDraft support**
* strengthened **DeterministicPlaybook reuse through shared UI states**

Your original fuller graph document still fit the architecture very well, so this version keeps that fuller structure instead of compressing it.  

---

# Part 3 — Knowledge Graph Schema

## AI QA Platform

### Final Architecture-Aligned Version

#### Full merged rewrite

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

This allows the system to answer questions like:

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

# 1. Why the knowledge graph must match the final architecture

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

# 2. Strategic schema win: the semantic state map as a graph

The most important strength of this schema is the elevation of **UIState** and **Transition** to first-class graph entities.

Traditional document-centric RAG systems flatten UI behavior into text. This design does not.

Instead, it lets the platform reason over an explicit state machine:

* `Login Form Ready`
* `Submit Valid Credentials`
* `Dashboard Stable`

## Why it works

This enables **path reasoning**.

For example, the platform can reason that:

* to reach `Dashboard Stable`
* from `Login Form Ready`
* it must traverse `Submit Valid Credentials`
* which may call `POST /auth/login`

That is much stronger than asking an LLM to guess the flow from scattered documents.

## Result

This reduces logic hallucinations during:

* test generation
* assertion planning
* execution preparation
* defect tracing
* coverage analysis

---

# 3. Graph design goals

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
17. path reasoning across UI states and transitions
18. pre-execution governance for unresolved critical mismatches
19. UI evolution history through fingerprint versioning
20. evidence-to-defect support confidence modeling

---

# 4. Modeling principles

## 4.1 Use stable business nodes

Nodes like `Case`, `Requirement`, `SemanticStateMap`, `TestAsset`, `Run`, `DefectDraft`, and `DeterministicPlaybook` should be first-class nodes.

## 4.2 Separate source artifacts from extracted requirements

A markdown file is not the same as the requirement extracted from it.

Example:

* `Artifact: /stories/US-101.md`
* `Requirement: user can login with valid credentials`

## 4.3 Separate fused understanding from raw artifacts

The system should distinguish:

* raw artifacts
* chunks
* fused semantic understanding
* state map entities

## 4.4 Separate execution from design-time assets

A generated Playwright test is a `TestAsset`.
A specific execution is a `Run`.

## 4.5 Preserve provenance

Every extracted or generated node should connect back to:

* source artifact
* chunk
* run
* review
* trigger

## 4.6 Prefer explicit relationships over implicit text meaning

Do not rely on free text alone to express:

* `validates`
* `maps_to`
* `triggers`
* `healed_from`
* `promoted_to_playbook`

## 4.7 Make chunk lineage explicit

Chunks are the bridge between unstructured source content and structured graph entities.

## 4.8 Make state lineage explicit

Semantic states, transitions, and expected outcomes must be explicit graph entities, not buried in JSON only.

## 4.9 Model graph expansion paths intentionally

The graph should make it easy to expand from:

* chunk → requirement
* requirement → flow
* flow → page/state/transition/API
* requirement → scenario/test asset
* run → evidence/defect/history
* unstable element → fingerprint → healing log
* diagnostic run → discovered state signals → deterministic playbook

## 4.10 Preserve history instead of replacing it

When the UI evolves, the graph should preserve older fingerprints and deprecate them rather than overwrite them. This supports Learning Agent analysis over time.

---

# 5. Top-level graph domains

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

This supports the final architecture’s explicit modeling of:

* distributed understanding
* semantic state
* mismatch/governance
* healing
* playbooks
* trigger lineage

---

# 6. Core node types

## 6.1 Case Domain

### `Case`

Represents a top-level QA case.

Example properties:

```json
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

## 6.2 Artifact Domain

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

Example properties:

```json
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

## 6.3 Retrieval Grounding Domain

### `ArtifactChunk`

Represents a chunked piece of source or summary content for retrieval and grounding.

Example properties:

```json
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

## 6.4 Understanding Domain

### `CaseUnderstanding`

Represents fused case understanding produced from distributed understanding.

It captures:

* merged interpretation of artifacts
* inferred flows/pages/APIs/rules
* structured gaps/conflicts

Example properties:

```json
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

## 6.5 Requirement Domain

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

Example properties:

```json
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

## 6.6 Semantic State Domain

### `SemanticStateMap`

Represents the state model for a case or a major slice of a case.

Example properties:

```json
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

Example properties:

```json
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

Example properties:

```json
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

### `UIElement`

Represents meaningful UI controls or regions.

### `ElementFingerprint`

Represents a multi-attribute identity for a meaningful UI element.

### `FingerprintVersion`

Represents a specific version of a fingerprint over time.

This is a key refinement. Instead of replacing the old fingerprint when the UI changes, the graph should preserve the old version and link the new one as active.

Example properties:

```json
{
  "fingerprintVersionId": "FPV-1002",
  "fingerprintId": "FP-1001",
  "version": 2,
  "status": "active",
  "capturedAt": "2026-04-20T12:00:00Z"
}
```

### `MismatchWarning`

Represents a detected requirement mismatch or fusion conflict that matters for QA.

Examples:

* story-wireframe mismatch
* state-expectation mismatch
* expected result contradiction

### `CriticalMismatch`

Optional specialization or severity classification for mismatches that should be eligible to block execution until reviewed.

---

## 6.7 Application Domain

### `Page`

Represents a UI page or view.

### `ApiEndpoint`

Represents a backend API endpoint.

### `DataEntity`

Represents domain/business objects or payload entities.

---

## 6.8 Test Domain

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

## 6.9 Execution Domain

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

### `TriggerEvent`

Represents local shift-left or request entry origin.

Examples:

* pre_commit
* watch_mode
* manual_local
* API request

---

## 6.10 Evidence Domain

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

Represents first-class lineage for:

* requirement line
* wireframe region
* DOM element
* executed step
* evidence ref

---

## 6.11 Healing Domain

### `HealingEvent`

Represents a healing decision or proposal generated during or after execution.

Example properties:

```json
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

### `DiagnosticDiscovery`

Optional node representing a discovery in diagnostic mode before it is hardened into a playbook.

---

## 6.12 Playbook Domain

### `DeterministicPlaybook`

Represents a reusable deterministic execution playbook promoted from diagnostic discoveries.

Example properties:

```json
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

## 6.13 Defect Domain

### `KnownDefect`

Represents an ingested defect from source materials.

### `DefectDraft`

Represents a defect-quality output created by the system.

### `DefectSummary`

Optional retrieval-oriented defect summary.

### `DefectPacketVersion`

Optional version node for edited defect drafts.

---

## 6.14 Review / Governance Domain

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

## 6.15 Learning Domain

### `LearningSignal`

Represents reusable learning outcomes.

Examples:

* selector instability observed
* recurring defect cluster
* repeated mismatch pattern
* rejected auto-healing pattern
* stable playbook pattern
* fingerprint evolution pattern

### `Pattern`

Optional node for stable learned patterns.

---

# 7. Core relationship types

## 7.1 Case relationships

```text
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

## 7.2 Artifact and grounding relationships

```text
(Artifact)-[:HAS_CHUNK]->(ArtifactChunk)
(Artifact)-[:HAS_RETRIEVAL_VIEW]->(RetrievalView)
(Artifact)-[:DERIVED_REQUIREMENT]->(Requirement)
(Artifact)-[:DESCRIBES_FLOW]->(Flow)
(Artifact)-[:DESCRIBES_PAGE]->(Page)
(Artifact)-[:DESCRIBES_API]->(ApiEndpoint)
(Artifact)-[:CAPTURED_FROM]->(SourceLocation)
```

### Chunk grounding relationships

```text
(ArtifactChunk)-[:GROUNDS_REQUIREMENT]->(Requirement)
(ArtifactChunk)-[:GROUNDS_FLOW]->(Flow)
(ArtifactChunk)-[:GROUNDS_PAGE]->(Page)
(ArtifactChunk)-[:GROUNDS_API]->(ApiEndpoint)
(ArtifactChunk)-[:GROUNDS_STATE]->(UIState)
(ArtifactChunk)-[:GROUNDS_KNOWN_DEFECT]->(KnownDefect)
(MismatchWarning)-[:DETECTED_FROM_CHUNK]->(ArtifactChunk)
```

### Direction note: `DETECTED_FROM_CHUNK`

A mismatch is not grounded in a single chunk the way a requirement or state is — it is detected by comparing two or more conflicting chunks. The relationship therefore points from the warning back to each contributing chunk, consistent with the artifact-level `(MismatchWarning)-[:DETECTED_FROM]->(Artifact)` in section 7.6. A single `MismatchWarning` may have two `DETECTED_FROM_CHUNK` edges: one to the chunk that stated the expectation and one to the chunk that contradicted it.

These are crucial for Graph-RAG expansion.

---

## 7.3 Understanding relationships

```text
(CaseUnderstanding)-[:DERIVED_FROM]->(Artifact)
(CaseUnderstanding)-[:IDENTIFIES_FLOW]->(Flow)
(CaseUnderstanding)-[:IDENTIFIES_PAGE]->(Page)
(CaseUnderstanding)-[:IDENTIFIES_API]->(ApiEndpoint)
(CaseUnderstanding)-[:IDENTIFIES_RULE]->(Rule)
(CaseUnderstanding)-[:HAS_CONFLICT]->(Conflict)
```

---

## 7.4 Requirement relationships

```text
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

## 7.5 Semantic state relationships

```text
(SemanticStateMap)-[:HAS_PAGE]->(Page)
(SemanticStateMap)-[:HAS_STATE]->(UIState)
(SemanticStateMap)-[:HAS_TRANSITION]->(Transition)
(SemanticStateMap)-[:HAS_FINGERPRINT]->(ElementFingerprint)

(Page)-[:HAS_ELEMENT]->(UIElement)
(Page)-[:HAS_STATE]->(UIState)

(UIElement)-[:TRIGGERS_TRANSITION]->(Transition)

(Transition)-[:FROM_STATE]->(UIState)
(Transition)-[:TO_STATE]->(UIState)
(Transition)-[:EXPECTS_OUTCOME]->(ExpectedOutcome)
(Transition)-[:CALLS_API]->(ApiEndpoint)

(UIState)-[:DISPLAYS_ELEMENT]->(UIElement)
(UIState)-[:SATISFIES_REQUIREMENT]->(Requirement)

(ExpectedOutcome)-[:RELATES_TO_REQUIREMENT]->(Requirement)
```

### Fingerprint versioning relationships

```text
(ElementFingerprint)-[:HAS_VERSION]->(FingerprintVersion)
(FingerprintVersion)-[:APPLIES_TO_STATE]->(UIState)
(FingerprintVersion)-[:APPLIES_TO_ELEMENT]->(UIElement)
(FingerprintVersion)-[:SUPERSEDED_BY]->(FingerprintVersion)
(ElementFingerprint)-[:HAS_ACTIVE_VERSION]->(FingerprintVersion)
(ElementFingerprint)-[:HAS_DEPRECATED_VERSION]->(FingerprintVersion)
```

This is the key fix for preserving UI evolution history.

---

## 7.6 Mismatch relationships

```text
(MismatchWarning)-[:DETECTED_FROM]->(Artifact)
(MismatchWarning)-[:DETECTED_IN_STATE_MAP]->(SemanticStateMap)
(MismatchWarning)-[:RELATES_TO_REQUIREMENT]->(Requirement)
(MismatchWarning)-[:RELATES_TO_PAGE]->(Page)
(MismatchWarning)-[:RELATES_TO_UI_ELEMENT]->(UIElement)
(MismatchWarning)-[:RELATES_TO_API]->(ApiEndpoint)
```

### Governance-oriented mismatch relationships

```text
(MismatchWarning)-[:BLOCKS_EXECUTION_OF]->(TestScenario)
(MismatchWarning)-[:REQUIRES_REVIEW_BY]->(ApprovalTask)
(PolicyDecision)-[:BLOCKED_BY_MISMATCH]->(MismatchWarning)
```

This supports programmatic pre-execution governance when a critical mismatch is unresolved.

---

## 7.7 Test and reusable asset relationships

```text
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

```text
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

## 7.8 Execution relationships

```text
(Run)-[:EXECUTES_TEST_ASSET]->(TestAsset)
(Run)-[:EXECUTES_SCENARIO]->(TestScenario)
(Run)-[:USES_CONTEXT]->(ExecutionContext)
(Run)-[:TRIGGERED_BY]->(TriggerEvent)
(Run)-[:USES_MODE]->(ExecutionMode)
(Run)-[:HAS_STEP]->(RunStep)

(RunStep)-[:IMPLEMENTS_FLOW_STEP]->(FlowStep)
(RunStep)-[:CHECKS_ASSERTION]->(Assertion)
(RunStep)-[:TARGETS_STATE]->(UIState)
(RunStep)-[:USES_FINGERPRINT]->(FingerprintVersion)
```

Using `FingerprintVersion` here is more correct than linking only to the abstract fingerprint identity.

---

## 7.9 Evidence relationships

```text
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

### Evidence-to-defect support relationship with confidence

```text
(Evidence)-[:SUPPORTS_DEFECT {
  confidence: 0.87,
  confidenceReason: "Evidence directly shows failed expected state and linked semantic trace."
}]->(DefectDraft)
```

This is the right place to model how strongly a piece of evidence supports a draft defect.

---

## 7.10 Healing relationships

```text
(HealingEvent)-[:RAISED_FROM_RUN]->(Run)
(HealingEvent)-[:RELATES_TO_RUN_STEP]->(RunStep)
(HealingEvent)-[:RELATES_TO_UI_ELEMENT]->(UIElement)
(HealingEvent)-[:USED_FINGERPRINT]->(FingerprintVersion)
(HealingEvent)-[:SUPPORTED_BY_EVIDENCE]->(Evidence)
(HealingLog)-[:LOGS_EVENT]->(HealingEvent)
(LearningSignal)-[:DERIVED_FROM_HEALING]->(HealingEvent)
```

### Optional fingerprint evolution relationships

```text
(HealingEvent)-[:DEPRECATES_FINGERPRINT_VERSION]->(FingerprintVersion)
(HealingEvent)-[:PROMOTES_FINGERPRINT_VERSION]->(FingerprintVersion)
```

---

## 7.11 Playbook relationships

```text
(DeterministicPlaybook)-[:DERIVED_FROM_RUN]->(Run)
(DeterministicPlaybook)-[:USES_SIGNAL]->(StateSignal)
(DeterministicPlaybook)-[:RELEVANT_TO_FLOW]->(Flow)
(DeterministicPlaybook)-[:RELEVANT_TO_STATE]->(UIState)
(DeterministicPlaybook)-[:APPROVED_BY]->(ReviewDecision)
(StateSignal)-[:DISCOVERED_IN_RUN]->(Run)
(StateSignal)-[:RELATES_TO_STATE]->(UIState)
```

### Shared-state playbook reuse

```text
(UIState)-[:HAS_REUSABLE_PLAYBOOK]->(DeterministicPlaybook)
(TestScenario)-[:CAN_REUSE_PLAYBOOK]->(DeterministicPlaybook)
```

This allows playbooks discovered from one test to benefit other tests that share the same state.

---

## 7.12 Defect relationships

```text
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

```text
(RetrievalView)-[:SUMMARIZES_DEFECT]->(KnownDefect)
(RetrievalView)-[:SUMMARIZES_DEFECT_DRAFT]->(DefectDraft)
```

---

## 7.13 Review / governance relationships

```text
(ApprovalTask)-[:REVIEWS]->(DefectDraft)
(ApprovalTask)-[:REVIEWS]->(TestAsset)
(ApprovalTask)-[:REVIEWS]->(HealingEvent)
(ApprovalTask)-[:REVIEWS]->(DeterministicPlaybook)
(ApprovalTask)-[:REVIEWS]->(MismatchWarning)

(ReviewDecision)-[:DECIDES]->(ApprovalTask)

(PolicyDecision)-[:APPLIES_TO]->(Run)
(PolicyDecision)-[:APPLIES_TO]->(DefectDraft)
(PolicyDecision)-[:APPLIES_TO]->(TestAsset)
(PolicyDecision)-[:APPLIES_TO]->(HealingEvent)
(PolicyDecision)-[:APPLIES_TO]->(DeterministicPlaybook)
(PolicyDecision)-[:APPLIES_TO]->(MismatchWarning)
```

---

## 7.14 Learning relationships

```text
(LearningSignal)-[:OBSERVED_IN_RUN]->(Run)
(LearningSignal)-[:RELATES_TO_TEST_ASSET]->(TestAsset)
(LearningSignal)-[:RELATES_TO_UI_ELEMENT]->(UIElement)
(LearningSignal)-[:RELATES_TO_FLOW]->(Flow)
(LearningSignal)-[:RELATES_TO_STATE]->(UIState)
(LearningSignal)-[:RELATES_TO_FINGERPRINT_VERSION]->(FingerprintVersion)
(ReviewDecision)-[:GENERATES_SIGNAL]->(LearningSignal)
```

---

## 7.15 Trigger relationships

```text
(TriggerEvent)-[:INITIATED_REQUEST_FOR]->(Case)
(TriggerEvent)-[:LED_TO_RUN]->(Run)
(TriggerEvent)-[:AFFECTED_ASSET]->(TestAsset)
```

---

## 7.16 Context relationships

```text
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

# 8. Recommended minimal schema vs extended schema

## 8.1 Minimal schema for early implementation

Start with these nodes:

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

## 8.2 Extended schema for production-mature design

Add:

* `CaseVersion`
* `CaseUnderstanding`
* `Conflict`
* `FlowStep`
* `UIElement`
* `Transition`
* `ExpectedOutcome`
* `ElementFingerprint`
* `FingerprintVersion`
* `ExecutionContext`
* `ExecutionMode`
* `EvidenceBundle`
* `EvidenceSummary`
* `SemanticTrace`
* `ApprovalTask`
* `PolicyDecision`
* `HealingEvent`
* `HealingLog`
* `DeterministicPlaybook`
* `StateSignal`
* `DiagnosticDiscovery`
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
* UI evolution history

---

# 9. Example subgraph: login flow with final architecture

```text
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
  -> USED_FINGERPRINT -> (FingerprintVersion: FPV-1002)

(DeterministicPlaybook: PLAYBOOK-1001)
  -> DERIVED_FROM_RUN -> (Run: RUN-3001)
  -> RELEVANT_TO_STATE -> (UIState: Login Form Ready)

(UIState: Login Form Ready)
  -> HAS_REUSABLE_PLAYBOOK -> (DeterministicPlaybook: PLAYBOOK-1001)
```

---

# 10. Node property standards

## 10.1 Common properties for most nodes

```json
{
  "id": "stable-id",
  "type": "logical-type",
  "status": "active|draft|retired|pending|failed",
  "createdAt": "ISO-8601 timestamp",
  "updatedAt": "ISO-8601 timestamp",
  "version": 1
}
```

## 10.2 Provenance properties where relevant

```json
{
  "sourceType": "folder|browser_url|generated|system",
  "sourcePath": "/test/case/login-flow/stories/US-101.md",
  "sourceUrl": null,
  "generatedBy": "test-authoring-agent",
  "generatedFromRunId": "RUN-3001"
}
```

## 10.3 Confidence properties where relevant

```json
{
  "confidence": 0.84,
  "confidenceReason": "multiple evidence sources support classification"
}
```

## 10.4 Retrieval properties where relevant

For `ArtifactChunk`, `RetrievalView`, `EvidenceSummary`, `MismatchWarning`, `DeterministicPlaybook`:

```json
{
  "retrievalStatus": "indexed",
  "sourceQuality": "high",
  "approvalStatus": "approved",
  "environmentScope": ["UAT"],
  "lastIndexedAt": "2026-04-18T13:00:00Z"
}
```

---

# 11. Relationship property standards

Relationships may also carry metadata.

Example:

```text
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

The new `Evidence -> DefectDraft` support relationship should also carry:

* `confidence`
* `confidenceReason`
* `createdAt`

---

# 12. Versioning strategy

Versioning matters because:

* source artifacts change
* state maps evolve
* generated tests evolve
* defect drafts are edited
* healing history accumulates
* playbooks are promoted
* retrieval summaries may be regenerated
* UI fingerprints evolve

## Recommended immutable versioning targets

* artifacts
* semantic state maps
* test assets
* deterministic playbooks
* defect drafts
* retrieval summaries where needed
* fingerprint versions

And optionally connect them with:

```text
(old_version)-[:SUPERSEDED_BY]->(new_version)
```

---

# 13. Coverage modeling in the graph

Coverage is one of the strongest graph use cases.

## Coverage relationships

```text
(TestScenario)-[:VALIDATES_REQUIREMENT]->(Requirement)
(TestScenario)-[:VALIDATES_STATE]->(UIState)
(TestScenario)-[:VALIDATES_TRANSITION]->(Transition)
(TestAsset)-[:IMPLEMENTS_SCENARIO]->(TestScenario)
(Run)-[:EXECUTES_TEST_ASSET]->(TestAsset)
```

From these, you can derive:

* requirement has tests
* requirement has executed tests
* requirement has passing coverage
* state has validating coverage
* transition has validating coverage
* requirement/state/transition has no coverage

---

# 14. Query patterns the graph must support

## Forward traceability

* Show me all tests impacted by a change in this user story.
* Show me all scenarios linked to this changed state.
* Show me all tests that can reuse this playbook.

## Backward traceability

* Show me exactly which requirement failed based on this screenshot.
* Show me which state and transition produced this evidence.
* Show me which mismatch warning may explain this blocked run.

## Coverage analysis

* Which UI states in our semantic map currently have zero associated test scenarios?
* Which transitions currently have no validating scenarios?
* Which critical requirements only have draft coverage?

## Failure analysis

* For failed run `RUN-3001`, what requirement, state, and flow were impacted?
* What evidence was produced?
* Was healing attempted?
* Which evidence supports the defect draft most strongly?

## Healing and stability

* Which UI elements have repeated instability?
* Which fingerprint versions were deprecated over time?
* Which self-healing proposals were rejected by humans?

## Playbook lineage

* Which diagnostic run produced playbook `PLAYBOOK-1001`?
* Which shared UI states can reuse it?
* Which approved tests currently depend on it?

---

# 15. Example graph queries

## 15.1 Find all scenarios validating a requirement

```cypher
MATCH (r:Requirement {requirementId: "REQ-501"})<-[:VALIDATES_REQUIREMENT]-(s:TestScenario)
RETURN s;
```

## 15.2 Find all runs and evidence for a requirement

```cypher
MATCH (r:Requirement {requirementId: "REQ-501"})<-[:VALIDATES_REQUIREMENT]-(s:TestScenario)
MATCH (t:TestAsset)-[:IMPLEMENTS_SCENARIO]->(s)
MATCH (run:Run)-[:EXECUTES_TEST_ASSET]->(t)
OPTIONAL MATCH (run)-[:PRODUCED_EVIDENCE]->(e:Evidence)
RETURN run, e;
```

## 15.3 Find uncovered requirements in a case

```cypher
MATCH (c:Case {name: "login-flow"})-[:CONTAINS_ARTIFACT]->(:Artifact)-[:HAS_CHUNK]->(ch:ArtifactChunk)-[:GROUNDS_REQUIREMENT]->(r:Requirement)
WHERE NOT EXISTS {
  MATCH (:TestScenario)-[:VALIDATES_REQUIREMENT]->(r)
}
RETURN DISTINCT r;
```

## 15.4 Find UI states with zero scenario coverage

```cypher
MATCH (:SemanticStateMap {stateMapId: "STATEMAP-1001"})-[:HAS_STATE]->(st:UIState)
WHERE NOT EXISTS {
  MATCH (:TestScenario)-[:VALIDATES_STATE]->(st)
}
RETURN st;
```

## 15.5 Find evidence supporting a defect draft with confidence

```cypher
MATCH (e:Evidence)-[rel:SUPPORTS_DEFECT]->(d:DefectDraft {defectDraftId: "DD-9001"})
RETURN e, rel.confidence, rel.confidenceReason
ORDER BY rel.confidence DESC;
```

## 15.6 Find reusable playbooks for a state

```cypher
MATCH (st:UIState {stateId: "STATE-LOGIN-READY"})-[:HAS_REUSABLE_PLAYBOOK]->(p:DeterministicPlaybook)
RETURN p;
```

---

# 16. Storage architecture

The platform commits to **Neo4j** as the graph store and a **Qdrant or pgvector** vector index as the retrieval/search layer. These are not recommendations — they are the committed technology choices recorded in the architectural design (Section 29 — Platform Technology Profile).

Neo4j is selected because:

* it natively supports labeled property graphs with typed relationships
* Cypher is expressive for path reasoning, coverage queries, and impact analysis
* it supports uniqueness constraints and indexes on node properties
* it supports multi-node transactions needed for atomic graph writes
* it supports MERGE semantics for idempotent writes

The graph and vector layers are loosely coupled through shared IDs. Neither layer stores the other's primary data.

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
* mismatch governance

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
* `transitionId`
* `testAssetId`
* `runId`
* `playbookId`
* `retrievalViewId`

---

# 17. Graph update workflows

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
* `FingerprintVersion`

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
* `InstabilitySignal`
* fingerprint evolution links where needed

## Playbook updates

Creates:

* `DiagnosticDiscovery`
* `DeterministicPlaybook`
* `StateSignal`

## Triage / defect / review updates

Creates:

* `DefectDraft`
* `ApprovalTask`
* `ReviewDecision`
* `LearningSignal`

---

## 17.1 Graph write atomicity and transaction boundaries

Every graph write from a service must be **atomic at the Neo4j transaction level**. A partial graph write — where some nodes are created and a subsequent relationship write fails — leaves the graph in an inconsistent state that is difficult to detect and repair.

### Transaction scope per service write

Each service graph write must be issued as a **single Neo4j transaction** covering all nodes and relationships that logically belong together:

| Service write          | Transaction scope                                                               |
| ---------------------- | ------------------------------------------------------------------------------- |
| Distributed Understanding writes `Artifact` + chunks + `Requirement` nodes | One transaction per artifact ingestion |
| Semantic State Service writes `SemanticStateMap` + `UIState` + `Transition` + `ElementFingerprint` + `FingerprintVersion` | One transaction per state map |
| Mismatch Detection writes `MismatchWarning` + `DETECTED_FROM` relationships | One transaction per mismatch event |
| Test Authoring writes `TestScenario` + `TestAsset` + `Assertion` + relationships | One transaction per asset generation |
| Execution Service writes `Run` + `RunStep` + `Evidence` relationships | One transaction per run record |
| Healing Service writes `HealingEvent` + fingerprint evolution links | One transaction per healing event |
| Playbook Service writes `DeterministicPlaybook` + `StateSignal` + playbook relationships | One transaction per playbook |

### Failure handling

If a Neo4j transaction rolls back due to a constraint violation or transient error:

* the service must **not** mark the workflow stage as complete in the relational store
* the service must emit a failure event or surface the error so the orchestrator can retry the stage
* the graph should be treated as unmodified — no partial cleanup is needed because the transaction rolled back
* if the error is a uniqueness constraint conflict on a node that already exists from a prior attempt, treat it as a re-ingestion case (see section 17.2)

### No cross-service graph transactions

Services must not participate in distributed transactions that span multiple services' graph writes. If Service A writes to Neo4j and Service B must write a relationship linking A's nodes to B's nodes, Service B must read A's nodes by ID and write its own relationships in a separate transaction. Partial failures in this case are handled by retry at the service level, not by distributed rollback.

---

## 17.2 Re-ingestion idempotency

A service may be retried after a partial failure, a workflow replay, or an intentional re-processing request. The graph must tolerate re-running the same write without creating duplicate nodes or inconsistent state.

### MERGE vs CREATE

All node writes to Neo4j must use `MERGE` on the node's stable business ID, not `CREATE`. A `MERGE` finds the existing node if present or creates it if absent — this is the correct primitive for idempotent node writes.

```cypher
// Correct — idempotent
MERGE (r:Requirement {requirementId: "REQ-501"})
ON CREATE SET r.text = $text, r.status = "active", r.createdAt = $now
ON MATCH SET r.updatedAt = $now

// Wrong — creates duplicate on retry
CREATE (r:Requirement {requirementId: "REQ-501", text: $text})
```

### Relationship idempotency

Relationships must also use `MERGE` to prevent duplicate edges between the same node pairs:

```cypher
MATCH (chunk:ArtifactChunk {chunkId: "CHUNK-9001"})
MATCH (req:Requirement {requirementId: "REQ-501"})
MERGE (chunk)-[:GROUNDS_REQUIREMENT]->(req)
```

For relationships that carry properties (e.g. `SUPPORTS_DEFECT` with confidence), `MERGE` on the relationship type and direction, then `SET` the properties on match:

```cypher
MATCH (e:Evidence {evidenceId: "EV-1001"})
MATCH (d:DefectDraft {defectDraftId: "DD-9001"})
MERGE (e)-[rel:SUPPORTS_DEFECT]->(d)
SET rel.confidence = $confidence, rel.confidenceReason = $reason, rel.updatedAt = $now
```

### Versioned nodes on re-ingestion

When a service re-ingests content that was previously processed (e.g. an artifact is re-parsed after the source file changed), it must:

1. `MERGE` the parent node (e.g. `Artifact`) by its stable ID — this finds the existing node
2. Increment the `version` property and set `updatedAt`
3. For version-sensitive child nodes (e.g. `FingerprintVersion`, `ArtifactChunk`), check whether the content has changed using a checksum comparison before deciding to create a new version node
4. If a new version is warranted, create the new version node and add a `SUPERSEDED_BY` relationship from the old version to the new one
5. Do not delete the old version node — preserve history

### Stale relationship cleanup

When a service regenerates a set of relationships (e.g. the Semantic State Service rebuilds a `SemanticStateMap` and its `HAS_STATE` edges), it must:

1. `MERGE` the `SemanticStateMap` node
2. For each new `UIState`, `MERGE` the state node and `MERGE` the `HAS_STATE` relationship
3. For states that no longer appear in the new map, set their `status` to `deprecated` — do not delete them, because runs and healing events may still reference them

---

# 18. Constraints and integrity rules

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
* `FingerprintVersion.fingerprintVersionId`
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
* every active `ElementFingerprint` should have exactly one active `FingerprintVersion`
* every `CriticalMismatch` should either be resolved or linked to an approval/governance decision before blocked execution proceeds

---

# 19. Recommended initial schema choice

For your current stage, I recommend this practical approach.

## Start with these primary nodes

* `Case`
* `Artifact`
* `ArtifactChunk`
* `Requirement`
* `Flow`
* `Page`
* `UIState`
* `SemanticStateMap`
* `Transition`
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
* `HAS_TRANSITION`
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

## Add early in V1.1 if possible

* `UIElement`
* `ExpectedOutcome`
* `ElementFingerprint`
* `FingerprintVersion`
* `HealingEvent`
* `SemanticTrace`
* `DeterministicPlaybook`
* `StateSignal`
* `ApprovalTask`

This gives you a practical graph that matches the final architecture without losing the most important refinements.

---

# 20. Final schema summary

The knowledge graph should model the platform as a connected system of:

* **Cases** containing **Artifacts**
* Artifacts containing **Chunks**
* Chunks grounding **Requirements**, **Flows**, **Pages**, **States**, **Transitions**, **APIs**, and **Known Defects**
* Cases producing **Case Understanding**
* Cases owning **Semantic State Maps**
* State maps containing **UI States**, **Transitions**, and **Fingerprints**
* Fingerprints carrying **version history** instead of being overwritten
* Requirements being linked to states and outcomes
* Requirements and artifacts producing **MismatchWarnings**
* Critical unresolved mismatches supporting **pre-execution governance**
* Requirements being validated by **TestScenarios**
* Scenarios being implemented by **TestAssets**
* Assets being summarized by **RetrievalViews**
* Assets being executed in **Runs**
* Runs producing **Evidence**
* Evidence supporting **DefectDrafts** with confidence on the support relationship
* Failures and UI shifts generating **HealingEvents**
* Diagnostic discoveries becoming **DeterministicPlaybooks**
* Playbooks being reusable through shared **UIStates**
* Human review producing **ReviewDecisions**
* Repeated outcomes producing **LearningSignals**

That gives you full traceability from:

## source artifact → chunk → requirement/flow/page/state/transition/API → test → run → evidence/healing → defect/playbook → review → learning
