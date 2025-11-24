---
description: Validate user story meets Definition of Ready criteria
argument-hint: <story-path>
model: claude-sonnet-4-5-20250929
---

# Validate Story Readiness

You are validating whether a user story meets all **Definition of Ready (DoR)** criteria and is ready for team grooming and estimation.

**Purpose:** Systematically check all readiness criteria and generate a clear pass/fail report with specific gaps identified.

**Input:** Path to user story markdown file: `$ARGUMENTS`

**Reference:** See `.claude/DEFINITION-OF-READY.md` for full criteria documentation.

---

## Phase 1: Load Story

**Read the story file:**
```
$ARGUMENTS
```

If no path provided:
```
Please provide the path to a user story file.

Usage: /validate-story-ready user-stories/drafts/20251124-feature-name.md
```

---

## Phase 2: Extract and Analyze Sections

Parse the story file to identify:

1. **Metadata** (frontmatter if present)
2. **Title**
3. **User Story** (As a... I want... So that...)
4. **Acceptance Criteria** (scenarios)
5. **Technical Context** (from /enrich-story-tech)
6. **QA Context** (from /enrich-story-qa)
7. **Additional Notes**

---

## Phase 3: Validate Each DoR Category

### 3.1 User Story Structure (PO Responsibility)

Check each criterion and record pass/fail:

| Criterion | Check | Result |
|-----------|-------|--------|
| User type is specific | Is it more than just "user"? | PASS/FAIL |
| Capability is clear | Single, focused action? | PASS/FAIL |
| Business value stated | Has "so that" clause? | PASS/FAIL |
| Appropriately sized | Estimated 1-3 days? | PASS/FAIL/UNKNOWN |
| Independent | No blocking dependencies? | PASS/FAIL/UNKNOWN |

### 3.2 Acceptance Criteria (PO + QA Responsibility)

| Criterion | Check | Result |
|-----------|-------|--------|
| Minimum 3 scenarios | Count scenarios >= 3 | PASS/FAIL |
| Given/When/Then format | All scenarios use BDD? | PASS/FAIL |
| Scenarios are testable | QA can verify each? | PASS/FAIL |
| Edge cases covered | Error/boundary scenarios? | PASS/FAIL |
| Performance requirements | If needed, are they stated? | PASS/FAIL/N/A |

### 3.3 Technical Context (Dev Lead Responsibility)

| Criterion | Check | Result |
|-----------|-------|--------|
| Technical Context section exists | Section present? | PASS/FAIL |
| Technical feasibility confirmed | Stated as feasible? | PASS/FAIL |
| API endpoints identified | Endpoints listed? | PASS/FAIL/N/A |
| Data model understood | Tables/fields listed? | PASS/FAIL/N/A |
| Dependencies identified | Dependencies listed? | PASS/FAIL |
| Security considerations noted | Security section exists? | PASS/FAIL |
| Similar patterns referenced | References provided? | PASS/FAIL |

### 3.4 QA Context (QA Lead Responsibility)

| Criterion | Check | Result |
|-----------|-------|--------|
| QA Context section exists | Section present? | PASS/FAIL |
| Test scenarios documented | Test scenarios listed? | PASS/FAIL |
| Test data requirements known | Test data specified? | PASS/FAIL |
| Integration points identified | Integration tests listed? | PASS/FAIL/N/A |
| Accessibility requirements noted | If applicable, noted? | PASS/FAIL/N/A |

### 3.5 Three Amigos Alignment

| Criterion | Check | Result |
|-----------|-------|--------|
| Three Amigos session completed | Noted in story? | PASS/FAIL/UNKNOWN |
| All questions resolved | No open questions? | PASS/FAIL |
| Scope is agreed | Clear in/out of scope? | PASS/FAIL |
| Risks identified | Risks documented? | PASS/FAIL |

---

## Phase 4: Calculate Readiness Score

**Scoring:**
- Each PASS = 1 point
- Each FAIL = 0 points
- N/A criteria are excluded from total

**Categories:**
- **User Story Structure:** X/5 points
- **Acceptance Criteria:** X/5 points
- **Technical Context:** X/7 points
- **QA Context:** X/5 points
- **Three Amigos:** X/4 points

**Total:** X/26 points (XX%)

**Readiness Threshold:**
- **READY** (Green): 90%+ with no FAIL in critical criteria
- **NEARLY READY** (Yellow): 75-89% or minor gaps
- **NOT READY** (Red): Below 75% or critical gaps

**Critical Criteria (must pass):**
- User type is specific
- Business value stated
- Minimum 3 scenarios
- Given/When/Then format
- Technical Context exists
- QA Context exists

---

## Phase 5: Generate Readiness Report

```markdown
# Story Readiness Report

**Story:** [Title]
**File:** [Path]
**Validated:** [Date/Time]

---

## Overall Status: [READY ✅ / NEARLY READY ⚠️ / NOT READY ❌]

**Readiness Score:** [XX]/[YY] ([ZZ]%)

---

## Category Results

### 1. User Story Structure [X/5] [✅/⚠️/❌]

| Criterion | Status | Notes |
|-----------|--------|-------|
| User type is specific | ✅/❌ | [Detail] |
| Capability is clear | ✅/❌ | [Detail] |
| Business value stated | ✅/❌ | [Detail] |
| Appropriately sized | ✅/❌/? | [Detail] |
| Independent | ✅/❌/? | [Detail] |

### 2. Acceptance Criteria [X/5] [✅/⚠️/❌]

| Criterion | Status | Notes |
|-----------|--------|-------|
| Minimum 3 scenarios | ✅/❌ | Found: [N] scenarios |
| Given/When/Then format | ✅/❌ | [X]/[Y] use correct format |
| Scenarios are testable | ✅/❌ | [Detail] |
| Edge cases covered | ✅/❌ | [Detail] |
| Performance requirements | ✅/❌/N/A | [Detail] |

### 3. Technical Context [X/7] [✅/⚠️/❌]

| Criterion | Status | Notes |
|-----------|--------|-------|
| Section exists | ✅/❌ | [Present/Missing] |
| Feasibility confirmed | ✅/❌ | [Detail] |
| API endpoints identified | ✅/❌/N/A | [Detail] |
| Data model understood | ✅/❌/N/A | [Detail] |
| Dependencies identified | ✅/❌ | [Detail] |
| Security noted | ✅/❌ | [Detail] |
| Patterns referenced | ✅/❌ | [Detail] |

### 4. QA Context [X/5] [✅/⚠️/❌]

| Criterion | Status | Notes |
|-----------|--------|-------|
| Section exists | ✅/❌ | [Present/Missing] |
| Test scenarios documented | ✅/❌ | Found: [N] scenarios |
| Test data requirements | ✅/❌ | [Detail] |
| Integration points | ✅/❌/N/A | [Detail] |
| Accessibility requirements | ✅/❌/N/A | [Detail] |

### 5. Three Amigos Alignment [X/4] [✅/⚠️/❌]

| Criterion | Status | Notes |
|-----------|--------|-------|
| Session completed | ✅/❌/? | [Detail] |
| Questions resolved | ✅/❌ | [Detail] |
| Scope agreed | ✅/❌ | [Detail] |
| Risks identified | ✅/❌ | [Detail] |

---

## Gaps to Address

### Critical Gaps (Must Fix)
[List any failed critical criteria]

1. **[Criterion]:** [What's wrong and how to fix]
2. **[Criterion]:** [What's wrong and how to fix]

### Minor Gaps (Should Fix)
[List any failed non-critical criteria]

1. **[Criterion]:** [What's wrong and how to fix]

### Recommendations
[List any improvements that would make the story better even if passing]

---

## Actions Required

[Based on gaps, generate specific action items]

**If NOT READY:**
- [ ] [Specific action 1] - Owner: [PO/Dev Lead/QA Lead]
- [ ] [Specific action 2] - Owner: [PO/Dev Lead/QA Lead]

**Commands to run:**
- `/enrich-story-tech [path]` - If Technical Context missing
- `/enrich-story-qa [path]` - If QA Context missing
- `/refine-story [path]` - If story structure has issues
- `/three-amigos-prep [path]` - If alignment session not done

---

## AI Implementation Readiness

**Separate from DoR, assess readiness for AI code generation:**

| Factor | Status | Notes |
|--------|--------|-------|
| Explicit requirements | ✅/⚠️/❌ | [Are requirements explicit or implicit?] |
| Error cases specified | ✅/⚠️/❌ | [Are all error cases documented?] |
| Technical patterns | ✅/⚠️/❌ | [Are code patterns referenced?] |
| API contracts | ✅/⚠️/❌ | [Are API formats specified?] |
| Test scenarios | ✅/⚠️/❌ | [Can AI generate tests from scenarios?] |

**AI Implementation Confidence:** [High/Medium/Low]

---

## Next Steps

[Generate appropriate next steps based on status]

**If READY:**
```
✅ This story is READY for team grooming!

Next steps:
1. Add to sprint backlog
2. Present at team grooming meeting
3. Team estimates story points
4. Commit to sprint

When ready to implement:
/convert-story [ADO-ID or story path]
```

**If NEARLY READY:**
```
⚠️ This story is NEARLY READY but has minor gaps.

Required actions:
[List specific actions]

After addressing gaps, run:
/validate-story-ready [path]
```

**If NOT READY:**
```
❌ This story is NOT READY for grooming.

Critical gaps must be addressed:
[List critical gaps]

Commands to run:
[List specific commands based on gaps]

After addressing ALL gaps, run:
/validate-story-ready [path]
```
```

---

## Phase 6: Update Story Metadata

If story has frontmatter, update validation status:

```yaml
---
# ... existing metadata ...
validation:
  last_validated: [date]
  status: ready|nearly_ready|not_ready
  score: XX/YY
  gaps: [list of gap categories]
---
```

---

## Quick Validation Mode

If user adds `--quick` flag, provide abbreviated output:

```
## Quick Validation: [Story Title]

Status: [READY ✅ / NEARLY READY ⚠️ / NOT READY ❌]
Score: [XX]%

Critical Gaps:
- [Gap 1 or "None"]
- [Gap 2]

Run `/validate-story-ready [path]` for full report.
```

---

## Integration with Workflow

This command is Step 5 in the Three Amigos workflow:

```
Step 1: /write-user-story  → PO creates draft         ✓
Step 2: /enrich-story-tech → Dev Lead adds technical  ✓
Step 3: /enrich-story-qa   → QA Lead adds test        ✓
Step 4: /three-amigos-prep → Prepare alignment session ✓
Step 5: /validate-story-ready → Check all DoR criteria ← YOU ARE HERE

If READY → Proceed to team grooming
If NOT READY → Address gaps, re-validate
```

---

**Output:** Comprehensive readiness report with pass/fail status, gaps identified, and specific actions to address any issues.
