---
created: 2025-11-24
status: training_example
category: business
purpose: Example of POOR user story - shows common mistakes to avoid
---

# Training Example: Poor User Story (What NOT to Do)

**Purpose:** This is an example of a POORLY WRITTEN user story with common mistakes. Compare this to `example-improved-story.md` to see how it should be fixed.

**⚠️ DO NOT USE THIS AS A TEMPLATE! This is an example of what to AVOID.**

---

## The Poor Story

### Title
Profile

### User Story
As a user I want to update my profile

###Accept Criteria
- User can update profile
- Changes are saved
- Profile works correctly

---

## What's Wrong With This Story

### ❌ Issue 1: Vague Title
**Problem:** "Profile" - what about the profile?
**Impact:** Unclear what functionality this covers

### ❌ Issue 2: Generic User Type
**Problem:** "As a user" - which user? All users? Specific role?
**Impact:** Unclear who this is for

### ❌ Issue 3: No Business Value
**Problem:** No "so that" clause
**Impact:** Why is this important? What's the benefit?

### ❌ Issue 4: Incomplete User Story
**Problem:** "I want to update my profile" - update what? How?
**Impact:** Too vague to implement

### ❌ Issue 5: Typo in Header
**Problem:** "Accept Criteria" instead of "Acceptance Criteria"
**Impact:** Looks unprofessional

### ❌ Issue 6: Not Testable
**Problem:** "User can update profile" - how do we test this?
**Impact:** QA cannot verify

### ❌ Issue 7: No Given/When/Then
**Problem:** No structured format
**Impact:** Ambiguous, not specific

### ❌ Issue 8: Vague Outcomes
**Problem:** "Changes are saved" - where? when? how do we know?
**Impact:** Unclear success criteria

### ❌ Issue 9: Meaningless Criterion
**Problem:** "Profile works correctly" - what does this even mean?
**Impact:** Completely untestable

### ❌ Issue 10: No Error Scenarios
**Problem:** Only mentions happy path
**Impact:** What happens when things go wrong?

### ❌ Issue 11: No Specifics
**Problem:** No mention of WHAT fields can be updated
**Impact:** Scope is unclear

### ❌ Issue 12: No Additional Context
**Problem:** No notes about dependencies, constraints, or requirements
**Impact:** Missing critical information

---

## INVEST Criteria Check

| Criteria | Pass? | Reason |
|----------|-------|--------|
| **Independent** | ❌ FAIL | Unclear what this depends on |
| **Negotiable** | ⚠️ UNCLEAR | Too vague to determine |
| **Valuable** | ❌ FAIL | No business value stated |
| **Estimable** | ❌ FAIL | Too vague to estimate |
| **Small** | ⚠️ UNCLEAR | Could be 1 day or 10 days |
| **Testable** | ❌ FAIL | No clear pass/fail criteria |

**Result:** This story FAILS quality standards.

---

## What Developers Will Ask

If a developer receives this story, they'll need to ask:

1. **Scope questions:**
   - What profile fields can be updated?
   - Name? Email? Phone? Photo? All of them?
   - Can users update everything or only certain fields?

2. **User type questions:**
   - Is this for all users or specific user types?
   - Are there permission restrictions?

3. **Business value questions:**
   - Why do users need to update their profile?
   - What problem does this solve?
   - What's the priority?

4. **Validation questions:**
   - Are there field validations?
   - Email format? Phone format?
   - Required vs optional fields?

5. **Error handling questions:**
   - What if update fails?
   - What if network is down?
   - What if data is invalid?

6. **Success criteria questions:**
   - How do we know it "works correctly"?
   - What confirms changes are saved?
   - Should there be confirmation message?

**All of these questions should be answered in the story BEFORE development starts.**

---

## Impact of Poor Quality

### On Development
- Delays while waiting for clarification
- Risk of building wrong thing
- Increased back-and-forth with PO
- Frustration and low morale

### On Testing
- QA cannot write test cases
- Unclear what to verify
- May miss critical scenarios
- Testing delays development

### On Project
- Increased rework
- Missed deadlines
- Lower quality deliverables
- Reduced team velocity

---

## How to Fix This Story

See `example-improved-story.md` for the properly written version with:
- Specific user type
- Clear business value
- Detailed Given/When/Then scenarios
- Comprehensive acceptance criteria
- Error handling
- Additional context

**This same vague requirement becomes a high-quality, implementable story!**

---

## Red Flags to Watch For

When reviewing a story, these are warning signs of poor quality:

- ❌ User type is just "user" (not specific)
- ❌ No "so that" clause (no business value)
- ❌ Acceptance criteria like "it should work"
- ❌ No Given/When/Then format
- ❌ Only 1-2 acceptance criteria
- ❌ Only happy path, no errors
- ❌ Vague words like "correctly", "properly", "successfully"
- ❌ Missing context about constraints or dependencies
- ❌ Cannot estimate story points confidently
- ❌ Unclear what "done" means

**If you see 3 or more red flags, use `/refine-story` before `/convert-story`!**

---

## For Product Owners

**If you wrote a story like this:**
- Don't worry! This is a learning opportunity
- Use `/write-user-story` to see how AI structures it
- Compare to the good examples
- Learn from the differences

**Key lesson:** More detail upfront = less rework later

---

## For Developers

**If you receive a story like this:**
1. Run `/refine-story` to analyze issues
2. Review the improved version
3. Decide whether to:
   - Use improved version (if you have authority)
   - Send suggestions to PO (if you need approval)
4. Do NOT proceed directly to `/convert-story` with poor quality

**Your responsibility:** Catch quality issues BEFORE implementation, not during or after.

---

## Related Examples

- `example-improved-story.md` - See this story done RIGHT ✅
- `example-good-login-story.md` - Another good example
- `example-good-password-reset-story.md` - Complex story done well
- `example-technical-story.md` - Technical work as user story

---

**Last Updated:** 2025-11-24
