I don’t see the Gemini review text in your message, so I can’t map changes to each comment one by one. I used your uploaded Part 4 as the source and strengthened the areas that most likely need refinement in line with the rest of the architecture: native state-aware execution, stricter diagnostic vs regression behavior, stronger forensic evidence hooks, clearer healing governance, and stronger playbook hardening. 

Below is the **rewritten Part 4 — Playwright Hybrid Framework**, kept full-length and aligned to the final architecture.

---

# Part 4 — Playwright Hybrid Framework

## AI QA Platform

### Final Architecture-Aligned Version

#### Full merged rewrite

This section defines the **Playwright + AI + Graph-RAG hybrid framework** for your QA platform.

The goal is **not** to let AI directly drive the browser in an uncontrolled way for every run.

The goal is to combine:

* **Playwright** for deterministic browser automation
* **AI agents** for planning, generation, mismatch-aware authoring, healing proposals, semantic assertions, and triage
* **Graph-RAG** for grounded requirement understanding, state-map-aware authoring, reusable asset reuse, and historical comparison
* **semantic state maps** as first-class execution guidance
* **governed test assets** for repeatability
* **forensic-grade evidence** for traceability and review
* **diagnostic discovery + deterministic playbook export** for long-term stability

This framework is the practical bridge between:

* your final agent architecture
* MCP tool contracts
* Retrieval / Graph-RAG subsystem
* semantic state service
* execution service
* evidence service
* healing service
* playbook service
* knowledge graph
* defect workflow

---

# 1. Framework goals

The framework should support:

1. deterministic browser execution
2. AI-assisted test generation
3. Graph-RAG-grounded authoring and reuse
4. semantic-state-aware execution
5. requirement mismatch awareness
6. reusable test modules
7. semantic and business-level assertions
8. forensic-grade evidence collection
9. controlled forensic self-healing
10. diagnostic discovery and deterministic playbook export
11. traceability to requirements, states, flows, pages, and APIs
12. future extension to visual checks, PR-based regression, and crawler discovery

The uploaded version already had the right direction. The main strengthening in this rewrite is to make the runtime layer more explicitly **state-native**, more explicitly **diagnostic vs regression aware**, and more explicitly connected to the evidence and hardening workflow. 

---

# 2. Core design principle

## 2.1 AI should author, discover, and explain — not replace the runtime

At runtime, the browser should be controlled by:

* Playwright-based code
* or structured execution specs compiled into deterministic Playwright behavior
* optionally guided by an approved deterministic playbook

AI should be used for:

* generating tests
* selecting flows
* mapping requirements to assertions
* reading mismatch warnings
* proposing locator healing
* interpreting failures
* drafting updates
* retrieving reusable patterns
* retrieving similar historical failures
* grounding scenario generation in artifacts, semantic state maps, and graph links
* discovering state signals in diagnostic mode

Playwright should be used for:

* launching browser
* navigation
* element interaction
* state-aware waiting
* state-aware assertions
* tracing
* screenshots/video
* DOM/network capture
* visual diff capture where needed

Graph-RAG should be used for:

* requirement grounding
* semantic state grounding
* reusable asset discovery
* assertion pattern discovery
* mismatch-aware authoring
* similar defect/run lookup
* authoring-time context assembly
* triage-time historical comparison

This keeps execution stable and authoring grounded.

---

# 3. Execution philosophy

The final architecture requires a stronger execution philosophy than normal browser automation.

## 3.1 Visible-truth execution

The framework should validate what is visible and observable:

* rendered UI state
* state transitions
* request/response outcomes
* evidence artifacts
* user-observable business outcomes

## 3.2 State-aware execution

The framework should execute against semantic state expectations, not only DOM selectors.

This means the runtime should understand:

* current expected state
* next expected state
* acceptable transition signals
* stable conditions for action/assertion
* mismatch warnings that may make state assumptions unsafe

## 3.3 Deterministic-by-default execution

Stable regression mode must not depend on free-form AI thinking at runtime.

## 3.4 Diagnostic discovery mode

When needed, the framework can run in a bounded discovery-oriented mode to:

* learn state signals
* discover stable waits
* test healing candidates
* export a deterministic playbook

## 3.5 Hardening through reuse

Once a stable diagnostic pattern is discovered, the framework should not keep rediscovering it forever.
It should promote that pattern into a governed deterministic playbook for later reuse.

---

# 4. Strategic framework win

The biggest strength of this framework is the separation between:

* **design-time intelligence**
* **state-aware deterministic runtime**
* **post-run forensic interpretation**
* **hardening into playbooks**

That gives you:

* AI flexibility where it helps
* deterministic runtime where it matters
* forensic audit where trust matters
* reusable stability where scale matters

---

# 5. Hybrid model overview

The framework has **four major layers**.

## 5.1 Design-Time AI + Graph-RAG Layer

Used before execution:

* requirement analysis
* mismatch-aware scenario generation
* test code/spec generation
* assertion generation
* reusable component discovery
* locator candidate generation
* semantic state grounding
* context-pack consumption
* graph-grounded requirement expansion

## 5.2 Semantic State Layer

Used before and during execution:

* semantic state maps
* UI states
* transitions
* expected outcomes
* element fingerprints
* mismatch warnings
* deterministic playbook refs

## 5.3 Runtime Execution Layer

Used during execution:

* Playwright sessions
* deterministic actions
* state-aware step execution
* state-aware assertions
* evidence capture
* bounded fallback logic
* dual execution mode handling

## 5.4 Post-Execution Analysis Layer

Used after or around execution:

* evidence summarization
* semantic trace output
* similar failure retrieval
* triage support
* defect draft support
* healing log output
* playbook export
* learning signal support

---

# 6. Framework architecture

```text
+------------------------------------------------------------------+
| Design-Time AI + Graph-RAG Layer                                 |
| - scenario generation                                            |
| - test code/spec generation                                      |
| - assertion generation                                           |
| - reusable asset retrieval                                       |
| - mismatch-aware authoring                                       |
| - graph-grounded requirement/state expansion                     |
| - healing proposal generation                                    |
| - failure interpretation                                         |
+------------------------------+-----------------------------------+
                               |
                               v
+------------------------------------------------------------------+
| Semantic State Layer                                             |
| - semantic state maps                                            |
| - UI states                                                      |
| - transitions                                                    |
| - expected outcomes                                              |
| - mismatch warnings                                              |
| - element fingerprints                                           |
| - deterministic playbooks                                        |
+------------------------------+-----------------------------------+
                               |
                               v
+------------------------------------------------------------------+
| Context / Asset Layer                                            |
| - retrieval context packs                                        |
| - generated Playwright specs                                     |
| - reusable flow modules                                          |
| - page/domain objects                                            |
| - assertion library                                              |
| - fixtures                                                       |
| - metadata + traceability                                        |
+------------------------------+-----------------------------------+
                               |
                               v
+------------------------------------------------------------------+
| Runtime Layer                                                    |
| - Playwright session manager                                     |
| - step executor                                                  |
| - state signal wait engine                                       |
| - semantic assertion engine                                      |
| - forensic healing adapter                                       |
| - evidence collector                                             |
| - runtime state observer                                         |
+------------------------------+-----------------------------------+
                               |
                               v
+------------------------------------------------------------------+
| Platform Services                                                |
| - Semantic State Service                                         |
| - Mismatch Detection Service                                     |
| - Retrieval / Context Pack Service                               |
| - Knowledge Graph                                                |
| - Execution Service                                              |
| - Evidence Service                                               |
| - Healing Service                                                |
| - Playbook Service                                               |
| - State Management                                               |
| - Triage & Confidence                                            |
+------------------------------------------------------------------+
```

---

# 7. Framework styles supported

The framework should support **four test representation styles**.

## 7.1 Code-first assets

Actual Playwright test files.

Examples:

* `valid-login.spec.ts`
* `business-registration.spec.ts`

Use these for:

* stable reusable regression tests
* approved assets
* CI-friendly execution

## 7.2 Structured scenario specs

JSON/YAML execution definitions that the framework translates into runtime steps.

Use these for:

* AI-generated drafts
* intermediate assets
* reviewable scenario definitions

## 7.3 Graph-RAG-grounded generated specs

Generated specs that explicitly reference:

* requirement refs
* context pack refs
* retrieved reusable asset refs
* graph-linked flow/page/API refs
* semantic state refs
* mismatch refs

This should be the default generation style.

## 7.4 Deterministic playbook-backed specs

Approved regression assets that include or reference:

* playbook refs
* approved state signals
* approved wait strategy
* approved healing assumptions if policy allows

This is required by the final architecture.

---

# 8. Recommended project structure

```text
qa-framework/
  playwright.config.ts
  src/
    core/
      session/
      execution/
      state-signals/
      state-observer/
      assertions/
      healing/
      evidence/
      data/
      policy/
      tracing/
      retrieval/
      context/
      compilation/
      playbooks/
      mismatch/
    state/
      maps/
      transitions/
      fingerprints/
      outcomes/
    domain/
      authentication/
      registration/
      profile/
      shared/
    page-objects/
      login.page.ts
      dashboard.page.ts
    flows/
      login.flow.ts
      forgot-password.flow.ts
    assertions/
      auth.assertions.ts
      common.assertions.ts
      state.assertions.ts
      business.assertions.ts
    playbooks/
      login/
      registration/
    fixtures/
      users.fixture.ts
      env.fixture.ts
      state.fixture.ts
      context.fixture.ts
      stateMap.fixture.ts
      playbook.fixture.ts
      evidence.fixture.ts
    generated/
      specs/
      scenarios/
      context-packs/
      playbooks/
      healing/
    adapters/
      evidence.adapter.ts
      graph.adapter.ts
      retrieval.adapter.ts
      state-map.adapter.ts
      healing.adapter.ts
      playbook.adapter.ts
      mcp.adapter.ts
    utils/
      locator.util.ts
      wait.util.ts
      text.util.ts
      visual.util.ts
  tests/
    authored/
    generated/
  reports/
  artifacts/
```

### Important additions

* `core/state-observer/`
* `state/outcomes/`
* `assertions/business.assertions.ts`
* `fixtures/evidence.fixture.ts`

These additions make the runtime and evidence responsibilities clearer.

---

# 9. Layered framework design

## 9.1 Core layer

Contains:

* browser/session management
* step execution
* state-aware waiting
* state-aware assertion runtime
* locator resolution
* evidence capture
* common errors
* logging/tracing
* retrieval/context interfaces
* scenario compilation

## 9.2 Graph-RAG context layer

Contains:

* retrieval adapter
* context pack model
* context pack validator
* reusable asset selector
* requirement grounding resolver
* mismatch ref intake

## 9.3 Semantic state layer

Contains:

* state map model
* state resolver
* transition resolver
* expected outcome mapping
* element fingerprint support
* mismatch interpretation support

## 9.4 Domain layer

Business-specific reusable logic.

## 9.5 Flow layer

Reusable end-to-end business flows.

## 9.6 Page object layer

Page-specific abstractions.

## 9.7 Assertion layer

Business, semantic, and state-aware assertions.

## 9.8 Playbook layer

Stores and consumes deterministic playbook logic for regression execution.

## 9.9 Generated layer

AI-generated assets that can later be reviewed and promoted.

---

# 10. Core runtime components

## 10.1 Session Manager

### Responsibility

Create and manage Playwright browser/session lifecycle.

### Responsibilities include

* launch browser/context/page
* load environment base URL
* apply auth profile or storage state
* isolate session per run
* register artifact capture hooks
* attach execution mode metadata

### Example interface

```ts
interface SessionManager {
  startSession(config: SessionConfig): Promise<TestSession>;
  closeSession(sessionId: string): Promise<void>;
}
```

### SessionConfig example

```ts
type SessionConfig = {
  runId: string;
  browser: 'chromium' | 'firefox' | 'webkit';
  baseUrl: string;
  recordVideo: boolean;
  recordTrace: boolean;
  executionMode: 'diagnostic' | 'regression';
  authProfile?: string;
  storageStatePath?: string;
  playbookRef?: string;
  stateMapRef?: string;
};
```

---

## 10.2 Step Executor

### Responsibility

Execute structured actions consistently.

Supported action types:

* navigate
* click
* fill
* select
* upload
* press
* wait_for
* wait_for_state_signal
* assert
* custom_flow_step

### Example interface

```ts
interface StepExecutor {
  executeStep(session: TestSession, step: TestStep, ctx: ExecutionContext): Promise<StepResult>;
}
```

### Example step model

```ts
type TestStep = {
  id: string;
  action: string;
  target?: ElementTarget;
  expectedStateRef?: string;
  value?: unknown;
  options?: Record<string, unknown>;
};
```

### Architectural rule

At runtime, Step Executor should **not** call retrieval for every action. Retrieval and grounding happen before runtime, except for tightly controlled diagnostic or post-failure paths.

---

## 10.3 Runtime State Observer

This should be explicit.

### Responsibility

Observe whether the browser has reached a meaningful execution state.

It should watch for:

* spinner disappearance
* component mounted and stable
* button enabled
* route stabilized
* validation visible
* expected content visible
* known async transitions settled

### Example interface

```ts
interface RuntimeStateObserver {
  detectCurrentState(session: TestSession, stateMap: StateMap): Promise<ObservedState>;
}
```

This strengthens state-native runtime behavior.

---

## 10.4 State Signal Wait Engine

### Responsibility

Wait for semantic and application-level state signals instead of naive sleeps.

### Examples of supported signals

* loading spinner disappears
* component becomes stable
* button becomes enabled
* route transition completes
* validation error appears
* dashboard ready state reached

### Example interface

```ts
interface StateSignalWaitEngine {
  waitForSignal(session: TestSession, signal: StateSignalSpec): Promise<SignalResult>;
}
```

### Example spec

```ts
type StateSignalSpec = {
  id: string;
  signalType: 'spinner_hidden' | 'component_ready' | 'route_stable' | 'validation_visible';
  targetRef?: string;
  timeoutMs?: number;
};
```

This is one of the most important runtime components in the whole framework.

---

## 10.5 Locator Resolver

### Responsibility

Resolve element targets using a stable strategy.

### Target model

```ts
type ElementTarget = {
  semanticName?: string;
  testId?: string;
  role?: { type: string; name?: string };
  label?: string;
  placeholder?: string;
  text?: string;
  css?: string;
  xpath?: string;
  sourceRef?: string;
  fingerprintRef?: string;
};
```

### Locator priority recommendation

1. `data-testid`
2. ARIA role + accessible name
3. label association
4. placeholder
5. visible text
6. stable CSS
7. XPath last resort

### Architectural rule

Locator resolution may be improved by:

* state-map metadata
* element fingerprint refs
* prior approved healing patterns

But in regression mode, it must remain bounded and deterministic.

---

## 10.6 Evidence Collector

### Responsibility

Capture forensic-grade evidence throughout execution.

Evidence types:

* before/after screenshots
* failure screenshot
* Playwright trace
* video
* console logs
* DOM snapshot
* network/HAR
* API evidence
* visual diff
* semantic trace
* reasoning log

### Example interface

```ts
interface EvidenceCollector {
  captureStep(session: TestSession, step: TestStep, result: StepResult): Promise<void>;
  captureFailure(session: TestSession, error: Error): Promise<EvidenceRefs>;
  finalizeRun(session: TestSession): Promise<EvidenceBundle>;
}
```

### Helper interfaces

```ts
interface SemanticTraceWriter {
  write(trace: SemanticTraceInput): Promise<string>;
}

interface ReasoningLogWriter {
  write(log: ReasoningLogInput): Promise<string>;
}

interface VisualDiffCollector {
  compare(actualRef: string, expectedRef: string): Promise<VisualDiffResult>;
}
```

The evidence path should be strong enough that a reviewer can understand **what failed and why** without replaying the whole run.

---

## 10.7 Semantic Assertion Engine

### Responsibility

Turn business intent and semantic state expectations into executable assertions.

### Examples

* `expectLoginSuccess`
* `expectInvalidPasswordError`
* `expectDashboardStable`
* `expectSpinnerGone`
* `expectAccountLockout`

### Example interface

```ts
interface SemanticAssertionEngine {
  assert(assertion: SemanticAssertion, session: TestSession, ctx: AssertionContext): Promise<AssertionResult>;
}
```

### Example assertion model

```ts
type SemanticAssertion = {
  id: string;
  type: 'business_outcome' | 'validation' | 'navigation' | 'api_state' | 'ui_state';
  name: string;
  expected: Record<string, unknown>;
  sourceRefs?: string[];
  stateRefs?: string[];
};
```

### Important strengthening

The runtime should prefer **state-aware assertions** over shallow browser checks whenever the state map provides enough information.

That means:

* not just “URL changed”
* but “expected semantic state was reached”

---

## 10.8 Forensic Healing Adapter

### Responsibility

Handle bounded healing attempts and produce persistent healing proposals/logs.

### Runtime behavior

* attempt safe fallback resolution when policy allows
* compare against fingerprints and state map
* continue only if confidence/mode/policy allow
* emit reviewable healing suggestion
* always log healing attempt

### Example output

```json
{
  "healingAttempted": true,
  "originalTarget": "button[type='submit']",
  "resolvedTarget": "getByRole('button', { name: 'Sign in' })",
  "confidence": 0.91,
  "requiresReview": true,
  "fingerprintRef": "FP-1001"
}
```

### Architectural rule

Healing must not be treated as just a fallback locator helper anymore.
It is part of a persistent forensic workflow.

### Additional constraint

Regression mode should never silently drift into low-confidence healing. Low-confidence healing should surface as:

* review-needed
* diagnostic retry candidate
* or test failure

---

## 10.9 Playbook Exporter

### Responsibility

Export deterministic playbooks from successful diagnostic discoveries.

### Responsibilities

* capture discovered state signals
* capture reliable wait patterns
* capture safe ordered action sequences
* convert diagnostic findings into deterministic playbook structure

### Example interface

```ts
interface PlaybookExporter {
  exportFromRun(run: DiagnosticRunAnalysis): Promise<DeterministicPlaybook>;
}
```

### Hardening rule

A playbook should only be exported when the run demonstrates:

* repeatable stable state signals
* acceptable evidence quality
* no unresolved blocking mismatch
* no weak healing dependence unless explicitly reviewed

This keeps playbooks trustworthy.

---

# 11. Architecture-specific framework components

## 11.1 Retrieval Adapter

### Responsibility

Call Retrieval/Context Pack service and return bounded context.

```ts
interface RetrievalAdapter {
  buildContextPack(input: ContextPackRequest): Promise<ContextPack>;
}
```

---

## 11.2 Context Pack Consumer

### Responsibility

Consume and validate retrieved context before it affects generated assets.

```ts
interface ContextPackConsumer {
  validate(pack: ContextPack): Promise<ValidatedContextPack>;
}
```

---

## 11.3 State Map Adapter

### Responsibility

Load semantic state maps, transitions, and fingerprints for authoring and execution preparation.

```ts
interface StateMapAdapter {
  getStateMap(caseId: string): Promise<StateMap>;
  getElementFingerprint(ref: string): Promise<ElementFingerprint>;
}
```

---

## 11.4 Mismatch Adapter

### Responsibility

Provide mismatch warnings so authoring and execution can respect unresolved conflicts.

```ts
interface MismatchAdapter {
  listWarnings(caseId: string): Promise<MismatchWarning[]>;
}
```

---

## 11.5 Scenario Grounding Resolver

### Responsibility

Convert retrieved requirements, flows, pages, states, and APIs into authoring-ready scenario inputs.

```ts
interface ScenarioGroundingResolver {
  resolve(pack: ValidatedContextPack, stateMap: StateMap): Promise<GroundedScenarioInput>;
}
```

### Rule

This resolver should use:

* state-map refs
* mismatch warnings
* approved playbook refs if applicable

---

## 11.6 Reusable Asset Selector

### Responsibility

Choose which retrieved reusable assets should be used.

### Selection signals

* same flow
* same page
* same state
* approval status
* playbook compatibility
* exact requirement overlap
* asset stability

---

## 11.7 Scenario Compiler

Now it must compile:

* scenario spec
* retrieved context refs
* reusable flow selections
* assertion modules
* state-map refs
* mismatch refs
* playbook refs
* metadata

into deterministic Playwright code or structured runtime specs.

---

# 12. Dual execution modes

## 12.1 Diagnostic Mode

Purpose:

* initial exploration
* authoring validation
* discovery of stable state signals
* investigation of flaky behavior
* forensic healing trials

Characteristics:

* richer evidence
* bounded think-observe-act loops allowed
* state-signal discovery
* more screenshots/DOM/network capture
* healing analysis allowed
* playbook export possible

## 12.2 Regression Mode

Purpose:

* stable approved suite execution

Characteristics:

* deterministic
* uses approved assets and optionally approved playbooks
* stricter waits and pass/fail rules
* no uncontrolled exploratory behavior
* no broad retrieval-driven runtime branching

## 12.3 Promotion path

Successful diagnostic discoveries can be exported into deterministic playbooks and then used by regression runs after review.

This is the central hardening loop of the framework.

---

# 13. Page objects vs flow objects vs domain actions vs state inputs

Use all four, but for different purposes.

## 13.1 Page Objects

Represent page-specific UI operations.

## 13.2 Flow Objects

Represent business flows spanning pages.

## 13.3 Domain Actions

Represent reusable domain capabilities across flows.

## 13.4 State Inputs

Represent semantic execution expectations used to choose:

* which flow to use
* which page objects are relevant
* which assertions apply
* which waits are required
* which playbook signals are relevant

---

# 14. Test authoring patterns

The framework should support:

## 14.1 Hand-authored stable tests

Written or refined by humans.

## 14.2 AI-generated draft tests

Generated from requirements and case artifacts.

## 14.3 Hybrid tests

AI generates structure, humans refine and approve.

## 14.4 Graph-RAG-grounded hybrid tests

AI generates or updates tests using:

* retrieved requirements
* graph-linked flows/pages/APIs
* semantic state refs
* approved reusable modules
* similar historical tests
* mismatch warnings

## 14.5 Playbook-backed regression tests

Approved tests that reference deterministic playbooks discovered in diagnostic mode.

---

# 15. Example authoring flow with Graph-RAG and state map

## Step 1

A request asks for a test for `invalid password`.

## Step 2

Retrieval Service builds a context pack containing:

* requirement `REQ-502`
* flow `FLOW-invalid-password`
* page `Login Page`
* API `POST /auth/login`
* state `STATE-invalid-password-error-visible`
* approved `LoginFlow`
* approved `AuthAssertions`

## Step 3

State Map Adapter loads:

* relevant transition
* expected outcome
* related fingerprint refs

## Step 4

Mismatch Adapter checks for unresolved conflicts.

## Step 5

Scenario Grounding Resolver chooses:

* `LoginFlow`
* `AuthAssertions.expectInvalidPasswordError`
* required state signal waits

## Step 6

Scenario Compiler emits:

* structured scenario spec
* Playwright spec
* state refs
* source refs
* metadata with context pack lineage

---

# 16. Example test style

## 16.1 Good framework-level style

```ts
test('valid login succeeds', async ({ app, authAssertions, testData }) => {
  await app.flows.login.performValidLogin(
    testData.user.email,
    testData.user.password
  );

  await authAssertions.expectLoginSuccess();
});
```

## 16.2 Example using flow + semantic assertion

```ts
test('invalid password shows validation error', async ({ app, authAssertions, testData }) => {
  await app.flows.login.performLoginAttempt(
    testData.user.email,
    testData.user.invalidPassword
  );

  await authAssertions.expectInvalidPasswordError();
});
```

## 16.3 Metadata example

```ts
export const testMeta = {
  caseId: 'CASE-101',
  scenarioId: 'SCN-2002',
  requirementIds: ['REQ-502'],
  flowId: 'FLOW-invalid-password',
  stateRefs: ['STATE-invalid-password-error-visible'],
  generatedBy: 'test-authoring-agent',
  contextPackId: 'CTXPACK-1001',
  stateMapId: 'STATEMAP-1001',
  sourceRefs: ['CHUNK-9002', 'TA-2001', 'ASSET-ASSERT-1001'],
  mismatchRefs: [],
  playbookRef: null,
  assetVersion: 1
};
```

---

# 17. Fixtures strategy

Use Playwright fixtures heavily.

## Recommended fixtures

* environment fixture
* session fixture
* test data fixture
* state fixture
* application facade fixture
* evidence fixture
* context fixture
* stateMap fixture
* playbook fixture

## `contextFixture`

Provides:

* validated context pack
* linked requirement refs
* linked reusable asset refs

## `stateMapFixture`

Provides:

* state map
* state refs
* transition refs
* fingerprint refs

## `playbookFixture`

Provides:

* approved playbook signals
* deterministic wait definitions
* mode-specific execution hints

These are essential for keeping raw test bodies clean.

---

# 18. Framework facade pattern

Expose a top-level app/testing facade to keep generated tests clean.

Example:

```ts
class AppFacade {
  constructor(
    public pages: PageRegistry,
    public flows: FlowRegistry,
    public assertions: AssertionRegistry
  ) {}
}
```

Generated tests should use:

* `app.pages...`
* `app.flows...`
* `app.assertions...`

### Architectural rule

Graph-RAG, state-map, and playbook logic should stay out of raw test bodies as much as possible. Use them before compilation and in fixtures/runtime helpers.

---

# 19. Assertion design

## 19.1 Three assertion levels

### Level 1 — Technical assertions

* element visible
* URL contains
* status code is 200

### Level 2 — Semantic UI assertions

* login error shown
* dashboard loaded
* upload completed

### Level 3 — Business and state outcome assertions

* user authenticated successfully
* registration completed
* account lockout enforced
* dashboard stable
* spinner disappeared before next action

The framework should prefer Levels 2 and 3 whenever possible.

## 19.2 Assertion sourcing

Assertions should be sourced from:

* retrieved requirements
* rule docs
* expected result docs
* state-map expected outcomes
* approved assertion modules
* approved playbook signals where relevant

---

# 20. Metadata and traceability in tests

Every generated test asset should carry metadata.

## Required metadata

* case ID
* scenario ID
* linked requirement IDs
* linked flow ID
* linked state refs
* generation source
* prompt/model version
* review state
* context pack ID
* state map ID
* source refs used
* reusable asset refs selected
* mismatch refs
* playbook ref if any

Example:

```ts
export const testMeta = {
  caseId: 'CASE-101',
  scenarioId: 'SCN-2001',
  requirementIds: ['REQ-501'],
  flowId: 'FLOW-1001',
  stateRefs: ['STATE-login-ready', 'STATE-dashboard-stable'],
  generatedBy: 'test-authoring-agent',
  contextPackId: 'CTXPACK-1001',
  stateMapId: 'STATEMAP-1001',
  sourceRefs: ['CHUNK-9001', 'REQ-501', 'FLOW-1001'],
  reusableAssetRefs: ['TA-2001', 'TA-ASSERT-001'],
  mismatchRefs: [],
  playbookRef: 'PLAYBOOK-1001',
  assetVersion: 1
};
```

---

# 21. Runtime state integration

The Playwright framework must integrate with State Management Service and Semantic State Service.

## Before a test

* verify preconditions
* provision test data
* load state map and playbook if required
* initialize session state

## During a test

* use run-scoped data
* isolate storage/session
* wait for state signals
* collect evidence and semantic trace
* evaluate semantic assertions against observed state

## After a test

* collect artifacts
* summarize evidence
* cleanup temporary state
* report run outcome
* write healing log if needed
* export playbook if diagnostic run is promotable

---

# 22. Error handling strategy

Framework errors should classify:

* locator failure
* timeout
* assertion failure
* navigation failure
* auth failure
* setup failure
* environment/network failure
* context grounding failure
* retrieval dependency failure
* state-signal failure
* mismatch-blocked execution
* playbook incompatibility
* healing-confidence-insufficient

### Error model

```ts
type FrameworkErrorType =
  | 'locator_not_found'
  | 'action_timeout'
  | 'assertion_failed'
  | 'navigation_failed'
  | 'auth_failed'
  | 'setup_failed'
  | 'environment_failed'
  | 'context_grounding_failed'
  | 'retrieval_failed'
  | 'state_signal_failed'
  | 'mismatch_blocked'
  | 'playbook_incompatible'
  | 'healing_confidence_low';
```

---

# 23. Forensic evidence capture strategy

## 23.1 Minimum evidence for every run

* first meaningful screenshot
* failure screenshot if failed
* Playwright trace
* step logs
* console logs
* final DOM snapshot

## 23.2 For important scenarios

Also capture:

* video
* HAR/network
* additional checkpoints
* visual diff
* semantic trace
* reasoning log

## 23.3 Naming scheme

```text
RUN-3001_step-04_after-click-submit.png
RUN-3001_trace.zip
RUN-3001_console.log
RUN-3001_semantic-trace.json
RUN-3001_visual-diff.png
```

## 23.4 Retrieval-friendly extensions

Generate:

* evidence summaries
* step outcome summaries
* run outcome summaries
* healing summaries
* playbook discovery summaries

---

# 24. Generated test promotion workflow

AI-generated assets should move through stages:

* generated draft
* runtime validated
* human reviewed
* approved regression asset
* active reusable asset

## Additional playbook promotion path

Diagnostic discoveries may move through:

* discovered
* exported
* reviewed
* approved playbook
* linked to regression asset

## Promotion rule recommendation

A generated Playwright spec should not become a permanent regression asset until:

* it runs successfully in clean state
* assertions make sense
* metadata is linked
* source refs are traceable
* state-map lineage is preserved
* mismatch warnings are resolved or accepted
* review is completed for critical flows

---

# 25. Healing strategy inside the framework

## 25.1 Runtime healing rules

Allowed:

* locator fallback resolution
* semantic role/name fallback
* fingerprint-assisted resolution if policy allows

Not allowed automatically:

* permanent update of approved test assets
* broad flow rewriting
* hidden pass after major UI/state shift
* silent reuse of low-confidence healing in regression mode

## 25.2 Healing result model

```ts
type HealingResult = {
  attempted: boolean;
  successful: boolean;
  originalLocator: string;
  resolvedLocator?: string;
  fingerprintRef?: string;
  confidence?: number;
  reviewRequired: boolean;
  sourceRefs?: string[];
};
```

## 25.3 Healing rule

Healing suggestions may use:

* prior accepted healing patterns
* linked UIElement semantics
* element fingerprints
* historical instability signals
* state-map context

But only in:

* draft mode
* diagnostic mode
* post-run analysis

---

# 26. AI generation boundaries

## AI may generate

* test scenarios
* draft Playwright specs
* assertion proposals
* locator candidates
* flow module proposals
* page object skeletons
* grounded scenario compilations from retrieved context
* state-signal proposals
* deterministic playbook proposals

## AI should not directly control

* unrestricted runtime browser actions in regression mode
* arbitrary external state mutation
* silent updates to approved assets
* uncontrolled live retrieval-driven runtime branching
* silent healing persistence

This remains a hard boundary.

---

# 27. Runtime modes

## 27.1 Draft mode

Used for first-time generated tests.

Characteristics:

* more logging
* more artifact capture
* optional extra checkpoints
* healing attempts allowed with review flags
* limited authoring-time RAG allowed

## 27.2 Diagnostic mode

Used for:

* building tests
* state discovery
* failure investigation
* playbook export

Characteristics:

* deeper logs
* more screenshots/DOM/network capture
* state-signal discovery
* healing history lookup allowed
* historical triage retrieval allowed

## 27.3 Regression mode

Used for approved stable suites.

Characteristics:

* deterministic
* stricter policies
* uses approved assets and playbooks
* tighter pass/fail rules
* no uncontrolled retrieval-driven runtime changes

---

# 28. Example internal interfaces

## Application facade

```ts
interface AppFacade {
  pages: {
    login: LoginPage;
    dashboard: DashboardPage;
  };
  flows: {
    login: LoginFlow;
  };
  assertions: {
    auth: AuthAssertions;
    state: StateAssertions;
  };
}
```

## Scenario executor

```ts
interface ScenarioExecutor {
  executeScenario(
    scenario: ScenarioDefinition,
    session: TestSession,
    ctx: ExecutionContext
  ): Promise<ScenarioResult>;
}
```

## Generated test compiler

```ts
interface GeneratedTestCompiler {
  compileScenarioToSpec(
    scenario: ScenarioDefinition,
    context: ValidatedContextPack,
    stateMap: StateMap
  ): Promise<CompiledTestAsset>;
}
```

## Playbook-aware compiler

```ts
interface PlaybookAwareCompiler {
  compileFromContext(
    input: GroundedScenarioInput,
    playbook?: DeterministicPlaybook
  ): Promise<CompiledTestAsset>;
}
```

---

# 29. Example scenario-to-code conversion

AI may produce a structured scenario like:

```json
{
  "name": "valid login succeeds",
  "flowRef": "FLOW-1001",
  "stateRefs": ["STATE-login-ready", "STATE-dashboard-stable"],
  "steps": [
    {"action": "navigate", "target": "/login"},
    {"action": "wait_for_state_signal", "targetRef": "STATE-login-ready"},
    {"action": "fill", "field": "email", "valueRef": "data.user.email"},
    {"action": "fill", "field": "password", "valueRef": "data.user.password"},
    {"action": "click", "elementRef": "submit_button"}
  ],
  "assertions": [
    {"type": "business_outcome", "name": "login_success"},
    {"type": "ui_state", "name": "dashboard_stable"}
  ]
}
```

Using a context pack and state map that include:

* `REQ-501`
* `FLOW-1001`
* `STATE-login-ready`
* `STATE-dashboard-stable`
* `LoginFlow`
* `AuthAssertions.expectLoginSuccess`

the compiler can render it into deterministic Playwright code.

---

# 30. Reporting hooks

The framework should emit structured events during execution.

Examples:

* `step_started`
* `step_passed`
* `step_failed`
* `assertion_passed`
* `assertion_failed`
* `healing_attempted`
* `evidence_captured`

### Additional important events

* `state_signal_wait_started`
* `state_signal_wait_satisfied`
* `state_observer_state_detected`
* `context_pack_loaded`
* `context_pack_validation_failed`
* `reusable_asset_selected`
* `grounded_scenario_compiled`
* `mismatch_warning_attached`
* `playbook_exported`

These should feed:

* Execution Service
* Evidence Service
* Healing Service
* Triage Service
* Audit logs

---

# 31. Framework configuration

## Global config

* base URL per environment
* artifact capture defaults
* timeout defaults
* browser selection
* retry policy
* healing policy
* approval thresholds
* execution mode
* retrieval mode defaults
* context pack limits
* approved-assets-only flags by mode
* approved-playbook-only flags by mode

## Scenario/test config

* linked requirement IDs
* linked state refs
* severity
* priority
* data profile
* cleanup profile
* allowed healing level
* source refs
* context pack ID
* reusable asset refs
* mismatch refs
* playbook ref

---

# 32. Recommended initial technical direction

For your current stage, the best practical implementation is:

## 32.1 Use TypeScript + Playwright

Because:

* Playwright is strongest in the TS/JS ecosystem
* code generation and runtime integration are simpler
* easier for AI-generated test assets
* strong fixture support

## 32.2 Use structured scenario + compiled spec model

Not only raw direct code generation.

Reason:

* easier to validate
* easier to attach metadata
* easier to recompile/update later
* cleaner bridge between agent output and execution

## 32.3 Use page objects + flows + semantic assertions + state-aware waits

This is the best maintainability pattern.

## 32.4 Keep Graph-RAG primarily pre-runtime

Retrieval and grounding should mostly happen **before execution**. Stable regression runs should not behave like live agentic browsing sessions.

## 32.5 Treat diagnostic mode as a producer of deterministic knowledge

Diagnostic execution should discover, validate, and export deterministic playbooks for future stable runs.

---

# 33. Minimal framework components for V1

Build these first:

1. Session Manager
2. Step Executor
3. Runtime State Observer
4. State Signal Wait Engine
5. Locator Resolver
6. Evidence Collector
7. Semantic Assertion Engine
8. Retrieval Adapter
9. Context Pack Consumer
10. State Map Adapter
11. Scenario Grounding Resolver
12. Scenario Compiler
13. App Facade
14. Login Page Object
15. Login Flow
16. Auth Assertions
17. State Assertions
18. Test Metadata Support
19. Healing Adapter
20. MCP/Execution adapters

This is the minimum serious framework set that fits the final architecture.

---

# 34. Final framework summary

The Playwright hybrid framework should be:

* **code-first at runtime**
* **AI-assisted at design time**
* **Graph-RAG-grounded before generation and triage**
* **semantic-state-aware**
* **diagnostic for discovery**
* **deterministic in regression**
* **forensic in evidence**
* **modular in page/flow/assertion structure**
* **traceable to requirements, states, flows, pages, and APIs**
* **controlled in healing**
* **capable of exporting deterministic playbooks**
* **promotable from draft to approved regression assets**

That gives you a framework much stronger than:

* raw Playwright scripts
* raw AI browser control
* ad hoc generated tests

