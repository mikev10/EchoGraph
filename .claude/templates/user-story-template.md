---
created: [YYYY-MM-DD]
status: draft
category: business
converted_to_ado: false
ado_id: null
sprint: null
story_points: null
---

# User Story Template (Business Feature)

**Instructions:** Fill in this template when writing a business user story manually. Delete these instructions before saving.

**Tip:** Consider using `/write-user-story` command for AI assistance instead of manual drafting.

---

### Title
[Action-oriented title describing the capability - e.g., "User Login with Email and Password"]

### User Story
As a [specific user type - be specific, not just "user"]
I want [specific capability or functionality]
So that [clear business value or benefit]

**Examples:**
- As a mobile app user / As a registered user / As an admin user
- As a first-time visitor to the website
- As a mobile app user who forgot my password

### Acceptance Criteria

- **Scenario 1: [Clear scenario title for happy path]**
  - Given [starting context or precondition]
  - When [user action or trigger]
  - Then [expected outcome with specific, measurable result]
  - And [additional outcome if needed]

- **Scenario 2: [Key variation or alternative path]**
  - Given [context]
  - When [action]
  - Then [outcome]

- **Scenario 3: [Error case or validation]**
  - Given [error condition]
  - When [action]
  - Then [error message or handling]

- **Scenario 4: [Additional error or edge case]**
  - Given [context]
  - When [action]
  - Then [outcome]

**Guidelines:**
- Include 3-6 scenarios total
- Cover: happy path + key variations + critical errors
- Be specific with error messages
- Use representative examples, not overly specific data
- Each scenario should be independently testable

### Additional Notes

**Dependencies:**
- [Other stories, systems, or prerequisites needed before this story]
- [Backend APIs that must be ready]
- [Design assets or mockups needed]

**Security:**
- [Authentication/authorization requirements]
- [Data protection considerations]
- [Input validation needs]

**User Experience:**
- [Loading states required]
- [Error handling approaches]
- [Accessibility requirements]
- [Responsive design considerations]

**Testing:**
- [Unit tests needed]
- [Integration tests needed]
- [E2E test scenarios]
- [Edge cases to test]

**Technical Constraints:**
- [Platform-specific requirements (iOS, Android, web)]
- [Performance requirements]
- [Compatibility requirements]
- [Known limitations or gotchas]

---

## Checklist Before Submitting

Use this checklist to ensure your story is complete:

- [ ] User type is specific (not just "user")
- [ ] Business value ("so that" clause) is clear
- [ ] 3-6 acceptance criteria scenarios included
- [ ] All scenarios use Given/When/Then format
- [ ] Scenarios cover happy path + variations + errors
- [ ] Formatting correct (bold scenario titles only, not keywords)
- [ ] No implementation details (no specific libraries or code)
- [ ] Story is appropriately sized (1-3 days, 3-8 story points)
- [ ] All criteria are testable
- [ ] Dependencies are noted
- [ ] Security considerations are included

---

## Related Resources

- **Training examples:** `user-stories/training/example-good-*.md`
- **Product Owner guide:** `docs/optional/PRODUCT_OWNER_GUIDE.md`
- **AI assistance:** Use `/write-user-story` command for help

---

**Original Requirements** _(delete if not applicable)_

[If converting from informal requirements, paste them here for reference]
