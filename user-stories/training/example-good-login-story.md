---
created: 2025-11-24
status: training_example
category: business
purpose: Perfect example of well-written user story for business feature
---

# Training Example: Excellent Login Story

**Purpose:** This is a PERFECT example of a well-written user story. Use this as a reference when writing your own stories.

---

### Title
User Login with Email and Password

### User Story
As a mobile app user
I want to login with my email and password
So that I can securely access my account and personal data

### Acceptance Criteria

- **Scenario 1: Successful Login**
  - Given I have a registered account with email "user@example.com" and valid password
  - When I enter my email and password correctly
  - And I tap the "Login" button
  - Then I am redirected to my dashboard within 2 seconds
  - And I see a welcome message with my name

- **Scenario 2: Invalid Credentials**
  - Given I enter an incorrect password
  - When I tap the "Login" button
  - Then I see the error message "Invalid email or password. Please try again."
  - And the password field is cleared
  - And I remain on the login screen

- **Scenario 3: Session Persistence**
  - Given I successfully logged in previously
  - When I close the app and reopen it within 30 days
  - Then I am automatically logged in
  - And I see my dashboard without entering credentials

- **Scenario 4: Password Visibility Toggle**
  - Given I am on the login screen
  - When I tap the "eye" icon next to the password field
  - Then I can see my password in plain text
  - And when I tap the icon again, the password is hidden

- **Scenario 5: Invalid Email Format**
  - Given I enter an invalid email format (e.g., "notanemail")
  - When I tap the "Login" button
  - Then I see the error message "Please enter a valid email address"
  - And the login button remains disabled until valid email is entered

- **Scenario 6: Network Error**
  - Given I have no internet connection
  - When I tap the "Login" button
  - Then I see the error message "No internet connection. Please check your network and try again."
  - And I can tap "Retry" to attempt login again

### Additional Notes

**Dependencies:**
- Backend authentication API must be available
- Secure token storage must be configured (iOS Keychain / Android Keystore)

**Security Requirements:**
- Passwords must never be logged or stored in plain text
- Login attempts should be rate-limited (max 5 attempts per 15 minutes)
- Session tokens must expire after 30 days of inactivity

**Platform Requirements:**
- Works on both iOS and Android
- Follows platform-specific design guidelines

---

## Why This Story Is Excellent

### ✅ Follows INVEST Criteria

1. **Independent**: Can be developed without waiting for other features
2. **Negotiable**: Clear requirements but implementation approach is flexible
3. **Valuable**: Delivers clear user value (secure account access)
4. **Estimable**: Has enough detail for accurate sizing (likely 3-5 story points)
5. **Small**: Can be completed within one sprint (1-3 days)
6. **Testable**: Every scenario has clear pass/fail criteria

### ✅ User Story Format

- Specific user type: "mobile app user" (not just "user")
- Clear capability: "login with email and password"
- Explicit business value: "securely access my account and personal data"
- No bold formatting, proper punctuation

### ✅ Acceptance Criteria Quality

- **Comprehensive coverage**: 6 scenarios covering:
  - Happy path (Scenario 1)
  - Error handling (Scenarios 2, 5, 6)
  - Key variations (Scenarios 3, 4)
- **Proper Given/When/Then format**: All scenarios follow BDD structure
- **Specific outcomes**: Uses exact error messages, timeouts, limits
- **Testable**: QA can verify each scenario independently
- **Representative examples**: Uses "user@example.com" instead of overly specific data

### ✅ Formatting

- Scenario titles are bold: `- **Scenario X: Title**`
- Given/When/Then/And keywords are NOT bold
- Proper indentation (2 spaces)
- Blank line after scenario title
- Clean, readable structure

### ✅ Completeness

- **Additional Notes section** includes:
  - Dependencies (what must be ready before this story)
  - Security requirements (critical for auth features)
  - Platform requirements (iOS and Android)
- **No implementation details**: Doesn't specify which libraries, frameworks, or technical approach
- **No unnecessary details**: Skips obvious things like "button should be tappable"

---

## How to Use This Example

### For Product Owners

**When drafting a new story:**
1. Use this structure as your template
2. Follow the same Given/When/Then format
3. Include 3-6 scenarios like this example
4. Cover happy path + error cases + key variations
5. Keep Additional Notes for dependencies and constraints

**Check your story against this example:**
- Does yours have specific user type? (not just "user")
- Does yours have clear business value? (the "so that" clause)
- Do your scenarios follow Given/When/Then?
- Do you have 3-6 scenarios covering different cases?

### For Developers

**When reviewing a story:**
- Compare the story you received to this example
- If it's missing key elements, consider using `/refine-story`
- This is the quality level you should expect before `/convert-story`

**When writing technical stories:**
- Follow the same structure
- Change user type to "As a developer..."
- Focus on technical outcomes instead of user outcomes

---

## Common Mistakes This Story Avoids

❌ **Vague user type**: Story specifies "mobile app user", not just "user"
❌ **Missing business value**: Clear "so that" clause explains why this matters
❌ **Untestable criteria**: All scenarios have specific, verifiable outcomes
❌ **Only happy path**: Covers errors, edge cases, and variations
❌ **No Given/When/Then**: Every scenario follows proper BDD format
❌ **Implementation details**: Doesn't specify libraries, code structure, or technical approach
❌ **Too large**: Focused on one capability (login), appropriately sized
❌ **Wrong formatting**: Scenario titles bold, keywords not bold

---

## Related Examples

- `example-good-password-reset-story.md` - Another perfect business story example
- `example-poor-story.md` - See what NOT to do
- `example-improved-story.md` - See how a poor story is improved
- `example-technical-story.md` - Technical work formatted as user story

---

**Last Updated:** 2025-11-24
