# Workitem Implementation Order Diagram

## High-Level Order (Story Chain)

```mermaid
flowchart LR
    S001[STORY-001] --> S002[STORY-002]
    S001 --> S004[STORY-004]
    S002 --> S003[STORY-003]
    S004 --> S005[STORY-005]
    S005 --> S006[STORY-006] --> S007[STORY-007]
    S007 --> S008[STORY-008] --> S009[STORY-009] --> S010[STORY-010]
    S010 --> S011[STORY-011] --> S012[STORY-012] --> S013[STORY-013] --> S014[STORY-014]
```

## Sprint-Oriented Execution Order

```mermaid
gantt
    title Implementation Order by Sprint
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d
    section Sprint 1
    STORY-001 + TASK-001/002/015 :a1, 2026-04-21, 5d
    STORY-002 + TASK-003/004     :a2, after a1, 4d
    STORY-003 + TASK-005/006     :a3, after a2, 3d
    STORY-004 + TASK-007/008     :a4, after a1, 4d
    section Sprint 2
    STORY-005 + TASK-009..012    :b1, after a4, 5d
    STORY-006 + TASK-013         :b2, after b1, 4d
    STORY-007 + TASK-014         :b3, after b2, 3d
    section Sprint 3+
    STORY-008                     :c1, after b3, 4d
    STORY-009                     :c2, after c1, 4d
    STORY-010                     :c3, after c2, 4d
    STORY-011                     :c4, after c3, 4d
    STORY-012                     :c5, after c4, 4d
    STORY-013                     :c6, after c5, 4d
    STORY-014                     :c7, after c6, 3d
```

## Ticket Dependency Graph (Stories + Tasks)

```mermaid
flowchart TD
    EPIC_001_spec_and_backbone --> STORY_001_contract_and_enum_lock
    STORY_001_contract_and_enum_lock --> STORY_002_request_trigger_orchestration
    STORY_002_request_trigger_orchestration --> STORY_003_policy_and_audit_foundation
    STORY_001_contract_and_enum_lock --> STORY_004_persistence_core_schema
    EPIC_001_spec_and_backbone --> STORY_005_mcp_core_set
    STORY_005_mcp_core_set --> STORY_006_distributed_understanding_pipeline
    STORY_004_persistence_core_schema --> STORY_006_distributed_understanding_pipeline
    STORY_006_distributed_understanding_pipeline --> STORY_007_semantic_state_and_mismatch
    STORY_007_semantic_state_and_mismatch --> STORY_008_graph_rag_foundation
    STORY_008_graph_rag_foundation --> STORY_009_agent_runtime_and_prompt_governance
    STORY_009_agent_runtime_and_prompt_governance --> STORY_010_test_asset_compiler_and_playwright_hybrid
    STORY_010_test_asset_compiler_and_playwright_hybrid --> STORY_011_execution_state_and_evidence
    STORY_011_execution_state_and_evidence --> STORY_012_triage_defect_and_hitl
    STORY_012_triage_defect_and_hitl --> STORY_013_healing_and_playbook_promotion
    STORY_013_healing_and_playbook_promotion --> STORY_014_ops_hardening_and_shift_left
    STORY_001_contract_and_enum_lock --> TASK_001_schema_package_and_fixtures
    TASK_001_schema_package_and_fixtures --> TASK_002_canonical_enum_constants
    STORY_002_request_trigger_orchestration --> TASK_003_request_dedup_key
    TASK_003_request_dedup_key --> TASK_004_workflow_state_machine
    STORY_003_policy_and_audit_foundation --> TASK_005_policy_decision_evaluator
    STORY_003_policy_and_audit_foundation --> TASK_006_audit_correlation_logging
    STORY_004_persistence_core_schema --> TASK_007_core_migration_pack
    TASK_007_core_migration_pack --> TASK_008_repository_roundtrip_tests
    STORY_005_mcp_core_set --> TASK_009_filesystem_mcp_and_policy_guard
    STORY_005_mcp_core_set --> TASK_010_document_parser_mcp
    STORY_005_mcp_core_set --> TASK_011_browser_reader_mcp
    STORY_005_mcp_core_set --> TASK_012_trigger_mcp
    STORY_006_distributed_understanding_pipeline --> TASK_013_understanding_fusion_engine
    STORY_007_semantic_state_and_mismatch --> TASK_014_state_map_and_mismatch_engine
    STORY_001_contract_and_enum_lock --> TASK_015_tdr_registry_and_decision_records
```

## Usage

- Follow story chain top-to-bottom; enforce dependency completion before starting downstream items.
- Within each story, execute task guides in dependency order from `api/doc/workitem/implementation-guides/`.
