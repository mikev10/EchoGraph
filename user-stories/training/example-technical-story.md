---
created: 2025-11-24
status: training_example
category: technical
purpose: Example of technical work formatted as user story
---

# Training Example: Technical Story

**Purpose:** Shows how to structure technical work (refactoring, bugs, tech debt) as a user story using the same format as business stories.

---

### Title
Refactor Authentication Module for Improved Testability

### User Story
As a developer working on the authentication system
I want to refactor the auth module to reduce code duplication and improve test coverage
So that we can confidently make changes without breaking existing functionality and reduce maintenance burden

### Acceptance Criteria

- **Scenario 1: Reduce Method Complexity**
  - Given the AuthService class currently has 15 methods with overlapping logic
  - When refactoring is complete
  - Then the class has ≤8 public methods with clear single responsibilities
  - And each method has cyclomatic complexity ≤5
  - And all redundant code is extracted to shared utilities

- **Scenario 2: Achieve Test Coverage Target**
  - Given current auth module has 45% test coverage
  - When refactoring is complete
  - Then module has ≥90% test coverage
  - And all critical authentication paths have unit tests
  - And all error scenarios are covered by tests

- **Scenario 3: Maintain Backwards Compatibility**
  - Given existing code depends on current AuthService interface
  - When refactoring is complete
  - Then all existing functionality works identically
  - And no breaking changes to public API
  - And all existing tests continue to pass

- **Scenario 4: Extract Reusable Validation Logic**
  - Given multiple methods duplicate email and password validation
  - When refactoring is complete
  - Then shared validation logic is in ValidationUtils
  - And validation functions are independently testable
  - And all validation has comprehensive unit tests

- **Scenario 5: Improve Error Handling**
  - Given current error handling is inconsistent
  - When refactoring is complete
  - Then all authentication errors use centralized AuthError types
  - And error messages are consistent and helpful
  - And errors are properly logged for debugging

### Additional Notes

**Technical Debt Context:**
- Current auth module was built quickly during prototype phase
- Has grown organically to 800+ lines in single file
- Difficult to test due to tight coupling with other services
- High bug rate (12 bugs in last 3 months)

**Files to Refactor:**
- `src/services/AuthService.ts` (main refactoring target)
- `src/utils/ValidationUtils.ts` (extract shared logic here)
- `src/types/AuthTypes.ts` (consolidate type definitions)

**Testing Requirements:**
- All existing tests must pass
- Add new tests for edge cases currently uncovered
- Use Jest for unit tests
- Mock external dependencies (API, storage)

**Performance:**
- Must not degrade authentication performance
- Target: < 100ms for token validation
- Target: < 500ms for login/logout operations

**Dependencies:**
- No other work blocks this
- This does NOT change any user-facing behavior
- Can be done incrementally in feature branches

---

## Why This Is a Good Technical Story

### ✅ Uses Same Format as Business Stories

**Structure:**
- "As a [technical user]" instead of "As a [end user]"
- "I want [technical improvement]"
- "So that [technical benefit]"
- Given/When/Then acceptance criteria

**This maintains consistency** across all work items.

### ✅ Technical User Type

**"As a developer working on the authentication system"**

This is specific - not just "As a developer" but the context is clear.

Other good technical user types:
- "As a developer maintaining the codebase"
- "As a team member working on performance"
- "As a developer fixing production bugs"

### ✅ Clear Technical Outcomes

**Measurable criteria:**
- ≤8 public methods (countable)
- ≥90% test coverage (measurable)
- Cyclomatic complexity ≤5 (measurable)
- Performance targets (< 100ms, < 500ms)

**Not vague like:**
- "Code is better"
- "More maintainable"
- "Cleaner architecture"

### ✅ Testable Even For Technical Work

**Each scenario can be verified:**
- Scenario 1: Count methods, measure complexity
- Scenario 2: Run coverage report
- Scenario 3: Run existing test suite
- Scenario 4: Check for ValidationUtils usage
- Scenario 5: Verify error types and logging

---

## Differences from Business Stories

### User Type
**Business:** "As a mobile app user"
**Technical:** "As a developer working on..."

### Value Proposition
**Business:** User benefit (convenience, efficiency, security)
**Technical:** Developer benefit (maintainability, testability, performance)

### Acceptance Criteria Focus
**Business:** User actions and outcomes
**Technical:** Code metrics and technical outcomes

### Additional Notes
**Business:** Dependencies, security, UX concerns
**Technical:** Files affected, technical debt context, performance requirements

---

## When to Use This Format

### ✅ Use for:
- Refactoring that improves code quality
- Performance optimizations
- Technical debt reduction
- Bug fixes that need proper documentation
- Infrastructure improvements
- Dependency upgrades with testing requirements

### ❌ Don't use for:
- Simple one-line bug fixes
- Typo corrections
- Configuration changes
- Emergency hotfixes (no time for stories)

### ⚠️ Consider using for:
- Medium-sized bugs (half day to 2 days)
- Architectural improvements
- Library/framework migrations

---

## Benefits of Technical Stories

### 1. Consistent Tracking
- Technical work visible in same system as features
- Consistent estimation and planning
- Technical debt doesn't get hidden

### 2. Clear Acceptance Criteria
- Defines "done" for technical work
- Prevents scope creep during refactoring
- Ensures backwards compatibility is verified

### 3. Better Communication
- Non-technical stakeholders can understand value
- Clear trade-offs and benefits
- Justifies time spent on technical work

### 4. Integration with Context Engineering
- Can use `/write-user-story` for technical work
- Can convert to INITIAL.md with `/convert-story`
- Can generate PRP and execute systematically
- Same workflow as business features

---

## Example: Using /write-user-story for Technical Work

**Command:**
```
/write-user-story Refactor authentication module to improve testability and reduce code duplication. Currently 15+ methods with overlapping logic and hard to unit test.
```

**AI asks:**
- Is this business or technical? → **Technical**
- What's the current test coverage? → 45%
- What's the target test coverage? → 90%
- Any performance requirements? → No degradation
- Any breaking changes allowed? → No
- Files affected? → AuthService.ts mainly

**AI generates:** Story similar to the example above

**Saved to:** `user-stories/technical/20251124-refactor-auth-module.md`

**Next steps:** Use `/convert-story` → `/generate-prp` → `/execute-prp`

---

## Comparing Technical vs Business Story Size

| Aspect | Business Story | Technical Story |
|--------|----------------|-----------------|
| **Typical duration** | 1-3 days | 1-3 days (same) |
| **Story points** | 3-8 | 3-8 (same) |
| **Complexity** | User flows | Code complexity |
| **Testing** | User acceptance | Unit/integration tests |
| **Visibility** | High (users see it) | Low (under the hood) |
| **Value** | Direct user benefit | Developer efficiency |

**Both should follow same sizing principles!**

---

## Related Examples

- `example-good-login-story.md` - Business story for comparison
- `example-good-password-reset-story.md` - Complex business story
- `example-poor-story.md` - Mistakes to avoid (applies to technical too!)
- `example-improved-story.md` - How to improve a story

---

**Last Updated:** 2025-11-24
