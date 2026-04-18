Below is the **rewritten Part 4 — Playwright Hybrid Framework**, updated to fit the **final architectural design**.

I kept the strongest parts of your previous framework design:

* Playwright as the deterministic runtime
* AI-assisted authoring instead of uncontrolled runtime AI browsing
* RAG-grounded generation and reuse
* semantic assertions
* evidence-rich execution
* controlled healing

I updated it to match the final architecture in these areas:

* **distributed understanding**
* **semantic state map as a first-class execution input**
* **requirement mismatch awareness**
* **dual execution modes**: diagnostic vs regression
* **forensic self-healing with persistent healing log**
* **deterministic playbook export**
* **forensic-grade evidence schema**
* **local shift-left compatibility**

Your previous framework was already strong on RAG-grounded authoring and stable execution. The main gap was that it did not yet fully reflect the final architecture’s **state-map-driven execution**, **diagnostic-to-playbook promotion**, **forensic healing**, and **semantic trace evidence**. 

---

# Part 4 — Playwright Hybrid Framework

## AI QA Platform

### Final Architecture-Aligned Version

This section defines the **Playwright + AI + Graph-RAG hybrid framework** for your QA platform.

The goal is still **not** to let AI directly drive the browser in an uncontrolled way for every run.

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

# 1. Framework Goals

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

The earlier version already covered most of these, but the final architecture requires much stronger emphasis on **state maps**, **dual execution modes**, **healing logs**, and **playbook export**. 

---

# 2. Core Design Principle

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
* assertions
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

# 3. Execution Philosophy

The final architecture requires a stronger execution philosophy than before.

## 3.1 Visible-truth execution

The framework should validate what is visible and observable:

* rendered UI state
* state transitions
* request/response outcomes
* evidence artifacts
* user-observable business outcomes

## 3.2 State-aware execution

The framework should execute against semantic state expectations, not only DOM selectors.

## 3.3 Deterministic-by-default execution

Stable regression mode must not depend on free-form AI thinking at runtime.

## 3.4 Diagnostic discovery mode

When needed, the framework can run in a bounded discovery-oriented mode to:

* learn state signals
* discover stable waits
* test healing candidates
* export a deterministic playbook

---

# 4. Hybrid Model Overview

The framework now has **four major layers**.

## 4.1 Design-Time AI + Graph-RAG Layer

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

## 4.2 Semantic State Layer

Used before and during execution:

* semantic state maps
* UI states
* transitions
* expected outcomes
* element fingerprints
* mismatch warnings
* deterministic playbook refs

## 4.3 Runtime Execution Layer

Used during execution:

* Playwright sessions
* deterministic actions
* state-aware step execution
* evidence capture
* runtime checks
* bounded fallback logic
* dual execution mode handling

## 4.4 Post-Execution Analysis Layer

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

# 5. Framework Architecture

```text id="dgn4h3"
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
| - state-aware wait engine                                        |
| - semantic assertion engine                                      |
| - forensic healing adapter                                       |
| - evidence collector                                             |
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

This is the major update required by the final architecture. 

---

# 6. Framework Styles Supported

The framework should support **four test representation styles**.

## 6.1 Code-first assets

Actual Playwright test files.

Examples:

* `valid-login.spec.ts`
* `business-registration.spec.ts`

Use these for:

* stable reusable regression tests
* approved assets
* CI-friendly execution

## 6.2 Structured scenario specs

JSON/YAML execution definitions that the framework translates into runtime steps.

Use these for:

* AI-generated drafts
* intermediate assets
* reviewable scenario definitions

## 6.3 Graph-RAG-grounded generated specs

Generated specs that explicitly reference:

* requirement refs
* context pack refs
* retrieved reusable asset refs
* graph-linked flow/page/API refs
* semantic state refs
* mismatch refs

This should now be the **default generation style**.

## 6.4 Deterministic playbook-backed specs

Approved regression assets that include or reference:

* playbook refs
* approved state signals
* approved wait strategy
* approved healing assumptions if policy allows

This is new and is required by the final architecture.

---

# 7. Recommended Project Structure

```text id="n3wz5j"
qa-framework/
  playwright.config.ts
  src/
    core/
      session/
      execution/
      state-signals/
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

### New additions required by the final architecture

* `core/state-signals/`
* `core/playbooks/`
* `core/mismatch/`
* `state/maps/`
* `state/transitions/`
* `state/fingerprints/`
* `fixtures/stateMap.fixture.ts`
* `fixtures/playbook.fixture.ts`
* `adapters/state-map.adapter.ts`
* `adapters/healing.adapter.ts`
* `adapters/playbook.adapter.ts`
* `generated/healing/`
* `generated/playbooks/`

---

# 8. Layered Framework Design

## 8.1 Core layer

The framework kernel.

Contains:

* browser/session management
* step execution
* state-aware waiting
* assertion runtime
* locator resolution
* evidence capture
* common errors
* logging/tracing
* retrieval/context interfaces
* scenario compilation

## 8.2 Graph-RAG context layer

Contains:

* retrieval adapter
* context pack model
* context pack validator
* reusable asset selector
* requirement grounding resolver
* mismatch ref intake

## 8.3 Semantic state layer

Contains:

* state map model
* state resolver
* transition resolver
* expected outcome mapping
* element fingerprint support
* mismatch interpretation support

## 8.4 Domain layer

Business-specific reusable logic.

## 8.5 Flow layer

Reusable end-to-end business flows.

## 8.6 Page object layer

Page-specific abstractions.

## 8.7 Assertion layer

Business, semantic, and state-aware assertions.

## 8.8 Playbook layer

Stores and consumes deterministic playbook logic for regression execution.

## 8.9 Generated layer

AI-generated assets that can later be reviewed and promoted.

---

# 9. Core Runtime Components

---

## 9.1 Session Manager

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

```ts id="dewhqk"
interface SessionManager {
  startSession(config: SessionConfig): Promise<TestSession>;
  closeSession(sessionId: string): Promise<void>;
}
```

### SessionConfig example

```ts id="hgbv4p"
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

This is similar to the previous version, but now execution mode, playbook, and state map are explicit. 

---

## 9.2 Step Executor

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

```ts id="f4l46y"
interface StepExecutor {
  executeStep(session: TestSession, step: TestStep, ctx: ExecutionContext): Promise<StepResult>;
}
```

### Example step model

```ts id="4sj6t3"
type TestStep = {
  id: string;
  action: string;
  target?: ElementTarget;
  expectedStateRef?: string;
  value?: unknown;
  options?: Record<string, unknown>;
};
```

### Architectural correction

At runtime, Step Executor should **not** call retrieval for every action.
Retrieval and grounding happen before runtime, except for tightly controlled diagnostic or post-failure analysis paths.

---

## 9.3 State Signal Wait Engine

This is a new explicit framework component required by the final architecture.

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

```ts id="7yajkz"
interface StateSignalWaitEngine {
  waitForSignal(session: TestSession, signal: StateSignalSpec): Promise<SignalResult>;
}
```

### Example spec

```ts id="k8p1v8"
type StateSignalSpec = {
  id: string;
  signalType: 'spinner_hidden' | 'component_ready' | 'route_stable' | 'validation_visible';
  targetRef?: string;
  timeoutMs?: number;
};
```

This is one of the most important additions to make the framework fit the final architecture.

---

## 9.4 Locator Resolver

### Responsibility

Resolve element targets using stable strategy.

### Target model

```ts id="7h1pce"
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

### Final-architecture correction

Locator resolution can be improved by:

* state-map metadata
* element fingerprint refs
* prior approved healing patterns

But in regression mode, it must remain bounded and deterministic.

---

## 9.5 Evidence Collector

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

```ts id="xv6sxd"
interface EvidenceCollector {
  captureStep(session: TestSession, step: TestStep, result: StepResult): Promise<void>;
  captureFailure(session: TestSession, error: Error): Promise<EvidenceRefs>;
  finalizeRun(session: TestSession): Promise<EvidenceBundle>;
}
```

### New helper interfaces

```ts id="6czyja"
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

This aligns the framework with the final evidence schema.

---

## 9.6 Semantic Assertion Engine

### Responsibility

Turn business intent and semantic state expectations into executable assertions.

### Examples

* `expectLoginSuccess`
* `expectInvalidPasswordError`
* `expectDashboardStable`
* `expectSpinnerGone`
* `expectAccountLockout`

### Example interface

```ts id="q7bpo0"
interface SemanticAssertionEngine {
  assert(assertion: SemanticAssertion, session: TestSession, ctx: AssertionContext): Promise<AssertionResult>;
}
```

### Example assertion model

```ts id="2cste7"
type SemanticAssertion = {
  id: string;
  type: 'business_outcome' | 'validation' | 'navigation' | 'api_state' | 'ui_state';
  name: string;
  expected: Record<string, unknown>;
  sourceRefs?: string[];
  stateRefs?: string[];
};
```

### Final-architecture correction

Assertions should preferably be grounded from:

* requirement refs
* flow refs
* semantic state refs
* expected outcome refs
* approved assertion modules

---

## 9.7 Forensic Healing Adapter

This replaces the earlier lighter healing concept with an architecture-aligned one.

### Responsibility

Handle bounded healing attempts and produce persistent healing proposals/logs.

### Runtime behavior

* attempt safe fallback resolution when policy allows
* compare against fingerprints and state map
* continue only if confidence/mode/policy allow
* emit reviewable healing suggestion
* always log healing attempt

### Example output

```json id="t7mdli"
{
  "healingAttempted": true,
  "originalTarget": "button[type='submit']",
  "resolvedTarget": "getByRole('button', { name: 'Sign in' })",
  "confidence": 0.91,
  "requiresReview": true,
  "fingerprintRef": "FP-1001"
}
```

### Correction

Healing must not be treated as just a fallback locator helper anymore.
It is now part of a persistent forensic workflow.

---

## 9.8 Playbook Exporter

This is new and required by the final architecture.

### Responsibility

Export deterministic playbooks from successful diagnostic discoveries.

### Responsibilities

* capture discovered state signals
* capture reliable wait patterns
* capture safe ordered action sequences
* convert diagnostic findings into deterministic playbook structure

### Example interface

```ts id="gljlwm"
interface PlaybookExporter {
  exportFromRun(run: DiagnosticRunAnalysis): Promise<DeterministicPlaybook>;
}
```

---

# 10. New Architecture-Specific Framework Components

---

## 10.1 Retrieval Adapter

### Responsibility

Call Retrieval/Context Pack service and return bounded context.

### Example interface

```ts id="kqf40g"
interface RetrievalAdapter {
  buildContextPack(input: ContextPackRequest): Promise<ContextPack>;
}
```

---

## 10.2 Context Pack Consumer

### Responsibility

Consume and validate retrieved context before it affects generated assets.

### Example interface

```ts id="9gcrk8"
interface ContextPackConsumer {
  validate(pack: ContextPack): Promise<ValidatedContextPack>;
}
```

---

## 10.3 State Map Adapter

This is new.

### Responsibility

Load semantic state maps, transitions, and fingerprints for authoring and execution preparation.

### Example interface

```ts id="pr7u3n"
interface StateMapAdapter {
  getStateMap(caseId: string): Promise<StateMap>;
  getElementFingerprint(ref: string): Promise<ElementFingerprint>;
}
```

---

## 10.4 Mismatch Adapter

This is new.

### Responsibility

Provide mismatch warnings so authoring and execution can respect unresolved conflicts.

### Example interface

```ts id="v6lbqq"
interface MismatchAdapter {
  listWarnings(caseId: string): Promise<MismatchWarning[]>;
}
```

---

## 10.5 Scenario Grounding Resolver

### Responsibility

Convert retrieved requirements, flows, pages, states, and APIs into authoring-ready scenario inputs.

### Example interface

```ts id="r0t4l5"
interface ScenarioGroundingResolver {
  resolve(pack: ValidatedContextPack, stateMap: StateMap): Promise<GroundedScenarioInput>;
}
```

### Correction

This resolver should now use:

* state-map refs
* mismatch warnings
* approved playbook refs if applicable

---

## 10.6 Reusable Asset Selector

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

## 10.7 Scenario Compiler

The previous design already had a Generated Test Compiler.
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

# 11. Dual Execution Modes

This is one of the biggest framework changes required by the final architecture.

## 11.1 Diagnostic Mode

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

## 11.2 Regression Mode

Purpose:

* stable approved suite execution

Characteristics:

* deterministic
* uses approved assets and optionally approved playbooks
* stricter waits and pass/fail rules
* no uncontrolled exploratory behavior
* no broad retrieval-driven runtime branching

## 11.3 Promotion path

Successful diagnostic discoveries can be exported into deterministic playbooks and then used by regression runs after review.

This is a core architecture fit requirement.

---

# 12. Page Objects vs Flow Objects vs Domain Actions vs State Inputs

Use all four, but for different purposes.

## 12.1 Page Objects

Represent page-specific UI operations.

## 12.2 Flow Objects

Represent business flows spanning pages.

## 12.3 Domain Actions

Represent reusable domain capabilities across flows.

## 12.4 State Inputs

Represent the semantic execution expectations used to choose:

* which flow to use
* which page objects are relevant
* which assertions apply
* which waits are required
* which playbook signals are relevant

This is the final-architecture upgrade.

---

# 13. Test Authoring Patterns

The framework should support:

## 13.1 Hand-authored stable tests

Written or refined by humans.

## 13.2 AI-generated draft tests

Generated from requirements and case artifacts.

## 13.3 Hybrid tests

AI generates structure, humans refine and approve.

## 13.4 Graph-RAG-grounded hybrid tests

AI generates or updates tests using:

* retrieved requirements
* graph-linked flows/pages/APIs
* semantic state refs
* approved reusable modules
* similar historical tests
* mismatch warnings

## 13.5 Playbook-backed regression tests

Approved tests that reference deterministic playbooks discovered in diagnostic mode.

This is new and required.

---

# 14. Example Authoring Flow with Graph-RAG and State Map

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

That is how the framework should now use the final architecture.

---

# 15. Example Test Style

## 15.1 Good framework-level test style

```ts id="3v2ffn"
test('valid login succeeds', async ({ app, authAssertions, testData }) => {
  await app.flows.login.performValidLogin(
    testData.user.email,
    testData.user.password
  );

  await authAssertions.expectLoginSuccess();
});
```

## 15.2 Example using flow + semantic assertion

```ts id="m3wfc0"
test('invalid password shows validation error', async ({ app, authAssertions, testData }) => {
  await app.flows.login.performLoginAttempt(
    testData.user.email,
    testData.user.invalidPassword
  );

  await authAssertions.expectInvalidPasswordError();
});
```

## 15.3 Final-architecture generation metadata example

```ts id="e5rkrd"
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

# 16. Fixtures Strategy

Use Playwright fixtures heavily.

## 16.1 Recommended fixtures

* environment fixture
* session fixture
* test data fixture
* state fixture
* application facade fixture
* evidence fixture
* context fixture
* **stateMap fixture**
* **playbook fixture**

## 16.2 `contextFixture`

Provides:

* validated context pack
* linked requirement refs
* linked reusable asset refs

## 16.3 `stateMapFixture`

Provides:

* state map
* state refs
* transition refs
* fingerprint refs

## 16.4 `playbookFixture`

Provides:

* approved playbook signals
* deterministic wait definitions
* mode-specific execution hints

These are required to fit the final architecture.

---

# 17. Framework Facade Pattern

Expose a top-level app/testing facade to keep generated tests clean.

Example:

```ts id="9wfq39"
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

### Important architectural rule

Graph-RAG, state-map, and playbook logic should stay out of raw test bodies as much as possible.
Use them before compilation and in fixtures/runtime helpers, not scattered in every test.

---

# 18. Assertion Design

## 18.1 Three assertion levels

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

Your framework should prefer levels 2 and 3 whenever possible.

## 18.2 Assertion sourcing

Assertions should be sourced from:

* retrieved requirements
* rule docs
* expected result docs
* state-map expected outcomes
* approved assertion modules
* approved playbook signals where relevant

This is the final-architecture-aligned version of semantic assertions.

---

# 19. Metadata and Traceability in Tests

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

```ts id="lwomww"
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

# 20. Runtime State Integration

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

## After a test

* collect artifacts
* summarize evidence
* cleanup temporary state
* report run outcome
* write healing log if needed
* export playbook if diagnostic run is promotable

---

# 21. Error Handling Strategy

## Distinguish error types

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
* **state-signal failure**
* **mismatch-blocked execution**
* **playbook incompatibility**
* **healing-confidence-insufficient**

### Error model

```ts id="vp6a34"
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

This is the final-architecture-aligned error model.

---

# 22. Forensic Evidence Capture Strategy

## 22.1 Minimum evidence for every run

* first meaningful screenshot
* failure screenshot if failed
* Playwright trace
* step logs
* console logs
* final DOM snapshot

## 22.2 For important scenarios

Also capture:

* video
* HAR/network
* additional checkpoints
* visual diff
* semantic trace
* reasoning log

## 22.3 Naming scheme

```text id="g9v4gj"
RUN-3001_step-04_after-click-submit.png
RUN-3001_trace.zip
RUN-3001_console.log
RUN-3001_semantic-trace.json
RUN-3001_visual-diff.png
```

## 22.4 Retrieval-friendly extensions

Generate:

* evidence summaries
* step outcome summaries
* run outcome summaries
* healing summaries
* playbook discovery summaries

This matches the final evidence schema.

---

# 23. Generated Test Promotion Workflow

AI-generated assets should move through stages.

## Stages

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

# 24. Healing Strategy Inside the Framework

## 24.1 Runtime healing rules

Allowed:

* locator fallback resolution
* semantic role/name fallback
* fingerprint-assisted resolution if policy allows

Not allowed automatically:

* permanent update of approved test assets
* broad flow rewriting
* hidden pass after major UI/state shift
* silent reuse of low-confidence healing in regression mode

## 24.2 Healing result model

```ts id="ab1mjlwm"
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

## 24.3 Final-architecture healing rules

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

This is stricter and more architecture-aligned than the previous version. 

---

# 25. AI Generation Boundaries

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

This is fully consistent with the final architecture.

---

# 26. Runtime Modes

## 26.1 Draft mode

Used for first-time generated tests.

Characteristics:

* more logging
* more artifact capture
* optional extra checkpoints
* healing attempts allowed with review flags
* limited authoring-time RAG allowed

## 26.2 Diagnostic mode

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

## 26.3 Regression mode

Used for approved stable suites.

Characteristics:

* deterministic
* stricter policies
* uses approved assets and playbooks
* tighter pass/fail rules
* no uncontrolled retrieval-driven runtime changes

This now exactly matches the final architecture’s dual-mode design.

---

# 27. Example Internal Interfaces

## Application facade

```ts id="ewuof5"
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

```ts id="h7dh5r"
interface ScenarioExecutor {
  executeScenario(
    scenario: ScenarioDefinition,
    session: TestSession,
    ctx: ExecutionContext
  ): Promise<ScenarioResult>;
}
```

## Generated test compiler

```ts id="5kwy6r"
interface GeneratedTestCompiler {
  compileScenarioToSpec(
    scenario: ScenarioDefinition,
    context: ValidatedContextPack,
    stateMap: StateMap
  ): Promise<CompiledTestAsset>;
}
```

## Playbook-aware compiler

```ts id="j9t6rf"
interface PlaybookAwareCompiler {
  compileFromContext(
    input: GroundedScenarioInput,
    playbook?: DeterministicPlaybook
  ): Promise<CompiledTestAsset>;
}
```

---

# 28. Example Scenario-to-Code Conversion

AI may produce a structured scenario like:

```json id="o5n6al"
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

That is the ideal final-architecture-aligned hybrid pattern.

---

# 29. Reporting Hooks

The framework should emit structured events during execution.

Examples:

* `step_started`
* `step_passed`
* `step_failed`
* `assertion_passed`
* `assertion_failed`
* `healing_attempted`
* `evidence_captured`

### New final-architecture events

* `state_signal_wait_started`
* `state_signal_wait_satisfied`
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

# 30. Framework Configuration

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

# 31. Recommended Initial Technical Direction

For your current stage, the best practical implementation is:

## 31.1 Use TypeScript + Playwright

Because:

* Playwright is strongest in the TS/JS ecosystem
* code generation and runtime integration are simpler
* easier for AI-generated test assets
* strong fixture support

## 31.2 Use structured scenario + compiled spec model

Not only raw direct code generation.

Reason:

* easier to validate
* easier to attach metadata
* easier to recompile/update later
* cleaner bridge between agent output and execution

## 31.3 Use page objects + flows + semantic assertions + state-aware waits

This is now the best maintainability pattern.

## 31.4 Keep Graph-RAG primarily pre-runtime

Retrieval and grounding should mostly happen **before execution**.
Stable regression runs should not behave like live agentic browsing sessions.

## 31.5 Treat diagnostic mode as a producer of deterministic knowledge

Diagnostic execution should discover, validate, and export deterministic playbooks for future stable runs.

This is the biggest new technical direction implied by the final architecture.

---

# 32. Minimal Framework Components for V1

Build these first:

1. Session Manager
2. Step Executor
3. State Signal Wait Engine
4. Locator Resolver
5. Evidence Collector
6. Semantic Assertion Engine
7. Retrieval Adapter
8. Context Pack Consumer
9. State Map Adapter
10. Scenario Grounding Resolver
11. Scenario Compiler
12. App Facade
13. Login Page Object
14. Login Flow
15. Auth Assertions
16. State Assertions
17. Test Metadata Support
18. Healing Adapter
19. MCP/Execution adapters

This is the minimum framework set that fits the final architecture.

---

# 33. Final Framework Summary

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

It becomes a **state-aware, Graph-RAG-grounded, deterministic execution framework** that matches the final architecture. 

