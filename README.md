# AI QA Code Tester

Production-oriented scaffold for the AI-powered QA platform we designed:

- **api**: portal-facing orchestration API
- **intelligence**: artifact processing, association, and scenario generation
- **worker**: execution and result analysis endpoints
- **shared contracts**: Pydantic models for commands, events, and domain entities

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .[dev]
uvicorn ai_qa_tester.api.main:app --reload --port 8000
uvicorn ai_qa_tester.intelligence.main:app --reload --port 8001
uvicorn ai_qa_tester.worker.main:app --reload --port 8002
```

## Suggested next implementation order

1. Replace in-memory repositories with PostgreSQL + Azure AI Search/Qdrant.
2. Add Azure DevOps connector implementation.
3. Add Figma fetch + artifact OCR pipeline.
4. Add Service Bus command/event publishing.
5. Add Playwright/Pytest execution workers.


## Wireframe upload flow

Upload a wireframe or screenshot directly into the system:

```bash
curl -X POST http://localhost:8000/api/v1/projects/proj_01/artifacts/upload-wireframe   -F "file=@business-search-wireframe.png"   -F "linked_entity_type=work_item"   -F "linked_entity_id=wk_123"
```

The API will:
- register the upload as an artifact
- process wireframe text and UI hints
- store extracted labels and inferred journey
- make the artifact available for association and scenario generation


## New in this build

- Automatic Azure DevOps work item attachment ingestion
- Attachment-based wireframe processing and journey detection
- Manual attachment sync endpoint: `POST /api/v1/projects/{project_id}/work-items/{work_item_id}/attachments/sync`


## Azure Service Bus support

This build can publish commands and events to Azure Service Bus while keeping a local fallback for development.

Environment variables:

```bash
export AI_QA_SERVICE_BUS_ENABLED=true
export AI_QA_SERVICE_BUS_CONNECTION_STRING="Endpoint=sb://..."
export AI_QA_SERVICE_BUS_COMMAND_QUEUE="aiqa-commands"
export AI_QA_SERVICE_BUS_EVENT_TOPIC="aiqa-events"
export AI_QA_EVENT_BUS_ENABLED=true
```

If Azure Service Bus is not configured or the optional package is missing, the scaffold falls back to an in-memory command/event store so local tests still work.

New endpoint for local worker-style processing:

```http
POST /api/v1/projects/{project_id}/jobs/process-next-command
```

This consumes the next locally queued command and executes the matching job.
