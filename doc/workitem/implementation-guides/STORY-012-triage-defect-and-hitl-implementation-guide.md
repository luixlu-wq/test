# STORY-012-triage-defect-and-hitl Detailed Implementation Guide

## Ticket Reference

- Source: `api/doc/workitem/STORY-012-triage-defect-and-hitl.md`
- Type: `story`
- Sprint candidate: `Sprint 5`

## 1. Environment Setup Steps

1. From repository root run: `cd api`
1. Create and activate venv: `python -m venv .venv` then `.venv\\Scripts\\activate`
1. Install dependencies: `pip install -e .[dev,runner]`
1. Install browser runtime when needed: `python -m playwright install chromium`
1. Set baseline env profile variables from implementation plan section 2.4/2.5/2.6.
1. Enable execution backend (`simulated` in CI, `playwright` in integration).
1. Provision evidence blob storage and retention-job schedule for operational tests.

## 2. Resources Required / Dependencies

**Required references and assets**
- Implementation plan: `api/doc/impl-plan/detailed-implementation-plan.md`
- Architecture: `api/doc/arc-design/architectural-design.md`
- Playwright hybrid framework design
- Agent prompts design
- Service design SLO/operations sections

**Upstream dependencies**
- `STORY-011-execution-state-and-evidence.md`

## 3. Dependent Components

**Upstream components**
- `STORY-011-execution-state-and-evidence.md`

**Downstream components impacted by this ticket**
- `STORY-013-healing-and-playbook-promotion.md`

## 4. Detailed Process Flow (Step-by-Step)

1. Confirm scope boundaries in STORY-012-triage-defect-and-hitl and freeze acceptance criteria from the source ticket.
2. Verify upstream dependencies are complete: STORY-011-execution-state-and-evidence.md.
3. Prepare environment profile (local-dev then integration) and seed required synthetic fixtures.
4. Implement contract/model changes first (schemas, constants, DTOs, DB fields) before service logic.
5. Implement the core STORY-012 Triage Defect And HITL service flow with idempotency and correlation-id propagation.
6. Integrate policy and audit hooks so blocked paths and successful paths are both traceable.
7. Add failure handling with deterministic failpoints for timeout/retry/crash scenarios as applicable.
8. Implement positive-path tests mapped to existing TC-S* cases in the ticket.
9. Implement negative and edge-path tests mapped to TCN-* and TCE-* catalog entries.
10. Run unit + contract + integration suites, then capture evidence and update ticket checklist status.

## 5. Process Flow Diagram

```mermaid
flowchart TD
    A[STORY-012-triage-defect-and-hitl: Scope Freeze] --> B[Environment Ready]
    B --> C[Core Implementation]
    C --> D[Policy and Audit Hooks]
    D --> E[Positive Test Pass]
    E --> F[Negative and Edge Test Pass]
    F --> G[CI Gate Pass]
    G --> H[Done]
```

## 6. Sequence Diagram

```mermaid
sequenceDiagram
    participant P1 as Developer
    participant P2 as Execution Orchestrator
    participant P3 as Runner/Triage Service
    participant P4 as Evidence/Approval Store
    participant P5 as CI Pipeline
    P1->>P2: Implement STORY-012-triage-defect-and-hitl changes
    P2->>P3: Execute core flow
    P3->>P4: Persist artifacts/state with correlation IDs
    P4-->>P3: Return result or structured error
    P3-->>P2: Emit audited outcome (success/deny/retryable failure)
    P2->>P5: Run TC-S / TCN / TCE suites
    P5-->>P1: Report gate status and coverage
```

## 7. Test Plan and Coverage Target (>= 85%)

- Scenario catalog size: **20**
- Minimum scenarios that must pass: **17** (>= 85%)
- Ticket baseline test IDs: TC-S10-001, TC-S10-002, TC-S10-003, TC-S10-004, TCN-S10-001, TCN-S10-002, TCE-S10-001

| Scenario Category | Target Count | Coverage Focus |
|---|---:|---|
| Happy path | 8 | Primary functional flow and data persistence |
| Negative path | 6 | Validation failures, policy-denied actions, contract errors |
| Edge conditions | 4 | Concurrency, large payload/context, idempotent replay |
| Recovery/failpoint | 2 | Timeout/retry/crash recovery with deterministic failpoints |

**Assertion standards**
- Structured error payloads include `errorCode`, `message`, `retryable`, `correlationId`.
- Duplicate/replay/out-of-order events do not corrupt persisted state.
- Deterministic mode: same input and snapshot yields structurally equivalent output.
- Secrets are masked in logs and test artifacts.

## 8. Implementation Checklist

- [ ] Contracts/schemas and enums updated first (if applicable)
- [ ] Service logic implemented with idempotency and policy checks
- [ ] Audit/correlation logging verified
- [ ] Unit + contract + integration + negative + edge tests implemented
- [ ] Coverage threshold satisfied (>= 85% scenario catalog)
- [ ] CI gates green and ticket acceptance criteria met
