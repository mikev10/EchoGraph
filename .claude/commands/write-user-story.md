---
description: Write user story from requirements (pre-ADO drafting tool for POs and developers)
argument-hint: <requirements...>
model: claude-sonnet-4-5-20250929
---

You are about to create a user story from provided requirements using the Context Engineering workflow.

**Purpose:** This command helps Product Owners draft well-structured user stories BEFORE creating Azure DevOps work items. It can also help developers structure technical work as user stories.

**Input**: Requirements provided as `$ARGUMENTS`

---

## Phase 1: Analyze Requirements

Review the provided requirements:

```
$ARGUMENTS
```

**Determine story category:**
- Is this business functionality from a Product Owner? → `/drafts/`
- Is this technical work (refactoring, bugs, tech debt)? → `/technical/`

If requirements are vague or incomplete:

- Ask clarifying questions before proceeding
- Request specific details about:
  - Who the user is (user type/role)
  - What functionality they need
  - Why they need it (business value)
  - Any acceptance criteria or constraints
  - Error cases or edge cases to consider
  - Platform requirements (mobile, web, both)
  - Performance or security requirements

**Ask user which category:**
"Is this a:
A) Business feature (for Product Owner to add to ADO)
B) Technical work (refactoring, bug, tech debt)"

Store their answer for file placement decision.

---

## Phase 2: Generate User Story

Use @story-expert agent to create a properly structured user story:

**Instructions for the agent:**

- Follow the Core Output Structure (Title, User Story, Acceptance Criteria, Notes)
- Create 3-6 acceptance criteria scenarios covering:
  - Happy path
  - Key variations
  - Critical error cases
- Keep concise (readable in 2-3 minutes)
- Focus on behavior (WHAT), not implementation (HOW)
- Follow INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- If requirements mention specific technical details, embed them appropriately:
  - Business rules → within acceptance criteria scenarios
  - Technical constraints → within acceptance criteria or Notes
  - Dependencies → in Notes section
- Remember: Technical implementation details will be added later during `/convert-story`

**Important context for agent:**
"This story is part of the Context Engineering Three Amigos workflow. It will be:
1. Reviewed and refined by the requester
2. Enriched by Dev Lead with technical context (/enrich-story-tech)
3. Enriched by QA Lead with test scenarios (/enrich-story-qa)
4. Aligned in Three Amigos session (/three-amigos-prep)
5. Validated for readiness (/validate-story-ready)
6. Used to create an Azure DevOps work item (manual)
7. Converted to technical specification (INITIAL.md) using /convert-story
8. Used to generate a comprehensive implementation plan (PRP)

Focus on clear business requirements and testable acceptance criteria. Be explicit about error scenarios since AI will implement this code. Technical research happens during the Three Amigos enrichment phase."

---

## CRITICAL FORMATTING RULES

Remind the @story-expert agent of these CRITICAL rules:

### User Story Format

❌ **WRONG FORMAT** (Do NOT use):

```
As a **user viewing the schedule in dark mode**,
I want **resource groups to have clear visual hierarchy and selected resources to remain readable**
so that **I can efficiently navigate and distinguish between different resources without eye strain**.
```

✅ **CORRECT FORMAT** (Always use):

```
As a user viewing the schedule in dark mode
I want resource groups to have clear visual hierarchy and selected resources to remain readable
so that I can efficiently navigate and distinguish between different resources without eye strain.
```

### Acceptance Criteria Format

**ONLY the scenario title should be bolded. Do NOT bold Given/When/Then/And keywords.**

❌ **WRONG FORMAT** (Do NOT use):

```
### Scenario 1: Table Background Colors
**Given** I am viewing a table
**When** the page loads
**Then** the table should display correctly
**And** colors should match the style guide
```

✅ **CORRECT FORMAT** (Always use):

```
- **Scenario 1: Table Background Colors**

  - Given I am viewing a table
  - When the page loads
  - Then the table should display correctly
  - And colors should match the style guide
```

**Key formatting rules:**

- Use a dash and bold for the scenario title: `- **Scenario X: [Title]**`
- Add a blank line after the scenario title
- Indent the Given/When/Then/And statements with two spaces
- Do NOT bold the Given/When/Then/And keywords
- Do NOT use ### for scenario headings
- Each Given/When/Then/And line starts with a dash, followed by the keyword and statement

---

## Phase 3: Create Markdown File

**Determine file location based on Phase 1 answer:**
- Business/PO story (option A) → `user-stories/drafts/`
- Technical story (option B) → `user-stories/technical/`

**Filename generation:**

1. Take the user story title from the agent output
2. Convert to lowercase
3. Replace spaces with hyphens
4. Remove special characters (keep only alphanumeric and hyphens)
5. Add timestamp prefix for uniqueness: `YYYYMMDD-{sanitized-title}.md`
6. Example: `20251124-password-reset-via-email.md`

**File content structure:**

```markdown
---
created: {current-date in YYYY-MM-DD format}
status: draft
category: {business|technical}
converted_to_ado: false
ado_id: null
sprint: null
story_points: null
three_amigos_complete: false
tech_context_added: false
qa_context_added: false
---

{Generated user story content from @story-expert}

---

## Original Requirements

{Copy of $ARGUMENTS for reference}
```

**Create the file** using Write tool with the full path and content.

---

## Phase 4: Next Steps Guidance

After creating the file, inform the user:

**For Business Stories (drafts/):**

```
✓ User story created: {full-path}
✓ Status: Draft (ready for review)
✓ Category: Business

┌─────────────────────────────────────────────────────────────┐
│              THREE AMIGOS WORKFLOW - NEXT STEPS              │
└─────────────────────────────────────────────────────────────┘

Step 1: Review & Refine (You - PO)
       Review the story and refine acceptance criteria if needed

Step 2: Technical Enrichment (Dev Lead)
       /enrich-story-tech {full-path}
       Adds: API specs, data models, patterns, security context

Step 3: QA Enrichment (QA Lead)
       /enrich-story-qa {full-path}
       Adds: Test scenarios, edge cases, test data requirements

Step 4: Three Amigos Alignment (All)
       /three-amigos-prep {full-path}
       Generates: Session agenda and discussion points
       Hold 30-60 min alignment meeting

Step 5: Validate Readiness
       /validate-story-ready {full-path}
       Checks: All Definition of Ready criteria

Step 6: Create ADO & Groom
       If READY → Create ADO work item, add to grooming

Step 7: Convert & Implement
       /convert-story [ADO-ID] → /generate-prp → /execute-prp

This story is NOT automatically synced to Azure DevOps.
```

**For Technical Stories (technical/):**

```
✓ User story created: {full-path}
✓ Status: Draft (ready for review)
✓ Category: Technical

┌─────────────────────────────────────────────────────────────┐
│              THREE AMIGOS WORKFLOW - NEXT STEPS              │
└─────────────────────────────────────────────────────────────┘

Step 1: Review & Refine (You)
       Review the story and refine if needed

Step 2: Technical Enrichment (Dev Lead or Self)
       /enrich-story-tech {full-path}
       Adds: API specs, data models, patterns, security context

Step 3: QA Enrichment (QA Lead or Self)
       /enrich-story-qa {full-path}
       Adds: Test scenarios, edge cases, test data requirements

Step 4: Validate Readiness (Optional for technical stories)
       /validate-story-ready {full-path}

Step 5: Convert & Implement
       /convert-story → /generate-prp → /execute-prp

Technical stories can proceed with lighter process if preferred.
```

---

## Quality Validation

Before completing, verify the generated story meets these criteria:

- [ ] User story follows format: "As a [user], I want [capability], so that [benefit]"
- [ ] User type is specific (not just "user")
- [ ] Functionality is clear and focused
- [ ] Business value is stated
- [ ] 3-6 acceptance criteria scenarios included
- [ ] Each scenario has Given/When/Then/And structure
- [ ] Scenarios cover happy path + variations + errors
- [ ] Formatting is correct (bold only scenario titles)
- [ ] No implementation details included
- [ ] Story is appropriately sized (1-3 days estimate)
- [ ] All criteria are testable
- [ ] File has correct metadata
- [ ] File saved to correct directory

If any criteria not met, regenerate with @story-expert.

---

## Error Handling

**If requirements are too vague:**
```
The requirements are too vague to create a quality user story.

I need more information about:
- [specific questions based on what's missing]

Please provide additional details and run the command again.
```

**If story title is too long (>60 chars):**
- Shorten the title for filename
- Keep full title in the story content

**If @story-expert output is malformed:**
- Regenerate with explicit formatting instructions
- Do not proceed with malformed output

---

## Examples

### Example 1: Business Story

**Input:**
```
/write-user-story Users need to be able to reset their password if they forget it. They should receive an email with a reset link that expires after 1 hour.
```

**Process:**
1. Ask: "Is this business or technical?" → User answers "Business"
2. Generate story with @story-expert
3. Create file: `user-stories/drafts/20251124-password-reset-via-email.md`
4. Show next steps for ADO creation

### Example 2: Technical Story

**Input:**
```
/write-user-story Refactor authentication module to improve testability and reduce code duplication. Current module has 15+ methods with overlapping logic.
```

**Process:**
1. Ask: "Is this business or technical?" → User answers "Technical"
2. Generate technical story with @story-expert
3. Create file: `user-stories/technical/20251124-refactor-auth-module.md`
4. Show next steps for /convert-story

### Example 3: Vague Requirements

**Input:**
```
/write-user-story Make the app faster
```

**Process:**
1. Identify vagueness
2. Ask clarifying questions:
   - What specific parts of the app are slow?
   - What is the current performance?
   - What is the target performance?
   - What user actions are affected?
   - Are there specific screens or features?
3. Wait for clarification before proceeding

---

## Critical Requirements

**DO:**

- Always use @story-expert agent for story generation
- Ask clarifying questions if requirements are vague
- Include original requirements in the file for reference
- Create file locally as markdown only
- Ensure filename is filesystem-safe and unique
- Use correct formatting (bold scenario titles only)
- Validate output before saving
- Store in appropriate directory (drafts/ or technical/)

**DO NOT:**

- Create or update work items in Azure DevOps (manual step for POs)
- Proceed if requirements are too vague (ask questions first)
- Skip the @story-expert agent
- Include technical implementation details (added later in /convert-story)
- Bold the Given/When/Then/And keywords (only bold scenario titles)
- Use ### for scenario headings (use dash + bold)

---

## Integration with Context Engineering Workflow

This command is the FIRST step in the Context Engineering Three Amigos workflow:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    FULL THREE AMIGOS WORKFLOW                                    │
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

**Key Points:**
- This creates a DRAFT for review - first step in a collaborative process
- Dev Lead and QA Lead enrich the story before grooming
- Three Amigos session ensures alignment before broader team sees it
- Story is validated against Definition of Ready before grooming
- PO still creates the ADO work item manually

**See also:**
- `.claude/DEFINITION-OF-READY.md` - Criteria for story readiness
- `.claude/docs/three-amigos-guide.md` - Full collaboration guide

---

**Output**: Full path to created markdown file and summary of next steps based on story category.
