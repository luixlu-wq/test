# STORY-001 Contract And Enum Lock

## Type

story

## Description

Create and lock canonical contract schemas, enum definitions, and version metadata used by MCP, agents, workflow records, and events.

## Scope

- Shared schema package in source.
- Canonical `execution_mode` and status enums.
- Schema fixtures for valid/invalid payload tests.

## Dependencies

- `EPIC-001-spec-and-backbone.md`

## Acceptance Criteria

1. Canonical enums used by all new modules.
2. Contract fixtures validate strict required fields.
3. Schema version metadata is persisted where required.

## Test Cases

- `TC-S0-001`
- `TC-S0-002`
- `TC-S0-003`

## Owner

TBD

## Status

todo
