# Product Owner Guide: Context Engineering Integration

## Quick Start

**Good news:** Your workflow doesn't change! Continue using Azure DevOps exactly as you do today.

**What's different:** Developers use an AI-assisted system (Context Engineering) to implement your user stories faster and more consistently.

**Your role:**
1. Write user stories in Azure DevOps (same as always)
2. Provide clear acceptance criteria
3. Assign to developers
4. Review completed work

That's it! The Context Engineering system works behind the scenes.

---

## What is Context Engineering?

Context Engineering is a development workflow that uses AI to:
- Research the codebase for similar patterns
- Generate comprehensive implementation plans (PRPs)
- Execute step-by-step with validation gates
- Ensure consistent code quality

**For you as a Product Owner:** It means developers can implement your stories faster and with fewer questions, but you still need to write clear, well-defined user stories.

---

## Writing Effective User Stories

### Standard Format

```
Title: [Concise description of capability]

As a [specific user type]
I want [specific capability]
So that [specific benefit/value]

Acceptance Criteria:
- Given [context], when [action], then [expected result]
- Given [context], when [action], then [expected result]
- Given [context], when [action], then [expected result]

Description:
[Additional context, links to designs, business rationale]
```

### Story Size: Keep It Small

**Target:** 1-3 days of development work (3-8 story points)

**Good size indicators:**
- ✅ Single focused capability
- ✅ Can be completed in one sprint
- ✅ Can be deployed independently
- ✅ Delivers incremental value

**Too large indicators:**
- ❌ Multiple "and" statements in the "I want" section
- ❌ More than 5 acceptance criteria
- ❌ Estimated at 13+ story points
- ❌ Requires multiple sprints

**If a story is too large:** Break it down into smaller stories that each deliver value independently.

---

## Acceptance Criteria Best Practices

### Use Given/When/Then Format

**Format:**
```
Given [initial context or state]
When [action or event]
Then [expected outcome]
```

**Why this matters:**
- Developers use acceptance criteria to generate test cases
- AI can better understand and implement clear, structured criteria
- QA can verify each criterion independently

### Good Examples

✅ **GOOD - Specific and testable:**
```
Acceptance Criteria:
- Given I'm on the login screen, when I tap "Forgot Password", then I see the password reset form
- Given I enter a valid email in the reset form, when I tap "Send Reset Link", then I see confirmation message
- Given I check my email, when I click the reset link, then the app opens to the password reset screen
- Given I enter a valid new password, when I tap "Reset Password", then I'm logged in with the new password
```

**Why it's good:**
- Each criterion is independently testable
- Clear Given/When/Then structure
- Specific actions and outcomes
- Covers the full user flow

---

❌ **BAD - Vague and untestable:**
```
Acceptance Criteria:
- Password reset works
- User can reset their password
- Email is sent
```

**Why it's bad:**
- Not testable (what does "works" mean?)
- No context or actions specified
- Missing edge cases
- No clear success indicators

---

### Common Pitfalls to Avoid

❌ **Too technical:**
```
Given API endpoint /auth/reset is called
When POST request includes valid token
Then database updates password hash
```
**Why:** This is implementation detail, not business requirement. Focus on user behavior, not technical mechanics.

✅ **Better - User-focused:**
```
Given I submitted a password reset request
When I click the link in the reset email within 1 hour
Then I can set a new password successfully
```

---

❌ **Too vague:**
```
Given user wants to reset password
When they try to reset it
Then it should work
```
**Why:** No specific actions, states, or outcomes.

✅ **Better - Specific:**
```
Given I'm logged out and on the login screen
When I tap "Forgot Password" and enter my email address
Then I receive a password reset email within 5 minutes
```

---

## What Makes a Good User Story for Context Engineering?

### Essential Elements

1. **Specific User Type**
   - ❌ "As a user..."
   - ✅ "As a mobile app user..."
   - ✅ "As an admin user managing team permissions..."
   - ✅ "As a first-time visitor to the website..."

2. **Clear Capability**
   - ❌ "I want better performance..."
   - ✅ "I want the dashboard to load in under 2 seconds..."
   - ❌ "I want to manage my profile..."
   - ✅ "I want to update my profile photo and display name..."

3. **Measurable Benefit**
   - ❌ "So that I can use the feature..."
   - ✅ "So that I can make faster decisions with real-time data..."
   - ❌ "So that it's more convenient..."
   - ✅ "So that I don't have to remember multiple passwords..."

4. **Testable Acceptance Criteria**
   - Minimum 2 criteria (ideally 3-5)
   - Each criterion is independently verifiable
   - Covers happy path and key error cases
   - Uses Given/When/Then format

5. **Sufficient Context**
   - Links to mockups/designs (if available)
   - Business rationale
   - Any constraints (deadlines, compliance, platform requirements)
   - Dependencies on other work

---

## Real-World Examples

### Example 1: Login Feature

```
Title: User login with email and password

As a mobile app user
I want to login with my email and password
So that I can securely access my account and personal data

Acceptance Criteria:
- Given I have a registered account, when I enter correct email and password, then I am logged in and see my dashboard
- Given I enter an incorrect password, when I tap "Login", then I see an error message "Invalid email or password"
- Given I am logged in, when I close and reopen the app, then I remain logged in automatically
- Given I tap the password field, when I tap the "eye" icon, then I can see/hide my password
- Given I enter an invalid email format, when I try to login, then I see an error "Please enter a valid email address"

Description:
This is the primary authentication method for the mobile app. Users should be able to login quickly and securely. Session should persist across app restarts to avoid requiring login every time.

Design mockup: [Link to Figma]
Story Points: 5
```

**Why this is excellent:**
- Specific user type (mobile app user)
- Clear capability (login with email/password)
- Measurable benefit (secure access)
- 5 comprehensive acceptance criteria covering happy path and error cases
- All criteria use Given/When/Then
- Additional context provided
- Appropriate size (5 points)

---

### Example 2: Profile Photo Upload

```
Title: Upload and update profile photo

As a registered user
I want to upload a new profile photo from my device
So that other users can recognize me in the app

Acceptance Criteria:
- Given I'm on my profile page, when I tap my current photo, then I see options to "Take Photo" or "Choose from Library"
- Given I select "Take Photo", when I take a photo and confirm, then my profile photo is updated with the new image
- Given I select "Choose from Library", when I select an existing photo, then I can crop it before uploading
- Given I upload a photo larger than 5MB, when I try to save, then I see an error "Photo must be smaller than 5MB"
- Given I've uploaded a new photo, when other users view my profile, then they see my updated photo

Description:
Users should be able to easily update their profile photo. The photo will be visible to other users in various parts of the app (comments, chat, user lists).

Constraints:
- Maximum file size: 5MB
- Supported formats: JPG, PNG
- Image should be cropped to square
- Must work on both iOS and Android

Design mockup: [Link to design]
Story Points: 3
```

**Why this is excellent:**
- Specific user type
- Clear capability
- Business value (recognition)
- 5 acceptance criteria covering different scenarios
- Additional constraints clearly documented
- Appropriate size for one sprint

---

## What You DON'T Need to Include

As a Product Owner, you are **NOT** expected to provide:

❌ Technical implementation details
- Don't specify which API endpoints to use
- Don't specify which libraries or frameworks
- Don't specify code architecture

❌ Detailed technical requirements
- Don't write database schemas
- Don't specify authentication mechanisms (unless it's a business requirement like "must support SAML")
- Don't specify performance optimization techniques

**Developers will research these during conversion using the Context Engineering system.**

**You SHOULD include:**
- Business requirements (e.g., "must comply with GDPR")
- User experience requirements (e.g., "should load in under 2 seconds")
- Platform requirements (e.g., "must work on iOS and Android")
- Integration requirements (e.g., "must integrate with Salesforce")

---

## Common Questions

### Q: How detailed should my acceptance criteria be?

**A:** Detailed enough to be testable by QA. If a QA engineer can read the criterion and verify whether it's met, it's detailed enough.

**Too vague:** "Login works correctly"
**Just right:** "Given I enter a correct email and password, when I tap Login, then I am redirected to the dashboard within 3 seconds"

---

### Q: Should I write technical details if I know them?

**A:** Only include technical details that are **business requirements or constraints**:

✅ Include:
- "Must comply with HIPAA" (regulatory)
- "Must work offline" (user requirement)
- "Must integrate with existing Stripe account" (business constraint)
- "Response time must be under 2 seconds" (performance requirement)

❌ Don't include:
- "Use React Query for data fetching" (implementation detail)
- "Store tokens in LocalStorage" (implementation detail - and potentially wrong!)
- "Use POST /api/v1/users endpoint" (unless you're documenting existing API)

---

### Q: What if I don't have designs yet?

**A:** That's okay! Provide as much detail as you can in the acceptance criteria and description. Developers can ask clarifying questions or work from similar patterns in the app.

**Consider:**
- Describing the layout in words
- Referencing similar screens in the app
- Sketching a rough wireframe
- Linking to competitor examples

---

### Q: How does this affect sprint planning?

**A:** Sprint planning works the same way:
1. You prioritize stories in the backlog
2. Team estimates story points
3. Team commits to stories for the sprint
4. Developers pull stories and implement them

**What changes:** Developers use Context Engineering to implement faster, but your sprint planning process remains identical.

---

### Q: Will developers ask me fewer questions?

**A:** Possibly! Because Context Engineering researches the codebase automatically, developers may have answers to technical questions without needing to ask you. However, you should still expect questions about:
- Business logic and edge cases
- User experience decisions
- Priority and scope clarifications

---

### Q: Can I see the AI-generated implementation plans?

**A:** Yes! Developers can share the generated PRP (Plan for Reliable Progression) with you if you're curious. However, it's quite technical and you don't need to review it.

**What you should review:**
- Completed implementation against acceptance criteria
- User experience and functionality
- Any deviations from the original story

---

## Checklist: Before Assigning a Story

Use this checklist to ensure your user story is ready for development:

- [ ] **User story format:** Has "As a [user], I want [capability], so that [benefit]"
- [ ] **Specific user type:** Not just "user" - be specific about who
- [ ] **Clear capability:** One focused capability, not multiple unrelated features
- [ ] **Measurable benefit:** Clear value proposition
- [ ] **Minimum 2 acceptance criteria:** Ideally 3-5 criteria
- [ ] **Given/When/Then format:** Each criterion structured properly
- [ ] **Testable criteria:** QA can verify each one
- [ ] **Appropriate size:** 1-3 days (3-8 story points)
- [ ] **Context provided:** Links to designs, mockups, or additional info if available
- [ ] **Constraints documented:** Any deadlines, platform requirements, or business constraints noted
- [ ] **Dependencies identified:** Other stories that must complete first are noted

---

## Getting Help

**Questions about user story format:**
- Review the examples in this guide
- Ask your development team during backlog refinement
- Consult with other Product Owners

**Questions about technical feasibility:**
- Discuss with developers during sprint planning
- Ask for rough estimates before writing detailed stories
- Developers can help break down large stories

**Questions about the Context Engineering workflow:**
- Ask your development lead
- Developers can explain how they use your stories
- See `.claude/CLAUDE.md` for technical documentation (advanced)

---

## Summary

**Your job hasn't changed:**
1. Write clear, focused user stories in Azure DevOps
2. Use Given/When/Then acceptance criteria
3. Provide business context and constraints
4. Prioritize and plan sprints

**What's new:**
- Developers implement faster with AI assistance
- You might get fewer clarifying questions
- Implementation is more consistent

**Keep doing:**
- ✅ Writing small, focused stories (1-3 days)
- ✅ Using Given/When/Then acceptance criteria
- ✅ Providing clear business value
- ✅ Linking to designs and context

**Stop doing:**
- ❌ Writing technical implementation details
- ❌ Creating large multi-week stories
- ❌ Leaving acceptance criteria vague

---

**Questions?** Ask your development team lead or consult the developer documentation at `.claude/CLAUDE.md`.
