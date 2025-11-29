# PRPs Directory

This directory contains all planning and requirements artifacts for the Context Engineering workflow.

## Directory Structure

```
PRPs/
├── active/              # PRPs currently being implemented
├── completed/           # Archived PRPs (finished implementations)
├── examples/            # Example PRPs for reference
├── feature-requests/    # INITIAL.md files (feature specifications)
├── templates/           # Templates for PRPs and user stories
├── ai_docs/             # Library-specific documentation for AI context
├── user-stories/        # User story drafts and technical stories
│   ├── drafts/          # Business stories awaiting ADO creation
│   └── technical/       # Technical stories (refactoring, bugs, debt)
└── scripts/             # Utility scripts for task parsing/validation
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    CONTEXT ENGINEERING WORKFLOW                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

User Story → Feature Request → PRP → Implementation → Archive

1. /write-user-story     → user-stories/{drafts,technical}/
2. Three Amigos Process  → Enrichment & Validation
3. /convert-story        → feature-requests/INITIAL.md
4. /generate-prp         → active/*.md
5. /execute-prp          → Implementation
6. /archive-prp          → completed/*.md
```

## Key Concepts

### User Stories (`user-stories/`)
Business or technical requirements written in user story format. These are drafted locally before being added to Azure DevOps.

- **drafts/**: Business stories from Product Owners
- **technical/**: Developer-initiated stories (refactoring, tech debt, bugs)

### Feature Requests (`feature-requests/`)
Technical specifications derived from user stories. Contains `INITIAL.md` files with:
- Acceptance criteria
- API endpoints
- Code patterns to follow
- Security considerations

### PRPs (`active/`, `completed/`)
Product Requirements Plans - detailed implementation guides with:
- Step-by-step tasks
- Validation commands
- File changes required
- Testing strategy

### AI Documentation (`ai_docs/`)
Library-specific documentation ingested for AI context. Used by Claude to understand project dependencies and patterns.

## Related Commands

| Command | Description |
|---------|-------------|
| `/story:write-user-story` | Create user story from requirements |
| `/story:enrich-story-tech` | Add technical context (Dev Lead) |
| `/story:enrich-story-qa` | Add QA context (QA Lead) |
| `/story:validate-story-ready` | Check Definition of Ready |
| `/story:convert-story` | Convert story to INITIAL.md |
| `/workflow:generate-prp` | Generate PRP from feature request |
| `/workflow:execute-prp` | Implement PRP step-by-step |
| `/workflow:archive-prp` | Archive completed PRP |

## See Also

- `.claude/PLANNING.md` - Architecture and goals
- `.claude/TASK.md` - Current task tracking
- `.claude/tasks/README.md` - Task system documentation
