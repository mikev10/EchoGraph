---
description: Prepare discussion points for Three Amigos alignment session
argument-hint: <story-path>
model: claude-sonnet-4-5-20250929
---

# Three Amigos Session Preparation

You are preparing a **Three Amigos** alignment session for a user story. This session brings together the **Product Owner** (business perspective), **Dev Lead** (technical perspective), and **QA Lead** (testing perspective) to ensure shared understanding before the story enters team grooming.

**Purpose:** Generate discussion agenda, identify potential issues, and prepare talking points for an effective 30-60 minute alignment session.

**Input:** Path to user story markdown file: `$ARGUMENTS`

---

## What is Three Amigos?

The Three Amigos pattern is a pre-refinement collaboration where three perspectives review a story:

1. **Product Owner (PO):** Ensures business intent is clear and valuable
2. **Dev Lead:** Ensures technical feasibility and identifies complexity
3. **QA Lead:** Ensures testability and identifies edge cases

**Goal:** Resolve ambiguities and align understanding BEFORE the broader team sees the story.

---

## Phase 1: Load and Analyze Story

**Read the story file:**
```
$ARGUMENTS
```

If no path provided:
```
Please provide the path to a user story file.

Usage: /three-amigos-prep PRPs/user-stories/drafts/20251124-feature-name.md

Tip: Run after /enrich-story-tech and /enrich-story-qa for best results.
```

**Analyze story sections:**
- User Story structure
- Acceptance Criteria completeness
- Technical Context (if present)
- QA Context (if present)
- Identified risks and dependencies

---

## Phase 2: Identify Discussion Points

Based on story analysis, identify:

### 2.1 Ambiguities
- Unclear requirements
- Missing acceptance criteria
- Vague language that could be interpreted multiple ways
- Implicit assumptions not made explicit

### 2.2 Technical Concerns
- Complexity factors
- Dependencies on other systems/stories
- Performance implications
- Security considerations
- Architecture decisions needed

### 2.3 Testing Concerns
- Difficult-to-test scenarios
- Missing edge cases
- Test data complexity
- Integration testing challenges

### 2.4 Scope Questions
- What's in scope vs. out of scope
- MVP vs. nice-to-have features
- Deferral candidates

### 2.5 Risk Factors
- Technical risks
- Business risks
- Timeline risks
- Dependency risks

---

## Phase 3: Generate Session Agenda

```markdown
# Three Amigos Session Agenda

**Story:** [Title]
**File:** [Path]
**Prepared:** [Date]
**Estimated Duration:** 30-45 minutes

---

## Attendees Required

- [ ] **Product Owner:** [Name if known]
- [ ] **Dev Lead:** [Name if known]
- [ ] **QA Lead:** [Name if known]

Optional:
- [ ] UX Designer (if UI-heavy story)
- [ ] Architect (if architectural decisions needed)

---

## Pre-Session Checklist

Before the session, ensure:
- [ ] All attendees have read the story
- [ ] Technical Context section is complete (or note gaps)
- [ ] QA Context section is complete (or note gaps)
- [ ] 30-45 minutes blocked on calendars

---

## Agenda

### 1. Story Overview (5 min) - PO Leads

**Objective:** Ensure everyone understands the business context

**Discussion Points:**
- What problem does this solve for users?
- Why is this valuable now?
- How does this fit into the broader product roadmap?

**PO to confirm:**
- [ ] User type is correctly identified
- [ ] Business value is clearly articulated
- [ ] Success metrics are defined

---

### 2. Acceptance Criteria Review (10 min) - All

**Objective:** Ensure criteria are clear, complete, and testable

**Current Scenarios:**
[List each acceptance criteria scenario from the story]

**Discussion Points:**

**For PO:**
- Are these scenarios complete? Any missing?
- Are the expected outcomes correct?
- What should happen in [specific ambiguous scenario]?

**For Dev Lead:**
- Are these scenarios technically feasible?
- Any technical constraints that affect expected behavior?
- Do we need to adjust any criteria based on technical reality?

**For QA Lead:**
- Are all scenarios testable as written?
- What edge cases are we missing?
- Do we need more specific expected outcomes?

---

### 3. Technical Feasibility (10 min) - Dev Lead Leads

**Objective:** Confirm approach and identify complexity

**Technical Context Summary:**
[Summarize Technical Context section if present]

**Discussion Points:**

**Architecture:**
- Is the proposed approach sound?
- Are there alternative approaches to consider?
- Any architectural decisions that need broader team input?

**Dependencies:**
- What does this story depend on?
- What depends on this story?
- Are there blocking dependencies we need to resolve?

**Complexity Assessment:**
- What's the estimated complexity? (Simple/Medium/Complex)
- What makes this complex? (if applicable)
- Any unknown unknowns we should spike first?

**Security:**
- Are there security implications?
- What validation/auth is required?
- Any data protection concerns?

---

### 4. Test Strategy (10 min) - QA Lead Leads

**Objective:** Confirm testing approach and coverage

**QA Context Summary:**
[Summarize QA Context section if present]

**Discussion Points:**

**Test Coverage:**
- Are the test scenarios comprehensive?
- What's the automation strategy?
- Are there integration test requirements?

**Edge Cases:**
- [List identified edge cases]
- Are we missing any critical edge cases?
- How should the system behave in [specific edge case]?

**Test Data:**
- What test data do we need?
- How will we set up test scenarios?
- Any test environment requirements?

**Risks:**
- What could go wrong in testing?
- Are there hard-to-test scenarios?
- What's the regression impact?

---

### 5. Scope Confirmation (5 min) - All

**Objective:** Agree on what's in and out of scope

**In Scope:**
- [List features/behaviors that ARE in scope]

**Out of Scope:**
- [List features/behaviors that are NOT in scope]

**Deferred Items:**
- [List items explicitly deferred to future stories]

**Questions:**
- Are there any scope creep risks?
- Should anything be moved out of scope to reduce complexity?
- Should anything be added that we're missing?

---

### 6. Risks and Blockers (5 min) - All

**Objective:** Identify and plan for risks

**Identified Risks:**
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Plan] |
| [Risk 2] | H/M/L | H/M/L | [Plan] |

**Potential Blockers:**
- [Blocker 1] - Owner: [Who]
- [Blocker 2] - Owner: [Who]

**Questions:**
- Are there risks we haven't considered?
- What could delay this story?
- Do we need to de-risk anything before grooming?

---

### 7. Action Items and Wrap-up (5 min) - All

**Capture:**
- [ ] Open questions that need follow-up
- [ ] Action items with owners
- [ ] Story updates needed before grooming

**Final Confirmation:**
- [ ] PO confirms business requirements are captured
- [ ] Dev Lead confirms technical approach is feasible
- [ ] QA Lead confirms story is testable

**Story Status:**
- Ready for grooming: Yes / No / Needs follow-up

---

## Post-Session Actions

After the session:

1. **Update story file** with any changes agreed upon
2. **Record session notes** in story's Additional Notes section
3. **Run validation** to check readiness:
   ```
   /validate-story-ready [story-path]
   ```
4. **Schedule grooming** if story is ready

---
```

---

## Phase 4: Generate Role-Specific Prep Notes

```markdown
## Role-Specific Preparation

### For Product Owner

**Your role:** Ensure business intent is clear and valuable

**Come prepared to discuss:**
1. Why this feature matters to users right now
2. How success will be measured
3. What's the minimum viable version of this feature
4. What can be deferred to future iterations

**Questions you might be asked:**
- "What should happen when [edge case]?"
- "Is [behavior X] more important than [behavior Y]?"
- "Can we simplify by removing [feature Z]?"

**Decisions you may need to make:**
- Scope trade-offs (what's in vs. out)
- Priority of edge cases
- Acceptance of technical constraints

---

### For Dev Lead

**Your role:** Ensure technical feasibility and identify complexity

**Come prepared to discuss:**
1. Proposed technical approach
2. Dependencies and blockers
3. Complexity estimate and reasoning
4. Security and performance considerations

**Questions you might be asked:**
- "Is this technically feasible as specified?"
- "How long do you think this will take?"
- "What's the riskiest part of this implementation?"

**Decisions you may need to make:**
- Architecture approach
- Technology choices
- Complexity/scope trade-offs

---

### For QA Lead

**Your role:** Ensure testability and identify edge cases

**Come prepared to discuss:**
1. Test scenarios and coverage strategy
2. Edge cases and boundary conditions
3. Test data requirements
4. Automation approach

**Questions you might be asked:**
- "Is this testable as written?"
- "What edge cases should we add?"
- "How will we test [specific scenario]?"

**Decisions you may need to make:**
- Which scenarios to automate vs. manual test
- Test data strategy
- Acceptance criteria clarity requests

---
```

---

## Phase 5: Identify Specific Discussion Items

Based on story analysis, highlight specific items that MUST be discussed:

```markdown
## Critical Discussion Items

**These items MUST be resolved during the session:**

### Ambiguities to Resolve
[List specific ambiguities found in story analysis]

1. **[Topic]:** [Specific question that needs an answer]
   - Options: [Option A] vs [Option B]
   - Impact if unresolved: [What happens if we don't decide]

2. **[Topic]:** [Specific question]
   - Options: [Option A] vs [Option B]
   - Impact if unresolved: [What happens]

### Technical Decisions Needed
[List specific technical decisions]

1. **[Decision]:** [What needs to be decided]
   - Recommendation: [If Dev Lead has a preference]
   - Trade-offs: [What's gained/lost with each option]

### Test Coverage Gaps
[List specific gaps in test coverage]

1. **[Gap]:** [What's missing]
   - Suggested addition: [Proposed scenario to add]
   - Risk if not covered: [What could go wrong]

### Scope Clarifications
[List items where scope is unclear]

1. **[Feature/Behavior]:** In scope or out?
   - PO to decide

---
```

---

## Phase 6: Output Complete Prep Package

Combine all generated content into a single document:

```
## Three Amigos Session Prep Complete

**Story:** [Title]
**File:** [Path]

### Generated Documents:
1. Session Agenda (above)
2. Role-Specific Prep Notes
3. Critical Discussion Items

### Recommended Session Flow:
1. Share this prep document with all attendees
2. Ask attendees to review story and prep notes before session
3. Use agenda to guide 30-45 minute session
4. Capture decisions and action items
5. Update story file with any changes
6. Run /validate-story-ready to confirm

### Quick Copy: Meeting Invite Text

```
Subject: Three Amigos Session: [Story Title]

Hi team,

Please join me for a Three Amigos session to align on the following user story before team grooming:

Story: [Title]
Duration: 30-45 minutes
Attendees: PO, Dev Lead, QA Lead

Pre-work:
- Review the attached story file
- Review your role-specific prep notes

Agenda attached.

Thanks!
```

### After the Session

Run: `/validate-story-ready [story-path]`

If ready → Add to grooming agenda
If not ready → Address gaps and re-validate
```

---

## Integration with Three Amigos Workflow

This command is Step 4 in the Three Amigos workflow:

```
Step 1: /write-user-story  → PO creates draft         ✓
Step 2: /enrich-story-tech → Dev Lead adds technical  ✓
Step 3: /enrich-story-qa   → QA Lead adds test        ✓
Step 4: /three-amigos-prep → Prepare alignment session ← YOU ARE HERE
Step 5: /validate-story-ready → Check all DoR criteria

After successful session → Story ready for team grooming
```

---

**Output:** Complete Three Amigos session preparation package including agenda, role-specific prep notes, and critical discussion items.
