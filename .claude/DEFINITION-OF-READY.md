# Definition of Ready (DoR)

A user story is **Ready** when it meets all the criteria below. Stories that don't meet these criteria should not enter sprint planning or be estimated by the team.

## Purpose

The Definition of Ready ensures that:
- Stories are clear enough for accurate estimation
- Dev and QA have what they need to start work immediately
- The Three Amigos have aligned on requirements before grooming
- AI-assisted implementation has sufficient context for success

## Readiness Criteria Checklist

### 1. User Story Structure (PO Responsibility)

- [ ] **User type is specific** - Not just "user" but a specific persona (e.g., "mobile app user with Premium subscription")
- [ ] **Capability is clear** - Single, focused action the user wants to perform
- [ ] **Business value is stated** - Clear "so that" clause explaining why this matters
- [ ] **Story is appropriately sized** - 1-3 days of work (3-8 story points)
- [ ] **Story is independent** - Can be developed without blocking dependencies

### 2. Acceptance Criteria (PO + QA Responsibility)

- [ ] **Minimum 3 scenarios** - At least: happy path, one variation, one error case
- [ ] **Given/When/Then format** - All scenarios use structured BDD format
- [ ] **Scenarios are testable** - QA can verify each scenario independently
- [ ] **Edge cases covered** - Boundary conditions and error states specified
- [ ] **Performance requirements stated** - If applicable, measurable performance criteria included

### 3. Technical Context (Dev Lead Responsibility)

- [ ] **Technical feasibility confirmed** - Dev Lead has reviewed and confirmed buildable
- [ ] **API endpoints identified** - If applicable, specific endpoints documented
- [ ] **Data model understood** - Relevant database tables/fields identified
- [ ] **Dependencies identified** - Other stories or systems this depends on are listed
- [ ] **Security considerations noted** - Auth, validation, data protection requirements stated
- [ ] **Similar patterns referenced** - Links to existing code patterns to follow

### 4. Test Readiness (QA Lead Responsibility)

- [ ] **Test scenarios documented** - Comprehensive test cases for all acceptance criteria
- [ ] **Test data requirements known** - What data is needed to test this story
- [ ] **Integration points identified** - External systems that need test coverage
- [ ] **Accessibility requirements noted** - If applicable, a11y testing criteria specified

### 5. Three Amigos Alignment

- [ ] **Three Amigos session completed** - PO, Dev Lead, and QA Lead have met
- [ ] **All questions resolved** - No open questions blocking development
- [ ] **Scope is agreed** - All parties understand what's in/out of scope
- [ ] **Risks identified** - Technical or business risks documented

## Quick Reference: Who Adds What

| Section | Primary Owner | AI Assist Command |
|---------|---------------|-------------------|
| User Story & Business Context | Product Owner | `/write-user-story` |
| Acceptance Criteria (initial) | Product Owner | `/write-user-story` |
| Technical Context | Dev Lead | `/enrich-story-tech` |
| Test Scenarios & Edge Cases | QA Lead | `/enrich-story-qa` |
| Final Validation | All Three | `/validate-story-ready` |

## Workflow Integration

```
┌─────────────────────────────────────────────────────────────────────┐
│                        STORY CREATION FLOW                           │
└─────────────────────────────────────────────────────────────────────┘

Step 1: PO Creates Draft
├── /write-user-story "requirements..."
├── AI asks clarifying questions
├── Story saved to user-stories/drafts/
└── Checklist: Section 1 & 2 (partial) complete

Step 2: Dev Lead Enriches
├── /enrich-story-tech [story-path]
├── AI researches codebase for patterns, APIs
├── Dev Lead adds technical context
└── Checklist: Section 3 complete

Step 3: QA Lead Enriches
├── /enrich-story-qa [story-path]
├── AI generates comprehensive test scenarios
├── QA Lead reviews and adds domain-specific cases
└── Checklist: Section 2 (complete) & 4 complete

Step 4: Three Amigos Session
├── /three-amigos-prep [story-path]
├── 30-60 min alignment meeting
├── Resolve questions, confirm scope
└── Checklist: Section 5 complete

Step 5: Validate Ready
├── /validate-story-ready [story-path]
├── AI checks all DoR criteria
├── Generates readiness report
└── Story is READY for grooming

Step 6: Team Grooming
├── Story presented to full team
├── Team estimates with confidence
└── Story committed to sprint
```

## What "Not Ready" Looks Like

A story is **NOT ready** if any of these are true:

- User type is generic ("As a user...")
- No "so that" clause (missing business value)
- Acceptance criteria are vague ("it should work correctly")
- No Given/When/Then format
- Only happy path covered (no error scenarios)
- Dev Lead hasn't reviewed technical feasibility
- QA Lead hasn't added test scenarios
- Three Amigos session hasn't occurred
- Open questions remain unresolved

## Benefits of Following DoR

**For the Team:**
- Fewer interruptions during sprint asking for clarification
- More accurate estimation (shared understanding)
- Higher sprint success rate (fewer blocked stories)

**For AI Implementation:**
- Sufficient context for one-pass success
- Explicit edge cases reduce rework
- Technical patterns identified upfront

**For Stakeholders:**
- Predictable delivery timelines
- Higher quality implementations
- Reduced rework and scope creep

## When to Skip DoR Criteria

In rare cases, teams may proceed with partially-ready stories:

- **Spike stories** - Research/exploration work may skip technical context
- **Emergency fixes** - Critical bugs may fast-track with lighter process
- **Technical debt** - May skip business value if purely technical

Document any exceptions and ensure the team understands the added risk.

## Related Documentation

- **Story Commands:** `.claude/docs/story-commands-quick-reference.md`
- **Story Workflow:** `.claude/docs/story-workflow-guide.md`
- **Product Owner Guide:** `.claude/PRODUCT-OWNER-GUIDE.md`
- **Three Amigos Guide:** `.claude/docs/three-amigos-guide.md`

---

**Last Updated:** 2025-11-24
**Version:** 1.0
