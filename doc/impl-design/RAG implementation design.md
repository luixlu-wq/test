I agree with most of Gemini’s comments. The strongest updates are:

* make **Hybrid Graph-RAG** the explicit standard, not just “hybrid retrieval”
* make **multi-hop reasoning over the Semantic State Map** more explicit as the main reason Graph-RAG is necessary for QA
* make **Context Pack assembly** a first-class anti-hallucination layer
* make **reranking** mandatory and explicit, especially for messy folder-based artifacts and multiple artifact versions
* strengthen the **forensic retrieval path** for Healing by explicitly retrieving prior fingerprints, prior healing logs, and prior approved healing outcomes
* make **diagnostic vs regression retrieval policy** sharper and more operational
* strengthen **Mismatch RAG** as a safety net during new ingestion and understanding
* emphasize the **Foundational Three** implementation priorities:

  1. ingestion pipeline
  2. state-map retriever
  3. evidence packager

I did **not** change the overall direction, because your uploaded Part 7 was already strong on Graph-RAG, semantic state retrieval, graph expansion, reranking, context packs, and auditability. The comments mostly sharpen the implementation priorities and make the retrieval behavior more explicitly production-grade. 

Below is the **rewritten Part 7 — RAG Implementation Design**, kept full-length and aligned to the final architecture.

---

# Part 7 — RAG Implementation Design

## AI QA Platform

### Final Architecture-Aligned Version

#### Full merged rewrite

This section defines the **RAG implementation subsystem** for your AI-powered QA platform.

This is not “document search plus LLM.”

This is a **multi-layered intelligence retrieval system** designed for software quality engineering, where the cost of wrong retrieval is high.

It defines:

* the RAG architecture
* ingestion pipeline
* chunking rules
* indexing strategy
* hybrid retrieval logic
* graph expansion logic
* reranking
* context-pack assembly
* semantic-state-aware retrieval
* mismatch-aware retrieval
* healing-aware retrieval
* playbook-aware retrieval
* evidence-aware retrieval
* agent-by-agent retrieval flow
* APIs/contracts for the Retrieval Service
* implementation priorities

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

# 1. Strategic RAG win

The most important design decision is:

## Vector RAG alone is not enough for QA

Pure vector search can find:

* similar text
* similar wording
* semantically close chunks

But QA needs more than similarity.
It needs **logic, sequence, state, and traceability**.

Examples:

* What happens after clicking Submit?
* Which UI state should exist before this assertion?
* Which transition takes the user from Login to Dashboard?
* Which prior healing applies to this same UI element?
* Which mismatch warning affects this requirement before test generation begins?

A vector store alone is weak at this.

So the correct standard is:

## Hybrid Graph-RAG + Semantic State Retrieval

That means:

* retrieval index for lexical and semantic candidate search
* knowledge graph for explicit relationship traversal
* semantic state map for UI and flow logic
* reranking for task precision
* context packs for bounded grounded agent input

This is the main architectural win in the RAG design. 

---

# 2. Purpose of RAG in this platform

RAG is not just “search documents and paste them into a prompt.”

In this QA platform, RAG must do **eight** jobs.

## 2.1 Ground agent reasoning

Agents must use source-backed context instead of guessing.

## 2.2 Connect scattered QA knowledge

Relevant truth is spread across:

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
* evidence summaries
* semantic traces

## 2.3 Reuse prior QA intelligence

The system should retrieve:

* existing good tests
* past similar failures
* known risky flows
* approved assertions
* accepted healing patterns
* approved deterministic playbooks
* state-signal baselines

## 2.4 Ground semantic state reasoning

The system must retrieve not only text, but also:

* state-map summaries
* state refs
* transition refs
* expected outcomes
* fingerprint summaries

## 2.5 Surface contradictions early

The system must retrieve:

* mismatch warnings
* unresolved conflicts
* conflicting expectations

so that strategy and authoring do not operate on silently inconsistent requirements.

## 2.6 Support mode-aware execution intelligence

The system must distinguish:

* **diagnostic retrieval** for discovery and analysis
* **regression retrieval** for approved, stable execution support

## 2.7 Support forensic interpretation

The system must retrieve:

* evidence summaries
* semantic traces
* prior healing events
* prior triage patterns
* similar defect drafts

## 2.8 Reconstruct the application’s mental model

This is the most important conceptual point from the review.

RAG must help the agent reconstruct:

* what the application is supposed to do
* what state it is currently in
* what transition should happen next
* what evidence proves success or failure

That is a much stronger goal than “find related text.”

---

# 3. RAG subsystem overview

```text id="scqv50"
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
  -> Feed Agent Prompt / Execution Preparation / Triage
```

This remains the right top-level pipeline, but the review is right that the transition from **Ingestion RAG** to **State-Aware RAG** should be made more explicit. 

---

# 4. RAG operating layers

The RAG subsystem should be understood as four layers.

## 4.1 Ingestion RAG

Transforms raw artifacts into retrieval- and graph-ready structured knowledge.

Outputs:

* normalized artifacts
* chunks
* metadata
* fusion summaries
* state summaries
* mismatch summaries
* retrieval views

## 4.2 State-Aware RAG

Makes semantic state maps retrievable and graph-expandable.

Outputs:

* state summaries
* transition summaries
* outcome summaries
* fingerprint summaries
* linked page/API/test relationships

## 4.3 Forensic RAG

Supports triage and healing using:

* evidence summaries
* semantic trace summaries
* healing logs
* historical failure summaries
* defect support context

## 4.4 Mode-Aware RAG

Changes retrieval behavior depending on:

* diagnostic mode
* regression mode

This is the right high-level conceptual split for the final architecture.

---

# 5. RAG architecture components

The RAG subsystem should have these components:

1. **Artifact Normalizer**
2. **Artifact Fusion Support Layer**
3. **Semantic State Summarizer**
4. **Mismatch Summary Generator**
5. **Evidence Packager / Evidence Summarizer**
6. **Chunking Engine**
7. **Metadata Enrichment Engine**
8. **Indexing Pipeline**
9. **Hybrid Retrieval Engine**
10. **Graph Expansion Engine**
11. **Reranker**
12. **Context Pack Builder**
13. **Retrieval Policy Layer**
14. **Retrieval Audit Log**

### Important refinement

The review is correct that the **Evidence Packager** should be treated as one of the foundational pipelines for RAG, not just a later convenience. It is essential for triage and forensic review. 

---

# 6. Component responsibilities

## 6.1 Artifact Normalizer

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

## 6.2 Artifact Fusion Support Layer

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

This is where Ingestion RAG becomes useful to downstream agents.

---

## 6.3 Semantic State Summarizer

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
* fingerprint summaries

These summaries let agents retrieve the application’s logic model, not just descriptive text.

---

## 6.4 Mismatch Summary Generator

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

This is the system’s main safety net against contradiction debt.

---

## 6.5 Evidence Packager / Evidence Summarizer

Creates retrieval-ready evidence bundles and summaries.

Input:

* screenshots
* traces
* DOM snapshots
* console logs
* HAR / API evidence
* semantic trace
* reasoning logs

Output:

* evidence summaries
* triage-ready bundles
* healing-support bundles
* playbook-support bundles
* retrieval views for evidence artifacts

This is one of the **Foundational Three** pipelines and should be treated as such.

---

## 6.6 Chunking Engine

Breaks artifacts and generated summaries into retrievable units.

Input:

* normalized artifact
* artifact type
* parse result
* state-map or mismatch summary if relevant
* evidence summary if relevant

Output:

* chunk records
* chunk metadata
* chunk ordering

---

## 6.7 Metadata Enrichment Engine

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
* healingRef
* evidenceRef
* executionMode relevance
* approval status
* recency/version hints

---

## 6.8 Indexing Pipeline

Writes chunks and retrieval views to search/vector infrastructure.

Responsibilities:

* generate embeddings
* store searchable text
* store metadata filters
* track index status
* keep index rows linked to graph and relational records

---

## 6.9 Hybrid Retrieval Engine

Retrieves candidate content using:

* keyword search
* vector similarity
* metadata filters
* exact reference matching

This is the entry point, not the whole retrieval story.

---

## 6.10 Graph Expansion Engine

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

This is what turns similar text into navigable logic.

---

## 6.11 Reranker

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
* version recency / approved-vs-old artifact preference

### Important refinement

The review is right that reranking should be treated as **mandatory**, not optional.
Folder-based artifacts can be messy, duplicated, or stale. A reranker is needed to prefer:

* approved wireframe version
* latest accepted state map summary
* approved asset instead of draft
* exact-state history over loosely similar history

---

## 6.12 Context Pack Builder

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
* evidence bundle refs where relevant

This remains one of the best parts of the design.

---

## 6.13 Retrieval Policy Layer

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

## 6.14 Retrieval Audit Log

Stores:

* queries
* filters
* candidates
* final selected refs
* context pack contents
* timing
* execution mode
* retrieval degradation
* reranking notes

This remains critical and becomes even more important in a multi-layer retrieval system.

---

# 7. RAG data categories

The index should distinguish content categories.

## 7.1 Source artifact content

* stories
* rules
* expected result docs
* API specs
* wireframe descriptions
* browser page captures
* defect docs

## 7.2 Fused understanding content

* case understanding summaries
* artifact fusion summaries
* identified conflicts/gaps

## 7.3 Semantic state content

* state-map summaries
* UI state summaries
* transition summaries
* expected outcome summaries
* fingerprint summaries

## 7.4 Mismatch content

* mismatch warnings
* mismatch explanation summaries
* conflict summaries

## 7.5 Generated QA assets

* strategy summaries
* scenario summaries
* approved test summaries
* assertion summaries
* reusable flow summaries

## 7.6 Runtime history

* run summaries
* failure summaries
* triage summaries
* defect draft summaries
* review outcomes

## 7.7 Healing and playbook content

* healing summaries
* accepted/rejected healing patterns
* playbook summaries
* discovered state-signal summaries

## 7.8 Evidence and forensic content

* evidence summaries
* semantic trace summaries
* reasoning log summaries
* triage bundles
* visual diff summaries

## 7.9 Learning content

* accepted healing patterns
* repeated unstable selectors/states
* recurring failure patterns
* accepted/rejected playbook patterns

This broader categorization better reflects the final architecture’s forensic side.

---

# 8. Current-stage RAG sources

For your current stage, RAG should use these inputs:

## 8.1 Folder-based sources

* `/stories`
* `/wireframes`
* `/screenshots`
* `/defects`
* `/api`
* `/rules`
* `/expected`
* `/refs/urls.yaml`

## 8.2 Browser-readable sources

* story pages
* defect pages
* wiki pages
* design preview pages
* internal documentation pages

## 8.3 Internal platform history

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
* evidence summaries
* learning signals

---

# 9. Chunking design

Chunking must be:

* artifact-type-aware
* state-type-aware
* forensic-type-aware

## 9.1 Story documents

Chunk by:

* title
* feature summary
* acceptance criteria block
* flow section
* validation section
* notes/constraints

## 9.2 Rules documents

Chunk by:

* rule heading
* rule block
* exception block
* edge cases

## 9.3 API specs

Chunk by:

* endpoint
* request schema
* response schema
* error responses
* auth notes

## 9.4 Defect documents

Chunk by:

* summary
* repro steps
* expected behavior
* actual behavior
* root cause notes
* workaround notes

## 9.5 Browser-readable captured pages

Chunk by:

* page title and summary
* extracted structured fields
* main body section
* identified ticket/story/bug info

## 9.6 Wireframes and screenshots

Do not index raw binaries.
Index:

* image summary
* OCR or vision-derived text if available
* extracted UI structure summary
* visible controls
* labeled expectations
* likely page/state summary

## 9.7 Semantic state maps

Chunk by:

* page-level state summary
* state summary
* transition summary
* expected-outcome summary
* fingerprint summary

## 9.8 Mismatch warnings

Chunk by:

* mismatch summary
* source conflict explanation
* affected requirement/page/state/API explanation

## 9.9 Test assets

Prefer summary chunks:

* scenario summary
* flow summary
* assertions summary
* reusable module description
* playbook linkage summary if present

## 9.10 Run and triage history

Chunk by:

* run summary
* failure reason summary
* classification summary
* evidence interpretation summary
* decision summary

## 9.11 Healing and playbook history

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

## 9.12 Evidence bundles

Chunk by:

* evidence summary
* semantic trace summary
* reasoning summary
* triage-support summary
* playbook-support summary

This extra chunk class is important for forensic RAG.

---

# 10. Chunk schema

Every chunk should carry rich metadata.

## 10.1 Base chunk fields

```json id="gqxolb"
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

## 10.2 Recommended metadata fields

```json id="g7w98h"
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
  "healingRefs": [],
  "evidenceRefs": [],
  "priority": "high",
  "status": "active",
  "sourceQuality": "high",
  "approvalStatus": "approved",
  "environmentScope": ["UAT"],
  "executionModeScope": ["diagnostic", "regression"]
}
```

These fields are essential for precise retrieval and bounded context assembly.

---

# 11. Indexing strategy

Use **hybrid indexing**.

## 11.1 Search fields

Store:

* title
* text
* normalized keywords
* IDs and exact references
* metadata filters

## 11.2 Vector fields

Store embedding vectors for:

* chunk text
* optionally chunk title + text combined

## 11.3 Filter fields

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
* version recency / document status if available

This last part is important when multiple versions of a wireframe or summary exist.

---

# 12. Retrieval modes

The Retrieval Service should support several modes.

## 12.1 Case understanding mode

Used by:

* Case Understanding Agent

Focus:

* stories
* rules
* expected docs
* browser-captured pages
* fusion summaries
* conflicts/gaps
* existing mismatch warnings for the same case

### Important refinement

Gemini’s comment is right: **Mismatch RAG** should feed intake/understanding to prevent contradiction debt from accumulating.

---

## 12.2 Requirement mapping mode

Used by:

* Requirement Mapping Agent

Focus:

* requirement-bearing chunks
* state-map summaries
* page/API summaries
* known defects
* mismatch warnings

---

## 12.3 Strategy mode

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

---

## 12.4 Authoring mode

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

---

## 12.5 Triage mode

Used by:

* Failure Triage Agent

Focus:

* current run evidence summaries
* semantic trace summaries
* similar historical runs
* triage summaries
* similar defect drafts
* related requirements
* healing history if relevant

### Important refinement

Current evidence should be packaged first, then historical analogs added as support.

---

## 12.6 Healing mode

Used by:

* Healing Agent

Focus:

* element fingerprint summaries
* prior healing events
* instability signals
* state refs
* screenshot/DOM summaries
* prior approved healing outcomes

This is the explicit forensic retrieval path the review highlighted.

---

## 12.7 Playbook review mode

Used by:

* Playbook Recommendation Agent

Focus:

* diagnostic run summaries
* discovered state-signal summaries
* similar approved/rejected playbooks
* mismatch warnings
* healing context
* performance baseline context if available

---

## 12.8 Learning mode

Used by:

* Learning Agent

Focus:

* review decisions
* healing attempts
* repeated run issues
* repeated mismatch patterns
* repeated playbook outcomes

---

# 13. Retrieval query model

Queries should not just be free text.
Use a structured query format.

## 13.1 Retrieval query shape

```json id="4qqthv"
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

Important fields:

* `executionMode`
* `includeMismatchWarnings`
* state-aware filters
* approval-aware filters
* version/recency controls where needed

---

# 14. Hybrid retrieval flow

## 14.1 Candidate generation

Get candidates from:

* keyword/BM25-style search
* vector similarity
* exact ID matching
* metadata filters

## 14.2 Merge candidate pools

Merge results from all retrieval channels.

## 14.3 Deduplicate

Remove duplicates by:

* sourceId
* chunk similarity
* semantic duplication

## 14.4 Graph expansion

Expand through graph relations.

## 14.5 Rerank

Apply task-aware scoring.

## 14.6 Build context pack

Return final grounded context.

This is still correct, but in this revision the **rerank step** is treated as mandatory and central.

---

# 15. Graph expansion rules

Graph expansion should be bounded and task-specific.

## 15.1 Example expansion from a requirement chunk

Expand to:

* linked flow
* linked page
* linked state
* linked transition
* linked API
* linked known defect
* linked approved scenario/test

## 15.2 Example expansion from a state summary

Expand to:

* linked requirement
* linked transition
* linked page
* linked assertions
* linked playbooks

## 15.3 Example expansion from a failed run summary

Expand to:

* executed test asset
* linked scenario
* linked requirement
* linked state
* similar prior triage results
* linked defect drafts
* linked healing events

## 15.4 Example expansion from a healing summary

Expand to:

* linked fingerprint
* linked state
* linked UI element
* similar instability signals
* prior approved healing outcomes
* review outcomes

## 15.5 Expansion depth

Recommended:

* max depth 1 or 2
* avoid unbounded traversal
* prefer explicit high-signal relationships

This is how the system gets multi-hop reasoning without uncontrolled graph wandering.

---

# 16. Reranking strategy

Reranking must depend on:

* agent task
* execution mode
* approval state
* case fidelity
* state fidelity
* artifact recency/version quality

## 16.1 Signals to score

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
* evidence freshness
* artifact version quality

## 16.2 Example score concept

```text id="mhvbc8"
final_score =
  0.22 * semantic_similarity +
  0.12 * keyword_match +
  0.15 * same_case_boost +
  0.10 * same_flow_boost +
  0.10 * same_state_boost +
  0.10 * source_quality_boost +
  0.10 * approval_status_boost +
  0.06 * recency_boost +
  0.05 * graph_proximity_boost
```

## 16.3 Cross-encoder recommendation

Gemini’s comment is correct: a dedicated reranker such as a **cross-encoder** is a strong fit here, especially for:

* multiple wireframe versions
* duplicate summaries
* approved vs draft asset ambiguity
* loosely similar but state-wrong evidence

Use it where latency budget allows.

## 16.4 Mode-aware reranking

### In regression mode

Boost:

* approved assets
* approved playbooks
* stable/high-confidence history
* exact state matches

Penalize:

* draft assets
* weakly supported healing summaries
* unresolved mismatches
* broad exploratory history

### In diagnostic mode

Allow:

* draft assets
* richer exploratory history
* healing history
* diagnostic playbook candidates
* broader graph expansion

This sharpens the diagnostic-vs-regression split as the review recommended.

---

# 17. Context pack builder

A context pack should be compact, task-shaped, and source-grounded.

## 17.1 Context pack sections

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

### G. Evidence bundle refs

For triage/healing/playbook review:

* semantic trace
* screenshot summary
* DOM snapshot summary
* reasoning summary

### H. Mode hints

Optional execution-mode-specific constraints:

* approved only
* diagnostic exploratory allowed
* mismatch unresolved
* healing unstable

This remains one of the best anti-hallucination design choices in the whole spec. 

---

## 17.2 Example context pack

```json id="wkltlb"
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

---

# 18. Agent-by-agent RAG flows

## 18.1 Case Understanding Agent

### Retrieval goal

Understand the case completely.

### Query sources

* story chunks
* rules
* API spec chunks
* browser-captured pages
* defect docs
* fusion summaries
* mismatch warnings

### Graph expansion

* requirement → flow
* flow → page/API
* defect → flow/page
* page → state if state-map summaries exist

### Output

* structured case summary

---

## 18.2 Requirement Mapping Agent

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

## 18.3 Risk & Strategy Agent

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

## 18.4 Test Authoring Agent

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

## 18.5 Failure Triage Agent

### Retrieval goal

Compare current failure to known patterns.

### Query sources

* current evidence summaries
* semantic trace summaries
* prior run summaries
* similar triage summaries
* similar defect drafts
* related requirements
* healing history if relevant

### Graph expansion

* run → asset → scenario → requirement
* run → state → prior failures
* defect draft → known defect similarity
* healing event → instability history

### Output

* classification with confidence

---

## 18.6 Healing Agent

### Retrieval goal

Compare current UI shift to known healing and instability patterns.

### Query sources

* fingerprint summaries
* prior healing summaries
* instability learning signals
* state refs
* state-map summaries
* current screenshot/DOM summaries
* prior approved healing outcomes

### Graph expansion

* fingerprint → element
* state → transition
* healing → review decision
* instability signal → repeated failures

### Output

* healing proposal with confidence

This is the clearest forensic retrieval path in the system.

---

## 18.7 Playbook Recommendation Agent

### Retrieval goal

Decide whether diagnostic discoveries are stable enough to export/promote.

### Query sources

* diagnostic run summaries
* state-signal summaries
* approved/rejected playbook summaries
* mismatch warnings
* healing summaries if any
* performance baseline history if available

### Graph expansion

* run → state → transition
* run → healing
* playbook → review outcomes

### Output

* playbook recommendation

---

## 18.8 Defect Drafting Agent

### Retrieval goal

Write a grounded issue draft.

### Query sources

* triage result
* linked requirement summary
* linked state summary
* current evidence bundle summaries
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

## 18.9 Learning Agent

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

# 19. Retrieval service APIs

This should remain a dedicated internal service.

## 19.1 `indexChunks`

Indexes chunks into retrieval store.

### Request

```json id="ud540a"
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

```json id="gltq2s"
{
  "indexed": 1,
  "failed": 0
}
```

---

## 19.2 `search`

Hybrid retrieval.

### Request

```json id="p5463g"
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

```json id="jmy6p4"
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

## 19.3 `expandGraphContext`

Expands IDs into linked entities.

### Request

```json id="6myhis"
{
  "seedRefs": ["REQ-501", "STATE-LOGIN-READY"],
  "maxDepth": 1,
  "relationshipTypes": ["RELATES_TO_PAGE", "MAPS_TO_STATE", "RELATES_TO_API", "VALIDATES_REQUIREMENT"]
}
```

### Response

```json id="5b7ow9"
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

## 19.4 `buildContextPack`

Builds final agent-ready context.

### Request

```json id="pdsvmd"
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

```json id="vp7r4v"
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
    "evidenceBundles": [],
    "gaps": []
  }
}
```

---

# 20. Retrieval policies

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
* exact state matches
* narrow graph expansion

### Diagnostic-oriented retrieval

Allow:

* draft assets
* healing patterns
* discovery-oriented summaries
* playbook candidates
* broader graph expansion

This sharper split is one of the best improvements from the review.

---

# 21. RAG logging and observability

You need to know what the system retrieved and why.

## 21.1 Log for each retrieval

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

## 21.2 Why this matters

This helps debug:

* wrong retrieval
* context pollution
* missing sources
* bad ranking
* poor agent outputs
* mismatch suppression
* inappropriate diagnostic content leaking into regression

---

# 22. RAG failure modes and safeguards

## 22.1 Failure mode: too much context

Fix:

* task-specific max limits
* reranking
* context compaction

## 22.2 Failure mode: wrong history dominates

Fix:

* same-case and same-flow boosts
* same-state boosts
* approval-status weighting
* recency controls

## 22.3 Failure mode: graph over-expansion

Fix:

* max expansion depth
* relationship allowlist per agent task

## 22.4 Failure mode: low-quality browser captures

Fix:

* source quality score
* provenance preserved
* lower ranking unless corroborated

## 22.5 Failure mode: prompt contamination from drafts

Fix:

* filter by approval state when needed
* prefer approved assets by default in authoring and strategy

## 22.6 Failure mode: unresolved mismatches silently ignored

Fix:

* include mismatch warnings in relevant context packs by default
* raise mismatch severity in reranking when task depends on affected state or requirement

## 22.7 Failure mode: diagnostic artifacts contaminate regression support

Fix:

* execution-mode-aware filtering
* approved-playbook-only bias in regression mode
* downrank exploratory artifacts unless explicitly requested

## 22.8 Failure mode: healing history overpowers current evidence

Fix:

* current-run evidence first in triage/healing
* healing summaries treated as support, not proof

These safeguards remain essential.

---

# 23. Foundational three implementation priorities

The review is right that the best initial build path is:

## 23.1 The ingestion pipeline

Normalize manual folder files into:

* chunks
* entities
* graph links
* retrieval views

## 23.2 The state-map retriever

Enable agents to ask:

* what is the current state?
* what state should follow?
* what transition belongs here?

and receive fused UI + story context.

## 23.3 The evidence packager

Automate assembly of:

* screenshots
* logs
* traces
* semantic trace
* DOM summaries

into a retrieval-ready bundle for triage and healing.

This is the best practical interpretation of the review’s implementation priorities. 

---

# 24. Initial RAG implementation order

Build in this order.

## Phase A — Foundational Three

1. artifact chunking
2. metadata enrichment
3. hybrid index
4. simple search API
5. graph linking
6. state-map summaries
7. evidence summaries and bundles

## Phase B — Core Graph-RAG

8. graph expansion API
9. reranking
10. context pack builder
11. mismatch summaries
12. state-aware retriever

## Phase C — Agent-specialized retrieval

13. agent-specific retrieval modes
14. retrieval logs
15. history-aware triage retrieval
16. reusable asset retrieval for authoring
17. healing-aware retrieval
18. playbook-aware retrieval

This is a more explicit and stronger implementation plan than before.

---

# 25. Minimal RAG for first working version

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

Then add:

* evidence summary retrieval
* healing history retrieval
* playbook summary retrieval

That gives real value without overbuilding.

---

# 26. Full RAG summary

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

## State-Aware RAG

Ground reasoning in:

* semantic states
* transitions
* expected outcomes
* fingerprints

## Forensic RAG

Ground triage and healing in:

* current evidence bundles
* semantic trace
* prior healing events
* prior defect/triage analogs

## Historical RAG

Reuse:

* approved tests
* past failures
* defect drafts
* review decisions
* healing signals
* approved playbooks
* learning signals

## Mode-Aware RAG

Differentiate:

* diagnostic retrieval behavior
* regression retrieval behavior

That makes RAG an actual implementation subsystem for the final architecture, not just a concept. 

---

# 27. Final position

So the corrected implementation view is:

* **Distributed Understanding Service** owns parsing, normalization, artifact fusion support, and chunk preparation
* **Semantic State Service** owns state-map generation and state summaries
* **Mismatch Detection Service** owns mismatch generation and mismatch summaries
* **Evidence Service** owns evidence packaging and evidence summaries
* **Knowledge Graph Service** owns entity and relationship structure
* **Retrieval Service** owns hybrid search, graph expansion, reranking, and context pack assembly
* **Agent Runtime Service** consumes context packs, not raw documents

