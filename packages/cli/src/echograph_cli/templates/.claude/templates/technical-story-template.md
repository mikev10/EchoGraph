---
created: [YYYY-MM-DD]
status: draft
category: technical
converted_to_ado: false
ado_id: null
sprint: null
story_points: null
---

# Technical Story Template

**Instructions:** Fill in this template when writing a technical user story (refactoring, bug fix, tech debt, performance improvement). Delete these instructions before saving.

**Tip:** Consider using `/write-user-story` command for AI assistance instead of manual drafting.

---

### Title
[Action-oriented title describing the technical work - e.g., "Refactor Authentication Module for Testability"]

### User Story
As a [developer/team member with specific context]
I want [specific technical improvement or fix]
So that [clear technical benefit]

**Examples:**
- As a developer working on the authentication system
- As a developer maintaining the codebase
- As a team member working on performance optimization
- As a developer fixing production bugs

### Acceptance Criteria

- **Scenario 1: [Primary technical outcome]**
  - Given [current state or metric]
  - When [work is complete]
  - Then [measurable outcome or improvement]
  - And [verification method]

- **Scenario 2: [Backwards compatibility or existing functionality]**
  - Given [existing behavior or dependencies]
  - When [changes are complete]
  - Then [existing functionality still works]
  - And [verification that nothing broke]

- **Scenario 3: [Testing or quality metric]**
  - Given [current test coverage or quality metric]
  - When [work is complete]
  - Then [improved metric with specific target]
  - And [all tests pass]

- **Scenario 4: [Performance or technical constraint]**
  - Given [current performance or constraint]
  - When [optimization is complete]
  - Then [improved performance with specific target]
  - And [meets technical requirements]

**Guidelines:**
- Use measurable outcomes (test coverage %, method count, performance ms)
- Include backwards compatibility verification
- Specify testing requirements
- Be specific with technical metrics

### Additional Notes

**Technical Debt Context:**
- [Why this work is needed]
- [Current problems or pain points]
- [History or background]

**Files to Modify:**
- `[file path 1]` - [what will change]
- `[file path 2]` - [what will change]

**Testing Requirements:**
- [Unit test requirements]
- [Integration test requirements]
- [Performance test requirements]
- [Existing tests that must pass]

**Performance Targets:**
- [Specific performance requirements]
- [Benchmarks to meet]
- [No degradation requirements]

**Dependencies:**
- [Other work that blocks this]
- [Other work that depends on this]
- [External systems or services involved]

**Migration Strategy** _(if applicable)_:
- [How to transition from old to new]
- [Backwards compatibility approach]
- [Rollback plan if needed]

---

## Checklist Before Submitting

Use this checklist to ensure your technical story is complete:

- [ ] Technical user type is clear (developer/team member + context)
- [ ] Technical benefit is explicit
- [ ] 3-6 acceptance criteria scenarios included
- [ ] All scenarios use Given/When/Then format
- [ ] Outcomes are measurable (numbers, percentages, counts)
- [ ] Backwards compatibility is addressed
- [ ] Testing requirements are specified
- [ ] Story is appropriately sized (1-3 days, 3-8 story points)
- [ ] Files to modify are listed
- [ ] Performance targets are specified (if applicable)
- [ ] No breaking changes unless explicitly called out

---

## Common Technical Story Types

### Refactoring Story
**Focus:** Code structure, maintainability, testability
**Metrics:** Method count, complexity, test coverage, duplication
**Example:** "Refactor AuthService to reduce complexity and improve test coverage"

### Performance Story
**Focus:** Speed, efficiency, resource usage
**Metrics:** Response time, memory usage, CPU usage, throughput
**Example:** "Optimize dashboard loading time from 5s to <2s"

### Bug Fix Story
**Focus:** Fixing defects, preventing regression
**Metrics:** Bug reproduction, test coverage for bug, regression tests
**Example:** "Fix authentication token expiration bug causing unexpected logouts"

### Technical Debt Story
**Focus:** Paying down shortcuts or outdated code
**Metrics:** Code quality metrics, dependency versions, security vulnerabilities
**Example:** "Upgrade React from v16 to v18 with full test coverage"

### Infrastructure Story
**Focus:** Build, deployment, development environment
**Metrics:** Build time, deployment success rate, developer productivity
**Example:** "Reduce CI/CD pipeline execution time from 20min to <10min"

---

## Related Resources

- **Training examples:** `user-stories/training/example-technical-story.md`
- **AI assistance:** Use `/write-user-story` command for help

---

**Original Requirements** _(delete if not applicable)_

[If converting from bug report, tech debt note, or informal requirements, paste them here for reference]
