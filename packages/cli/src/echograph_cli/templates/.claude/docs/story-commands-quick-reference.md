# Story Commands Quick Reference

**One-page cheat sheet for Context Engineering user story commands**

---

## Commands Overview

### Story Creation Commands

| Command | Who | When | Input | Output |
|---------|-----|------|-------|--------|
| `/write-user-story` | PO, Dev | Draft new story | Requirements | Markdown file |
| `/refine-story` | Dev | Improve poor story | ADO-ID or text | Before/after comparison |
| `/convert-story` | Dev | Create tech spec | ADO-ID | SPEC.md |

### Three Amigos Commands (Recommended)

| Command | Who | When | Input | Output |
|---------|-----|------|-------|--------|
| `/enrich-story-tech` | Dev Lead | After PO drafts story | Story path | Technical Context section |
| `/enrich-story-qa` | QA Lead | After tech enrichment | Story path | QA Context section |
| `/three-amigos-prep` | Facilitator | Before alignment meeting | Story path | Meeting agenda |
| `/validate-story-ready` | Any | Before grooming | Story path | Readiness report |

---

## `/write-user-story` - Draft New Story

**Purpose:** Create well-structured user story from requirements

**Usage:**
```
/write-user-story Users need to reset their password via email
```

**Process:**
1. AI asks clarifying questions
2. You answer with details
3. AI generates structured story
4. Saved to `user-stories/drafts/` or `user-stories/technical/`

**When to use:**
- ✅ Complex features needing careful planning
- ✅ Learning to write better stories
- ✅ Uncertain how to structure acceptance criteria
- ✅ Offline planning (no ADO access)
- ✅ Technical work without PO

**When to skip:**
- ❌ Simple straightforward stories
- ❌ Experienced PO with clear requirements
- ❌ Time-sensitive (ADO direct is faster)

**Output example:**
```
✓ User story created: user-stories/drafts/20251124-password-reset-via-email.md
✓ Status: Draft (ready for review)

Next steps:
1. Review and refine
2. Create ADO work item
3. Run /convert-story when ready
```

---

## `/refine-story` - Improve Existing Story

**Purpose:** Analyze and improve poorly-written user stories

**Usage:**
```
/refine-story US-4523
[Paste story content when prompted]
```

**Process:**
1. AI analyzes story against INVEST criteria
2. Identifies specific quality issues
3. Generates improved version
4. Shows before/after comparison
5. Asks what to do next

**When to use:**
- ✅ Vague user type or missing business value
- ✅ No Given/When/Then format
- ✅ Missing error scenarios
- ✅ Ambiguous requirements
- ✅ Story too large or too small

**Options after refinement:**
- **A)** Use improved version for /convert-story
- **B)** Save and send suggestions to PO
- **C)** Proceed with original anyway
- **D)** Further refine with changes

**Quality checks:**
| Criteria | Check |
|----------|-------|
| Independent | Can develop without dependencies? |
| Negotiable | Clear requirements, flexible implementation? |
| Valuable | Business value stated? |
| Estimable | Enough detail to estimate? |
| Small | Fits in 1-3 days? |
| Testable | Clear pass/fail criteria? |

---

## `/convert-story` - Create Technical Spec

**Purpose:** Convert user story to technical feature request (SPEC.md)

**Usage:**
```
/convert-story US-4523
[Paste story when prompted]
```

**Process:**
1. AI researches codebase for patterns
2. Finds relevant APIs, libraries, files
3. Asks technical questions
4. Generates SPEC.md with examples and documentation

**When to use:**
- ✅ After story is written/refined
- ✅ Ready to start implementation
- ✅ Story quality is good

**Output:** `PRPs/feature-requests/US-4523-feature-name-SPEC.md`

**Next steps:** `/generate-prp` → `/execute-prp`

---

## Three Amigos Commands

### `/enrich-story-tech` - Add Technical Context

**Purpose:** Dev Lead adds technical specifications to story

**Usage:**
```
/enrich-story-tech user-stories/drafts/20251124-password-reset.md
```

**What it adds:**
- Architecture approach and component mapping
- API specifications (endpoints, request/response)
- Data model and migration requirements
- Dependencies and prerequisites
- Security considerations
- Technical risks and patterns

**When to use:** After PO creates story, before QA enrichment

---

### `/enrich-story-qa` - Add Test Scenarios

**Purpose:** QA Lead adds comprehensive test coverage

**Usage:**
```
/enrich-story-qa user-stories/drafts/20251124-password-reset.md
```

**What it adds:**
- Happy path test scenarios
- Negative/error test scenarios
- Boundary test scenarios
- Edge case scenarios
- Test data requirements
- Accessibility checklist
- Regression impact analysis

**When to use:** After tech enrichment, before Three Amigos meeting

---

### `/three-amigos-prep` - Prepare Alignment Meeting

**Purpose:** Generate agenda for 30-45 min alignment session

**Usage:**
```
/three-amigos-prep user-stories/drafts/20251124-password-reset.md
```

**What it generates:**
- Meeting agenda with time allocations
- Role-specific prep notes (PO, Dev Lead, QA Lead)
- Critical discussion items to resolve
- Questions that need answers
- Risk assessment

**When to use:** Before scheduling Three Amigos alignment meeting

---

### `/validate-story-ready` - Check Definition of Ready

**Purpose:** Validate story meets all DoR criteria

**Usage:**
```
/validate-story-ready user-stories/drafts/20251124-password-reset.md
```

**What it checks:**
- User Story Structure (5 criteria)
- Acceptance Criteria (5 criteria)
- Technical Context (7 criteria)
- QA Context (5 criteria)
- Three Amigos Alignment (4 criteria)

**Status outcomes:**
- **READY** (90%+): Proceed to team grooming
- **NEARLY READY** (75-89%): Address minor gaps
- **NOT READY** (<75%): Address critical gaps

**When to use:** After Three Amigos session, before team grooming

---

## Decision Trees

### For Product Owners

```
Need to write story?
├─ Complex feature? → /write-user-story
├─ New to stories? → /write-user-story (learning)
├─ Unsure of format? → /write-user-story
└─ Simple & experienced? → Write in ADO directly
```

### For Developers

```
Received story from PO?
├─ Check quality:
│  ├─ Specific user type? ✓
│  ├─ Clear business value? ✓
│  ├─ Given/When/Then format? ✓
│  ├─ Testable criteria? ✓
│  └─ Error scenarios? ✓
│
├─ All checks pass? → /convert-story
└─ Quality issues? → /refine-story
   ├─ Can adjust? → Choose A (use improved)
   └─ Need PO approval? → Choose B (send to PO)
```

### For Technical Work

```
Technical work (refactoring, bug, tech debt)?
├─ /write-user-story → Select "Technical"
├─ Saved to user-stories/technical/
├─ Optional: Create ADO item
└─ /convert-story → /generate-prp → /execute-prp
```

---

## Complete Workflows

### Recommended: Three Amigos Workflow
```
/write-user-story → /enrich-story-tech → /enrich-story-qa → /three-amigos-prep
     │                    │                    │                    │
     ▼                    ▼                    ▼                    ▼
  PO drafts          Dev Lead adds        QA Lead adds       30-45 min
   story              tech context        test scenarios      meeting
                                                                 │
                                                                 ▼
                            /validate-story-ready → Team Grooming → /convert-story → PRP
```

### Workflow 1: PO Drafting (Simple)
```
Requirements → /write-user-story → Review → Create ADO → Dev runs /convert-story → PRP
```

### Workflow 2: Direct ADO
```
PO writes in ADO → Dev checks quality → /convert-story → PRP
```

### Workflow 3: Story Refinement
```
Poor ADO story → /refine-story → Use improved or send to PO → /convert-story → PRP
```

### Workflow 4: Technical Story
```
Tech need → /write-user-story (technical) → /convert-story → PRP
```

---

## File Locations

| Type | Location | Purpose |
|------|----------|---------|
| **Drafts** | `user-stories/drafts/` | PO pre-ADO drafts |
| **Technical** | `user-stories/technical/` | Dev technical stories |
| **Training** | `user-stories/training/` | Examples and learning |
| **Templates** | `.claude/templates/` | Blank templates |
| **SPEC.md** | `PRPs/feature-requests/` | Technical specs |

---

## Story Quality Checklist

Before creating ADO item or running /convert-story:

- [ ] Specific user type (not just "user")
- [ ] Clear business value ("so that" clause)
- [ ] 3-6 acceptance criteria scenarios
- [ ] Given/When/Then format for all scenarios
- [ ] Covers happy path + variations + errors
- [ ] Formatting correct (bold scenario titles only)
- [ ] No implementation details
- [ ] Story size 1-3 days (3-8 points)
- [ ] All criteria testable
- [ ] Dependencies noted
- [ ] Security considered

---

## Common Mistakes to Avoid

❌ Generic user type: "user"
✅ Specific: "mobile app user who forgot password"

❌ No business value
✅ Clear "so that" clause

❌ Vague criteria: "it works correctly"
✅ Specific: "Then I see confirmation message within 2 seconds"

❌ No error scenarios
✅ Include validation errors, network errors, edge cases

❌ Implementation details: "Use React Query for API calls"
✅ Requirements: "Data refreshes automatically every 5 minutes"

---

## Story Formatting Rules

### User Story Format
```
✅ CORRECT:
As a mobile app user
I want to login with email and password
So that I can access my account securely

❌ WRONG:
As a **mobile app user**,
I want **to login**
So that **I can access my account**.
```

### Acceptance Criteria Format
```
✅ CORRECT:
- **Scenario 1: Successful Login**
  - Given I have valid credentials
  - When I tap "Login"
  - Then I see my dashboard

❌ WRONG:
### Scenario 1: Successful Login
**Given** I have valid credentials
**When** I tap "Login"
**Then** I see my dashboard
```

---

## Getting Help

| Resource | Location | Use For |
|----------|----------|---------|
| **Three Amigos guide** | `docs/optional/THREE_AMIGOS_GUIDE.md` | Complete Three Amigos process |
| **Definition of Ready** | `docs/optional/DEFINITION_OF_READY.md` | DoR criteria checklist |
| **PO guide** | `docs/optional/PRODUCT_OWNER_GUIDE.md` | Writing effective stories |
| **Training examples** | `user-stories/training/` | Learning from examples |
| **Templates** | `.claude/templates/` | Blank story templates |
| **CLAUDE.md** | `.claude/CLAUDE.md` | Full CE workflow |

---

## Tips for Success

### For Product Owners
1. Try `/write-user-story` for complex features
2. Answer AI questions thoroughly
3. Review generated stories critically
4. Still create ADO work items (no auto-sync)
5. Use as learning tool to improve skills

### For Developers
1. Check story quality before `/convert-story`
2. Use `/refine-story` when stories are poor
3. Communicate with PO about quality
4. Structure technical work with `/write-user-story`
5. Don't skip quality checks to save time

### For Teams
1. Make `/write-user-story` optional for POs
2. Require quality check before `/convert-story`
3. Track metrics (story quality, questions, rework)
4. Share training examples regularly
5. Continuously improve based on feedback

---

**Last Updated:** 2025-11-24
**Version:** 2.0 (Added Three Amigos commands)
