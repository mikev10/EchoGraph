# Three Amigos Collaboration Guide

## What is Three Amigos?

**Three Amigos** is a collaborative practice where three key perspectives come together before a user story enters team grooming:

1. **Product Owner (PO)** - Business perspective
2. **Dev Lead** - Technical perspective
3. **QA Lead** - Testing perspective

The goal is to ensure shared understanding, identify gaps, and resolve ambiguities **before** the broader team sees the story.

## Why Three Amigos?

### The Problem Without It

Without pre-grooming collaboration:
- Stories enter grooming with ambiguities
- Dev asks "What about this edge case?" - PO doesn't know
- QA asks "How do we test this?" - No one has thought about it
- Team spends grooming time clarifying instead of estimating
- Stories get blocked mid-sprint due to undiscovered complexity
- AI-generated code fails due to implicit assumptions

### The Benefits

With Three Amigos:
- **40% fewer unexpected blockers** during sprints
- **More accurate estimates** (shared understanding = better sizing)
- **Higher quality AI implementation** (explicit context = better code)
- **Faster grooming sessions** (questions already answered)
- **Better test coverage** (QA involved early)

## The Three Perspectives

### Product Owner (Business)

**Brings:**
- Business requirements and user needs
- Priority and value understanding
- Scope decisions
- Success metrics

**Key Questions to Answer:**
- Why does this feature matter?
- What's the minimum viable version?
- What can be deferred?
- How will we measure success?

### Dev Lead (Technical)

**Brings:**
- Technical feasibility assessment
- Architecture and design insights
- Complexity estimation
- Security and performance considerations
- Knowledge of existing patterns

**Key Questions to Answer:**
- Is this technically feasible as specified?
- What's the complexity? (Simple/Medium/Complex)
- What dependencies or risks exist?
- What patterns should we follow?

### QA Lead (Testing)

**Brings:**
- Test scenario identification
- Edge case discovery
- Test data requirements
- Quality criteria
- Accessibility considerations

**Key Questions to Answer:**
- Is this testable as written?
- What edge cases are we missing?
- What test data do we need?
- What could go wrong?

## AI-Assisted Three Amigos Workflow

The traditional Three Amigos meeting is enhanced with AI assistance at each stage:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI-ENHANCED THREE AMIGOS WORKFLOW                     │
└─────────────────────────────────────────────────────────────────────────┘

STEP 1: STORY CREATION (Product Owner)
├── Tool: /write-user-story
├── AI assists with: Structure, acceptance criteria, INVEST validation
├── Output: Draft story in user-stories/drafts/
└── Time: 15-30 minutes

STEP 2: TECHNICAL ENRICHMENT (Dev Lead)
├── Tool: /enrich-story-tech
├── AI assists with: Codebase research, API identification, pattern matching
├── Output: Technical Context section added to story
└── Time: 20-40 minutes

STEP 3: QA ENRICHMENT (QA Lead)
├── Tool: /enrich-story-qa
├── AI assists with: Test scenario generation, edge case identification
├── Output: QA Context section added to story
└── Time: 20-40 minutes

STEP 4: ALIGNMENT SESSION (All Three)
├── Tool: /three-amigos-prep
├── AI assists with: Agenda generation, discussion point identification
├── Output: Meeting prep document
├── Meeting: 30-45 minute sync session
└── Time: 30-45 minutes (meeting)

STEP 5: VALIDATION (All Three)
├── Tool: /validate-story-ready
├── AI assists with: DoR criteria checking, gap identification
├── Output: Readiness report
└── Time: 5-10 minutes

TOTAL TIME: ~2-3 hours (vs. 4-6 hours without AI assistance)
```

## When to Use Three Amigos

### Always Use For:
- New features with user-facing changes
- Complex technical stories
- Stories with multiple acceptance criteria
- Stories touching security or payments
- Stories with unknown complexity

### Can Skip For:
- Bug fixes with clear reproduction steps
- Technical debt with dev-only impact
- Spikes/research tasks
- Trivial changes (typo fixes, config changes)

### Red Flags That Require Three Amigos:
- PO says "it should just work"
- Dev says "I'm not sure how complex this is"
- QA says "how do I test this?"
- Story has no acceptance criteria
- Story references "similar to existing feature" without specifics

## Running a Three Amigos Session

### Before the Meeting

1. **PO:** Create story using `/write-user-story`
2. **Dev Lead:** Run `/enrich-story-tech [story-path]`
3. **QA Lead:** Run `/enrich-story-qa [story-path]`
4. **Facilitator:** Run `/three-amigos-prep [story-path]`
5. **All:** Review prep document before meeting

### Meeting Agenda (30-45 minutes)

| Time | Topic | Lead | Purpose |
|------|-------|------|---------|
| 5 min | Story Overview | PO | Ensure everyone understands the "why" |
| 10 min | Acceptance Criteria | All | Confirm completeness and testability |
| 10 min | Technical Feasibility | Dev Lead | Confirm approach and identify complexity |
| 10 min | Test Strategy | QA Lead | Confirm test coverage and data needs |
| 5 min | Scope & Risks | All | Agree on in/out of scope, identify risks |
| 5 min | Actions & Next Steps | All | Capture decisions and follow-ups |

### During the Meeting

**DO:**
- Focus on understanding, not implementation details
- Capture decisions in the story document
- Identify what's in scope vs. out of scope
- Note any follow-up actions needed
- Use the generated agenda as a guide

**DON'T:**
- Design the solution in detail
- Estimate story points (that's for team grooming)
- Invite the whole team (keep it to three people)
- Skip any perspective (all three must attend)
- Rush through to meet time constraints

### After the Meeting

1. **Update story** with decisions and clarifications
2. **Run validation:** `/validate-story-ready [story-path]`
3. **Address gaps** identified in validation
4. **Add to grooming agenda** when status is READY

## Definition of Ready (DoR)

A story is **Ready** for team grooming when it passes all DoR criteria:

### User Story Structure (PO)
- [ ] User type is specific (not just "user")
- [ ] Capability is clear and focused
- [ ] Business value is stated ("so that...")
- [ ] Story is appropriately sized (1-3 days)
- [ ] Story is independent

### Acceptance Criteria (PO + QA)
- [ ] Minimum 3 scenarios
- [ ] Given/When/Then format
- [ ] Scenarios are testable
- [ ] Edge cases covered
- [ ] Performance requirements stated (if applicable)

### Technical Context (Dev Lead)
- [ ] Technical feasibility confirmed
- [ ] API endpoints identified
- [ ] Data model understood
- [ ] Dependencies identified
- [ ] Security considerations noted
- [ ] Similar patterns referenced

### QA Context (QA Lead)
- [ ] Test scenarios documented
- [ ] Test data requirements known
- [ ] Integration points identified
- [ ] Accessibility requirements noted (if applicable)

### Three Amigos Alignment
- [ ] Session completed
- [ ] All questions resolved
- [ ] Scope agreed
- [ ] Risks identified

**Validation Command:** `/validate-story-ready [story-path]`

## AI-Ready Story Requirements

Because AI will implement these stories, certain elements must be explicit:

### Error Handling (AI cannot infer)
Stories must specify:
- What happens when network fails?
- What happens when data doesn't exist?
- What happens when user doesn't have permission?
- What happens when input is invalid?

### Boundaries (AI needs explicit limits)
Stories must specify:
- Maximum/minimum values
- Character limits
- File size limits
- Timeout durations

### Success Criteria (AI needs measurable outcomes)
Stories must specify:
- What does success look like?
- What feedback does the user see?
- What data is persisted?
- What events are logged?

## Command Quick Reference

| Command | Who Uses | Purpose |
|---------|----------|---------|
| `/write-user-story` | PO | Create initial story draft |
| `/refine-story` | PO/Dev | Improve existing story quality |
| `/enrich-story-tech` | Dev Lead | Add technical context |
| `/enrich-story-qa` | QA Lead | Add test scenarios |
| `/three-amigos-prep` | Facilitator | Generate meeting agenda |
| `/validate-story-ready` | All | Check DoR criteria |
| `/convert-story` | Developer | Convert to INITIAL.md for implementation |

## Common Pitfalls

### Pitfall 1: Skipping Steps
**Symptom:** Story enters grooming without technical or QA context
**Impact:** Questions during grooming, blocked stories, poor estimates
**Solution:** Use `/validate-story-ready` to catch missing sections

### Pitfall 2: Async-Only Collaboration
**Symptom:** Each person adds their section without discussion
**Impact:** Misaligned assumptions, conflicting requirements
**Solution:** Always hold the sync meeting (even 15 minutes helps)

### Pitfall 3: Over-Engineering Stories
**Symptom:** 50-line acceptance criteria, every edge case documented
**Impact:** Stories too large, paralysis by analysis
**Solution:** Stories should be 1-3 days; split larger work

### Pitfall 4: Under-Specifying Errors
**Symptom:** Only happy path documented
**Impact:** AI generates code without error handling, bugs in production
**Solution:** Every acceptance criteria needs an error scenario

### Pitfall 5: Vague Acceptance Criteria
**Symptom:** "System should work correctly"
**Impact:** QA can't test, AI can't implement
**Solution:** Use Given/When/Then format with specific outcomes

## Integration with Development Workflow

```
THREE AMIGOS                    DEVELOPMENT
─────────────────────────────────────────────────────────────
/write-user-story          
        │                       
        ▼                       
/enrich-story-tech         
        │                       
        ▼                       
/enrich-story-qa           
        │                       
        ▼                       
/three-amigos-prep         
        │                       
        ▼                       
[30-45 min Session]        
        │                       
        ▼                       
/validate-story-ready      
        │                       
        ▼                       
[Team Grooming] ──────────────▶ Story Estimated
        │                       
        ▼                       
[Sprint Planning] ─────────────▶ Story Committed
        │                       
        ▼                       
/convert-story ────────────────▶ INITIAL.md Created
        │                       
        ▼                       
/generate-prp ─────────────────▶ PRP Created
        │                       
        ▼                       
/execute-prp ──────────────────▶ Code Implemented
        │                       
        ▼                       
[Code Review + Testing] ───────▶ PR Merged
        │                       
        ▼                       
[Deployed]                 
```

## Metrics to Track

### Leading Indicators
- % of stories with Technical Context before grooming
- % of stories with QA Context before grooming
- % of stories passing DoR validation

### Lagging Indicators
- Sprint completion rate
- Stories blocked mid-sprint
- Defects found in code review
- Production bugs per story

### Target State
- 100% of feature stories have Three Amigos session
- 90%+ pass DoR validation before grooming
- <10% stories blocked mid-sprint
- <5% stories require re-grooming

## FAQ

**Q: Do we need Three Amigos for every story?**
A: No. Bug fixes, technical debt, and trivial changes can skip it. Use it for features and complex stories.

**Q: What if one of the three isn't available?**
A: Reschedule. The value of Three Amigos comes from all three perspectives. A meeting with two is a different meeting.

**Q: How long should the meeting be?**
A: 30-45 minutes for most stories. If you need more time, the story might be too large.

**Q: Can we do Three Amigos async?**
A: The enrichment steps (tech, QA) can be async. The alignment session should be synchronous, even if brief.

**Q: What if we find the story needs to be split?**
A: Great! That's a success. Split it and run Three Amigos on each part.

**Q: When in the sprint should we do Three Amigos?**
A: Before grooming. Ideally 2-3 days before the story might enter a sprint.

---

## Related Documentation

- **Definition of Ready:** `docs/optional/DEFINITION_OF_READY.md`
- **Story Commands:** `.claude/docs/story-commands-quick-reference.md`
- **Product Owner Guide:** `docs/optional/PRODUCT_OWNER_GUIDE.md`

---

**Last Updated:** 2025-11-24
**Version:** 1.0
