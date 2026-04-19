# AI QA Platform High Level System Diagram

This document summarizes the architecture in `api/doc/arc-design/architectural-design.md` as visual diagrams plus a component walkthrough.

## 1. Full System Picture

```mermaid
flowchart TB
    U[User, CLI, Local Hook, Watch Mode, API Caller] --> G[Request Gateway and Trigger Layer]

    subgraph CP[Control Plane]
        O[QA Orchestration Service]
        A[Agent Runtime]
        P[Policy and Approval Service]
        L[Audit and Observability Service]
    end

    G --> O
    O --> A
    O <--> P
    O --> L
    A --> L

    subgraph KC[Knowledge and Context Layer]
        D[Distributed Understanding Service]
        S[Semantic State Service]
        M[Mismatch Detection Service]
        K[Knowledge Graph Service]
        R[Retrieval Service Hybrid Graph RAG]
        C[Context Pack Builder]
    end

    O --> D
    D --> S
    S --> M
    D --> K
    D --> R
    K --> R
    M --> R
    R --> C
    C --> A

    subgraph AE[Assets and Execution Layer]
        T[Test Asset Service]
        X[Execution Service]
        W[Browser Worker plus Browser Automation MCP]
        Y[API Worker plus API Runner MCP]
        Z[State Management Service]
        E[Evidence Service]
    end

    O --> T
    T --> X
    Z --> X
    X --> W
    X --> Y
    W --> E
    Y --> E
    X --> L

    subgraph IG[Intelligence and Governance Layer]
        F[Triage and Confidence Service]
        H[Healing Service]
        B[Defect Draft Service]
        Q[Playbook Service]
        N[Learning Service]
        RVR[Human Reviewer]
    end

    E --> F
    E --> H
    F --> B
    H --> Q
    F --> N
    H --> N
    B --> N

    O --> F
    O --> H
    O --> B
    O --> N

    RVR <--> P
    RVR <--> B
    RVR --> N
```

## 2. End to End Runtime Sequence

```mermaid
sequenceDiagram
    autonumber
    participant U as User or Hook
    participant G as Request Gateway
    participant O as Orchestrator
    participant D as Distributed Understanding
    participant S as Semantic State
    participant M as Mismatch Detection
    participant R as Retrieval and Context Pack
    participant A as Agent Runtime
    participant T as Test Asset Service
    participant X as Execution Service
    participant E as Evidence Service
    participant F as Triage and Confidence
    participant H as Healing
    participant B as Defect Draft
    participant P as Policy and Approval
    participant N as Learning

    U->>G: Submit request or trigger event
    G->>O: Normalized request

    O->>D: Ingest and fuse artifacts
    D->>S: Build semantic state map
    S->>M: Evaluate requirement mismatches

    O->>R: Build grounded context pack
    R->>A: Bounded context by mode and policy
    A->>T: Generate strategy and test assets

    O->>X: Run deterministic execution plan
    X->>E: Persist evidence and run artifacts

    O->>F: Classify failure and compute confidence
    O->>H: Run healing analysis when needed
    O->>B: Build defect draft packet

    O->>P: Request review gate decisions if required
    P-->>O: Allow, block, or require human review

    O->>N: Persist learning signals and outcomes
    O-->>U: Return run summary and traceability refs
```

## 3. Diagnostic vs Regression Modes

```mermaid
flowchart LR
    RQ[Run Request] --> MD{Execution Mode}

    MD --> DIAG[Diagnostic Mode]
    MD --> REG[Regression Mode]

    DIAG --> D1[Allow richer evidence capture]
    DIAG --> D2[Allow bounded exploration]
    DIAG --> D3[Allow healing analysis]
    DIAG --> D4[Produce playbook candidates]

    REG --> R1[Use approved assets only]
    REG --> R2[Use approved playbooks only]
    REG --> R3[No uncontrolled exploration]
    REG --> R4[Deterministic pass fail behavior]
```

## 4. How Each Component Works

| Component | What it does | Main inputs | Main outputs |
|---|---|---|---|
| Request Gateway and Trigger Layer | Accepts inbound requests from UI, CLI, hooks, API. Validates and normalizes requests. | request payload, trigger events | normalized request, correlation IDs, workflow kickoff |
| QA Orchestration Service | Controls workflow stages, retries, policy checks, and ordering. | normalized request, stage results | stage transitions, service calls, final run summary |
| Distributed Understanding Service | Reads case folders and browser readable sources. Fuses artifacts into structured understanding. | case files, parsed docs, browser captures | artifact records, chunkable summaries, provenance refs |
| Semantic State Service | Builds state map of pages, states, transitions, expected outcomes. | fused understanding, UI/API context | semantic state map, fingerprints, transition refs |
| Mismatch Detection Service | Detects contradictions across requirements, state map, and expected behavior before execution. | requirements, state map, expected outcomes | mismatch warnings, severity, blocking signals |
| Knowledge Graph Service | Stores explicit traceability relationships across requirements, tests, runs, and defects. | entities and links from understanding and runtime | relationship graph, impact neighborhoods |
| Retrieval Service Hybrid Graph RAG | Retrieves relevant chunks and graph neighbors using filters and mode aware policy. | retrieval query, case scope, mode | ranked candidate refs, retrieval logs |
| Context Pack Builder | Builds bounded prompt context with facts, refs, mismatches, and reusable assets. | retrieval results, policy constraints | context pack for agents |
| Agent Runtime | Runs role specific agents for mapping, strategy, authoring, triage, healing, learning. | context pack, task contract | structured agent outputs with confidence and refs |
| Test Asset Service | Produces strategies, scenarios, scripts, fixtures, and versioned assets. | agent outputs, templates, reusable assets | executable test assets, metadata, version links |
| State Management Service | Ensures deterministic preconditions, setup, and cleanup for runs. | run plan, environment policy | setup actions, cleanup actions, state readiness |
| Execution Service | Schedules and coordinates browser and API workers under policy and mode constraints. | test assets, playbooks, state setup | run steps, execution status, worker events |
| Browser Worker plus Browser Automation MCP | Executes web steps and assertions, collects browser evidence. | browser plan, selectors, state signals | screenshots, traces, logs, assertion results |
| API Worker plus API Runner MCP | Executes API flows and assertions with controlled auth/session setup. | API test plan, fixtures | request/response evidence, assertion results |
| Evidence Service | Stores evidence, builds bundles and summaries, and returns evidence refs. | raw artifacts from workers | evidence refs, bundles, semantic traces |
| Triage and Confidence Service | Classifies failures and computes confidence with evidence grounding. | run outcomes, evidence bundles, history | triage result, confidence, recommended action |
| Healing Service | Performs forensic healing analysis and proposes safe updates. | failed steps, fingerprints, historical healing | healing suggestions, healing logs |
| Playbook Service | Promotes validated diagnostic discoveries into deterministic playbooks. | approved healing outcomes, stable patterns | approved playbooks for regression mode |
| Defect Draft Service | Builds defect quality packets with repro, expected/actual, and evidence refs. | triage result, evidence, requirement links | defect drafts, review ready packets |
| Policy and Approval Service | Applies action tier policy and human gate logic for risky actions. | proposed actions, confidence, mode | allow, deny, or review decisions |
| Audit and Observability Service | Captures full trace of decisions, tool calls, and stage timings. | all workflow and service events | audit logs, telemetry, debugging views |
| Learning Service | Converts outcomes and reviewer feedback into reusable signals. | triage outcomes, healing outcomes, review decisions | learning signals, retrieval boosts, quality improvements |
| Human Reviewer | Reviews uncertain outputs and approves blocked or risky decisions. | review tasks, defect drafts, healing proposals | approval decisions, corrections, feedback |

## 5. Operational Reading Guide

Use this sequence to reason about failures quickly:

1. Check `Orchestrator` stage timeline.
2. Check `Mismatch Detection` output before execution.
3. Check `Execution Service` and worker run-step logs.
4. Check `Evidence Service` bundles for missing or weak evidence.
5. Check `Triage and Confidence` rationale.
6. Check `Policy and Approval` decision path.
7. Check `Learning` signal writeback for future runs.

