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
"This story is part of Context Engineering workflow. It will be:
1. Reviewed and refined by the requester
2. Used to create an Azure DevOps work item (manual)
3. Converted to technical specification (INITIAL.md) using /convert-story
4. Used to generate a comprehensive implementation plan (PRP)

Focus on clear business requirements and testable acceptance criteria. Technical research happens later."

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

Next steps:
1. Review the story and refine acceptance criteria if needed
2. Create Azure DevOps work item and copy this content
3. When ready for development, developer runs: /convert-story [ADO-ID]

This story is NOT automatically synced to Azure DevOps.
```

**For Technical Stories (technical/):**

```
✓ User story created: {full-path}
✓ Status: Draft (ready for review)
✓ Category: Technical

Next steps:
1. Review the story and refine if needed
2. (Optional) Create ADO work item for tracking
3. Run: /convert-story with this story content to generate INITIAL.md
4. Continue with standard PRP workflow (/generate-prp, /execute-prp)

Technical stories can proceed without ADO if preferred.
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

This command is the FIRST step in the Context Engineering workflow:

```
/write-user-story → Review → Create ADO → /convert-story → /generate-prp → /execute-prp
     (Draft)                  (Manual)     (Tech Spec)      (Plan)        (Implement)
```

**Remember:** This creates a DRAFT for review. The PO still needs to create the ADO work item manually.

---

**Output**: Full path to created markdown file and summary of next steps based on story category.
