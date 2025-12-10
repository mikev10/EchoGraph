# Converting User Stories to Feature Requests (SPEC.md)

## Overview

This template shows how to convert a user story from Azure DevOps into a Context Engineering feature request (SPEC.md format) for PRP generation.

**Key Principle:** 1 User Story (1-3 days) = 1 Feature Request = 1 PRP

---

## ADO User Story Template

```
Title: User login with email and password

As a mobile app user
I want to login with my email and password
So that I can access my account securely

Acceptance Criteria:
- Given I have a valid account, when I enter correct email/password, then I am logged in
- Given I enter incorrect password, when I submit, then I see "Invalid credentials" error
- Given I am logged in, when I restart the app, then I remain logged in (token persists)

Description:
Users need a secure way to authenticate into the mobile app. This is the first authentication method we're implementing.

Story Points: 3
Sprint: Sprint 12
ADO ID: US-4523
```

---

## Converted SPEC.md

```markdown
<!-- SOURCE: ADO US-4523 -->
<!-- SPRINT: Sprint 12 -->
<!-- STORY POINTS: 3 -->

## FEATURE

Implement email and password login for mobile app users.

**User Story:**
As a mobile app user, I want to login with my email and password, so that I can access my account securely.

**Acceptance Criteria:**
- [ ] Given I have a valid account, when I enter correct email/password, then I am logged in
- [ ] Given I enter incorrect password, when I submit, then I see "Invalid credentials" error
- [ ] Given I am logged in, when I restart the app, then I remain logged in (token persists)

**Functional Requirements:**
- Login form with email and password inputs
- Email validation (format check)
- Password visibility toggle
- Form validation and error display
- Loading state during authentication
- Persistent session using secure token storage
- Error handling for network failures

## EXAMPLES

[This section will be populated during /convert-story command using codebase research]

**Similar implementations to reference:**
- Existing auth patterns in codebase
- Similar forms or input handling
- API integration examples

## DOCUMENTATION

[This section will be populated during /convert-story command using codebase research]

**API Endpoints:**
- Authentication endpoints
- Token management endpoints

**Libraries/Frameworks:**
- Form validation libraries
- Secure storage libraries
- HTTP client configuration

**Related Files:**
- Existing auth-related code
- API client setup
- State management for user session

## OTHER CONSIDERATIONS

**Security:**
- Store tokens securely (never in plain text)
- Validate credentials server-side
- Handle token expiration gracefully
- Implement rate limiting for failed attempts

**User Experience:**
- Clear error messages
- Smooth loading states
- Accessibility compliance
- Keyboard navigation support

**Testing:**
- Unit tests for form validation
- Integration tests for API calls
- E2E tests for full login flow
- Test error scenarios

**Dependencies:**
- Backend API must be ready
- Secure storage library must be configured
- [Add any other dependencies found during research]

**Technical Constraints:**
- [Add platform-specific considerations]
- [Add performance requirements]
- [Add compatibility requirements]
```

---

## Conversion Guidelines

### 1. FEATURE Section

**Include:**
- ✅ User story verbatim (As a... I want... So that...)
- ✅ Acceptance criteria as checkboxes
- ✅ Functional requirements derived from acceptance criteria
- ✅ Explicit list of what needs to be built

**Derive functional requirements by asking:**
- What UI components are needed?
- What validation is required?
- What states need to be handled (loading, error, success)?
- What persistence is needed?

### 2. EXAMPLES Section

**During conversion, AI will research:**
- Similar features in the codebase
- Existing patterns to follow
- Code snippets to reference
- Components that can be reused

**Developer can add:**
- Links to design mockups (if in ADO story)
- Screenshots of competitor implementations
- Links to style guides

### 3. DOCUMENTATION Section

**During conversion, AI will identify:**
- API endpoints needed (search API specs)
- Libraries already in use
- Related files in codebase
- Existing documentation

**Developer should verify:**
- API endpoints match current API specification
- Libraries are the correct versions
- Documentation links are current

### 4. OTHER CONSIDERATIONS Section

**Include:**
- Security considerations (always!)
- User experience requirements
- Testing requirements
- Dependencies on other work
- Technical constraints from ADO story
- Platform-specific gotchas

---

## Good vs. Bad Conversions

### ✅ GOOD: Complete Context

```markdown
## FEATURE

Implement password reset flow for mobile app users.

**User Story:**
As a mobile app user who forgot my password, I want to request a password reset via email, so that I can regain access to my account.

**Acceptance Criteria:**
- [ ] Given I'm on the login screen, when I tap "Forgot Password", then I see password reset form
- [ ] Given I enter my email, when I tap "Send Reset Link", then I receive a password reset email
- [ ] Given I click the reset link in email, when I enter a new password, then my password is updated

**Functional Requirements:**
- "Forgot Password" link on login screen
- Password reset request form (email input)
- Email validation
- Success confirmation screen
- Password reset form (from email link)
- Password strength requirements
- Confirmation password field
- Form validation
- Success state and auto-redirect to login

## EXAMPLES

- Reset password form pattern: `src/components/forms/ResetPasswordForm.tsx`
- Email validation utility: `src/utils/validation.ts`
- Success confirmation pattern: `src/components/SuccessMessage.tsx`

## DOCUMENTATION

**API Endpoints:**
- `POST /api/v1/auth/reset-password-request` - Request reset email
- `POST /api/v1/auth/reset-password` - Submit new password with token
- API Spec: `docs/api/auth-api-spec.json`

**Libraries:**
- `react-hook-form` (v7.43.0) - Form management
- `zod` (v3.20.2) - Validation schema

**Related Files:**
- `src/screens/LoginScreen.tsx` - Add "Forgot Password" link
- `src/api/auth.ts` - Add reset password API calls
- `src/navigation/AuthNavigator.tsx` - Add reset password screen route

## OTHER CONSIDERATIONS

**Security:**
- Reset tokens must expire after 1 hour
- Reset tokens are single-use only
- Rate limit reset requests (max 3 per hour per email)
- Validate password strength (min 8 chars, 1 uppercase, 1 number)

**Email Template:**
- Must use branded email template
- Include expiration time in email
- Deep link must work on mobile app

**Testing:**
- Test expired token scenario
- Test invalid token scenario
- Test successful reset flow
- Test rate limiting

**Dependencies:**
- Email service must be configured
- Deep linking must be set up in app config
```

### ❌ BAD: Missing Context

```markdown
## FEATURE

Password reset

## EXAMPLES

None

## DOCUMENTATION

API endpoint for password reset

## OTHER CONSIDERATIONS

Need email service
```

**Why it's bad:**
- No user story or acceptance criteria
- No functional requirements detail
- No specific examples from codebase
- No specific API endpoints or libraries
- No security considerations
- No testing requirements

---

## Quick Checklist

Before running `/generate-prp`, verify SPEC.md has:

- [ ] User story included verbatim
- [ ] All acceptance criteria listed as checkboxes
- [ ] Functional requirements derived from acceptance criteria
- [ ] Examples from codebase research (added by `/convert-story`)
- [ ] Specific API endpoints identified
- [ ] Libraries and related files listed
- [ ] Security considerations documented
- [ ] Testing requirements specified
- [ ] Dependencies and constraints noted
- [ ] Source metadata (ADO ID, sprint, story points)

---

## When to Skip Conversion

**Skip the conversion and write SPEC.md directly if:**
- User story is very technical (refactoring, bug fix, technical debt)
- No Product Owner involved (developer-initiated work)
- Story is too vague and needs significant research first

**In these cases:**
- Write SPEC.md from scratch
- Use the standard SPEC.md template
- Proceed directly to `/generate-prp`
