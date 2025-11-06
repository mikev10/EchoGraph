# Context Engineering Template

A universal, reusable template for implementing **Context Engineering** in your software projects. This system enables AI coding assistants (like Claude) to achieve **one-pass implementation success** through comprehensive upfront context, established patterns, and validated workflows.

## What is Context Engineering?

Context Engineering = Providing AI with everything it needs upfront:
- **Comprehensive documentation** (conventions, architecture, gotchas)
- **Working code examples** (not descriptions, actual working code)
- **Validation loops** (automated testing at each step)
- **Step-by-step blueprints** (PRPs with implementation guidance)

**The Insight:** Most AI failures aren't model failures—they're context failures. Give AI complete context, and it succeeds.

## Key Results

Based on the EZMobile implementation (this template's origin):
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
- **hooks/** - Data hooks/functions
- **state/** - State management
- **security/** - Auth, audit logging
- **testing/** - Test patterns

### 4. Start Using
```bash
# Load all context into Claude's memory
/prime-core

# Generate a PRP from a feature request
/generate-prp .claude/INITIAL.md

# Execute the PRP
/execute-prp PRPs/your-feature.md
```

## Directory Structure

```
.
├── .claude/                   # AI context & commands
│   ├── CLAUDE.md             # Global conventions (CUSTOMIZE THIS)
│   ├── PLANNING.md           # Architecture & goals (CUSTOMIZE THIS)
│   ├── TASK.md               # Project tasks (CUSTOMIZE THIS)
│   ├── INITIAL.md            # Feature request template
│   └── commands/             # 12 slash commands (workflows)
│
├── PRPs/                      # Product Requirement Prompts
│   ├── ai_docs/              # Library documentation (AI-optimized)
│   ├── templates/            # PRP templates
│   ├── scripts/              # Automation scripts
│   └── completed/            # Archived PRPs
│
├── examples/                  # Working code patterns (CRITICAL)
│   ├── security/             # Auth, audit logging patterns
│   ├── offline/              # Offline mutation queue
│   └── testing/              # Test patterns
│
└── docs/                      # Project documentation
    ├── SETUP_GUIDE.md        # Setup instructions
    ├── CUSTOMIZATION_GUIDE.md # How to adapt to your domain
    └── CONTEXT_ENGINEERING_REUSABILITY_GUIDE.md # Master guide
```

## Core Components

### Slash Commands (12 workflows)
Located in `.claude/commands/`:
- `/prime-core` - Load all context into Claude's memory
- `/generate-prp` - Generate PRP from feature request
- `/execute-prp` - Execute PRP step-by-step with validation
- `/validate-context` - Check completeness of context files
- `/review-general` - Comprehensive code review
- `/review-staged` - Review git staged changes
- `/create-pr` - Generate PR description
- `/debug` - Systematic debugging workflow
- And more...

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

## Time Investment & ROI

### Initial Setup
- Phase 1 (Structure): 2-4 hours
- Phase 2 (Documentation): 4-6 hours
- Phase 3 (Examples): 8-12 hours
- Phase 4 (Library Docs): 4-6 hours
- **Total: 16-26 hours** (average 20 hours)

### Returns
- **50-70% reduction** in feature development time
- **Payback**: After ~2-3 features
- **Long-term**: 45-115 hours saved per 10 features

## Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Step-by-step setup instructions
- **[Customization Guide](docs/CUSTOMIZATION_GUIDE.md)** - How to adapt to your project
- **[Reusability Guide](docs/CONTEXT_ENGINEERING_REUSABILITY_GUIDE.md)** - Comprehensive 47KB guide

## Examples & Templates

### PRP Templates
- `PRPs/templates/prp-template.md` - Blank PRP structure
- `PRPs/templates/prp-example.md` - Example filled PRP

### Code Examples (Universal Patterns Only)
- `examples/security/token-manager.ts` - Token management pattern
- `examples/security/audit-logger.ts` - Audit logging pattern
- `examples/offline/mutation-queue.ts` - Offline mutation queue
- `examples/testing/component.test.tsx` - Component test structure
- `examples/testing/hook.test.ts` - Hook/function test structure

All examples use `[[PLACEHOLDER]]` syntax - replace with your values.

**Note:** Framework-specific patterns (API clients, data fetching, state management, UI components) should be created based on YOUR tech stack. See `docs/CUSTOMIZATION_GUIDE.md` for guidance.

## Usage with Claude Code

This template is optimized for **Claude Code** (Anthropic's official CLI). The slash commands in `.claude/commands/` are automatically discovered and can be invoked with `/command-name`.

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
/execute-prp PRPs/your-feature.md

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

## Support & Resources

- **Original Implementation**: EZMobile project (reference implementation)
- **External Resources**:
  - [Cole Medin's Context Engineering](https://github.com/coleam00/context-engineering-intro)
  - [Wirasm PRPs](https://github.com/Wirasm/PRPs-agentic-eng)
  - [Anthropic Engineering](https://www.anthropic.com/engineering)

## License

[[ADD_YOUR_LICENSE_HERE]]

## Contributing

[[ADD_CONTRIBUTING_GUIDELINES_HERE]]

---

**Ready to get started?** See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for step-by-step setup instructions.
