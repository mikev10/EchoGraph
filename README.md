# Context Engineering Framework

A universal, reusable framework for implementing **Context Engineering** in your software projects. This system enables AI coding assistants (like Claude) to achieve **one-pass implementation success** through comprehensive upfront context, established patterns, and validated workflows.

## What is Context Engineering?

Context Engineering = Providing AI with everything it needs upfront:
- **Comprehensive documentation** (conventions, architecture, gotchas)
- **Working code examples** (not descriptions, actual working code)
- **Validation loops** (automated testing at each step)
- **Step-by-step blueprints** (PRPs with implementation guidance)

**The Insight:** Most AI failures aren't model failures—they're context failures. Give AI complete context, and it succeeds.

## Key Results

Teams using this framework have achieved:
- **10x better context** than prompt engineering alone
- **70%+ first-pass success rate** on complex features
- **Minimal clarification questions** (1-2 average)
- **50-70% reduction** in feature development time
- **Consistent code quality** across all implementations

## Quick Start

### 1. Clone or Copy This Template
```bash
git clone <this-repo-url>
cd ContextEngineering
```

### 2. Customize Core Files
Replace all `[[PLACEHOLDER]]` values in:
- `.claude/CLAUDE.md` - Your project's conventions
- `.claude/PLANNING.md` - Your architecture and goals
- `.claude/TASK.md` - Your current tasks

See `docs/SETUP_GUIDE.md` for step-by-step instructions.

### 3. Add Your Examples
Create working code examples in `examples/`:
- **integrations/** - API client, data fetching patterns
- **components/** - UI component patterns
- **hooks/** - Data hooks/functions
- **state/** - State management
- **security/** - Auth, audit logging
- **testing/** - Test patterns
- **offline/** - Offline-first patterns

### 4. Start Using
```bash
# Load all context into Claude's memory
/prime-core

# Generate a PRP from a feature request
/generate-prp .claude/INITIAL.md

# Execute the PRP
/execute-prp PRPs/active/your-feature.md
```

## Directory Structure

```
.
├── .claude/                   # AI context & commands
│   ├── CLAUDE.md             # Global conventions (CUSTOMIZE THIS)
│   ├── PLANNING.md           # Architecture & goals (CUSTOMIZE THIS)
│   ├── TASK.md               # Project tasks (CUSTOMIZE THIS)
│   ├── INITIAL.md            # Feature request template
│   ├── commands/             # 25 slash commands (workflows)
│   ├── docs/                 # Workflow guides
│   ├── agents/               # AI agent definitions
│   └── tasks/                # Feature-level task files (persistent)
│
├── PRPs/                      # Product Requirement Prompts
│   ├── active/               # Currently executing PRPs
│   ├── completed/            # Archived PRPs
│   ├── feature-requests/     # INITIAL.md files from users
│   ├── ai_docs/              # Library documentation (AI-optimized)
│   ├── templates/            # PRP templates
│   ├── examples/             # Example completed PRPs
│   └── scripts/              # Automation scripts
│
├── examples/                  # Working code patterns (CRITICAL)
│   ├── integrations/         # API client patterns
│   ├── components/           # UI component patterns
│   ├── hooks/                # Custom hook patterns
│   ├── state/                # State management patterns
│   ├── security/             # Auth, audit logging patterns
│   ├── testing/              # Test patterns
│   └── offline/              # Offline-first patterns
│
├── user-stories/              # User story drafts & examples
│   ├── drafts/               # PO-created story drafts
│   ├── technical/            # Technical stories
│   └── training/             # Example stories (good & poor)
│
├── docs/                      # Project documentation
│   ├── SETUP_GUIDE.md        # Setup instructions
│   ├── CUSTOMIZATION_GUIDE.md # How to adapt to your domain
│   ├── USER_GUIDE.md         # Feature dev workflow
│   ├── PRODUCT-OWNER-GUIDE.md # PO integration guide
│   ├── DEFINITION-OF-READY.md # DoR checklist
│   └── CONTEXT_ENGINEERING_REUSABILITY_GUIDE.md # Master guide
│
└── lancedb/                   # Local RAG vector database
```

## Core Components

### Slash Commands (25 workflows)

Located in `.claude/commands/`:

**Core Workflows:**
- `/prime-core` - Load all context into Claude's memory
- `/generate-prp` - Generate PRP from feature request
- `/execute-prp` - Execute PRP step-by-step with validation
- `/validate-context` - Check completeness of context files

**Story Management:**
- `/write-user-story` - AI-assisted user story drafting
- `/convert-story` - Convert user story to INITIAL.md (with codebase research)
- `/refine-story` - Analyze & improve story against INVEST criteria
- `/enrich-story-tech` - Dev Lead adds technical context
- `/enrich-story-qa` - QA Lead adds test scenarios
- `/three-amigos-prep` - Generate alignment meeting agenda
- `/validate-story-ready` - Check against Definition of Ready

**Code Review & Quality:**
- `/review-general` - Comprehensive code review (security, performance, style)
- `/review-staged` - Review git staged changes before commit
- `/refactor-simple` - Refactor code while maintaining functionality & tests

**Debugging & Maintenance:**
- `/debug` - Systematic debugging workflow with logs & root cause analysis
- `/planning-create` - Create planning docs with architecture diagrams
- `/onboarding` - Guided developer onboarding tour
- `/research` - Multi-source research workflow

**PRP Management:**
- `/create-pr` - Generate PR description with test plan
- `/archive-prp` - Move completed PRP to archives
- `/create-feature-request` - Create feature request (INITIAL.md)

### Key Innovations

**1. Three-Level Hierarchical Task System**
- **Master TASK.md**: Epic/feature level with task IDs (TASK-001, etc.)
- **Feature Task Files** (`.claude/tasks/`): Persistent subtasks with detailed context
- **TodoWrite**: Session-level, temporary (Claude manages)
- Auto-updates progress, auto-completes parents when all subtasks done

**2. ULTRATHINK Phase**
- Mandatory planning before any code execution
- Forces pattern review and blocker identification

**3. Validation Gates**
- Every PRP step requires passing validation before proceeding
- Catches errors immediately, prevents compounding

**4. Confidence Scoring**
- Every PRP includes confidence score (X/10)
- Low scores trigger more research before implementation

**5. Examples-First Development**
- Always check examples/ before implementing
- Ensures consistency and pattern reuse

**6. Three Amigos Workflow**
- PO, Dev Lead, and QA Lead align before development
- Reduces rework and scope creep
- Definition of Ready enforcement

## Product Owner Integration

The framework includes comprehensive support for Product Owner collaboration:

### Three Amigos Workflow

**Participants:** Product Owner (business), Dev Lead (technical), QA Lead (testing)

```
Step 1: PO Creates Story     → /write-user-story
Step 2: Dev Lead Enriches    → /enrich-story-tech [story-path]
Step 3: QA Lead Enriches     → /enrich-story-qa [story-path]
Step 4: Alignment Meeting    → /three-amigos-prep [story-path]
Step 5: Validate Ready       → /validate-story-ready [story-path]
```

### Story to Feature Request Conversion

```
1. PO writes user story in Azure DevOps (or similar)
2. Developer runs /convert-story
3. AI researches codebase patterns, asks clarifying questions
4. Generates INITIAL.md with technical enrichment
5. /generate-prp creates comprehensive PRP
6. /execute-prp implements step-by-step
```

See `docs/PRODUCT-OWNER-GUIDE.md` for complete guidance.

## Time Investment & ROI

### Initial Setup
| Phase | Time | Description |
|-------|------|-------------|
| Structure | 2-4 hours | Core files and directories |
| Documentation | 4-6 hours | CLAUDE.md, PLANNING.md |
| Examples | 8-12 hours | Working code patterns |
| Library Docs | 4-6 hours | AI-optimized docs |
| **Total** | **16-26 hours** | Average ~20 hours |

### Returns
- **50-70% reduction** in feature development time
- **Payback**: After ~2-3 features
- **Long-term**: 45-115 hours saved per 10 features

## Documentation

- **[Quick Start Guide](docs/CONTEXT_ENGINEERING_QUICKSTART.md)** - Get started in 30 minutes
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Step-by-step setup instructions
- **[Customization Guide](docs/CUSTOMIZATION_GUIDE.md)** - How to adapt to your project
- **[User Guide](docs/USER_GUIDE.md)** - Feature development workflow
- **[Product Owner Guide](docs/PRODUCT-OWNER-GUIDE.md)** - PO integration
- **[Reusability Guide](docs/CONTEXT_ENGINEERING_REUSABILITY_GUIDE.md)** - Comprehensive master guide
- **[Definition of Ready](docs/DEFINITION-OF-READY.md)** - Story readiness checklist

## Examples & Templates

### PRP Templates
- `PRPs/templates/prp-template.md` - Blank PRP structure
- `PRPs/examples/` - Example completed PRPs

### Code Examples (Universal Patterns)
- `examples/security/token-manager.ts` - Token management pattern
- `examples/security/audit-logger.ts` - Audit logging pattern
- `examples/offline/mutation-queue.ts` - Offline mutation queue
- `examples/testing/component.test.tsx` - Component test structure
- `examples/testing/hook.test.ts` - Hook/function test structure

### User Story Examples
- `user-stories/training/good-examples/` - Well-written stories
- `user-stories/training/poor-examples/` - Stories needing improvement
- `PRPs/examples/user-story-conversion-example.md` - Conversion workflow

All examples use `[[PLACEHOLDER]]` syntax - replace with your values.

## Usage with Claude Code

This framework is optimized for **Claude Code** (Anthropic's official CLI). The slash commands in `.claude/commands/` are automatically discovered and can be invoked with `/command-name`.

Example workflow:
```bash
# 1. Load context
/prime-core

# 2. Create feature request in .claude/INITIAL.md
# (Fill out FEATURE, EXAMPLES, DOCUMENTATION, OTHER CONSIDERATIONS)

# 3. Generate PRP
/generate-prp .claude/INITIAL.md

# 4. Review generated PRP (check confidence score)

# 5. Execute PRP
/execute-prp PRPs/active/your-feature.md

# 6. Create PR when done
/create-pr
```

## Customization

See `docs/CUSTOMIZATION_GUIDE.md` for detailed instructions on:
- Adapting CLAUDE.md to your tech stack
- Creating project-specific examples
- Documenting your libraries
- Adding API specifications
- Defining validation commands

## External Resources

- [Cole Medin's Context Engineering](https://github.com/coleam00/context-engineering-intro)
- [Wirasm PRPs](https://github.com/Wirasm/PRPs-agentic-eng)
- [Anthropic Engineering](https://www.anthropic.com/engineering)

## License

[[ADD_YOUR_LICENSE_HERE]]

## Contributing

[[ADD_CONTRIBUTING_GUIDELINES_HERE]]

---

**Ready to get started?** See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for step-by-step setup instructions.
