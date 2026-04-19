# EPIC-001 Spec And Backbone

## Type

epic

## Description

Establish the non-negotiable platform foundation: contract lock, canonical enums, request/trigger/orchestration backbone, policy controls, audit trail, and persistence baseline.

## Scope

- Step 0, Step 1, Step 2 from implementation plan.
- Contract schema package and validation tests.
- Stateful orchestration with idempotent stage transitions.
- Policy decision and approval scaffolding.
- Audit event capture with correlation IDs.
- Initial SQL schema migrations for core entities.

## Dependencies

- None.

## Acceptance Criteria

1. Step 0 Technology Decision Records are completed and merged under `api/doc/tdr/` before Step 1 implementation is closed.
2. Contract schemas are versioned and validated by automated tests.
3. Request deduplication and workflow idempotency work end-to-end.
4. Policy engine returns explicit decision + rationale.
5. Audit logs are emitted for every workflow stage transition.
6. Core persistence migrations run cleanly in local and integration profile.
7. Negative-path errors follow contract fields: `errorCode`, `message`, `retryable`, `correlationId`.

## Test Cases

- `TC-S0-001`, `TC-S0-002`, `TC-S0-003`
- `TCN-S0-001`, `TCN-S0-002`, `TCE-S0-001`
- `TC-S1-001`, `TC-S1-002`, `TC-S1-003`, `TC-S1-004`
- `TCN-S1-001`, `TCN-S1-002`, `TCE-S1-001`
- `TC-S2-001`, `TC-S2-002`, `TC-S2-003`, `TC-S2-004`
- `TCN-S2-001`, `TCN-S2-002`, `TCE-S2-001`

## Owner

TBD

## Status

todo
