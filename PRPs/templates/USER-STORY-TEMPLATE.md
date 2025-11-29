# User Story Template

Use this template when creating user stories manually. For automated creation, use `/story:write-user-story`.

---

## Frontmatter

```yaml
---
created: YYYY-MM-DD
status: draft
category: business | technical
converted_to_ado: false
ado_id: null
sprint: null
story_points: null
three_amigos_complete: false
tech_context_added: false
qa_context_added: false
---
```

---

## Story Structure

```markdown
# [Concise, Descriptive Title]

As a [specific user type/role]
I want [capability or feature]
so that [business value or benefit].

## Acceptance Criteria

- **Scenario 1: [Happy Path Title]**

  - Given [precondition or context]
  - When [action performed]
  - Then [expected outcome]
  - And [additional outcome if needed]

- **Scenario 2: [Variation or Edge Case]**

  - Given [different precondition]
  - When [action performed]
  - Then [expected outcome]

- **Scenario 3: [Error Case]**

  - Given [error condition]
  - When [action performed]
  - Then [error handling behavior]
  - And [user feedback shown]

## Notes

[Optional: Additional context, constraints, dependencies, or clarifications]

---

## Original Requirements

[Copy of original requirements for reference]
```

---

## Formatting Rules

### User Story Statement

**CORRECT:**
```
As a mobile app user
I want to reset my password via email
so that I can regain access to my account if I forget my credentials.
```

**INCORRECT:**
```
As a **mobile app user**,
I want **to reset my password via email**
so that **I can regain access**...
```

Do NOT use bold, commas after clauses, or line breaks within the statement.

### Acceptance Criteria

**CORRECT:**
```markdown
- **Scenario 1: Successful Password Reset**

  - Given I have a registered account
  - When I request a password reset
  - Then I receive an email with a reset link
  - And the link expires after 1 hour
```

**INCORRECT:**
```markdown
### Scenario 1: Successful Password Reset
**Given** I have a registered account
**When** I request a password reset
**Then** I receive an email with a reset link
```

Key rules:
- Use `- **Scenario X: Title**` format (dash, bold)
- Add blank line after scenario title
- Indent Given/When/Then/And with two spaces
- Do NOT bold keywords (Given/When/Then/And)
- Do NOT use ### for scenario headings

---

## Quality Checklist

Before submitting a story, verify:

- [ ] User type is specific (not just "user")
- [ ] Capability is clear and focused
- [ ] Business value is stated
- [ ] 3-6 acceptance criteria scenarios
- [ ] Happy path scenario included
- [ ] At least one error scenario included
- [ ] All criteria are testable
- [ ] Story is appropriately sized (1-3 days)
- [ ] No implementation details (WHAT not HOW)
- [ ] Formatting follows template rules

---

## Examples

### Business Story Example

```markdown
# Password Reset via Email

As a mobile app user who has forgotten my password
I want to reset my password using my registered email
so that I can regain access to my account without contacting support.

## Acceptance Criteria

- **Scenario 1: Successful Reset Request**

  - Given I am on the login screen
  - When I tap "Forgot Password" and enter my registered email
  - Then I see a confirmation message
  - And I receive a password reset email within 2 minutes

- **Scenario 2: Reset Link Usage**

  - Given I received a password reset email
  - When I tap the reset link within 1 hour
  - Then I am taken to the password reset screen
  - And I can enter a new password

- **Scenario 3: Expired Reset Link**

  - Given my reset link is older than 1 hour
  - When I tap the expired link
  - Then I see "This link has expired"
  - And I am prompted to request a new reset link

- **Scenario 4: Unregistered Email**

  - Given the email is not registered
  - When I request a password reset
  - Then I see the same confirmation message (for security)
  - And no email is sent

## Notes

- Reset link should be single-use
- Password requirements: min 8 chars, 1 uppercase, 1 number
- Rate limit: max 3 reset requests per hour per email
```

### Technical Story Example

```markdown
# Refactor Authentication Module

As a developer maintaining the codebase
I want to refactor the authentication module for better testability
so that we can increase test coverage and reduce coupling.

## Acceptance Criteria

- **Scenario 1: Extracted Token Service**

  - Given the auth module is refactored
  - When I import TokenService
  - Then it has no dependencies on HTTP clients
  - And it can be unit tested in isolation

- **Scenario 2: Maintained Functionality**

  - Given the refactored code is deployed
  - When users authenticate
  - Then all existing auth flows work unchanged
  - And no breaking changes to public APIs

- **Scenario 3: Improved Test Coverage**

  - Given the refactoring is complete
  - When I run the test suite
  - Then auth module coverage is above 80%
  - And all existing tests pass

## Notes

- Current auth module: `src/auth/index.ts` (450 lines)
- Target: Split into TokenService, SessionManager, AuthProvider
- Preserve backwards compatibility for external consumers
```

---

## See Also

- `/story:write-user-story` - Automated story creation
- `/story:enrich-story-tech` - Add technical context
- `/story:enrich-story-qa` - Add QA context
- `PRPs/user-stories/README.md` - Workflow documentation
