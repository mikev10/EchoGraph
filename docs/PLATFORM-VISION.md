# Platform Vision & Technical Roadmap

> Transforming how product and development teams build software through AI-native workflows.

## The Problem We're Solving

**Today's Workflow (Disconnected, Slow):**
```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│   PO    │───►│  Team   │───►│  Plan   │───►│  Code   │
│ writes  │    │estimates│    │ sprint  │    │ (hope   │
│ story   │    │ (guess) │    │ (weeks) │    │ it's    │
│         │    │         │    │         │    │ right)  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     ❌ No AI context flows through
     ❌ Manual handoffs lose information
     ❌ Slow iteration cycles
     ❌ Tribal knowledge not captured
```

**Our Vision (Connected, AI-Native):**
```
┌──────────────────────────────────────────────────────────┐
│                    THE PLATFORM                           │
├──────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌────────┐│
│  │   PO    │───►│   AI    │───►│   AI    │───►│  AI    ││
│  │ writes  │    │enriches │    │ plans   │    │executes││
│  │ intent  │    │+ sizes  │    │ + PRPs  │    │ code   ││
│  └─────────┘    └─────────┘    └─────────┘    └────────┘│
│       ▲              │              │              │     │
│       └──────────────┴──────────────┴──────────────┘     │
│              ✅ Context flows through EVERYTHING          │
│              ✅ AI assists at every stage                 │
│              ✅ Hours instead of weeks                    │
│              ✅ Knowledge captured and reusable           │
└──────────────────────────────────────────────────────────┘
```

## Core Principles

1. **Context is King** - Information flows from initial idea through to deployed code
2. **Human-in-the-Loop** - AI assists, humans approve at key gates
3. **Open Core** - CLI is open source, platform adds enterprise value
4. **Language Agnostic** - Works with any tech stack (C#, Angular, React Native, etc.)
5. **Progressive Enhancement** - Teams can adopt incrementally

---

## Architecture Overview

### Two-Tier System

```
┌─────────────────────────────────────────────────────────────┐
│                     OPEN SOURCE (CLI)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   [name] CLI                                                 │
│   ├── init          # Scaffold .claude/ into any project    │
│   ├── update        # Pull framework updates                │
│   ├── validate      # Check configuration health            │
│   ├── story         # AI-assisted story writing             │
│   ├── plan          # Generate PRPs                         │
│   ├── build         # Execute with AI                       │
│   └── doctor        # Diagnose common issues                │
│                                                              │
│   Framework Files (copied to projects)                       │
│   ├── .claude/ templates                                    │
│   ├── Slash commands                                        │
│   ├── PRP system                                            │
│   └── Documentation                                          │
│                                                              │
│   ⚡ Works standalone - no platform required                 │
│   ⚡ Claude Code does the heavy lifting                      │
│   ⚡ No LangChain/LangGraph needed at this layer            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                    (optional connection)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   WEB PLATFORM (Paid/Enterprise)             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Product Owner Portal                                       │
│   ├── Write stories with AI assistance                      │
│   ├── See estimates instantly                               │
│   ├── Track from idea → deployed                            │
│   └── Approve/reject at gates                               │
│                                                              │
│   Developer Portal                                           │
│   ├── PRPs auto-generated from stories                      │
│   ├── AI-assisted implementation                            │
│   ├── Context from entire project history                   │
│   └── Code review assistance                                │
│                                                              │
│   Team Dashboard                                             │
│   ├── Velocity metrics (AI vs traditional)                  │
│   ├── Quality tracking                                      │
│   ├── Knowledge base of completed features                  │
│   └── Audit logging                                         │
│                                                              │
│   ⚡ LangGraph powers the workflow orchestration            │
│   ⚡ Multi-agent coordination                               │
│   ⚡ Human-in-the-loop approval gates                       │
│   ⚡ Enterprise SSO, audit, compliance                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Decisions

### CLI Layer

| Component | Technology | Rationale |
|-----------|------------|-----------|
| CLI Framework | Node.js (Commander/Oclif) | Cross-platform, familiar to devs |
| AI Engine | Claude Code (Anthropic) | Production-grade, handles complexity |
| Configuration | JSON + Markdown files | Simple, version-controllable |
| Templating | Handlebars or EJS | Variable substitution in templates |

**Why NOT LangChain/LangGraph for CLI:**
- CLI just scaffolds files - no orchestration needed
- Claude Code handles all AI complexity
- Research shows CLAUDE.md guidance outperforms tool orchestration
- Adding frameworks = unnecessary complexity

### Platform Layer

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Workflow Engine | **LangGraph** | Multi-stage, human-in-the-loop, state management |
| Observability | LangSmith | Debugging, tracing, evaluation |
| Backend | Python (FastAPI) or Node.js | LangGraph native support |
| Database | PostgreSQL | State persistence, audit logs |
| Auth | SSO (SAML/OIDC) | Enterprise requirement |

**Why LangGraph for Platform:**

| Platform Need | LangGraph Feature |
|---------------|-------------------|
| Multi-stage workflow (story → PRP → code) | Graph-based state machines |
| Human approval gates between stages | Human-in-the-loop nodes |
| Context flowing through everything | Persistent state management |
| Different AI agents per stage | Multi-agent coordination |
| Production retry/error handling | Built-in fault tolerance |
| Debugging why a PRP went wrong | State versioning + rollback |
| Tracking the full journey | LangSmith observability |

### Platform Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   LANGGRAPH WORKFLOW ENGINE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌────────┐ │
│  │ Story   │────►│ Enrich  │────►│  PRP    │────►│ Code   │ │
│  │ Writer  │     │ Agent   │     │ Agent   │     │ Exec   │ │
│  │ Agent   │     │         │     │         │     │ Agent  │ │
│  └─────────┘     └─────────┘     └─────────┘     └────────┘ │
│       │               │               │               │      │
│       ▼               ▼               ▼               ▼      │
│  [Human Node]   [Human Node]   [Human Node]    [Human Node] │
│   PO Approve    Team Review    Dev Approve     Code Review  │
│       │               │               │               │      │
│       └───────────────┴───────────────┴───────────────┘      │
│                    (reject = loop back)                      │
│                                                              │
│  Persistent State Across Journey:                            │
│  {                                                           │
│    story: { ... },                                          │
│    enrichment: { ... },                                     │
│    prp: { ... },                                            │
│    code: { ... },                                           │
│    approvals: [ ... ],                                      │
│    context: { codebase, patterns, history }                 │
│  }                                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Phased Roadmap

### Phase 1: CLI + Local Development (No LangGraph)

**Goal:** Prove value with open source CLI that teams can use today.

**Deliverables:**
- [ ] CLI package published to npm
- [ ] `init` command - scaffold framework into any project
- [ ] `update` command - pull framework updates
- [ ] `validate` command - check configuration health
- [ ] Presets for common stacks (Angular, .NET, React Native, Node.js)
- [ ] Documentation and examples

**User Journey:**
```bash
# Developer adds framework to existing project
cd my-angular-project
npx [name] init

? Project name: EZ Booking App
? Tech stack: Angular
? Create example PRP? Yes

✅ Framework installed!

# They use Claude Code as normal
claude

You: /generate-prp
Claude: [Uses the framework to generate PRP]
```

**Tech Stack:**
- Node.js CLI
- File templating (Handlebars)
- Claude Code (user's own installation)

**Success Metrics:**
- 10+ internal projects using framework
- Measurable reduction in story-to-code time
- Developer satisfaction feedback

---

### Phase 2: Platform MVP (Evaluate LangGraph)

**Goal:** Web UI for Product Owners, simple linear workflow.

**Deliverables:**
- [ ] PO Portal - write stories with AI assistance
- [ ] Story → PRP conversion via web UI
- [ ] Basic approval workflow
- [ ] Integration with Azure DevOps / Jira
- [ ] Team dashboard with basic metrics

**Architecture Decision Point:**
At this phase, evaluate whether custom code is becoming unwieldy:
- If workflows are simple/linear → custom orchestration may suffice
- If complexity grows (branching, retries, state) → introduce LangGraph

**User Journey:**
```
1. PO logs into web portal
2. Writes user story with AI assistance
3. AI suggests acceptance criteria, estimates size
4. PO approves → story sent to dev team
5. Developer sees story, clicks "Generate PRP"
6. AI generates PRP with codebase context
7. Developer approves → begins implementation
```

**Tech Stack:**
- Frontend: React or Next.js
- Backend: Python (FastAPI) or Node.js
- Database: PostgreSQL
- Auth: Basic SSO
- AI: Claude API (direct calls or early LangGraph)

**Success Metrics:**
- PO adoption rate
- Time from story → PRP
- Quality of generated PRPs

---

### Phase 3: Full Platform (LangGraph Recommended)

**Goal:** Enterprise-grade platform with full workflow orchestration.

**Deliverables:**
- [ ] Complete LangGraph workflow engine
- [ ] Multi-agent system (Story, Enrich, PRP, Code agents)
- [ ] Human-in-the-loop approval at every stage
- [ ] State persistence and rollback
- [ ] LangSmith integration for observability
- [ ] Advanced analytics and reporting
- [ ] Enterprise features (SSO, audit logs, compliance)
- [ ] Self-hosted option (Docker/Kubernetes)

**Why LangGraph is Essential Here:**
```
Without LangGraph (Custom Code):          With LangGraph:
─────────────────────────────────         ─────────────────────────
❌ Custom state management                 ✅ Built-in state machines
❌ Custom retry logic                      ✅ Fault tolerance included
❌ Custom approval flows                   ✅ Human-in-the-loop nodes
❌ Custom observability                    ✅ LangSmith integration
❌ Months of infrastructure work           ✅ Focus on business logic
```

**User Journey:**
```
1. PO writes intent in natural language
2. Story Agent drafts user story
3. PO reviews → approves/requests changes (human gate)
4. Enrich Agent adds technical context, estimates
5. Team reviews → approves/discusses (human gate)
6. PRP Agent generates implementation plan
7. Developer reviews → approves/modifies (human gate)
8. Code Agent executes PRP step-by-step
9. Code review → approves/requests changes (human gate)
10. Deployment (with appropriate gates)

All state persisted. Full audit trail. Rollback possible.
```

**Tech Stack:**
- Workflow: LangGraph
- Observability: LangSmith
- Backend: Python (FastAPI)
- Frontend: React/Next.js
- Database: PostgreSQL
- Infrastructure: Docker, Kubernetes
- Auth: Enterprise SSO (SAML, OIDC)

**Success Metrics:**
- End-to-end cycle time (story → production)
- Quality metrics (bugs, rework)
- Team velocity improvement
- Enterprise customer adoption

---

## Business Model

```
┌─────────────────────────────────────────────────────────────┐
│                      OPEN SOURCE                             │
│                         (Free)                               │
├─────────────────────────────────────────────────────────────┤
│  CLI Tool                                                    │
│  ├── Full framework functionality                           │
│  ├── All slash commands                                     │
│  ├── PRP system                                             │
│  ├── Local RAG (optional)                                   │
│  └── Community support                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    TEAM PLAN ($X/user/mo)                    │
├─────────────────────────────────────────────────────────────┤
│  Everything in Open Source, plus:                            │
│  ├── Web platform access                                    │
│  ├── PO Portal                                              │
│  ├── Team dashboard                                         │
│  ├── Basic integrations (ADO, Jira)                         │
│  └── Email support                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 ENTERPRISE (Custom pricing)                  │
├─────────────────────────────────────────────────────────────┤
│  Everything in Team, plus:                                   │
│  ├── Self-hosted option                                     │
│  ├── SSO (SAML, OIDC)                                       │
│  ├── Audit logging                                          │
│  ├── Advanced analytics                                     │
│  ├── Custom integrations                                    │
│  ├── SLA guarantees                                         │
│  └── Dedicated support                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

### Immediate (This Week)
1. [ ] Finalize project name and secure domain
2. [ ] Create GitHub repository (public or private initially)
3. [ ] Scaffold CLI package structure
4. [ ] Implement `init` command with basic templating

### Short-term (Next 2-4 Weeks)
1. [ ] Complete CLI with all core commands
2. [ ] Add presets for EZFacility tech stacks
3. [ ] Internal rollout to 2-3 pilot teams
4. [ ] Gather feedback and iterate

### Medium-term (1-3 Months)
1. [ ] Begin platform backend design
2. [ ] Prototype LangGraph workflows
3. [ ] Design PO portal UX
4. [ ] Evaluate hosting options

---

## Naming Candidates

> To be finalized

**Top Contenders:**
- Forge (if domain available via variation)
- Foundry
- Anvil
- [Other candidates from brainstorming]

**Domain Options to Check:**
- [name].dev
- [name].io
- get[name].dev
- use[name].dev
- [name]hq.dev

---

## References

- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- LangSmith: https://smith.langchain.com/
- Claude Code: https://claude.ai/claude-code
- Context Engineering Framework: (this repository)

---

*Last Updated: 2025-01-25*
*Document Version: 1.0*
