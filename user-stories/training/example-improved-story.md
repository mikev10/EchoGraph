---
created: 2025-11-24
status: training_example
category: business
purpose: Shows how to improve poor story - before/after comparison
---

# Training Example: Improved Story (Before → After)

**Purpose:** This shows how to transform a poor user story into a high-quality one. Compare to `example-poor-story.md` to see the improvements.

---

## Before: The Poor Story

### Title
Profile

### User Story
As a user I want to update my profile

### Accept Criteria
- User can update profile
- Changes are saved
- Profile works correctly

---

## After: The Improved Story

### Title
Update Profile Information (Name, Email, Phone)

### User Story
As a registered mobile app user
I want to update my profile information (name, email, phone number)
So that my account information stays current and other users can reach me

### Acceptance Criteria

- **Scenario 1: Navigate to Profile Edit**
  - Given I am logged into the app
  - When I tap "Profile" in the main menu
  - And I tap "Edit Profile"
  - Then I see an edit form with my current name, email, and phone number

- **Scenario 2: Successfully Update Name**
  - Given I am on the profile edit screen
  - When I change my name to a new valid name
  - And I tap "Save Changes"
  - Then I see confirmation message "Profile updated successfully"
  - And my profile displays the new name
  - And other users see my new name

- **Scenario 3: Successfully Update Email**
  - Given I change my email to a new valid email address
  - When I tap "Save Changes"
  - Then I receive a verification email at the new address
  - And I see message "Verification email sent to [new email]. Please verify to complete the change."
  - And my email is updated after I click the verification link

- **Scenario 4: Successfully Update Phone Number**
  - Given I change my phone number to a valid format
  - When I tap "Save Changes"
  - Then my phone number is updated immediately
  - And I see confirmation message "Profile updated successfully"

- **Scenario 5: Invalid Email Format**
  - Given I enter an email in invalid format (e.g., "notanemail")
  - When I try to save
  - Then I see error message "Please enter a valid email address"
  - And the "Save Changes" button remains disabled

- **Scenario 6: Cancel Changes**
  - Given I made changes to my profile
  - When I tap "Cancel"
  - Then I see confirmation dialog "Discard changes?"
  - And when I confirm, my changes are not saved
  - And I return to my profile view

- **Scenario 7: Network Error**
  - Given I tap "Save Changes"
  - When the network request fails
  - Then I see error message "Unable to save changes. Please check your connection and try again."
  - And I can tap "Retry"

### Additional Notes

**Dependencies:**
- User must be logged in
- Backend profile update API must be available
- Email verification service must be configured

**Validation Requirements:**
- Name: 2-50 characters, letters and spaces only
- Email: Valid email format, must be unique in system
- Phone: Valid format for user's country code

**Security:**
- Email changes require verification to prevent account hijacking
- Only the account owner can edit their profile
- Sensitive changes (email) should be logged for audit

---

## Key Improvements Made

### 1. Title: Specific and Clear
**Before:** "Profile"
**After:** "Update Profile Information (Name, Email, Phone)"
**Impact:** Immediately clear what the story covers

### 2. User Type: Specific Persona
**Before:** "As a user"
**After:** "As a registered mobile app user"
**Impact:** Clear who this is for and what context

### 3. Capability: Detailed and Focused
**Before:** "I want to update my profile"
**After:** "I want to update my profile information (name, email, phone number)"
**Impact:** Specific fields in scope

###4. Business Value: Clear Benefit
**Before:** (missing)
**After:** "So that my account information stays current and other users can reach me"
**Impact:** Explains WHY this matters

### 5. Acceptance Criteria: Comprehensive and Testable
**Before:** 3 vague statements
**After:** 7 detailed scenarios with Given/When/Then
**Impact:** Clear, testable, comprehensive

### 6. Error Handling: Multiple Scenarios
**Before:** None
**After:** Invalid email, network error, cancel confirmation
**Impact:** Robust feature that handles problems gracefully

### 7. Validation: Explicit Requirements
**Before:** None mentioned
**After:** Specific format requirements for each field
**Impact:** Clear boundaries and constraints

### 8. Security: Addressed Critical Concerns
**Before:** None mentioned
**After:** Email verification, audit logging, authorization
**Impact:** Secure implementation from the start

---

## Transformation Analysis

### Scope Clarification

| Aspect | Before | After |
|--------|--------|-------|
| **Fields** | Unclear | Name, email, phone only |
| **Actions** | "Update" | Edit, save, cancel, verify |
| **Platform** | Unknown | Mobile app |
| **User type** | Any user | Registered users |

### Scenarios Added

**The improved version adds 7 specific scenarios:**
1. Navigate to edit screen (user flow)
2. Update name (happy path)
3. Update email with verification (complex flow)
4. Update phone (happy path variation)
5. Invalid email format (validation error)
6. Cancel changes (user choice)
7. Network error (system error)

**The poor version had none of these details!**

### Testability Comparison

**Before:**
- "User can update profile" - How do we test this?
- "Changes are saved" - Where? When? How do we verify?
- "Profile works correctly" - What does this mean?

**After:**
- Every scenario is independently testable
- Clear pass/fail criteria for each
- Specific user actions and system responses
- Measurable outcomes

---

## Story Size Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Estimable?** | ❌ No - too vague | ✅ Yes - clear scope |
| **Story points** | ??? | 5-8 points |
| **Duration** | Unknown | 2-3 days |
| **Complexity** | Unclear | Medium complexity |

---

## INVEST Criteria: Before vs After

| Criteria | Before | After |
|----------|--------|-------|
| **Independent** | ❌ Unclear | ✅ Yes - can implement standalone |
| **Negotiable** | ⚠️ Too vague | ✅ Yes - clear requirements, flexible implementation |
| **Valuable** | ❌ No value stated | ✅ Yes - keeps account info current |
| **Estimable** | ❌ Cannot estimate | ✅ Yes - 5-8 points |
| **Small** | ⚠️ Might be huge | ✅ Yes - 2-3 days |
| **Testable** | ❌ Not testable | ✅ Yes - all scenarios testable |

---

## Questions Answered

The improved story answers questions that developers would have asked:

✅ What fields can be updated? → Name, email, phone
✅ What validations are needed? → Format requirements specified
✅ What happens on error? → Error scenarios included
✅ Can changes be cancelled? → Cancel scenario included
✅ Is there confirmation? → Confirmation messages specified
✅ Who can edit profile? → Only account owner
✅ Any security concerns? → Email verification required
✅ What platforms? → Mobile app

---

## How /refine-story Would Handle This

If you ran `/refine-story` on the poor story, the AI would:

1. **Identify all the issues** listed in example-poor-story.md
2. **Ask clarifying questions** to fill in gaps
3. **Generate improved version** similar to this
4. **Show comparison** of before vs after
5. **Explain improvements** made

**The result would be very similar to this improved version!**

---

## For Product Owners

**Key lesson:** The extra 15 minutes spent on details saves hours of developer questions and rework.

**Process:**
1. Write initial story (even if rough)
2. Use `/write-user-story` or `/refine-story` for help
3. Review AI suggestions
4. Add your domain expertise
5. Result: High-quality story like the "After" version

---

## For Developers

**When you receive a story like the "Before" version:**
1. Do NOT start implementation
2. Run `/refine-story` immediately
3. Review the improvements
4. Share with PO or proceed with improved version
5. Avoid wasting time on unclear requirements

---

## Related Examples

- `example-poor-story.md` - The original poor version with issues explained
- `example-good-login-story.md` - Another perfect story example
- `example-good-password-reset-story.md` - Complex story done right
- `example-technical-story.md` - Technical work as user story

---

**Last Updated:** 2025-11-24
