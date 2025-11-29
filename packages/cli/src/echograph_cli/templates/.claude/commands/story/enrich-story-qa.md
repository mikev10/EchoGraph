---
description: Add test scenarios and QA context to user story (QA Lead workflow)
argument-hint: <story-path>
model: claude-sonnet-4-5-20250929
---

# Enrich Story with QA Context

You are helping a **QA Lead** add comprehensive test scenarios, edge cases, and testing requirements to a user story. This is a critical step in the Three Amigos workflow that ensures stories have sufficient test coverage defined before development begins.

**Purpose:** Generate comprehensive test scenarios, identify edge cases, define test data requirements, and ensure all acceptance criteria are testable.

**Input:** Path to user story markdown file: `$ARGUMENTS`

---

## Phase 1: Load and Analyze Story

**Read the story file:**
```
$ARGUMENTS
```

If no path provided or file not found:
```
Please provide the path to a user story file.

Usage: /enrich-story-qa user-stories/drafts/20251124-feature-name.md

Or paste the story content directly and I'll help add QA context.
```

**Extract and analyze:**
1. User Story (who, what, why)
2. Existing Acceptance Criteria
3. Technical Context (if present from /enrich-story-tech)
4. Any mentioned constraints or requirements

---

## Phase 2: Generate Comprehensive Test Scenarios

Based on the story analysis, generate test scenarios covering:

### 2.1 Happy Path Tests
For each acceptance criterion, create a test scenario that validates the expected behavior when everything works correctly.

### 2.2 Negative Tests / Error Cases
Identify what should happen when:
- Invalid input is provided
- Required fields are missing
- Data doesn't exist
- User doesn't have permission
- External services fail

### 2.3 Boundary Tests
Identify boundaries and test at the edges:
- Minimum/maximum values
- Empty vs. single vs. many items
- Character limits
- Date ranges
- Numeric limits

### 2.4 Edge Cases
Identify unusual but valid scenarios:
- Special characters in input
- Unicode/internationalization
- Concurrent operations
- Session timeout during operation
- Network interruption

### 2.5 Integration Tests
If Technical Context exists, identify:
- API endpoint tests
- Database integration tests
- External service integration tests

### 2.6 Non-Functional Tests
Based on requirements:
- Performance tests (if performance criteria specified)
- Security tests (if security requirements exist)
- Accessibility tests (if applicable)
- Usability tests

---

## Phase 3: Present Scenarios to QA Lead

```markdown
## Generated Test Scenarios

Based on the story and acceptance criteria, here are the proposed test scenarios:

### Happy Path Tests
| ID | Scenario | Expected Result |
|----|----------|-----------------|
| HP-01 | [Scenario description] | [Expected outcome] |
| HP-02 | [Scenario description] | [Expected outcome] |

### Error/Negative Tests
| ID | Scenario | Expected Result |
|----|----------|-----------------|
| NEG-01 | [Invalid input scenario] | [Expected error handling] |
| NEG-02 | [Missing data scenario] | [Expected error handling] |

### Boundary Tests
| ID | Boundary | Min Test | Max Test | Expected |
|----|----------|----------|----------|----------|
| BND-01 | [Field/value] | [Min value] | [Max value] | [Behavior] |

### Edge Cases
| ID | Scenario | Expected Result |
|----|----------|-----------------|
| EDGE-01 | [Edge case description] | [Expected handling] |

### Integration Tests
| ID | Integration Point | Test Approach |
|----|-------------------|---------------|
| INT-01 | [API/Service] | [How to test] |

---

## Questions for QA Lead

1. **Coverage Gaps:**
   Are there any scenarios I've missed that are important for this feature?

2. **Priority:**
   Which scenarios are critical path vs. nice-to-have?

3. **Test Data:**
   What specific test data do we need to set up for these scenarios?

4. **Automation:**
   Which of these scenarios should be automated vs. manual?

5. **Environment:**
   Are there any specific environment requirements for testing?

6. **Accessibility:**
   Are there specific accessibility requirements to test?

7. **Performance:**
   Are there specific performance thresholds to validate?
```

Wait for QA Lead input before finalizing.

---

## Phase 4: Generate QA Context Section

Based on generated scenarios and QA Lead input:

```markdown
## QA Context

**Added by:** QA Lead
**Date:** [current date]
**Status:** Test planning complete

### Test Strategy

**Test Types Required:**
- [x] Functional Testing
- [x] Negative Testing
- [x] Boundary Testing
- [ ] Performance Testing (if applicable)
- [ ] Security Testing (if applicable)
- [ ] Accessibility Testing (if applicable)

**Automation Strategy:**
- **Automated:** [List scenarios to automate]
- **Manual:** [List scenarios for manual testing]

### Test Scenarios

#### Happy Path Tests

- **HP-01: [Scenario Title]**
  - Preconditions: [Setup required]
  - Steps:
    1. [Step 1]
    2. [Step 2]
  - Expected: [Expected outcome]
  - Priority: Critical / High / Medium / Low

- **HP-02: [Scenario Title]**
  - Preconditions: [Setup required]
  - Steps:
    1. [Step 1]
    2. [Step 2]
  - Expected: [Expected outcome]
  - Priority: Critical / High / Medium / Low

#### Negative Tests

- **NEG-01: [Scenario Title]**
  - Preconditions: [Setup required]
  - Steps:
    1. [Invalid action]
  - Expected: [Error handling behavior]
  - Priority: Critical / High / Medium / Low

- **NEG-02: [Scenario Title]**
  - Preconditions: [Setup required]
  - Steps:
    1. [Invalid action]
  - Expected: [Error handling behavior]
  - Priority: Critical / High / Medium / Low

#### Boundary Tests

- **BND-01: [Boundary Description]**
  - Minimum value test: [Value] → [Expected]
  - Maximum value test: [Value] → [Expected]
  - Just over maximum: [Value] → [Expected error]
  - Priority: High / Medium / Low

#### Edge Cases

- **EDGE-01: [Edge Case Title]**
  - Scenario: [Description]
  - Expected: [Handling]
  - Priority: Medium / Low

### Test Data Requirements

**Required Test Data:**
| Data Type | Description | Setup Method |
|-----------|-------------|--------------|
| [Type] | [Description] | [How to create] |

**Test Users:**
| User Type | Permissions | Purpose |
|-----------|-------------|---------|
| [Role] | [Permissions] | [What to test] |

**Test Fixtures:**
- [ ] [Fixture description and location]

### Integration Test Points

| Integration | Test Approach | Mock/Real |
|-------------|---------------|-----------|
| [Service/API] | [How to test] | Mock / Real |

### Performance Criteria (if applicable)

| Metric | Target | Test Approach |
|--------|--------|---------------|
| [Response time] | [Target] | [How to measure] |
| [Throughput] | [Target] | [How to measure] |

### Accessibility Checklist (if applicable)

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG AA
- [ ] Focus indicators visible
- [ ] Error messages are accessible

### Regression Impact

**Areas to Regression Test:**
- [ ] [Feature/area that might be affected]
- [ ] [Feature/area that might be affected]

**Existing Tests to Update:**
- [ ] [Test file/suite that needs updates]

### Definition of Done (Testing)

- [ ] All happy path scenarios pass
- [ ] All critical negative tests pass
- [ ] Boundary conditions validated
- [ ] No P1/P2 bugs open
- [ ] Automated tests written and passing
- [ ] Regression suite updated
```

---

## Phase 5: Enhance Acceptance Criteria

Review the existing acceptance criteria and suggest improvements:

1. **Add missing scenarios** - If acceptance criteria don't cover error cases, suggest additions
2. **Make criteria more testable** - If criteria are vague, suggest specific, measurable versions
3. **Add edge cases** - If important edge cases aren't in acceptance criteria, suggest additions

```markdown
### Suggested Acceptance Criteria Enhancements

**Current gaps identified:**
1. [Gap description] - Suggest adding scenario for [case]
2. [Gap description] - Suggest adding scenario for [case]

**Suggested additional scenarios:**

- **Scenario X: [New Scenario Title]**
  - Given [context]
  - When [action]
  - Then [specific, testable outcome]

- **Scenario Y: [New Scenario Title]**
  - Given [context]
  - When [action]
  - Then [specific, testable outcome]

**Should these be added to the Acceptance Criteria section?** (yes/no)
```

---

## Phase 6: Update Story File

Append the QA Context section to the story file:

1. Read the current story content
2. Insert QA Context section (after Technical Context if present, otherwise after Acceptance Criteria)
3. Optionally update Acceptance Criteria with enhanced scenarios
4. Update file metadata

---

## Phase 7: Summary and Next Steps

```
## QA Enrichment Complete

**Story:** [story title]
**File:** [full path]

### What Was Added:
- [X] test scenarios across happy path, negative, boundary, and edge cases
- Test data requirements
- Integration test points
- Performance criteria (if applicable)
- Accessibility checklist (if applicable)
- Regression impact analysis

### Acceptance Criteria Updates:
- [Added/No changes to] acceptance criteria
- [X] new scenarios suggested

### Definition of Ready Checklist (QA):
- [x] Test scenarios documented
- [x] Test data requirements known
- [x] Integration points identified
- [x] Accessibility requirements noted (if applicable)

### Next Steps:
1. **Review with PO:** Confirm suggested acceptance criteria additions
2. **Three Amigos session:** Run `/three-amigos-prep [story-path]`
3. **Validation:** Run `/validate-story-ready [story-path]`

### Coverage Summary:
- Happy Path: [X] scenarios
- Negative Tests: [X] scenarios
- Boundary Tests: [X] scenarios
- Edge Cases: [X] scenarios
- Integration Tests: [X] scenarios
Total: [XX] test scenarios defined
```

---

## Error Handling

**If no acceptance criteria exist:**
```
This story has no acceptance criteria defined yet.

QA test scenarios are derived from acceptance criteria.
Please run /write-user-story or /refine-story first to add acceptance criteria.

Alternatively, I can help generate both acceptance criteria AND test scenarios together.
Would you like me to do that? (yes/no)
```

**If story is too vague:**
```
The story is too vague to generate meaningful test scenarios.

Issues found:
- [List vagueness issues]

Recommendations:
1. Run /refine-story to improve story clarity
2. Ask PO for more specific requirements
3. Run /enrich-story-tech first if technical context is missing

Would you like to proceed with partial test scenarios? (yes/no)
```

---

## Quality Checklist

Before finalizing, verify:

- [ ] Happy path tests cover all acceptance criteria
- [ ] Negative tests cover expected error cases
- [ ] Boundary conditions are identified and tested
- [ ] Edge cases are documented
- [ ] Test data requirements are clear
- [ ] Integration points are identified
- [ ] Priority assigned to all scenarios
- [ ] Automation strategy defined

---

## Examples

### Example 1: Login Feature

**Input:** User story for login with email/password

**Generated Test Scenarios:**
- HP-01: Successful login with valid credentials
- HP-02: Session persists after app restart
- NEG-01: Invalid password shows error message
- NEG-02: Non-existent email shows error message
- NEG-03: Empty fields prevent submission
- BND-01: Password at minimum length (8 chars)
- BND-02: Password at maximum length (128 chars)
- BND-03: Email at maximum length (254 chars)
- EDGE-01: Special characters in password
- EDGE-02: Unicode characters in email
- EDGE-03: Network timeout during login

### Example 2: File Upload

**Input:** User story for profile photo upload

**Generated Test Scenarios:**
- HP-01: Upload valid JPG under size limit
- HP-02: Upload valid PNG under size limit
- NEG-01: Upload file over size limit (5MB)
- NEG-02: Upload invalid file type (.exe)
- NEG-03: Upload with no network
- BND-01: Upload exactly 5MB file (boundary)
- BND-02: Upload 1KB file (minimum)
- EDGE-01: Upload file with special chars in name
- EDGE-02: Cancel upload mid-progress
- EDGE-03: Multiple rapid uploads

---

## Integration with Three Amigos Workflow

This command is Step 3 in the Three Amigos workflow:

```
Step 1: /write-user-story  → PO creates draft         ✓
Step 2: /enrich-story-tech → Dev Lead adds technical  ✓
Step 3: /enrich-story-qa   → QA Lead adds test        ← YOU ARE HERE
Step 4: /three-amigos-prep → Prepare alignment session
Step 5: /validate-story-ready → Check all DoR criteria
```

---

**Output:** Updated story file with comprehensive QA Context section and test scenarios.
