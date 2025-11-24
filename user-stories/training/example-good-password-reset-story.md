---
created: 2025-11-24
status: training_example
category: business
purpose: Perfect example of well-written user story for complex feature with multiple flows
---

# Training Example: Excellent Password Reset Story

**Purpose:** This is a PERFECT example of a well-written user story for a more complex feature with multiple user flows. Use this to see how to handle multi-step processes.

---

### Title
Password Reset via Email Link

### User Story
As a mobile app user who forgot my password
I want to request a password reset via email
So that I can regain access to my account without contacting support

### Acceptance Criteria

- **Scenario 1: Request Reset from Login Screen**
  - Given I am on the login screen
  - When I tap "Forgot Password"
  - Then I see a password reset form with an email input field
  - And I see instructions "Enter your email address and we'll send you a link to reset your password"

- **Scenario 2: Successful Reset Request**
  - Given I entered a valid registered email address
  - When I tap "Send Reset Link"
  - Then I see confirmation message "Password reset email sent. Check your inbox."
  - And I receive an email within 5 minutes
  - And the email contains a reset link that expires in 1 hour

- **Scenario 3: Reset Request for Unregistered Email**
  - Given I entered an email address that's not registered
  - When I tap "Send Reset Link"
  - Then I see the same confirmation message (for security)
  - And no email is sent

- **Scenario 4: Click Reset Link**
  - Given I received the password reset email
  - When I click the reset link within 1 hour
  - Then the app opens to the password reset screen
  - And I see two password fields: "New Password" and "Confirm Password"

- **Scenario 5: Successful Password Reset**
  - Given I am on the password reset screen
  - When I enter a valid new password in both fields
  - And I tap "Reset Password"
  - Then my password is updated
  - And I am automatically logged in
  - And I see my dashboard

- **Scenario 6: Expired Reset Link**
  - Given I received the password reset email more than 1 hour ago
  - When I click the reset link
  - Then I see error message "This reset link has expired. Please request a new one."
  - And I see a "Request New Link" button

- **Scenario 7: Password Validation**
  - Given I am on the password reset screen
  - When I enter a password that doesn't meet requirements
  - Then I see error message "Password must be at least 8 characters with 1 uppercase letter and 1 number"
  - And the "Reset Password" button remains disabled

- **Scenario 8: Password Mismatch**
  - Given I entered different passwords in the two fields
  - When I tap "Reset Password"
  - Then I see error message "Passwords do not match"
  - And both password fields are cleared

### Additional Notes

**Dependencies:**
- Email service must be configured and operational
- Deep linking must be configured for mobile app
- Backend API endpoints for reset request and password update

**Security Requirements:**
- Reset tokens must be single-use only (cannot be reused)
- Reset tokens must expire after 1 hour
- Old password is immediately invalidated upon successful reset
- Rate limiting: Max 3 reset requests per email per hour
- Reset requests for invalid emails should not reveal account existence

**User Experience:**
- Email must use branded template
- Reset link must work seamlessly on mobile devices
- Password requirements must be clearly visible
- Success confirmation should be clear and reassuring

**Technical Constraints:**
- Reset link format: `app://reset-password?token={secure_token}`
- Deep linking must handle both app installed and not installed cases
- Email delivery must be tracked for monitoring

---

## Why This Story Is Excellent

### ✅ Handles Complex Multi-Step Flow

This story involves multiple screens and systems:
1. Login screen → Password reset request form
2. Email system → User's inbox
3. Email link → App opens to reset screen
4. Reset form → Success confirmation

**The story breaks this down into clear, testable scenarios** without getting lost in implementation details.

### ✅ Comprehensive Error Handling

Covers many error cases:
- Unregistered email (Scenario 3)
- Expired link (Scenario 6)
- Invalid password format (Scenario 7)
- Password mismatch (Scenario 8)

### ✅ Security Considerations

- Doesn't reveal account existence (Scenario 3)
- Token expiration (1 hour)
- Single-use tokens (in notes)
- Rate limiting (in notes)
- Password requirements (Scenario 7)

### ✅ Appropriate Story Size

Even though this is a complex feature, it's still:
- Focused on ONE capability (password reset)
- Estimable at 5-8 story points
- Completable in 2-3 days
- Not split unnecessarily

**This is the maximum complexity for a single story** - any more and it should be split.

---

## How This Story Handles Complexity

### Multi-Step Processes

**Good approach (this story):**
- Each step is a separate scenario
- Clear transitions between steps
- All steps testable independently

**Bad approach:**
- One giant scenario trying to cover everything
- Vague "user completes password reset" statement
- No clarity on individual steps

### External Systems

**Email Service:**
- Story mentions email but doesn't specify HOW
- Includes timing requirement (within 5 minutes)
- Notes dependency in Additional Notes

**Deep Linking:**
- Story shows expected behavior (app opens to reset screen)
- Doesn't specify technical implementation
- Notes technical constraint in Additional Notes

### Security Requirements

**In scenarios (where testable):**
- Password validation (Scenario 7)
- Link expiration (Scenario 6)
- Password mismatch (Scenario 8)

**In Additional Notes (where not directly testable):**
- Single-use tokens
- Rate limiting
- Account existence protection

---

## Learning Points

### 1. Balancing Detail and Brevity

**Too vague:**
"User can reset their password via email"

**Too detailed:**
"System generates SHA-256 token, stores in Redis with 3600s TTL, sends via SendGrid API with template ID 'd-abc123'..."

**Just right (this story):**
- Clear user actions and outcomes
- Specific where it matters (1 hour expiration, email within 5 minutes)
- Technical constraints in notes, not scenarios

### 2. Security Without Implementation

**This story specifies:**
- WHAT security is needed (tokens expire, single-use, rate limiting)
- WHEN it applies (expired link scenario, rate limit noted)

**This story doesn't specify:**
- HOW tokens are generated
- WHERE rate limiting is enforced
- WHICH encryption algorithm to use

**Developers will determine technical approach during `/convert-story`**

### 3. User Experience Requirements

**Embedded in scenarios:**
- Clear error messages (exact wording provided)
- Confirmation messages (specific text)
- Form fields and buttons (what user sees)

**In Additional Notes:**
- Branded email template
- Password requirements visibility
- Success confirmation clarity

---

## Common Questions

### Q: Should each scenario be a separate story?

**A:** No! These scenarios are all part of ONE user capability (password reset). They should stay together because:
- They're not valuable independently
- They share dependencies (email service, reset API)
- They're part of one user journey
- Together they're still small enough (2-3 days)

### Q: How many scenarios is too many?

**A:** This story has 8 scenarios, which is on the high end but acceptable because:
- Feature is complex and warrants thorough coverage
- Each scenario is distinct and necessary
- Story is still estimable and completable in one sprint

**General guidance:**
- 3-6 scenarios is ideal
- 8 scenarios is maximum before considering split
- More than 8 suggests story is too large

### Q: Should I specify exact error messages?

**A:** Yes, when they're important for user experience:
- ✅ Security-related messages (show exact wording)
- ✅ Validation feedback (help user fix the problem)
- ✅ Error instructions (tell user what to do next)
- ❌ Generic system errors (implementation can decide)

---

## Comparing to Login Story

| Aspect | Login Story | Password Reset Story |
|--------|-------------|---------------------|
| **Complexity** | Simple (one screen) | Complex (multi-step) |
| **Systems** | App + API | App + API + Email |
| **Scenarios** | 6 | 8 |
| **Story Points** | 3-5 | 5-8 |
| **Duration** | 1-2 days | 2-3 days |
| **Split?** | No | No (but close to limit) |

Both stories are good examples at different complexity levels.

---

## Related Examples

- `example-good-login-story.md` - Simpler business story
- `example-poor-story.md` - See mistakes to avoid
- `example-improved-story.md` - See how to improve a poor story
- `example-technical-story.md` - Technical work as user story

---

**Last Updated:** 2025-11-24
