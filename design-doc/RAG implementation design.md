Below is the **rewritten Part 7 — RAG Implementation Design**, updated to fit the **final architectural design**.

I kept the strongest parts of your previous RAG design:

* RAG as a first-class subsystem
* hybrid retrieval instead of vector-only retrieval
* graph expansion
* reranking
* context-pack assembly
* agent-by-agent retrieval flows
* retrieval logs and auditability

I updated it to match the final architecture in these areas:

* **distributed understanding**
* **semantic state map as a first-class retrieval source**
* **requirement mismatch awareness**
* **dual execution modes**: diagnostic vs regression
* **forensic healing retrieval**
* **deterministic playbook retrieval**
* **forensic-grade evidence schema**
* **local trigger / shift-left awareness**

Your previous Part 7 was already strong on Graph-RAG and service ownership. The main gap was that it did not yet fully model the final architecture’s **state layer**, **mismatch layer**, **healing layer**, **playbook layer**, and **mode-aware retrieval policies**. 

---

# Part 7 — RAG Implementation Design

## AI QA Platform

### Final Architecture-Aligned Version

This section makes **Graph-RAG a first-class implementation subsystem** in your AI QA platform.

It defines:

* the RAG architecture
* ingestion pipeline
* chunking rules
* indexing strategy
* hybrid retrieval logic
* graph expansion logic
* reranking
* context pack assembly
* semantic-state-aware retrieval
* mismatch-aware retrieval
* healing-aware retrieval
* playbook-aware retrieval
* agent-by-agent retrieval flow
* APIs/contracts for the Retrieval Service

This design matches your final architecture:

* local case folders
* browser-readable URLs
* no direct Jira/Figma/Azure DevOps API integrations yet
* web + API testing
* knowledge graph + retrieval
* distributed understanding
* semantic state maps
* deterministic + diagnostic execution modes
* forensic healing
* deterministic playbooks
* evidence-first triage

---

# 1. Purpose of RAG in This Platform

RAG is not just “search documents and paste them into a prompt.”

In this QA platform, RAG must do **six** jobs.

## 1.1 Ground agent reasoning

Agents must use source-backed context instead of guessing.

## 1.2 Connect scattered QA knowledge

The relevant truth is spread across:

* stories
* wireframes
* screenshots
* rules
* API specs
* defects
* semantic state maps
* mismatch warnings
* approved tests
* prior runs
* triage results
* review decisions
* healing logs
* playbooks

## 1.3 Reuse prior QA intelligence

The system should retrieve:

* existing good tests
* past similar failures
* known risky flows
* approved assertions
* accepted healing patterns
* approved deterministic playbooks

## 1.4 Ground semantic state reasoning

The system must retrieve not only text, but also:

* state-map summaries
* state refs
* transition refs
* expected outcomes
* fingerprint summaries

## 1.5 Surface contradictions early

The system must retrieve:

* mismatch warnings
* unresolved conflicts
* conflicting expectations

so that strategy and authoring do not operate on silently inconsistent requirements.

## 1.6 Support mode-aware execution intelligence

The system must distinguish:

* **diagnostic retrieval** for discovery and analysis
* **regression retrieval** for approved, stable execution support

So the correct design is:

## **Hybrid Graph-RAG + Semantic State Retrieval**

* retrieval index for search
* graph for relationships
* reranking for task relevance
* context packs for agent prompts
* semantic state summaries as retrievable context
* mismatch/healing/playbook summaries as retrievable context

---

# 2. RAG Subsystem Overview

```text id="0lxykk"
Source Artifacts
  -> Parse / Normalize
  -> Artifact Fusion
  -> Semantic State Generation
  -> Mismatch Detection
  -> Chunk
  -> Metadata Enrich
  -> Index
  -> Link into Graph
  -> Retrieve Candidates
  -> Expand with Graph
  -> Rerank
  -> Build Context Pack
  -> Feed Agent Prompt / Execution Preparation
```

This is the biggest conceptual upgrade from the prior Part 7: RAG now explicitly sits downstream of **distributed understanding**, **state-map generation**, and **mismatch detection**. 

---

# 3. RAG Architecture Components

The RAG subsystem should have these components:

1. **Artifact Normalizer**
2. **Artifact Fusion Support Layer**
3. **Semantic State Summarizer**
4. **Mismatch Summary Generator**
5. **Chunking Engine**
6. **Metadata Enrichment Engine**
7. **Indexing Pipeline**
8. **Hybrid Retrieval Engine**
9. **Graph Expansion Engine**
10. **Reranker**
11. **Context Pack Builder**
12. **Retrieval Policy Layer**
13. **Retrieval Audit Log**

The original list was already good; the final architecture requires explicit additions for:

* semantic state summarization
* mismatch summary generation

---

# 4. Component Responsibilities

## 4.1 Artifact Normalizer

Transforms raw source material into structured representations.

Input:

* file content
* browser-captured pages
* parsed doc outputs

Output:

* normalized artifact records
* extracted fields
* document structure
* source provenance

---

## 4.2 Artifact Fusion Support Layer

Supports the distributed understanding pipeline by producing retrieval-ready fused summaries.

Input:

* normalized artifacts
* classified artifact types
* OCR/vision or browser-visible extraction outputs

Output:

* fused artifact summaries
* cross-artifact relationship hints
* likely flow/page/state/API hints
* fusion conflicts and gaps

This is new and aligns RAG with the final architecture’s distributed understanding model.

---

## 4.3 Semantic State Summarizer

Creates retrievable summaries from semantic state maps.

Input:

* state map
* states
* transitions
* expected outcomes
* fingerprints

Output:

* state-map summaries
* state summaries
* transition summaries
* expected-outcome summaries
* fingerprint summaries where useful

These summaries are critical because agents should not consume only raw JSON state maps.

---

## 4.4 Mismatch Summary Generator

Creates retrieval-ready mismatch summaries.

Input:

* mismatch warnings
* source refs
* severity
* affected requirements/states/pages

Output:

* mismatch summary records
* retrieval views for mismatches
* conflict metadata for context packs

This is new and required by the final architecture.

---

## 4.5 Chunking Engine

Breaks artifacts and generated summaries into retrievable units.

Input:

* normalized artifact
* artifact type
* parse result
* state-map or mismatch summary if relevant

Output:

* chunk records
* chunk metadata
* chunk ordering

---

## 4.6 Metadata Enrichment Engine

Adds structured labels and links to chunks.

Examples:

* caseId
* artifactType
* storyId
* defectId
* pageRef
* flowRef
* stateRef
* transitionRef
* apiRef
* priority
* source quality
* mismatchRef
* playbookRef
* executionMode relevance

---

## 4.7 Indexing Pipeline

Writes chunks and retrieval views to search/vector infrastructure.

Responsibilities:

* generate embeddings
* store searchable text
* store metadata filters
* track index status
* keep index rows linked to graph and relational records

---

## 4.8 Hybrid Retrieval Engine

Retrieves candidate content using:

* keyword search
* vector similarity
* metadata filters
* exact reference matching

---

## 4.9 Graph Expansion Engine

Expands retrieved candidates using graph relationships.

Example:
retrieved a requirement chunk → expand to:

* linked flow
* linked page
* linked state
* linked transition
* linked API
* linked test asset
* linked known defect
* linked mismatch warning

---

## 4.10 Reranker

Reorders candidates using:

* task-specific relevance
* same-case bias
* same-flow bias
* same-state bias
* approved asset preference
* approved playbook preference
* confidence and recency
* mismatch relevance
* healing/playbook relevance

---

## 4.11 Context Pack Builder

Builds task-shaped prompt context.

It should produce:

* facts
* relevant chunks
* linked entities
* semantic state refs
* mismatch warnings
* reusable assets
* playbook candidates where applicable
* conflicts/gaps
* source refs

---

## 4.12 Retrieval Policy Layer

Controls:

* which source types an agent may query
* whether historical runs are included
* whether drafts are allowed
* whether playbooks are allowed
* whether healing history is allowed
* max context size
* which environments are considered
* whether diagnostic vs regression constraints apply

---

## 4.13 Retrieval Audit Log

Stores:

* queries
* filters
* candidates
* final selected refs
* context pack contents
* timing
* execution mode
* retrieval degradation

This remains critical and becomes even more important in the final architecture.

---

# 5. RAG Data Categories

The index should distinguish content categories.

## 5.1 Source artifact content

* stories
* rules
* expected result docs
* API specs
* wireframe descriptions
* browser page captures
* defect docs

## 5.2 Fused understanding content

* case understanding summaries
* artifact fusion summaries
* identified conflicts/gaps

## 5.3 Semantic state content

* state-map summaries
* UI state summaries
* transition summaries
* expected outcome summaries
* fingerprint summaries

## 5.4 Mismatch content

* mismatch warnings
* mismatch explanation summaries
* conflict summaries

## 5.5 Generated QA assets

* strategy summaries
* scenario summaries
* approved test summaries
* assertion summaries
* reusable flow summaries

## 5.6 Runtime history

* run summaries
* failure summaries
* triage summaries
* defect draft summaries
* review outcomes

## 5.7 Healing and playbook content

* healing summaries
* accepted/rejected healing patterns
* playbook summaries
* discovered state-signal summaries

## 5.8 Learning content

* accepted healing patterns
* repeated unstable selectors/states
* recurring failure patterns
* accepted/rejected playbook patterns

This is the most direct expansion of the earlier RAG data categories.

---

# 6. Current-Stage RAG Sources

For your current stage, RAG should use these inputs:

## 6.1 Folder-based sources

* `/stories`
* `/wireframes`
* `/screenshots`
* `/defects`
* `/api`
* `/rules`
* `/expected`
* `/refs/urls.yaml`

## 6.2 Browser-readable sources

* story pages
* defect pages
* wiki pages
* design preview pages
* internal documentation pages

## 6.3 Internal platform history

* case understanding summaries
* semantic state maps and summaries
* mismatch warnings
* approved scenarios
* approved test assets
* prior runs
* triage results
* defect drafts
* review decisions
* healing events/logs
* playbook summaries
* learning signals

---

# 7. Chunking Design

Chunking must be **artifact-type-aware** and now also **state-type-aware**.

---

## 7.1 Story documents

Chunk by:

* title
* feature summary
* acceptance criteria block
* flow section
* validation section
* notes/constraints

---

## 7.2 Rules documents

Chunk by:

* rule heading
* rule block
* exception block
* edge cases

---

## 7.3 API specs

Chunk by:

* endpoint
* request schema
* response schema
* error responses
* auth notes

---

## 7.4 Defect documents

Chunk by:

* summary
* repro steps
* expected behavior
* actual behavior
* root cause notes
* workaround notes

---

## 7.5 Browser-readable captured pages

Chunk by:

* page title and summary
* extracted structured fields
* main body section
* identified ticket/story/bug info

---

## 7.6 Wireframes and screenshots

Do not index raw binaries.
Index:

* image summary
* OCR or vision-derived text if available
* extracted UI structure summary
* visible controls
* labeled expectations
* likely page/state summary

---

## 7.7 Semantic state maps

This is new.

Chunk by:

* page-level state summary
* state summary
* transition summary
* expected-outcome summary
* fingerprint summary where useful

Example chunks:

* `Login State Map Summary`
* `State — Login Form Ready`
* `Transition — Submit Valid Credentials`
* `Expected Outcome — Dashboard Stable`

---

## 7.8 Mismatch warnings

This is new.

Chunk by:

* mismatch summary
* source conflict explanation
* affected requirement/page/state/API explanation

---

## 7.9 Test assets

Do not only chunk raw code.
Prefer summary chunks:

* scenario summary
* flow summary
* assertions summary
* reusable module description
* playbook linkage summary if present

---

## 7.10 Run and triage history

Chunk by:

* run summary
* failure reason summary
* classification summary
* evidence interpretation summary
* decision summary

---

## 7.11 Healing and playbook history

This is new.

### Healing

Chunk by:

* healing summary
* element instability summary
* approved/rejected healing decision summary

### Playbooks

Chunk by:

* playbook summary
* discovered state signals
* promotion decision summary

---

# 8. Chunk Schema

Every chunk should carry rich metadata.

## 8.1 Base chunk fields

```json id="x1hpcr"
{
  "chunkId": "CHUNK-9001",
  "sourceType": "artifact_chunk",
  "sourceId": "ART-201",
  "caseId": "CASE-101",
  "artifactType": "story",
  "chunkType": "acceptance_criteria",
  "title": "Acceptance Criteria — Valid Login",
  "text": "User can sign in with valid credentials",
  "orderIndex": 3,
  "metadata": {}
}
```

## 8.2 Recommended metadata fields

```json id="mxuxlf"
{
  "storyId": "US-101",
  "defectId": null,
  "flowRefs": ["FLOW-1001"],
  "pageRefs": ["PAGE-301"],
  "stateRefs": ["STATE-LOGIN-READY"],
  "transitionRefs": ["TRANS-1001"],
  "apiRefs": ["API-401"],
  "requirementRefs": ["REQ-501"],
  "mismatchRefs": [],
  "playbookRefs": [],
  "priority": "high",
  "status": "active",
  "sourceQuality": "high",
  "approvalStatus": "approved",
  "environmentScope": ["UAT"],
  "executionModeScope": ["diagnostic", "regression"]
}
```

The additions here are important:

* `stateRefs`
* `transitionRefs`
* `mismatchRefs`
* `playbookRefs`
* `executionModeScope`

---

# 9. Indexing Strategy

Use **hybrid indexing**.

## 9.1 Search fields

Store:

* title
* text
* normalized keywords
* IDs and exact references
* metadata filters

## 9.2 Vector fields

Store embedding vectors for:

* chunk text
* optionally chunk title + text combined

## 9.3 Filter fields

Must support filters on:

* caseId
* artifactType
* chunkType
* flowRefs
* pageRefs
* stateRefs
* transitionRefs
* apiRefs
* mismatchRefs
* approvalStatus
* environmentScope
* executionModeScope
* sourceType

This extends the earlier indexing strategy to match the final architecture’s state-aware and mode-aware retrieval needs.

---

# 10. Retrieval Modes

The Retrieval Service should support several modes.

## 10.1 Case understanding mode

Used by:

* Case Understanding Agent

Focus:

* stories
* rules
* expected docs
* browser-captured pages
* fusion summaries
* conflicts/gaps

## 10.2 Requirement mapping mode

Used by:

* Requirement Mapping Agent

Focus:

* requirement-bearing chunks
* state-map summaries
* page/API summaries
* known defects
* mismatch warnings

## 10.3 Strategy mode

Used by:

* Risk & Strategy Agent

Focus:

* requirements
* states
* transitions
* known defects
* prior failing runs
* approved related tests
* critical rules
* mismatch warnings

## 10.4 Authoring mode

Used by:

* Test Authoring Agent

Focus:

* approved scenarios
* reusable flow modules
* page object summaries
* assertion modules
* linked requirements
* linked state refs
* approved playbooks if relevant
* mismatch warnings

## 10.5 Triage mode

Used by:

* Failure Triage Agent

Focus:

* similar historical runs
* triage summaries
* similar defect drafts
* linked requirements
* semantic trace/evidence summaries
* healing history if relevant

## 10.6 Healing mode

Used by:

* Healing Agent

Focus:

* element fingerprint summaries
* prior healing events
* instability signals
* state refs
* screenshot/DOM summaries

## 10.7 Playbook review mode

Used by:

* Playbook Recommendation Agent

Focus:

* diagnostic run summaries
* discovered state-signal summaries
* similar approved/rejected playbooks
* mismatch warnings
* healing context

## 10.8 Learning mode

Used by:

* Learning Agent

Focus:

* review decisions
* healing attempts
* repeated run issues
* repeated mismatch patterns
* repeated playbook outcomes

This is one of the clearest upgrades over the earlier Part 7.

---

# 11. Retrieval Query Model

Queries should not just be free text.
Use a structured query format.

## 11.1 Retrieval query shape

```json id="odnnpp"
{
  "mode": "strategy",
  "caseId": "CASE-101",
  "executionMode": "diagnostic",
  "queryText": "high risk authentication requirements states and related defects",
  "filters": {
    "artifactTypes": ["story", "rule_doc", "known_defect", "triage_summary", "state_map_summary"],
    "approvalStatus": ["approved", "active"]
  },
  "graphExpansion": true,
  "includeHistory": true,
  "includeMismatchWarnings": true,
  "limit": 12
}
```

### Important final-architecture additions

* `executionMode`
* `includeMismatchWarnings`
* state-aware source filtering

---

# 12. Hybrid Retrieval Flow

## 12.1 Candidate generation

Get candidates from:

* keyword/BM25-style search
* vector similarity
* exact ID matching
* metadata filters

## 12.2 Merge candidate pools

Merge results from all retrieval channels.

## 12.3 Deduplicate

Remove duplicates by:

* sourceId
* chunk similarity
* semantic duplication

## 12.4 Graph expansion

Expand through graph relations.

## 12.5 Rerank

Apply task-aware scoring.

## 12.6 Build context pack

Return final grounded context.

This remains correct, but graph expansion and reranking must now understand states, mismatches, healing, and playbooks too. 

---

# 13. Graph Expansion Rules

Graph expansion should be bounded and task-specific.

## 13.1 Example expansion from a requirement chunk

Expand to:

* linked flow
* linked page
* linked state
* linked transition
* linked API
* linked known defect
* linked approved scenario/test

## 13.2 Example expansion from a state summary

Expand to:

* linked requirement
* linked transition
* linked page
* linked assertions
* linked playbooks

## 13.3 Example expansion from a failed run summary

Expand to:

* executed test asset
* linked scenario
* linked requirement
* linked state
* similar prior triage results
* linked defect drafts
* linked healing events

## 13.4 Example expansion from a healing summary

Expand to:

* linked fingerprint
* linked state
* linked UI element
* similar instability signals
* review outcomes

## 13.5 Expansion depth

Recommended:

* max depth 1 or 2
* avoid unbounded traversal
* prefer explicit high-signal relationships

---

# 14. Reranking Strategy

Reranking must depend on the agent task and execution mode.

## 14.1 Signals to score

* semantic similarity
* keyword match
* same case
* same flow
* same state
* same page/API
* source quality
* approval status
* playbook approval status
* recency
* graph proximity
* confidence of linked entities
* mismatch relevance
* diagnostic vs regression compatibility

## 14.2 Example score concept

```text id="tad4jd"
final_score =
  0.25 * semantic_similarity +
  0.15 * keyword_match +
  0.15 * same_case_boost +
  0.10 * same_flow_boost +
  0.10 * same_state_boost +
  0.10 * source_quality_boost +
  0.10 * approval_status_boost +
  0.05 * recency_boost
```

This does not need to be exact initially, but the design should support weighted reranking.

## 14.3 Mode-aware reranking

### In regression mode

Boost:

* approved assets
* approved playbooks
* stable/high-confidence history

Penalize:

* draft assets
* weakly supported healing summaries
* unresolved mismatches

### In diagnostic mode

Allow:

* draft assets
* richer exploratory history
* healing history
* diagnostic playbook candidates

This is new and required by the final architecture.

---

# 15. Context Pack Builder

This is the key output of RAG.

A context pack should be compact, task-shaped, and source-grounded.

---

## 15.1 Context pack sections

### A. Facts

Small structured summary:

* case
* flows
* pages
* states
* APIs
* defects

### B. Relevant chunks

Top chunks with short text and source refs

### C. Linked entities

Graph-linked entities:

* requirements
* scenarios
* approved tests
* runs
* defect drafts
* playbooks

### D. Semantic state refs

Important state refs and transition refs relevant to the task

### E. Constraints and conflicts

Ambiguities, missing info, contradictions, mismatch warnings

### F. Reusable assets

Relevant modules, assertions, flows, and possibly playbooks

### G. Mode hints

Optional execution-mode-specific constraints:

* approved only
* diagnostic exploratory allowed
* mismatch unresolved
* healing unstable

---

## 15.2 Example context pack

```json id="58jip3"
{
  "contextType": "test_authoring",
  "caseId": "CASE-101",
  "executionMode": "diagnostic",
  "facts": {
    "flows": ["valid login", "invalid password"],
    "pages": ["Login Page", "Dashboard"],
    "states": ["Login Form Ready", "Invalid Password Error Visible"],
    "apis": ["POST /auth/login"]
  },
  "requirements": [
    {
      "id": "REQ-501",
      "text": "User can sign in with valid credentials",
      "sourceRefs": ["CHUNK-9001"]
    },
    {
      "id": "REQ-502",
      "text": "Invalid password shows validation error",
      "sourceRefs": ["CHUNK-9002"]
    }
  ],
  "stateRefs": [
    {
      "id": "STATE-LOGIN-READY",
      "summary": "Login form ready for interaction"
    },
    {
      "id": "STATE-INVALID-PASSWORD-ERROR",
      "summary": "Validation error shown after invalid password"
    }
  ],
  "reusableAssets": [
    {
      "assetId": "TA-2001",
      "type": "flow_module",
      "summary": "Reusable login flow module"
    },
    {
      "assetId": "TA-2002",
      "type": "assertion_module",
      "summary": "Authentication semantic assertions"
    }
  ],
  "mismatchWarnings": [
    {
      "id": "MM-1001",
      "summary": "Wireframe shows CAPTCHA but story does not mention it"
    }
  ],
  "relatedDefects": [
    {
      "id": "BUG-120",
      "summary": "Forgot password link broken"
    }
  ],
  "playbooks": [],
  "gaps": [],
  "conflicts": [
    "Wireframe shows CAPTCHA but story does not mention it"
  ]
}
```

This is the final-architecture version of the earlier context-pack example.

---

# 16. Agent-by-Agent RAG Flows

---

## 16.1 Case Understanding Agent

### Retrieval goal

Understand the case completely.

### Query sources

* story chunks
* rules
* API spec chunks
* browser-captured pages
* defect docs
* fusion summaries

### Graph expansion

* requirement → flow
* flow → page/API
* defect → flow/page
* page → state if state-map summaries exist

### Output

* structured case summary

---

## 16.2 Requirement Mapping Agent

### Retrieval goal

Create evidence-backed mappings.

### Query sources

* requirements-like chunks
* page summaries
* state-map summaries
* transition summaries
* API summaries
* known defect summaries
* mismatch warnings

### Graph expansion

* chunk → requirement
* requirement → flow
* requirement → state
* state → transition
* page → API
* defect → requirement

### Output

* mappings with evidence refs and confidence

---

## 16.3 Risk & Strategy Agent

### Retrieval goal

Identify what matters most.

### Query sources

* high-priority requirements
* high-priority states/transitions
* known defects
* prior failed runs
* approved tests
* rules
* mismatch warnings

### Graph expansion

* flow → prior runs
* requirement → defect
* state → prior failures
* test asset → reuse potential

### Output

* prioritized strategy

---

## 16.4 Test Authoring Agent

### Retrieval goal

Reuse before creating from scratch.

### Query sources

* approved scenarios
* flow modules
* assertion modules
* page object summaries
* linked requirements
* state-map summaries
* transition summaries
* approved playbooks where appropriate
* mismatch warnings

### Graph expansion

* requirement → scenario
* scenario → asset
* asset → assertions
* page → flow module
* state → playbook

### Output

* structured scenario + generated asset proposal

---

## 16.5 Failure Triage Agent

### Retrieval goal

Compare current failure to known patterns.

### Query sources

* prior run summaries
* similar triage summaries
* similar defect drafts
* related requirements
* evidence summaries
* semantic trace summaries
* healing history if relevant

### Graph expansion

* run → asset → scenario → requirement
* run → state → prior failures
* defect draft → known defect similarity
* healing event → instability history

### Output

* classification with confidence

---

## 16.6 Healing Agent

### Retrieval goal

Compare current UI shift to known healing and instability patterns.

### Query sources

* fingerprint summaries
* prior healing summaries
* instability learning signals
* state refs
* state-map summaries

### Graph expansion

* fingerprint → element
* state → transition
* healing → review decision
* instability signal → repeated failures

### Output

* healing proposal with confidence

---

## 16.7 Playbook Recommendation Agent

### Retrieval goal

Decide whether diagnostic discoveries are stable enough to export/promote.

### Query sources

* diagnostic run summaries
* state-signal summaries
* approved/rejected playbook summaries
* mismatch warnings
* healing summaries if any

### Graph expansion

* run → state → transition
* run → healing
* playbook → review outcomes

### Output

* playbook recommendation

---

## 16.8 Defect Drafting Agent

### Retrieval goal

Write a grounded issue draft.

### Query sources

* triage result
* linked requirement summary
* linked state summary
* similar defect drafts
* historical wording patterns

### Graph expansion

* run → requirement
* run → state
* run → evidence
* triage → defect similarity

### Output

* internal defect-quality packet

---

## 16.9 Learning Agent

### Retrieval goal

Find repeat patterns.

### Query sources

* review decisions
* healing attempts
* repeated triage classes
* repeated run issues
* repeated mismatch warnings
* playbook outcomes

### Graph expansion

* asset → repeated failures
* page/state → repeated locator issues
* review decisions → accepted/rejected patterns
* playbook → promotion success/failure patterns

### Output

* learning signals

---

# 17. Retrieval Service APIs

This should remain a dedicated internal service.

---

## 17.1 `indexChunks`

Indexes chunks into retrieval store.

### Request

```json id="l153qs"
{
  "items": [
    {
      "chunkId": "CHUNK-9001",
      "text": "User can sign in with valid credentials",
      "metadata": {
        "caseId": "CASE-101",
        "artifactType": "story",
        "flowRefs": ["FLOW-1001"],
        "stateRefs": ["STATE-LOGIN-READY"]
      }
    }
  ]
}
```

### Response

```json id="4jtvhl"
{
  "indexed": 1,
  "failed": 0
}
```

---

## 17.2 `search`

Hybrid retrieval.

### Request

```json id="b1wzh4"
{
  "mode": "strategy",
  "executionMode": "diagnostic",
  "queryText": "authentication requirements states and known defects",
  "filters": {
    "caseId": "CASE-101",
    "artifactTypes": ["story", "rule_doc", "known_defect", "state_map_summary"]
  },
  "limit": 10
}
```

### Response

```json id="5m6fie"
{
  "candidates": [
    {
      "sourceType": "chunk",
      "sourceId": "CHUNK-9001",
      "score": 0.92,
      "text": "User can sign in with valid credentials",
      "metadata": {
        "artifactType": "story"
      }
    }
  ]
}
```

---

## 17.3 `expandGraphContext`

Expands IDs into linked entities.

### Request

```json id="jr3rn1"
{
  "seedRefs": ["REQ-501", "STATE-LOGIN-READY"],
  "maxDepth": 1,
  "relationshipTypes": ["RELATES_TO_PAGE", "MAPS_TO_STATE", "RELATES_TO_API", "VALIDATES_REQUIREMENT"]
}
```

### Response

```json id="9875tq"
{
  "entities": [
    {"id": "PAGE-301", "type": "Page", "name": "Login Page"},
    {"id": "API-401", "type": "ApiEndpoint", "name": "POST /auth/login"}
  ],
  "relationships": [
    {"from": "REQ-501", "to": "STATE-LOGIN-READY", "type": "MAPS_TO_STATE"}
  ]
}
```

---

## 17.4 `buildContextPack`

Builds final agent-ready context.

### Request

```json id="mfhm0m"
{
  "agentType": "test_authoring",
  "caseId": "CASE-101",
  "executionMode": "diagnostic",
  "queryText": "invalid password scenario",
  "filters": {
    "includeHistory": true,
    "includeMismatchWarnings": true,
    "includePlaybooks": false
  },
  "limits": {
    "chunks": 8,
    "entities": 12,
    "assets": 5
  }
}
```

### Response

```json id="9g2yy2"
{
  "contextPack": {
    "facts": {},
    "requirements": [],
    "stateRefs": [],
    "chunks": [],
    "reusableAssets": [],
    "relatedHistory": [],
    "mismatchWarnings": [],
    "playbooks": [],
    "gaps": []
  }
}
```

---

# 18. Retrieval Policies

Different agents should have different retrieval policies.

## Example policy table

| Agent                   | Include Draft Assets | Include History | Include Learning Signals | Include Mismatches | Include Playbooks | Max Chunks |
| ----------------------- | -------------------: | --------------: | -----------------------: | -----------------: | ----------------: | ---------: |
| Case Understanding      |                   No |         Limited |                       No |                Yes |                No |         12 |
| Requirement Mapping     |                   No |         Limited |                       No |                Yes |                No |         10 |
| Strategy                |                  Yes |             Yes |                      Yes |                Yes |           Limited |         12 |
| Test Authoring          |                  Yes |             Yes |                      Yes |                Yes |           Limited |         10 |
| Triage                  |                  Yes |             Yes |                      Yes |                Yes |           Limited |         14 |
| Healing                 |              Limited |             Yes |                      Yes |                Yes |                No |         10 |
| Playbook Recommendation |              Limited |             Yes |                      Yes |                Yes |               Yes |         10 |
| Defect Drafting         |                  Yes |             Yes |                  Limited |                Yes |                No |          8 |
| Learning                |                  Yes |             Yes |                      Yes |                Yes |               Yes |         16 |

## Mode-aware rule

### Regression-oriented retrieval

Prefer:

* approved assets
* approved playbooks
* approved stable history

### Diagnostic-oriented retrieval

Allow:

* draft assets
* healing patterns
* discovery-oriented summaries
* playbook candidates

This policy split is required by the final architecture.

---

# 19. RAG Logging and Observability

You need to know what the system retrieved and why.

## 19.1 Log for each retrieval

Store:

* query
* filters
* agent type
* execution mode
* raw candidates
* reranked candidates
* final context refs
* latency
* errors
* retrieval degradation notes

## 19.2 Why this matters

This helps debug:

* wrong retrieval
* context pollution
* missing sources
* bad ranking
* poor agent outputs
* mismatch suppression
* inappropriate diagnostic content leaking into regression

---

# 20. RAG Records to Support

These records were already present in your operational model, but now they must be used with the final-architecture intent:

* `retrieval_query_log`
* `retrieval_result_log`
* `context_pack_log`

And they must now explicitly support:

* `executionMode`
* `stateRefs`
* `mismatchRefs`
* `playbookRefs`
* `healingRefs`

This is a usage correction rather than a net-new schema concept.

---

# 21. RAG Failure Modes and Safeguards

## 21.1 Failure mode: too much context

Fix:

* task-specific max limits
* reranking
* context compaction

## 21.2 Failure mode: wrong history dominates

Fix:

* same-case and same-flow boosts
* same-state boosts
* approval-status weighting
* recency controls

## 21.3 Failure mode: graph over-expansion

Fix:

* max expansion depth
* relationship allowlist per agent task

## 21.4 Failure mode: low-quality browser captures

Fix:

* source quality score
* provenance preserved
* lower ranking unless corroborated

## 21.5 Failure mode: prompt contamination from drafts

Fix:

* filter by approval state when needed
* prefer approved assets by default in authoring and strategy

## 21.6 Failure mode: unresolved mismatches silently ignored

Fix:

* include mismatch warnings in relevant context packs by default
* raise mismatch severity in reranking when task depends on affected state or requirement

## 21.7 Failure mode: diagnostic artifacts contaminate regression support

Fix:

* execution-mode-aware filtering
* approved-playbook-only bias in regression mode
* downrank exploratory artifacts unless explicitly requested

## 21.8 Failure mode: healing history overpowers current evidence

Fix:

* current-run evidence first in triage/healing
* healing summaries treated as support, not proof

These safeguards are direct consequences of the final architecture.

---

# 22. Initial RAG Implementation Order

Build in this order:

## Phase A

1. artifact chunking
2. metadata enrichment
3. hybrid index
4. simple search API

## Phase B

5. artifact fusion summaries
6. semantic state summaries
7. mismatch summaries
8. graph linking
9. graph expansion API
10. reranking
11. context pack builder

## Phase C

12. agent-specific retrieval modes
13. retrieval logs
14. history-aware triage retrieval
15. reusable asset retrieval for authoring
16. healing-aware retrieval
17. playbook-aware retrieval

This is the final-architecture-aligned implementation sequence.

---

# 23. Minimal RAG for First Working Version

If you want the smallest serious implementation that still fits the final architecture:

* chunk stories, rules, API specs, defects
* generate simple state-map summaries
* index with hybrid retrieval
* filter by caseId and artifactType
* retrieve top 8 chunks
* expand one hop through graph
* build small context packs
* include mismatch warnings when present
* use in:

  * Case Understanding Agent
  * Requirement Mapping Agent
  * Risk & Strategy Agent
  * Test Authoring Agent

That already gives major value while staying aligned with the final architecture.

---

# 24. Full RAG Summary

The correct RAG design for your final architecture is:

## Ingestion RAG

Convert source artifacts into:

* normalized artifacts
* structured chunks
* fusion summaries
* semantic state summaries
* mismatch summaries
* graph-linked entities

## Runtime Graph-RAG

For each agent task:

* hybrid retrieve
* graph expand
* rerank
* build context pack
* feed grounded prompt

## Historical RAG

Reuse:

* approved tests
* past failures
* defect drafts
* review decisions
* healing signals
* approved playbooks
* learning signals

## State-Aware RAG

Ground reasoning in:

* semantic states
* transitions
* expected outcomes
* fingerprints

## Mode-Aware RAG

Differentiate:

* diagnostic retrieval behavior
* regression retrieval behavior

That makes RAG an actual implementation subsystem for the final architecture, not just a concept. 

---

# 25. Final Position

So the corrected implementation view is:

* **Distributed Understanding Service** owns parsing, normalization, artifact fusion support, and chunk preparation
* **Semantic State Service** owns state-map generation and state summaries
* **Mismatch Detection Service** owns mismatch generation and mismatch summaries
* **Knowledge Graph Service** owns entity and relationship structure
* **Retrieval Service** owns hybrid search, graph expansion, reranking, and context pack assembly
* **Agent Runtime Service** consumes context packs, not raw documents
