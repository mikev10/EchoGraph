# User Stories

This directory contains user story drafts created as part of the Context Engineering Three Amigos workflow.

## Directory Structure

```
user-stories/
├── drafts/      # Business stories from Product Owners
└── technical/   # Technical stories (refactoring, bugs, tech debt)
```

### drafts/
Business feature stories that will eventually become Azure DevOps work items. These go through the full Three Amigos enrichment process.

### technical/
Developer-initiated stories for:
- Refactoring work
- Bug fixes
- Technical debt reduction
- Infrastructure improvements

Technical stories can use a lighter process if preferred.

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    THREE AMIGOS WORKFLOW                                         │
└─────────────────────────────────────────────────────────────────────────────────┘

/write-user-story → /enrich-story-tech → /enrich-story-qa → /three-amigos-prep
     (PO Draft)        (Dev Lead)           (QA Lead)         (Alignment)
         │                  │                   │                  │
         ▼                  ▼                   ▼                  ▼
    User Story      + Technical Context   + QA Context      Session Prep
                                                                  │
                                                                  ▼
/validate-story-ready → Create ADO → /convert-story → /generate-prp → /execute-prp
    (Validation)         (Manual)     (Tech Spec)       (Plan)        (Implement)
```

## File Naming Convention

Files are named with a date prefix for uniqueness:
```
YYYYMMDD-short-description.md
```

Examples:
- `20251129-password-reset-via-email.md`
- `20251129-refactor-auth-module.md`

## Story Metadata

Each story file includes frontmatter:

```yaml
---
created: 2025-11-29
status: draft              # draft | enriched | ready | converted
category: business         # business | technical
converted_to_ado: false
ado_id: null
sprint: null
story_points: null
three_amigos_complete: false
tech_context_added: false
qa_context_added: false
---
```

## Status Lifecycle

1. **draft** - Initial creation via `/write-user-story`
2. **enriched** - After Dev Lead and QA Lead add context
3. **ready** - Passed `/validate-story-ready` checks
4. **converted** - ADO item created, converted to INITIAL.md

## Commands

| Command | Description |
|---------|-------------|
| `/story:write-user-story <requirements>` | Create new story |
| `/story:refine-story <path>` | Refine existing story |
| `/story:enrich-story-tech <path>` | Add technical context |
| `/story:enrich-story-qa <path>` | Add QA/test context |
| `/story:three-amigos-prep <path>` | Prepare alignment session |
| `/story:validate-story-ready <path>` | Check Definition of Ready |
| `/story:convert-story` | Convert to feature request |

## User Story Format

Stories follow this structure:

```markdown
# [Story Title]

As a [specific user type]
I want [capability/feature]
so that [business value/benefit].

## Acceptance Criteria

- **Scenario 1: [Title]**

  - Given [precondition]
  - When [action]
  - Then [expected result]
  - And [additional result]

- **Scenario 2: [Title]**
  ...

## Notes

[Additional context, constraints, or dependencies]
```

## Quality Criteria (INVEST)

Good user stories are:
- **I**ndependent - Can be developed separately
- **N**egotiable - Details can be discussed
- **V**aluable - Delivers user/business value
- **E**stimable - Can be sized (1-3 days ideal)
- **S**mall - Fits in a sprint
- **T**estable - Has clear acceptance criteria

## See Also

- `PRPs/templates/USER-STORY-TEMPLATE.md` - Full template
- `docs/optional/DEFINITION_OF_READY.md` - Readiness criteria
- `docs/optional/THREE_AMIGOS_GUIDE.md` - Collaboration guide
