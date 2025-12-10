# Context Engineering Framework

A universal, reusable framework for implementing **Context Engineering** in your software projects. This system enables AI coding assistants (like Claude) to achieve **one-pass implementation success** through comprehensive upfront context, established patterns, and validated workflows.

## What is Context Engineering?

Context Engineering = Providing AI with everything it needs upfront:
- **Comprehensive documentation** (conventions, architecture, gotchas)
- **Working code examples** (not descriptions, actual working code)
- **Validation loops** (automated testing at each step)
- **Step-by-step blueprints** (PRPs with implementation guidance)

**The Insight:** Most AI failures aren't model failures - they're context failures. Give AI complete context, and it succeeds.

## Key Results

Teams using this framework achieve:
- **10x better context** than prompt engineering alone
- **70%+ first-pass success rate** on complex features
- **Minimal clarification questions** (1-2 average)
- **50-70% reduction** in feature development time
- **Consistent code quality** across all implementations

---

## Quick Start (2 minutes)

### Option 1: Using the CLI (Recommended)

```bash
# Install the CLI
pip install echograph

# Initialize Context Engineering in your project
cd your-project
echograph init

# Verify setup
echograph doctor

# Validate your context files
echograph validate
```

### Option 2: Manual Setup

```bash
# Clone this repository
git clone <this-repo-url>

# Copy to your project
cp -r ContextEngineering/.claude /path/to/your-project/
cp -r ContextEngineering/PRPs /path/to/your-project/
```

### After Setup

1. **Customize** - Edit `.claude/CLAUDE.md` with your project conventions
2. **Start using** - Run Claude Code commands:

```bash
# Load all context into Claude's memory
/prime-core

# Generate a PRP from a feature request (SPEC.md)
/generate-prp PRPs/feature-requests/your-feature-SPEC.md

# Execute the PRP
/execute-prp PRPs/active/your-feature-PRP.md
```

See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for complete setup instructions.

---

## Directory Structure

```
.claude/                   # AI context & commands
├── CLAUDE.md             # Global conventions (CUSTOMIZE)
├── PLANNING.md           # Architecture & goals (CUSTOMIZE)
├── TASK.md               # Task tracking
├── SPEC.md               # Feature request template
├── commands/             # 25 slash commands
└── tasks/                # Feature-level task files

PRPs/                      # Product Requirement Prompts
├── feature-requests/     # Your feature requests
├── templates/            # PRP templates
└── ai_docs/              # Library documentation

examples/                  # Working code patterns
├── security/             # Auth, audit logging
├── testing/              # Test patterns
└── offline/              # Offline-first patterns

docs/                      # Documentation
├── SETUP_GUIDE.md        # Setup + customization
├── WORKFLOW_GUIDE.md     # Feature development workflow
└── optional/             # Product Owner & Three Amigos guides
```

---

## Slash Commands (25 workflows)

### Core Workflows
| Command | Description |
|---------|-------------|
| `/prime-core` | Load all context into Claude's memory |
| `/generate-prp` | Generate PRP from feature request |
| `/execute-prp` | Execute PRP step-by-step with validation |
| `/validate-context` | Check completeness of context files |

### Story Management
| Command | Description |
|---------|-------------|
| `/write-user-story` | AI-assisted user story drafting |
| `/convert-story` | Convert user story to SPEC.md |
| `/refine-story` | Improve story against INVEST criteria |
| `/enrich-story-tech` | Dev Lead adds technical context |
| `/enrich-story-qa` | QA Lead adds test scenarios |

### Code Quality
| Command | Description |
|---------|-------------|
| `/review-general` | Comprehensive code review |
| `/review-staged` | Review git staged changes |
| `/debug` | Systematic debugging workflow |
| `/create-pr` | Generate PR description |

---

## Key Innovations

**1. Three-Level Task System**
- **Master TASK.md**: Epic/feature level tracking
- **Feature Task Files**: Persistent subtasks with context
- **TodoWrite**: Session-level granular tasks

**2. Validation Gates**
- Every PRP step requires passing validation
- Catches errors immediately, prevents compounding

**3. Confidence Scoring**
- Every PRP includes confidence score (X/10)
- Low scores trigger more research before implementation

**4. Examples-First Development**
- Always check `examples/` before implementing
- Ensures consistency and pattern reuse

---

## Documentation

| Guide | Description |
|-------|-------------|
| [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) | Setup and customization |
| [WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) | Feature development workflow |

### Optional Guides (for teams with POs)
| Guide | Description |
|-------|-------------|
| [PRODUCT_OWNER_GUIDE.md](docs/optional/PRODUCT_OWNER_GUIDE.md) | Product Owner integration |
| [THREE_AMIGOS_GUIDE.md](docs/optional/THREE_AMIGOS_GUIDE.md) | Three Amigos workflow |
| [DEFINITION_OF_READY.md](docs/optional/DEFINITION_OF_READY.md) | Story readiness checklist |

---

## Time Investment & ROI

### Initial Setup
| Phase | Time |
|-------|------|
| Copy template | 30 minutes |
| Customize CLAUDE.md | 1-2 hours |
| Create examples | 4-8 hours |
| **Total** | **~8-12 hours** |

### Returns
- **50-70% reduction** in feature development time
- **Payback**: After 2-3 features

---

## Usage with Claude Code

This framework is optimized for **Claude Code** (Anthropic's CLI). Commands in `.claude/commands/` are automatically discovered.

```bash
# Typical workflow
/prime-core                                          # Load context
# Create feature-SPEC.md in PRPs/feature-requests/
/generate-prp PRPs/feature-requests/feature-SPEC.md  # Generate plan
/execute-prp PRPs/active/feature-PRP.md              # Implement
/create-pr                                           # Create PR
```

---

## External Resources

- [Cole Medin's Context Engineering](https://github.com/coleam00/context-engineering-intro)
- [Wirasm PRPs](https://github.com/Wirasm/PRPs-agentic-eng)

---

**Ready to get started?** See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
