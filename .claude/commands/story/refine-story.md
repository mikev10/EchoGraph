---
description: Refine existing user story for better clarity and testability
argument-hint: <ADO-ID or story text>
model: claude-sonnet-4-5-20250929
---

You are helping a developer improve an existing user story that may be poorly written, vague, or missing critical details.

**Purpose:** This command analyzes an existing user story, identifies quality issues, and generates an improved version using the @story-expert agent.

**Input**: `$ARGUMENTS` can be:
- Azure DevOps work item ID (e.g., "US-4523")
- Full story text pasted by user
- Path to a markdown file containing a story

---

## Phase 1: Gather User Story Information

**Determine input type:**

```
$ARGUMENTS
```

**If looks like ADO-ID (pattern: letters-numbers):**
```
Please paste the complete user story content from Azure DevOps work item $ARGUMENTS:

Include:
- Story title
- User story (As a... I want... So that...)
- All acceptance criteria
- Any description or additional context
```

Wait for user to provide the content.

**If looks like story text:**
Parse it directly and proceed to Phase 2.

**If looks like file path:**
Read the file and extract story content, then proceed to Phase 2.

---

## Phase 2: Analyze Story Quality

**Parse the story to extract:**
- User type/role
- Desired capability
- Business value
- Acceptance criteria
- Any additional context

**Evaluate against INVEST criteria:**

1. **Independent**: Can this be developed without waiting for other stories?
2. **Negotiable**: Are requirements clear but implementation flexible?
3. **Valuable**: Does it deliver measurable value to users?
4. **Estimable**: Is there enough detail for accurate sizing?
5. **Small**: Can it fit within one sprint (1-3 days, ≤8 points)?
6. **Testable**: Are there clear pass/fail criteria?

**Check formatting:**
- [ ] User story uses "As a... I want... So that..." format?
- [ ] User type is specific (not just "user")?
- [ ] Acceptance criteria use Given/When/Then format?
- [ ] Each acceptance criterion is testable?
- [ ] Scenarios cover happy path and error cases?
- [ ] Story is focused and not too broad?

**Identify specific issues:**
- Vague user type ("user" instead of specific persona)
- Missing "so that" clause (no business value)
- Vague acceptance criteria ("it should work")
- No Given/When/Then structure
- Missing error scenarios
- Story too large (multiple features)
- Not testable
- Implementation details instead of requirements
- Ambiguous language

**Create issues list:**
```
Issues found in this story:
1. [Issue 1 with explanation]
2. [Issue 2 with explanation]
3. [Issue 3 with explanation]
```

---

## Phase 3: Generate Improved Story

Use @story-expert agent to create an improved version:

**Instructions for the agent:**

"Improve this user story based on the identified issues:

Original story:
{paste original story}

Issues to address:
{paste issues list}

Create an improved version that:
- Uses specific user type
- Has clear business value
- Includes 3-6 testable acceptance criteria with Given/When/Then
- Covers happy path + key variations + critical errors
- Follows INVEST criteria
- Uses correct formatting
- Removes implementation details
- Is appropriately sized (1-3 days)"

**Important:** Ensure @story-expert follows all formatting rules (bold scenario titles only, no bold Given/When/Then).

---

## Phase 4: Show Comparison

Present the analysis and improvements in this format:

```markdown
# Story Refinement Analysis

## Original Story

{Display original story exactly as provided}

---

## Quality Assessment

### INVEST Criteria Analysis
- **Independent**: [Pass/Fail] - [Brief explanation]
- **Negotiable**: [Pass/Fail] - [Brief explanation]
- **Valuable**: [Pass/Fail] - [Brief explanation]
- **Estimable**: [Pass/Fail] - [Brief explanation]
- **Small**: [Pass/Fail] - [Brief explanation]
- **Testable**: [Pass/Fail] - [Brief explanation]

### Issues Identified

{numbered list of issues with explanations}

---

## Improved Story

{Display improved story from @story-expert}

---

## Key Improvements Made

1. [Improvement 1 - what changed and why]
2. [Improvement 2 - what changed and why]
3. [Improvement 3 - what changed and why]

---

## Impact on Development

**Before refinement:**
- [Potential problems developers would face]
- [Questions they would need to ask]
- [Ambiguities that could cause rework]

**After refinement:**
- [How improved version helps developers]
- [Reduced ambiguity and clearer requirements]
- [Better testability and acceptance criteria]

```

---

## Phase 5: Ask Developer for Next Action

After showing the comparison, ask:

```
How would you like to proceed?

A) Use improved version for /convert-story
   I'll proceed with the refined story to generate INITIAL.md

B) Save improved version and send suggestions to Product Owner
   I'll save the improved story for you to share with the PO

C) Proceed with original story anyway
   Continue with /convert-story using the original version

D) Further refine
   Make additional changes or adjustments

Please respond with A, B, C, or D.
```

**Handle each option:**

**Option A**:
```
Great! Proceeding with improved story for /convert-story.

The improved story is ready to be converted to INITIAL.md. Run:
/convert-story

When prompted, paste the improved story content (not the original).
```

**Option B**:
Save improved story to `PRPs/user-stories/drafts/[ADO-ID]-refined-YYYYMMDD.md` with metadata:
```markdown
---
created: {date}
status: refined
category: business
converted_to_ado: false
ado_id: {ADO-ID if provided}
original_story_issues: {list of issues}
refinement_date: {date}
---

{Improved story content}

---

## Original Story (For Reference)

{Original story content}

---

## Improvements Made

{List of key improvements}
```

Then inform user:
```
✓ Refined story saved: PRPs/user-stories/drafts/{filename}

Share this with your Product Owner:
- Show the comparison of original vs improved
- Explain the issues identified
- Request they update the ADO work item

Once ADO is updated, run: /convert-story [ADO-ID]
```

**Option C**:
```
Understood. Proceeding with original story.

Note: The identified issues may cause problems during /convert-story:
- {issue 1}
- {issue 2}

You may want to clarify these with the Product Owner before proceeding.

When ready, run: /convert-story
```

**Option D**:
Ask what specific changes they want, then regenerate with @story-expert.

---

## Quality Validation

Before completing, ensure the improved story meets:

- [ ] User story format correct (As a... I want... So that...)
- [ ] User type is specific
- [ ] Business value is clear
- [ ] 3-6 acceptance criteria scenarios
- [ ] All scenarios use Given/When/Then format
- [ ] Scenarios cover happy path + variations + errors
- [ ] Formatting correct (bold scenario titles only)
- [ ] No implementation details
- [ ] Story appropriately sized (1-3 days)
- [ ] All criteria testable
- [ ] Addresses all identified issues

---

## Examples

### Example 1: Vague Story

**Input:**
```
/refine-story US-5001
[User pastes: "Users can reset password"]
```

**Issues identified:**
- No "As a... I want... So that..." format
- No acceptance criteria
- Too vague

**Output:**
Show comparison with improved version that includes:
- Proper user story format
- 4-5 detailed acceptance criteria
- Clear scenarios with Given/When/Then

### Example 2: Missing Error Cases

**Input:**
```
/refine-story As a user I want to login with email and password so I can access my account.
Acceptance criteria: User can login successfully.
```

**Issues identified:**
- Generic "user" type
- Only happy path, no error cases
- Acceptance criteria not testable (no Given/When/Then)

**Output:**
Show improved version with:
- Specific user type ("mobile app user")
- 5-6 scenarios covering happy path, invalid credentials, network errors, etc.
- Proper Given/When/Then format

### Example 3: Too Large

**Input:**
```
/refine-story US-3000
[Story includes: login, logout, password reset, profile management, and settings]
```

**Issues identified:**
- Too large (5+ features in one story)
- Violates "Small" principle
- Cannot be completed in one sprint

**Output:**
Suggest breaking into smaller stories:
1. Login functionality
2. Logout functionality
3. Password reset
4. Profile management
5. Settings management

Then offer to generate refined version of just one feature.

---

## Error Handling

**If story text is empty or invalid:**
```
I couldn't parse a valid user story from the input provided.

Please provide one of:
- Azure DevOps work item ID (then paste the story content)
- Complete story text with at least a user story statement
- Path to a markdown file containing the story

Example: /refine-story US-4523
```

**If story is already high quality:**
```
Good news! This story already meets high quality standards.

INVEST Criteria: All Pass ✓
Formatting: Correct ✓
Acceptance Criteria: Well-defined ✓

This story is ready for /convert-story without refinement.

Would you like to proceed with /convert-story? (yes/no)
```

**If @story-expert output is malformed:**
Regenerate with explicit instructions about formatting rules.

---

## Critical Requirements

**DO:**

- Always use @story-expert for generating improved version
- Show clear before/after comparison
- Identify specific issues with explanations
- Evaluate against INVEST criteria
- Offer multiple next-step options
- Save refined version if requested
- Validate improved story meets quality standards

**DO NOT:**

- Proceed without showing comparison
- Skip quality analysis
- Make changes without using @story-expert
- Modify the original story in place (always show both)
- Assume developer wants to use improved version (always ask)

---

## Integration with Context Engineering Workflow

This command fits into the workflow when story quality is questionable:

```
ADO Story → /refine-story → Review comparison → Choose action → /convert-story
                                                                       ↓
                                                                  INITIAL.md
```

**Value:** Catching story quality issues BEFORE /convert-story leads to better INITIAL.md and ultimately better PRPs.

---

**Output**: Comparison of original vs improved story, quality assessment, and recommended next actions.
