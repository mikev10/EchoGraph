# Story Workflow Guide: Complete Context Engineering Flow

This guide shows all possible workflows for user stories in Context Engineering, from initial requirements through implementation.

---

## Table of Contents

1. [Overview: All Workflow Paths](#overview-all-workflow-paths)
2. [Three Amigos Workflow (Recommended)](#three-amigos-workflow-recommended)
3. [Workflow 1: PO Drafting (Pre-ADO)](#workflow-1-po-drafting-pre-ado)
4. [Workflow 2: Direct ADO to Implementation](#workflow-2-direct-ado-to-implementation)
5. [Workflow 3: Story Refinement](#workflow-3-story-refinement)
6. [Workflow 4: Technical Story](#workflow-4-technical-story)
7. [Decision Trees](#decision-trees)
8. [Command Reference](#command-reference)
9. [Troubleshooting](#troubleshooting)

---

## Overview: All Workflow Paths

### Recommended: Three Amigos Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   THREE AMIGOS WORKFLOW (RECOMMENDED)                    │
└─────────────────────────────────────────────────────────────────────────┘

STEP 1: PO Creates Draft Story
├── /write-user-story
└── Story saved to user-stories/drafts/
        │
        ▼
STEP 2: Dev Lead Enriches (Technical Context)
├── /enrich-story-tech
└── Adds: API specs, data model, patterns, security
        │
        ▼
STEP 3: QA Lead Enriches (Test Scenarios)
├── /enrich-story-qa
└── Adds: Test cases, edge cases, test data requirements
        │
        ▼
STEP 4: Three Amigos Alignment Session
├── /three-amigos-prep (generates agenda)
├── 30-45 minute meeting: PO + Dev Lead + QA Lead
└── Resolve questions, confirm scope
        │
        ▼
STEP 5: Validate Readiness
├── /validate-story-ready
├── Confirms Definition of Ready criteria met
└── Status: READY / NEARLY READY / NOT READY
        │
        ▼
STEP 6: Team Grooming → Estimation → Sprint Commit
        │
        ▼
STEP 7: Implementation
├── /convert-story
├── /generate-prp
├── /execute-prp
└── Code complete!
```

### Alternative: Simplified Paths

```
┌─────────────────────────────────────────────────────────────┐
│                     STARTING POINT                           │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 PO has            Developer has
               requirements        technical work
                    │                   │
        ┌───────────┴───────────┐      │
        │                       │      │
    Draft with AI          Write in ADO    Technical story
    /write-user-story         directly       /write-user-story
        │                       │               │
        ▼                       ▼               ▼
    Review &               Story quality     Save to
    create ADO              check           technical/
        │                       │               │
        │               ┌───────┴───────┐       │
        │               │               │       │
        │           Good story    Poor story    │
        │               │               │       │
        └───────────────┼───────────────┘       │
                        │       │               │
                        │   /refine-story       │
                        │       │               │
                        └───────┴───────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
              Use Three Amigos      Skip to Implementation
              (recommended)          (simple stories only)
                    │                       │
        ┌───────────┴───────────┐           │
        │                       │           │
    /enrich-story-tech    /enrich-story-qa  │
        │                       │           │
        └───────────┬───────────┘           │
                    ▼                       │
            /three-amigos-prep              │
                    │                       │
                    ▼                       │
            /validate-story-ready           │
                    │                       │
                    └───────────┬───────────┘
                                │
                         /convert-story
                                │
                          INITIAL.md
                                │
                         /generate-prp
                                │
                              PRP
                                │
                         /execute-prp
                                │
                        IMPLEMENTATION
```

---

## Three Amigos Workflow (Recommended)

**Use case:** Full collaborative workflow ensuring stories are fully ready before team grooming

The Three Amigos workflow brings together PO (business), Dev Lead (technical), and QA Lead (testing) perspectives before a story enters team grooming. This is the **recommended workflow** for new features and complex stories.

### Why Three Amigos?

| Without Three Amigos | With Three Amigos |
|---------------------|-------------------|
| Stories enter grooming with ambiguities | Stories are fully understood before grooming |
| Team asks clarifying questions during grooming | Questions already answered |
| Developers blocked mid-sprint by surprises | Risks identified upfront |
| AI generates code with missing error handling | Explicit edge cases documented |
| QA discovers gaps during testing | Test scenarios defined before dev starts |

### Step-by-Step Process

#### Step 1: PO Creates Draft Story

**Command:** `/write-user-story [requirements]`

**Who:** Product Owner (or BA)

**Output:** Story saved to `user-stories/drafts/[date]-[title].md`

**What's created:**
- User story with specific user type
- 3-5 acceptance criteria in Given/When/Then format
- Happy path, variations, and error scenarios

#### Step 2: Dev Lead Adds Technical Context

**Command:** `/enrich-story-tech [story-path]`

**Who:** Dev Lead

**Output:** Technical Context section added to story file

**What's added:**
- Architecture approach and component mapping
- API specifications (endpoints, request/response formats)
- Data model and migration requirements
- Dependencies and prerequisites
- Security considerations
- Technical risks assessment
- Implementation patterns from codebase

**Example:**
```
/enrich-story-tech user-stories/drafts/20251124-password-reset.md
```

#### Step 3: QA Lead Adds Test Scenarios

**Command:** `/enrich-story-qa [story-path]`

**Who:** QA Lead

**Output:** QA Context section added to story file

**What's added:**
- Comprehensive test scenarios (happy path, negative, boundary, edge cases)
- Test data requirements
- Integration test points
- Accessibility checklist (if applicable)
- Regression impact analysis
- Automation strategy

**Example:**
```
/enrich-story-qa user-stories/drafts/20251124-password-reset.md
```

#### Step 4: Three Amigos Alignment Session

**Command:** `/three-amigos-prep [story-path]`

**Who:** All three (PO, Dev Lead, QA Lead)

**Output:** Meeting agenda and discussion points

**Meeting structure (30-45 min):**
| Time | Topic | Lead |
|------|-------|------|
| 5 min | Story Overview | PO |
| 10 min | Acceptance Criteria Review | All |
| 10 min | Technical Feasibility | Dev Lead |
| 10 min | Test Strategy | QA Lead |
| 5 min | Scope & Risks | All |
| 5 min | Actions & Wrap-up | All |

**Example:**
```
/three-amigos-prep user-stories/drafts/20251124-password-reset.md
```

#### Step 5: Validate Readiness

**Command:** `/validate-story-ready [story-path]`

**Who:** Any team member (usually facilitator)

**Output:** Definition of Ready report

**Checks:**
- User Story Structure (5 criteria)
- Acceptance Criteria (5 criteria)
- Technical Context (7 criteria)
- QA Context (5 criteria)
- Three Amigos Alignment (4 criteria)

**Status outcomes:**
- **READY** (90%+): Proceed to team grooming
- **NEARLY READY** (75-89%): Address minor gaps
- **NOT READY** (<75%): Address critical gaps

**Example:**
```
/validate-story-ready user-stories/drafts/20251124-password-reset.md
```

#### Step 6: Team Grooming & Estimation

**Manual step:** Present story to full development team

**With Three Amigos complete:**
- Story already well-understood
- Technical complexity known
- Test approach defined
- Estimates are more accurate

#### Step 7: Implementation

**Commands:**
```
/convert-story US-4523
/generate-prp
/execute-prp
```

**Flow:** Story → INITIAL.md → PRP → Implementation

### When to Use Three Amigos

**Always use for:**
- ✅ New features with user-facing changes
- ✅ Complex technical stories
- ✅ Stories with multiple acceptance criteria
- ✅ Stories touching security or payments
- ✅ Stories with unknown complexity

**Can skip for:**
- ❌ Bug fixes with clear reproduction steps
- ❌ Technical debt with dev-only impact
- ❌ Trivial changes (typo fixes, config changes)
- ❌ Spike/research tasks

### Commands Summary

| Step | Command | Owner |
|------|---------|-------|
| 1 | `/write-user-story` | PO |
| 2 | `/enrich-story-tech` | Dev Lead |
| 3 | `/enrich-story-qa` | QA Lead |
| 4 | `/three-amigos-prep` | Facilitator |
| 5 | `/validate-story-ready` | Any |
| 6 | Manual grooming | Team |
| 7 | `/convert-story` → `/generate-prp` → `/execute-prp` | Developer |

---

## Workflow 1: PO Drafting (Pre-ADO)

**Use case:** Product Owner wants to draft story with AI assistance before creating ADO work item

### Step-by-Step Process

#### 1. Draft Story with AI

**Command:** `/write-user-story [requirements]`

**Example:**
```
/write-user-story Users need to be able to reset their password if they forget it.
They should receive an email with a reset link that expires after 1 hour.
```

**AI Response:**
- Asks clarifying questions
- Generates structured story with Given/When/Then acceptance criteria
- Saves to `user-stories/drafts/20251124-password-reset-via-email.md`

#### 2. Review Generated Story

**Check:**
- [ ] User type is specific
- [ ] Business value is clear
- [ ] Acceptance criteria are testable
- [ ] Scenarios cover happy path + variations + errors
- [ ] Story size is appropriate (1-3 days)
- [ ] All business rules are captured

**Edit if needed:** Make any adjustments directly in the markdown file

#### 3. Create ADO Work Item

**Manual steps:**
1. Open Azure DevOps
2. Create new User Story work item
3. Copy title, user story, and acceptance criteria from markdown file
4. Add additional ADO fields (sprint, story points, tags, etc.)
5. Link designs, mockups, related work items
6. Assign to developer

**Note the ADO Work Item ID** (e.g., US-4523)

#### 4. Developer Converts to Technical Spec

**When developer is ready to implement:**

**Command:** `/convert-story US-4523`

**Process:**
- Developer pastes story content from ADO
- AI researches codebase for patterns, APIs, libraries
- AI asks technical clarifying questions
- Generates `PRPs/feature-requests/US-4523-password-reset-INITIAL.md`

#### 5. Continue with Standard PRP Workflow

```
/generate-prp → /execute-prp → Implementation Complete
```

### When to Use This Workflow

**Best for:**
- ✅ Complex features with many edge cases
- ✅ POs new to writing user stories
- ✅ Features with unclear acceptance criteria
- ✅ Collaborative planning sessions
- ✅ Learning exercise for better story writing

**Skip if:**
- ❌ Simple, straightforward stories
- ❌ Experienced PO with clear requirements
- ❌ Time-sensitive work (direct to ADO faster)

---

## Workflow 2: Direct ADO to Implementation

**Use case:** PO writes story directly in ADO, developer implements

### Step-by-Step Process

#### 1. PO Creates Story in ADO

**Manual steps:**
1. Write user story in ADO
2. Add acceptance criteria (ideally Given/When/Then)
3. Assign to developer

#### 2. Developer Assesses Story Quality

**Quick check:**
- Does story have clear user type?
- Are acceptance criteria testable?
- Does it use Given/When/Then format?
- Are error cases covered?
- Is story appropriately sized?

**Decision:**
- **Good quality** → Proceed to Step 3
- **Poor quality** → Use Workflow 3 (Refinement)

#### 3. Developer Converts Story

**Command:** `/convert-story US-4523`

**Process:**
- Paste story content from ADO
- AI researches codebase
- AI asks technical questions
- Generates INITIAL.md

#### 4. Continue with PRP Workflow

```
/generate-prp → /execute-prp → Implementation
```

### When to Use This Workflow

**Best for:**
- ✅ Experienced POs with good story-writing skills
- ✅ Simple, well-defined features
- ✅ Established team with consistent story quality
- ✅ Standard workflow - most common path

---

## Workflow 3: Story Refinement

**Use case:** Developer receives poorly-written ADO story and needs to improve it

### Step-by-Step Process

#### 1. Identify Quality Issues

**Common problems:**
- Vague user type ("user" instead of specific persona)
- Missing "so that" clause (no business value)
- No Given/When/Then format
- Vague acceptance criteria ("it should work")
- Missing error scenarios
- Story too large
- Implementation details instead of requirements

#### 2. Run Refinement Command

**Command:** `/refine-story US-5001`

**Paste story content when prompted**

**AI Process:**
- Analyzes story against INVEST criteria
- Identifies specific issues
- Generates improved version with @story-expert
- Shows before/after comparison

#### 3. Review Comparison

**AI Output:**
```
# Story Refinement Analysis

## Original Story
[displays original with issues highlighted]

## Quality Assessment
- Independent: FAIL - Depends on auth system completion
- Negotiable: PASS
- Valuable: FAIL - No clear business value stated
...

## Issues Identified
1. User type too generic ("user")
2. No "so that" benefit clause
3. Acceptance criteria not testable
4. Missing error scenarios
...

## Improved Story
[displays enhanced version with proper structure]

## Key Improvements Made
1. Changed "user" to "mobile app user who forgot password"
2. Added business value: "so that I can regain access to my account"
3. Rewrote acceptance criteria in Given/When/Then format
4. Added 3 error scenarios
...
```

#### 4. Choose Next Action

**AI Asks:**
```
How would you like to proceed?

A) Use improved version for /convert-story
B) Save improved version and send suggestions to Product Owner
C) Proceed with original story anyway
D) Further refine

Please respond with A, B, C, or D.
```

**Option A** - Use Improved Version:
- Proceed directly to `/convert-story` with improved story
- Best when you have authority to adjust requirements

**Option B** - Send to PO:
- Saves improved version to `user-stories/drafts/US-5001-refined-[date].md`
- Share comparison with PO
- Wait for PO to update ADO
- Then run `/convert-story`

**Option C** - Proceed with Original:
- Continue with original despite issues
- May lead to more questions during implementation
- Use only if issues are minor or time-critical

**Option D** - Further Refine:
- Make additional adjustments
- Re-run @story-expert with specific changes

#### 5. Continue Based on Choice

**If chose A or C:**
```
/convert-story → /generate-prp → /execute-prp
```

**If chose B:**
```
Share with PO → Wait for ADO update → /convert-story → /generate-prp → /execute-prp
```

### When to Use This Workflow

**Use when:**
- ✅ Story lacks clear acceptance criteria
- ✅ No Given/When/Then format
- ✅ Missing error scenarios
- ✅ Vague or ambiguous requirements
- ✅ Story too large or too small
- ✅ Missing business value

**Benefit:**
- Catches issues BEFORE technical conversion
- Results in better INITIAL.md quality
- Reduces back-and-forth with PO during implementation

---

## Workflow 4: Technical Story

**Use case:** Developer needs to structure technical work (refactoring, bugs, tech debt) as a user story

### Step-by-Step Process

#### 1. Identify Technical Need

**Examples:**
- Refactor module for testability
- Fix performance issue
- Reduce technical debt
- Upgrade dependencies
- Improve error handling

#### 2. Run Story Command

**Command:** `/write-user-story [technical requirements]`

**Example:**
```
/write-user-story Refactor authentication module to improve testability and reduce code duplication.
Current module has 15+ methods with overlapping logic and is difficult to unit test.
```

**AI asks:**
"Is this a:
A) Business feature (for Product Owner to add to ADO)
B) Technical work (refactoring, bug, tech debt)"

**Answer:** B

#### 3. AI Generates Technical Story

**AI Process:**
- Creates user story with technical user type (e.g., "As a developer")
- Structures technical requirements as acceptance criteria
- Focuses on technical outcomes and testability
- Saves to `user-stories/technical/20251124-refactor-auth-module.md`

**Example Output:**
```markdown
### Title
Refactor Authentication Module for Testability

### User Story
As a developer working on the authentication system
I want to refactor the auth module to reduce duplication and improve testability
So that we can confidently make changes without breaking existing functionality

### Acceptance Criteria

- **Scenario 1: Reduce Method Count**
  - Given the auth module currently has 15+ methods
  - When refactoring is complete
  - Then module has ≤8 public methods with clear single responsibilities
  - And all redundant code is eliminated

- **Scenario 2: Improve Test Coverage**
  - Given current auth module has <50% test coverage
  - When refactoring is complete
  - Then module has ≥90% test coverage
  - And all critical paths have unit tests

- **Scenario 3: Maintain Backwards Compatibility**
  - Given existing code depends on current auth module interface
  - When refactoring is complete
  - Then all existing functionality works identically
  - And no breaking changes to public API

- **Scenario 4: Extract Reusable Logic**
  - Given multiple methods share validation logic
  - When refactoring is complete
  - Then shared logic is in reusable utility functions
  - And functions are independently testable
```

#### 4. Optional: Create ADO Item

**If tracking in ADO:**
- Create Tech Debt or Bug work item
- Copy content from generated markdown
- Link to related work items

**If not tracking in ADO:**
- Proceed directly with story content

#### 5. Convert to Technical Spec

**Command:** `/convert-story`

**Paste technical story content**

**Process:**
- AI researches codebase for refactoring patterns
- Identifies files to modify
- Notes testing patterns to follow
- Generates INITIAL.md

#### 6. Continue with PRP Workflow

```
/generate-prp → /execute-prp → Technical Work Complete
```

### When to Use This Workflow

**Use for:**
- ✅ Refactoring without PO involvement
- ✅ Bug fixes needing proper structure
- ✅ Technical debt reduction
- ✅ Performance improvements
- ✅ Infrastructure upgrades
- ✅ Developer-initiated improvements

**Benefit:**
- Maintains consistent story format for all work
- Documents technical requirements clearly
- Provides testable acceptance criteria for technical work
- Integrates seamlessly with PRP workflow

---

## Decision Trees

### For Product Owners: Should I Use /write-user-story?

```
Start: Do I need to write a user story?
│
├─ Is this a complex feature with many edge cases?
│  └─ YES → Use /write-user-story ✅
│  └─ NO → Continue
│
├─ Am I new to writing user stories?
│  └─ YES → Use /write-user-story (learning tool) ✅
│  └─ NO → Continue
│
├─ Am I unsure how to structure acceptance criteria?
│  └─ YES → Use /write-user-story ✅
│  └─ NO → Continue
│
├─ Do I need to work offline (no ADO access)?
│  └─ YES → Use /write-user-story ✅
│  └─ NO → Continue
│
├─ Is this a simple, straightforward feature?
│  └─ YES → Write directly in ADO ✅
│
└─ Am I experienced and confident in my story writing?
   └─ YES → Write directly in ADO ✅
```

### For Developers: Which Command Should I Use?

```
Start: I have work to do
│
├─ Is this from a Product Owner?
│  └─ YES → Continue
│  └─ NO → Technical work → Use /write-user-story (technical) ✅
│
├─ Is there already an ADO work item?
│  └─ YES → Continue
│  └─ NO → Ask PO to create one first
│
├─ Read the ADO story. Is it well-written?
│  │
│  ├─ Check: Specific user type? → NO → Poor quality
│  ├─ Check: Clear business value? → NO → Poor quality
│  ├─ Check: Given/When/Then format? → NO → Poor quality
│  ├─ Check: Testable criteria? → NO → Poor quality
│  ├─ Check: Error scenarios covered? → NO → Poor quality
│  │
│  └─ All checks pass?
│     ├─ YES → Good story → Use /convert-story ✅
│     └─ NO → Poor story → Continue
│
├─ Story needs improvement. Do you have authority to adjust?
│  ├─ YES → Use /refine-story → Choose option A ✅
│  └─ NO → Use /refine-story → Choose option B (send to PO) ✅
```

### Decision: /refine-story Options

```
After running /refine-story:
│
├─ Can I proceed with improved version?
│  ├─ YES → Is this acceptable without PO approval?
│  │  ├─ YES → Choose A (use improved version) ✅
│  │  └─ NO → Choose B (send to PO) ✅
│  └─ NO → Continue
│
├─ Are the improvements critical for implementation?
│  ├─ YES → Choose B (must get PO approval) ✅
│  └─ NO → Continue
│
├─ Is the original story "good enough"?
│  ├─ YES → Choose C (proceed with original) ✅
│  └─ NO → Continue
│
└─ Do improvements need further adjustment?
   └─ YES → Choose D (further refine) ✅
```

---

## Command Reference

### All Story Commands

| Command | Purpose | Input | Output | Who Uses |
|---------|---------|-------|--------|----------|
| `/write-user-story` | Draft new story from requirements | Requirements text | Story markdown file | PO, Developer |
| `/refine-story` | Improve existing story | ADO-ID or story text | Before/after comparison | Developer |
| `/enrich-story-tech` | Add technical context | Story path | Technical Context section | Dev Lead |
| `/enrich-story-qa` | Add test scenarios | Story path | QA Context section | QA Lead |
| `/three-amigos-prep` | Prepare alignment meeting | Story path | Meeting agenda | Facilitator |
| `/validate-story-ready` | Check Definition of Ready | Story path | Readiness report | Any |
| `/convert-story` | Convert story to technical spec | ADO-ID | INITIAL.md | Developer |
| `/generate-prp` | Create implementation plan | INITIAL.md path | PRP file | Developer |
| `/execute-prp` | Implement step-by-step | PRP path | Code changes | Developer |

### Three Amigos Commands

| Command | Step | Owner | What It Does |
|---------|------|-------|--------------|
| `/enrich-story-tech` | 2 | Dev Lead | Researches codebase, adds API specs, data model, patterns, security |
| `/enrich-story-qa` | 3 | QA Lead | Generates test scenarios, edge cases, test data requirements |
| `/three-amigos-prep` | 4 | Facilitator | Creates meeting agenda with discussion points for 30-45 min session |
| `/validate-story-ready` | 5 | Any | Validates story against all Definition of Ready criteria |

### Command Decision Matrix

| Situation | Command to Use | Alternative |
|-----------|---------------|-------------|
| PO drafting new story | `/write-user-story` | Write in ADO directly |
| Developer received poor story | `/refine-story` | Ask PO to revise |
| Developer received good story | `/convert-story` | Use Three Amigos first (recommended) |
| Dev Lead adding technical context | `/enrich-story-tech` | N/A |
| QA Lead adding test scenarios | `/enrich-story-qa` | N/A |
| Preparing Three Amigos meeting | `/three-amigos-prep` | N/A |
| Checking if story is ready | `/validate-story-ready` | Manual DoR checklist |
| Developer has technical work | `/write-user-story` | Write INITIAL.md directly |
| Ready to implement | `/generate-prp` + `/execute-prp` | N/A |

---

## Troubleshooting

### Problem: /write-user-story generates poor quality story

**Possible causes:**
- Input requirements too vague
- AI didn't ask enough clarifying questions
- Missing important business context

**Solutions:**
1. Provide more detailed requirements upfront
2. Answer all AI questions thoroughly
3. Review and manually edit the generated story
4. Re-run with more specific requirements

---

### Problem: /refine-story says "story is already high quality" but I disagree

**Possible causes:**
- Story meets technical criteria but not business needs
- Specific business rules AI doesn't understand
- Domain-specific requirements not captured

**Solutions:**
1. Manually edit the story
2. Add business context AI might not know
3. Consult with PO for clarification
4. Use /write-user-story to regenerate from scratch

---

### Problem: /convert-story generates weak INITIAL.md

**Possible causes:**
- User story quality is poor
- Missing acceptance criteria
- No error scenarios
- Vague requirements

**Solutions:**
1. First run `/refine-story` to improve story quality
2. Add more specific acceptance criteria
3. Include error scenarios
4. Re-run `/convert-story` with improved story

---

### Problem: PO doesn't want to use /write-user-story

**This is OK!**
- `/write-user-story` is OPTIONAL
- POs can continue writing directly in ADO
- Developers can use `/refine-story` to improve stories if needed

**No pressure to change workflow if current process works well.**

---

### Problem: Story too large after /write-user-story

**Solutions:**
1. Break requirements into smaller pieces
2. Run `/write-user-story` separately for each piece
3. AI should detect if story is too large and suggest splitting
4. Each story should be 1-3 days of work

---

### Problem: AI asks too many questions in /write-user-story

**This is a feature!**
- More questions = better story quality
- Better to answer questions now than during implementation
- Skip questions if you want (but story quality may suffer)

**If truly too many:**
- Provide more complete initial requirements
- AI will ask fewer clarifying questions

---

## Best Practices

### For Product Owners

1. **Try /write-user-story** for your next complex feature
2. **Answer all AI questions** thoroughly
3. **Review generated stories** critically
4. **Still create ADO work items** (no automatic sync)
5. **Use as learning tool** to improve your story-writing skills

### For Developers

1. **Check story quality** before /convert-story
2. **Use /refine-story** when stories are poor
3. **Communicate with PO** when refinement is needed
4. **Structure technical work** with /write-user-story
5. **Document technical requirements** as acceptance criteria

### For Teams

1. **Make /write-user-story optional** for POs
2. **Require /refine-story** when stories are poor
3. **Track metrics** (story quality, clarifying questions, rework)
4. **Share training examples** from user-stories/training/
5. **Continuously improve** based on what works

---

## Related Documentation

- **Three Amigos Guide:** `.claude/docs/three-amigos-guide.md` - Complete guide to the Three Amigos collaboration process
- **Definition of Ready:** `.claude/DEFINITION-OF-READY.md` - Full DoR criteria checklist
- **For POs:** `.claude/PRODUCT-OWNER-GUIDE.md` - Complete guide to writing effective user stories
- **For Developers:** `.claude/CLAUDE.md` - Full Context Engineering workflow
- **Quick Reference:** `.claude/docs/story-commands-quick-reference.md` - One-page command cheat sheet
- **Examples:** `user-stories/training/` - Real examples of good and poor stories
- **Templates:** `.claude/templates/` - Blank templates for manual story writing

---

**Last Updated:** 2025-11-24
**Version:** 2.0 (Added Three Amigos workflow)
