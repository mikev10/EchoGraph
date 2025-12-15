# Agentic Workflow Architecture Proposal

**Status**: DRAFT
**Created**: 2024-12-15
**Author**: Claude (based on product team feedback + agentic AI research)

---

## Executive Summary

This proposal extends the product workflow redesign to support a **fully agentic architecture** where AI agents autonomously execute workflows from concept to feature, with human approval gates at critical decision points.

EchoGraph should be positioned as an **agentic workflow platform** - not just a workflow documentation tool with AI assistance. This differentiates it from tools like n8n (procedural automation) and positions it alongside modern agentic frameworks like LangGraph and CrewAI.

**Key differentiators:**
- **Open-source core** + **hosted paid solution** (dual licensing model)
- **Knowledge graph memory** for multi-hop reasoning (GraphRAG)
- **Role-based AI agents** that mirror real product team roles
- **Human-in-the-loop** approval gates at critical decisions
- **Full traceability** from concept → feature → code

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Three-Layer Architecture](#three-layer-architecture)
3. [Why Not n8n](#why-not-n8n)
4. [Framework Comparison](#framework-comparison)
5. [Proposed Agentic Architecture](#proposed-agentic-architecture)
6. [Agent Definitions](#agent-definitions)
7. [Memory Layer](#memory-layer)
8. [Workflow Example](#workflow-example)
9. [Human-in-the-Loop Design](#human-in-the-loop-design)
10. [Open Source vs Hosted Split](#open-source-vs-hosted-split)
11. [Phased Implementation Plan](#phased-implementation-plan)
12. [Technology Recommendations](#technology-recommendations)
13. [Sources](#sources)

---

## Problem Statement

### User Feedback

Product teams reported confusion about:
1. Order of command execution and role responsibilities
2. Missing step-by-step guide for agile/scrum teams
3. Unclear relationship between plans, feature requests, and user stories
4. Need to organize commands as real team members (PM, BA, PO)

### Deeper Issue

The initial proposal addressed workflow documentation but missed the **agentic vision**:

> "This is more than just building this product team. This is one part of the overall vision of EchoGraph. Full agentic workflow from concept to feature. We will build this in phases and use tools to help handle the agentic workflow and memory, knowledge graph, RAG, Graph RAG, and more."

EchoGraph should be a platform where **AI agents autonomously execute** the product development workflow, not just assist humans in following a documented process.

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: AGENTIC ORCHESTRATION                                              │
│ AI agents that autonomously execute workflows with human approval gates     │
│ Framework: LangGraph + CrewAI-style role agents + Agent Memory              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: WORKFLOW DEFINITION                                                │
│ The artifact hierarchy and agent behavior specifications                    │
│ Initiative → Epic → Feature → Story → PRP → Task                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: INFRASTRUCTURE                                                     │
│ Storage, search, embeddings, knowledge retrieval                            │
│ LanceDB + SQLite + Knowledge Graph + Nomic Embeddings + Hybrid Search       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Purpose | Components |
|-------|---------|------------|
| **Layer 1: Infrastructure** | Data storage and retrieval | LanceDB, SQLite, Knowledge Graph, Embeddings |
| **Layer 2: Workflow** | Define what agents do | Artifact hierarchy, agent behaviors, approval gates |
| **Layer 3: Agentic** | Execute workflows autonomously | LangGraph orchestration, role agents, memory |

---

## Why Not n8n

Many teams use n8n for workflow automation. Here's why EchoGraph needs a different approach:

### n8n Limitations for Agentic AI

| n8n Limitation | Impact | EchoGraph Solution |
|----------------|--------|-------------------|
| **Stateless architecture** | Memory wiped after each workflow run | Persistent agent memory via knowledge graph |
| **No native knowledge base** | Can't do multi-hop reasoning | GraphRAG for complex queries |
| **Manual debugging** | No automatic feedback loops | Self-improving agents with evaluation |
| **Procedural only** | Just executes predefined steps | Cognitive orchestration - agents reason and adapt |
| **No autonomous planning** | Can't decompose complex goals | Goal-oriented agents that break down tasks |
| **No long-term memory** | Each run starts fresh | Episodic + semantic memory persists |

### The Fundamental Difference

> "If n8n is about procedural automation, agentic AI is about cognitive orchestration. One executes steps; the other coordinates intelligence."

n8n: `trigger → step 1 → step 2 → step 3 → done`

Agentic: `goal → reason → plan → execute → learn → adapt → achieve`

---

## Framework Comparison

### Major Agentic AI Frameworks (2024)

| Framework | Architecture | Best For | Adoption |
|-----------|--------------|----------|----------|
| **LangGraph** | Graph-based DAG workflows | Complex multi-step orchestration | 6.17M monthly downloads |
| **CrewAI** | Role-based "crews" | Team collaboration metaphor | 1.38M monthly downloads |
| **AutoGen** | Conversation-centric | Research and R&D | Enterprise focus |

### LangGraph

- **Strength**: Fine-grained control over workflow state and transitions
- **Architecture**: Directed acyclic graphs (DAGs) with nodes (functions) and edges (transitions)
- **Production**: Used by LinkedIn, AppFolio, and others
- **License**: MIT (open source)

> "LangGraph excels in managing structured workflows using its graph-based architecture. By treating workflows as directed acyclic graphs (DAGs), LangGraph provides fine-grained control over task dependencies and process visualization."

### CrewAI

- **Strength**: Intuitive role-based metaphor (agents as team members)
- **Architecture**: Crews (agent teams) + Flows (task orchestration)
- **Backing**: AI Fund (Andrew Ng), $18M Series A
- **License**: MIT (open source), enterprise features paid

> "CrewAI's architecture is built around the metaphor of a 'crew' of agents working as a team. A Crew is a collection of role-defined agents plus a set of tasks for them."

### Recommendation for EchoGraph

**Use LangGraph for orchestration with CrewAI-style role definitions.**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Orchestration** | LangGraph | Higher production adoption, graph-based aligns with "context graph" vision |
| **Agent Design** | CrewAI-style roles | Intuitive PM/BA/PO/Dev/QA metaphor |
| **Memory** | Graphiti + LanceDB | Built for agentic systems, temporal awareness |
| **Deployment** | Self-hosted + Cloud option | Supports open-source + hosted model |

---

## Proposed Agentic Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ECHOGRAPH AGENTIC ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ AGENT CREW (Role-Based Agents)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ PM Agent │  │ BA Agent │  │ PO Agent │  │Dev Agent │  │ QA Agent │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │             │             │             │            │
│       └─────────────┴──────┬──────┴─────────────┴─────────────┘            │
│                            │                                               │
│                            ▼                                               │
│                   ┌─────────────────┐                                      │
│                   │  ORCHESTRATOR   │  ← LangGraph state machine           │
│                   │  (Workflow DAG) │                                      │
│                   └────────┬────────┘                                      │
│                            │                                               │
└────────────────────────────┼───────────────────────────────────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────────────────┐
│ MEMORY LAYER               │                                               │
├────────────────────────────┼───────────────────────────────────────────────┤
│                            ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    KNOWLEDGE GRAPH (Graphiti/Neo4j)                  │  │
│  │  - Entity relationships (code ↔ decisions ↔ PRs ↔ people)           │  │
│  │  - Temporal awareness (what changed when)                           │  │
│  │  - Multi-hop reasoning                                              │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                            │                                               │
│  ┌─────────────────────────┴───────────────────────────────────────────┐  │
│  │                    VECTOR STORE (LanceDB)                            │  │
│  │  - Semantic search over code, docs, decisions                       │  │
│  │  - Hybrid retrieval (vector + BM25S)                                │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                            │                                               │
│  ┌─────────────────────────┴───────────────────────────────────────────┐  │
│  │                    EPISODIC MEMORY (SQLite/Postgres)                 │  │
│  │  - Conversation history                                              │  │
│  │  - Agent decisions and rationale                                     │  │
│  │  - Human feedback loops                                              │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────────────────┐
│ HUMAN-IN-THE-LOOP          │                                               │
├────────────────────────────┼───────────────────────────────────────────────┤
│                            ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  APPROVAL GATES                                                      │  │
│  │  - Initiative approval (PM Agent → Human Stakeholder)               │  │
│  │  - Feature scope approval (BA Agent → Human PO)                     │  │
│  │  - Sprint commitment (PO Agent → Human Team)                        │  │
│  │  - Code merge approval (Dev Agent → Human Lead)                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  FEEDBACK CHANNELS                                                   │  │
│  │  - Slack/Teams notifications                                        │  │
│  │  - Email digests                                                    │  │
│  │  - CLI interactive prompts                                          │  │
│  │  - Web dashboard (hosted version)                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Definitions

### PM Agent (Product Manager)

**Role**: Strategic planning, initiative creation, roadmap management

**Capabilities**:
- Analyze business requirements and market context
- Create initiatives with ROI projections
- Break initiatives into epics
- Prioritize based on business value
- Track initiative progress and success metrics

**Memory Access**:
- Knowledge Graph: Business context, stakeholder relationships, historical decisions
- Vector Store: Similar past initiatives, market research docs
- Episodic: Past stakeholder feedback, approval history

**Artifacts Created**:
- `initiatives/INI-*.md`
- `epics/EPIC-*.md`
- Roadmap updates

**Approval Gates**:
- Initiative creation → Human stakeholder approval
- Major scope changes → Human PM approval

---

### BA Agent (Business Analyst)

**Role**: Requirements analysis, feature specification, story decomposition

**Capabilities**:
- Analyze features to understand detailed requirements
- Research codebase for existing patterns
- Decompose features into user stories
- Document business rules and edge cases
- Validate requirements completeness

**Memory Access**:
- Knowledge Graph: Code relationships, existing feature patterns, API mappings
- Vector Store: Similar features, documentation, code examples
- Episodic: Past requirement clarifications, stakeholder discussions

**Artifacts Created**:
- `features/FEAT-*.md`
- `user-stories/US-*.md` (drafts)
- Business rule documentation

**Approval Gates**:
- Feature scope → Human PO approval
- Story decomposition → Human review

---

### PO Agent (Product Owner)

**Role**: Backlog management, prioritization, sprint planning, acceptance

**Capabilities**:
- Prioritize features and stories by value
- Validate stories against Definition of Ready
- Plan sprint capacity and commitment
- Accept or reject completed work
- Communicate with stakeholders

**Memory Access**:
- Knowledge Graph: Team velocity, dependency relationships, stakeholder priorities
- Vector Store: Historical sprint data, acceptance criteria patterns
- Episodic: Past sprint outcomes, feedback loops

**Artifacts Created**:
- Prioritized backlog
- Sprint plans
- Acceptance decisions

**Approval Gates**:
- Sprint commitment → Human team approval
- Feature acceptance → Human PO confirmation

---

### Dev Agent (Developer/Tech Lead)

**Role**: Technical specification, implementation, code review

**Capabilities**:
- Add technical context to stories (architecture, APIs, data models)
- Generate PRPs with step-by-step implementation
- Execute code changes following PRP
- Run tests and validation
- Create pull requests
- Review code for patterns and security

**Memory Access**:
- Knowledge Graph: Code architecture, API relationships, security patterns
- Vector Store: Code examples, documentation, similar implementations
- Episodic: Past implementation decisions, code review feedback

**Artifacts Created**:
- Technical specifications in stories
- `active/PRP-*.md`
- Code changes
- Pull requests

**Approval Gates**:
- PRP generation → Human tech lead review (optional)
- Code merge → Human code review required

---

### QA Agent (Quality Assurance)

**Role**: Test planning, quality validation, acceptance criteria

**Capabilities**:
- Add test scenarios to stories (happy path, errors, edge cases)
- Validate Definition of Ready criteria
- Create feature test plans
- Verify acceptance criteria are testable
- Identify regression risks

**Memory Access**:
- Knowledge Graph: Test coverage, bug history, regression patterns
- Vector Store: Test examples, quality documentation
- Episodic: Past QA feedback, bug resolutions

**Artifacts Created**:
- Test scenarios in stories
- Feature test plans
- QA validation reports

**Approval Gates**:
- Definition of Ready → Human QA lead confirmation (optional)

---

## Memory Layer

### Why Memory Matters for Agentic Systems

> "Traditional RAG applications lack the ability to capture complex data relationships. They struggle to perform tasks such as multihop reasoning, relational context, and understanding hierarchical data."

EchoGraph needs three types of memory:

### 1. Knowledge Graph (Semantic Memory)

**Purpose**: Store relationships between entities for multi-hop reasoning

**Technology**: Graphiti (recommended) or Neo4j

**Entities**:
- Code (files, functions, classes)
- People (developers, stakeholders)
- Artifacts (initiatives, epics, features, stories, PRPs)
- Decisions (ADRs, design choices)
- Events (commits, PRs, deployments)

**Relationships**:
```
Developer --[authored]--> Commit
Commit --[implements]--> Story
Story --[belongs_to]--> Feature
Feature --[part_of]--> Epic
Epic --[delivers]--> Initiative
Code --[changed_by]--> Commit
Decision --[affects]--> Code
```

**Why Graphiti over raw Neo4j**:
> "Graphiti represents a meaningful departure from traditional RAG methods, specifically because it was built from the ground up as a memory infrastructure for dynamic agentic systems. It offers incremental, real-time updates through its temporally aware knowledge graph."

### 2. Vector Store (Semantic Search)

**Purpose**: Fast similarity search over unstructured content

**Technology**: LanceDB (already chosen)

**Content Indexed**:
- Code chunks (functions, classes)
- Documentation (README, API docs)
- Artifacts (initiatives, features, stories, PRPs)
- Decisions (ADRs)
- Conversations (chat history with agents)

**Retrieval**:
- Hybrid search (vector similarity + BM25S keyword)
- Metadata filtering (by type, date, author)

### 3. Episodic Memory (Conversation/Decision History)

**Purpose**: Track agent decisions, human feedback, and conversation context

**Technology**: SQLite (local) / Postgres (hosted)

**Content Stored**:
- Agent reasoning traces (why decisions were made)
- Human feedback (approvals, rejections, corrections)
- Conversation history (context for follow-up queries)
- Workflow state (current position in DAG)

---

## Workflow Example

### End-to-End: Concept to Feature

```
USER: "We need password reset functionality for the mobile app"
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: Analyzes input, determines starting point                     │
│ Decision: This is a feature request, route to BA Agent                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ BA AGENT: Creates feature, researches codebase                              │
│                                                                             │
│ Actions:                                                                    │
│   1. Query Knowledge Graph: "What auth patterns exist in codebase?"        │
│   2. Query Vector Store: "Similar features implemented before?"            │
│   3. Generate: features/FEAT-042-password-reset.md                         │
│   4. Decompose into 3 user stories:                                        │
│      - US-101: Email input validation                                      │
│      - US-102: Reset token generation and email                            │
│      - US-103: Password update flow                                        │
│                                                                             │
│ Output: Feature doc + 3 story drafts                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🚦 APPROVAL GATE: Human reviews feature scope                               │
│                                                                             │
│ Notification sent to: Product Owner (Slack/Email/CLI)                      │
│ Options: [APPROVE] / [REQUEST CHANGES] / [REJECT]                          │
│                                                                             │
│ Human response: APPROVE with comment "Add rate limiting requirement"       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ APPROVED
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ BA AGENT: Incorporates feedback                                             │
│                                                                             │
│ Actions:                                                                    │
│   1. Update feature with rate limiting requirement                         │
│   2. Add US-104: Rate limiting for reset attempts                          │
│   3. Store feedback in episodic memory for learning                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV AGENT: Enriches stories with technical context                          │
│                                                                             │
│ Actions:                                                                    │
│   1. Query Knowledge Graph: "API patterns for auth endpoints?"             │
│   2. Query Vector Store: "Security best practices for password reset?"     │
│   3. Update each story with:                                               │
│      - Architecture approach                                               │
│      - API specifications                                                  │
│      - Data model changes                                                  │
│      - Security considerations                                             │
│      - Dependencies                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA AGENT: Adds test scenarios                                               │
│                                                                             │
│ Actions:                                                                    │
│   1. Query Knowledge Graph: "What test patterns exist for auth?"           │
│   2. Generate for each story:                                              │
│      - Happy path scenarios                                                │
│      - Error/negative scenarios                                            │
│      - Edge cases (expired tokens, rate limits, etc.)                      │
│      - Test data requirements                                              │
│   3. Validate Definition of Ready checklist                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PO AGENT: Prioritizes and schedules                                         │
│                                                                             │
│ Actions:                                                                    │
│   1. Query Knowledge Graph: "Current sprint capacity?"                     │
│   2. Compare against backlog items by business value                       │
│   3. Recommend: "Add to Sprint 23 (starts Monday)"                         │
│   4. Generate sprint commitment proposal                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🚦 APPROVAL GATE: Human confirms sprint commitment                          │
│                                                                             │
│ Notification sent to: Team Lead + PO                                       │
│ Options: [COMMIT TO SPRINT] / [DEFER TO NEXT SPRINT] / [NEEDS DISCUSSION]  │
│                                                                             │
│ Human response: COMMIT TO SPRINT                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ COMMITTED
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV AGENT: Generates PRP and implements (for each story)                    │
│                                                                             │
│ Actions:                                                                    │
│   1. Generate: active/PRP-101-email-validation.md                          │
│      - Step-by-step implementation plan                                    │
│      - Code patterns to follow                                             │
│      - Test strategy                                                       │
│   2. Create feature branch                                                 │
│   3. Execute implementation:                                               │
│      - Write code following PRP steps                                      │
│      - Run tests after each step                                           │
│      - Validate against acceptance criteria                                │
│   4. Create pull request with summary                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🚦 APPROVAL GATE: Human reviews code                                        │
│                                                                             │
│ Notification sent to: Tech Lead + assigned reviewer                        │
│ PR Link: https://github.com/org/repo/pull/123                              │
│ Options: [APPROVE] / [REQUEST CHANGES]                                     │
│                                                                             │
│ Human response: REQUEST CHANGES "Add input sanitization"                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ CHANGES REQUESTED
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV AGENT: Addresses feedback                                               │
│                                                                             │
│ Actions:                                                                    │
│   1. Parse feedback: "Add input sanitization"                              │
│   2. Query Vector Store: "Input sanitization patterns in codebase?"        │
│   3. Implement requested changes                                           │
│   4. Update PR                                                             │
│   5. Store feedback in episodic memory for future learning                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🚦 APPROVAL GATE: Human re-reviews code                                     │
│                                                                             │
│ Human response: APPROVE                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │ APPROVED
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: Finalizes and updates knowledge                               │
│                                                                             │
│ Actions:                                                                    │
│   1. Merge PR                                                              │
│   2. Update Knowledge Graph:                                               │
│      - New code entities and relationships                                 │
│      - Link: Story → Commit → Code                                         │
│   3. Archive PRP to completed/                                             │
│   4. Ingest new code patterns to vector store                              │
│   5. Update feature progress (1/4 stories complete)                        │
│   6. Notify stakeholders of completion                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                         [Continue with next story...]
```

---

## Human-in-the-Loop Design

### Approval Gate Types

| Gate | Trigger | Approvers | Timeout Action |
|------|---------|-----------|----------------|
| **Initiative** | New initiative created | Stakeholders | Escalate to PM |
| **Feature Scope** | Feature decomposed | Product Owner | Escalate to PM |
| **Sprint Commit** | Stories ready for sprint | Team Lead + PO | Defer to next sprint |
| **Code Review** | PR created | Tech Lead + Reviewer | Block merge |
| **Acceptance** | Story implemented | Product Owner | Escalate to PM |

### Notification Channels

| Channel | Use Case | Configuration |
|---------|----------|---------------|
| **CLI** | Developer working locally | Default for open-source |
| **Slack** | Team collaboration | Webhook integration |
| **Teams** | Enterprise teams | Webhook integration |
| **Email** | Async notifications | SMTP configuration |
| **Web Dashboard** | Hosted platform | Built-in UI |

### Feedback Loop

Human feedback is stored and used to improve agent behavior:

```
Human: "Add rate limiting requirement"
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ EPISODIC MEMORY: Store feedback                                             │
│                                                                             │
│ {                                                                           │
│   "context": "feature creation",                                           │
│   "feedback_type": "requirement_addition",                                 │
│   "original": "password reset feature",                                    │
│   "addition": "rate limiting for reset attempts",                          │
│   "agent": "BA Agent",                                                     │
│   "timestamp": "2024-12-15T10:30:00Z"                                      │
│ }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ LEARNING: Future BA Agent prompts include                                   │
│                                                                             │
│ "When creating authentication-related features, consider:                  │
│  - Rate limiting for security-sensitive operations                         │
│  - Based on past feedback from this organization"                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Open Source vs Hosted Split

### Dual Model Strategy

| Component | Open Source (Free) | Hosted (Paid) |
|-----------|-------------------|---------------|
| **Agents** | All 5 role agents | Same + fine-tuned models |
| **Orchestration** | Self-hosted LangGraph | Managed orchestration |
| **Memory** | SQLite + LanceDB + local graph | Managed Postgres + Neo4j Aura |
| **Approval Gates** | CLI-based prompts | Web dashboard + Slack/Teams |
| **Knowledge Graph** | File-based or local Neo4j | Managed graph database |
| **Limits** | Unlimited local executions | Pay per agent execution |
| **Observability** | Basic logging | Full tracing + analytics |
| **Support** | Community (GitHub) | SLA + dedicated support |

### Pricing Model (Hosted)

| Tier | Price | Includes |
|------|-------|----------|
| **Free** | $0/mo | 100 agent executions, 1 project, community support |
| **Pro** | $49/mo | 1,000 executions, 5 projects, email support |
| **Team** | $199/mo | 10,000 executions, unlimited projects, Slack integration, priority support |
| **Enterprise** | Custom | Unlimited, SSO, dedicated instance, SLA |

---

## Phased Implementation Plan

### Phase 0: Foundation (Current State)

**Status**: Partially complete

- ✅ LanceDB vector store
- ✅ Hybrid search (vector + BM25S)
- ✅ CLI scaffolding (echograph init, etc.)
- ✅ Basic embedding pipeline
- 🔲 Knowledge graph infrastructure

**Deliverable**: EchoGraph CLI with search capabilities

---

### Phase 1: Memory Layer

**Goal**: Add knowledge graph and episodic memory

**Tasks**:
1. Integrate Graphiti for knowledge graph
2. Implement entity extraction from code/docs/PRs
3. Build relationship mapping (code ↔ decisions ↔ people)
4. Add episodic memory tables to SQLite
5. Implement GraphRAG for multi-hop queries

**Deliverable**: Memory infrastructure ready for agents

---

### Phase 2: Single Agent (Dev Agent)

**Goal**: Prove agent concept with one agent

**Tasks**:
1. Implement Dev Agent using LangGraph
2. Connect to memory layer (vector + knowledge graph)
3. Implement PRP generation workflow
4. Add human approval gate for code review
5. Test end-to-end: story → PRP → code → PR

**Deliverable**: Working Dev Agent that can implement stories

---

### Phase 3: Multi-Agent Crew

**Goal**: Full product team simulation

**Tasks**:
1. Add BA Agent (feature analysis, story decomposition)
2. Add PO Agent (prioritization, sprint planning)
3. Add QA Agent (test scenarios, validation)
4. Add PM Agent (initiative creation, roadmap)
5. Implement orchestrator (workflow DAG)
6. Agent-to-agent handoffs
7. Persistent conversation memory

**Deliverable**: Complete agent crew working together

---

### Phase 4: Human-in-the-Loop

**Goal**: Production-ready approval system

**Tasks**:
1. Implement approval gate system
2. CLI notification interface
3. Slack/Teams integration
4. Email notifications
5. Feedback loops (human corrections improve agents)
6. Audit trail and explainability

**Deliverable**: Agents with human oversight ready for teams

---

### Phase 5: Hosted Platform

**Goal**: Monetizable SaaS offering

**Tasks**:
1. Multi-tenant architecture
2. Web dashboard for approvals and monitoring
3. Usage metering and billing (Stripe)
4. Enterprise SSO (SAML, OIDC)
5. Advanced observability (tracing, analytics)
6. API for integrations

**Deliverable**: Hosted EchoGraph platform

---

## Technology Recommendations

### Final Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Agent Framework** | LangGraph | Production-proven, graph-based, MIT license |
| **Agent Roles** | CrewAI-style design | Intuitive metaphor, implement on LangGraph |
| **Knowledge Graph** | Graphiti | Built for agentic systems, temporal awareness |
| **Vector Store** | LanceDB | Already chosen, file-based, no Docker |
| **Episodic Memory** | SQLite / Postgres | Simple, reliable, scales to hosted |
| **Orchestration** | LangGraph | State machines, checkpointing, human-in-loop |
| **LLM Provider** | OpenAI / Anthropic / Local | Configurable per deployment |
| **Embeddings** | Nomic Embed v1.5 | Already chosen, runs locally |
| **API Server** | FastAPI | Already chosen, async-native |
| **CLI** | Typer + Rich | Already chosen |

### Key Libraries

```toml
# pyproject.toml additions for agentic features
[project.dependencies]
langgraph = ">=0.2.0"
graphiti-core = ">=0.3.0"  # Zep's knowledge graph
langchain-core = ">=0.3.0"
langsmith = ">=0.1.0"       # Optional: observability
```

---

## Sources

### Agentic Frameworks
- [LangGraph vs CrewAI - ZenML](https://www.zenml.io/blog/langgraph-vs-crewai)
- [Top 5 LangGraph Agents in Production 2024](https://blog.langchain.com/top-5-langgraph-agents-in-production-2024/)
- [CrewAI MIT License Discussion](https://github.com/crewAIInc/crewAI/discussions/1594)
- [Open Source Agentic Frameworks - PremAI](https://blog.premai.io/open-source-agentic-frameworks-langgraph-vs-crewai-more/)
- [Technical Comparison of AutoGen, CrewAI, LangGraph](https://ai.plainenglish.io/technical-comparison-of-autogen-crewai-langgraph-and-openai-swarm-1e4e9571d725)

### n8n vs Agentic
- [n8n AI Agentic Workflows](https://blog.n8n.io/ai-agentic-workflows/)
- [n8n AI Agents 2025 Review](https://latenode.com/blog/low-code-no-code-platforms/n8n-setup-workflows-self-hosting-templates/n8n-ai-agents-2025-complete-capabilities-review-implementation-reality-check)
- [LangGraph vs n8n - ZenML](https://www.zenml.io/blog/langgraph-vs-n8n)

### Knowledge Graph & RAG
- [GraphRAG - IBM](https://www.ibm.com/think/topics/graphrag)
- [Graphiti - Knowledge Graph Memory](https://github.com/getzep/graphiti)
- [Graphiti - Neo4j Blog](https://medium.com/neo4j/graphiti-knowledge-graph-memory-for-a-post-rag-agentic-world-0fd2366ba27d)
- [GraphRAG and Agentic Architecture - Neo4j](https://neo4j.com/blog/developer/graphrag-and-agentic-architecture-with-neoconverse/)
- [Rise and Evolution of RAG in 2024](https://ragflow.io/blog/the-rise-and-evolution-of-rag-in-2024-a-year-in-review)

### Product Team Roles
- [Scrum Alliance - Product Owner Explained](https://resources.scrumalliance.org/Article/product-owner-explained)
- [IIBA - Product Owner vs Business Analyst](https://www.iiba.org/business-analysis-blogs/product-owner-vs-business-analyst/)
- [Atlassian - Epics, Stories, and Initiatives](https://www.atlassian.com/agile/project-management/epics-stories-themes)
- [Microsoft - Define Features and Epics](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics)

---

## Next Steps

1. [ ] Review this proposal with stakeholders
2. [ ] Decide on Phase 1 scope (memory layer)
3. [ ] Spike: Integrate Graphiti with existing codebase
4. [ ] Spike: Create minimal Dev Agent with LangGraph
5. [ ] Define approval gate UX for CLI
6. [ ] Create detailed PRPs for each phase

---

**This proposal is a living document. Feedback welcome!**
