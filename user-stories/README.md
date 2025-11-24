# User Stories Directory

This directory contains user stories in various stages of the Context Engineering workflow.

## Directory Structure

### `/drafts/`
Product Owner-drafted stories before Azure DevOps creation.

**Workflow:**
1. PO runs `/write-user-story` with requirements
2. AI asks clarifying questions and generates structured story
3. Story saved here for review and refinement
4. PO creates ADO work item manually (copy content)
5. Developer uses `/convert-story [ADO-ID]` when ready to implement

**When to use:**
- Drafting complex features that need careful planning
- Learning to write better user stories
- Collaborating on story structure offline
- Need AI assistance with acceptance criteria
- Planning sessions before ADO work item creation

### `/technical/`
Developer-written stories for technical work (refactoring, bugs, tech debt).

**Workflow:**
1. Developer identifies technical need (refactoring, bug fix, tech debt)
2. Developer runs `/write-user-story` to structure it properly
3. Story saved here for documentation
4. Developer runs `/convert-story` to generate INITIAL.md
5. Proceeds with standard PRP workflow (`/generate-prp`, `/execute-prp`)

**When to use:**
- Technical refactoring without PO involvement
- Bug fixes that need proper structure
- Technical debt reduction
- Infrastructure improvements
- Developer-initiated improvements

### `/training/`
Example stories for learning and reference.

**Contents:**
- Perfect examples of well-written stories
- Before/after examples showing improvements
- Common patterns and anti-patterns
- Technical story examples

**Usage:**
- Reference when writing new stories
- Training new POs or developers
- Understanding story quality standards
- Learning Given/When/Then format

## Key Workflows

### Workflow 1: PO Drafting (Pre-ADO)
```
Requirements → /write-user-story → Review → Create ADO → /convert-story → PRP
```

**Steps:**
1. PO has feature requirements
2. Run: `/write-user-story "Users need to reset their password..."`
3. AI asks clarifying questions
4. AI generates structured story in `/drafts/`
5. PO reviews and refines
6. PO creates ADO work item (manual)
7. Developer runs `/convert-story [ADO-ID]` to generate INITIAL.md

### Workflow 2: Story Refinement
```
Poor ADO Story → /refine-story → Improved Story → /convert-story → PRP
```

**Steps:**
1. Developer receives poorly-written ADO story
2. Run: `/refine-story [ADO-ID]`
3. AI analyzes and shows improvements
4. Developer uses improved version for `/convert-story`
5. Proceeds with PRP workflow

### Workflow 3: Technical Story
```
Technical Need → /write-user-story → /convert-story → PRP
```

**Steps:**
1. Developer identifies technical work needed
2. Run: `/write-user-story "Refactor auth module for testability"`
3. AI generates technical story in `/technical/`
4. Developer runs `/convert-story` with generated story
5. Proceeds with PRP workflow

## Important Notes

- ✅ Stories in this directory are **NOT** automatically synced to Azure DevOps
- ✅ Use `/convert-story` to convert ADO stories to INITIAL.md (technical specifications)
- ✅ Use `/write-user-story` to draft stories before ADO (optional but recommended)
- ✅ Use `/refine-story` to improve poorly-written stories
- ❌ Do NOT skip ADO work item creation (this is drafting, not replacement)

## File Format

Stories in this directory use this metadata format:

```markdown
---
created: 2025-11-24
status: draft|ready|converted
category: business|technical
converted_to_ado: false
ado_id: null
sprint: null
story_points: null
---

### Title
[Story title]

### User Story
As a [user type]
I want [capability]
So that [benefit]

### Acceptance Criteria
- **Scenario 1: [Title]**
  - Given [context]
  - When [action]
  - Then [outcome]

[Additional scenarios...]

### Additional Notes
[Dependencies, questions, future considerations]

---

## Original Requirements
[Context from original request - for reference]
```

## Commands Reference

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/write-user-story` | Draft new story from requirements | Requirements text | Story in `/drafts/` or `/technical/` |
| `/refine-story` | Improve existing story | ADO-ID or story text | Comparison + improved version |
| `/convert-story` | Convert ADO story to INITIAL.md | ADO-ID | INITIAL.md in `PRPs/feature-requests/` |

## Quality Standards

All stories in this directory should meet these criteria:

**INVEST Criteria:**
- ✅ **Independent**: Can be developed without waiting for other stories
- ✅ **Negotiable**: Requirements clear but implementation flexible
- ✅ **Valuable**: Delivers measurable value to users
- ✅ **Estimable**: Contains enough detail for accurate sizing
- ✅ **Small**: Fits within one sprint (1-3 days, ≤8 story points)
- ✅ **Testable**: Has clear pass/fail criteria

**Format Requirements:**
- ✅ Specific user type (not just "user")
- ✅ Clear capability description
- ✅ Business value/benefit stated
- ✅ Minimum 2-3 acceptance criteria
- ✅ Given/When/Then format for criteria
- ✅ Covers happy path + key error cases

## Getting Help

**Questions about story format:**
- Review examples in `/training/` directory
- Consult `docs/PRODUCT-OWNER-GUIDE.md`
- Run `/write-user-story` and learn from AI output

**Questions about commands:**
- See `.claude/docs/story-commands-quick-reference.md`
- Review `.claude/CLAUDE.md` Product Owner Integration section

**Questions about workflow:**
- See `.claude/docs/story-workflow-guide.md` (comprehensive guide)
- Ask your development lead
- Review existing examples in this directory

## Examples

See `/training/` directory for:
- `example-good-login-story.md` - Perfect business story
- `example-good-password-reset-story.md` - Complex feature example
- `example-poor-story.md` - Common mistakes highlighted
- `example-improved-story.md` - After refinement
- `example-technical-story.md` - Technical work example

---

**Last Updated:** 2025-11-24
