---
description: Convert Azure DevOps user story to Context Engineering feature request (SPEC.md)
---

# Convert User Story to Feature Request

You are helping a developer convert a user story from Azure DevOps into a Context Engineering feature request (SPEC.md) for PRP generation.

## Context

**Key Principle:** 1 User Story (1-3 days) = 1 Feature Request = 1 PRP

The Product Owner has written a user story in Azure DevOps. The developer now needs to convert this into the SPEC.md format, enriched with technical context from codebase research.

**Reference:** See `.claude/templates/story-to-spec.md` for conversion guidelines and examples.

---

## Process

### Step 1: Gather User Story Information

Ask the developer to provide the following information from the ADO user story:

```
Please provide the following from the Azure DevOps user story:

1. **ADO Work Item ID** (e.g., US-4523):
2. **Story Title**:
3. **User Story** (As a... I want... So that...):
4. **Acceptance Criteria** (all criteria):
5. **Description/Additional Context**:
6. **Story Points** (optional):
7. **Sprint** (optional):
8. **Any attached designs, mockups, or reference links** (optional):
```

**Developer can:**
- Copy/paste directly from ADO
- Provide a link to the ADO work item (you'll extract the details)
- Type it out manually

### Step 2: Parse and Validate User Story

**Validate the user story has:**
- [ ] Clear user type (not just "user")
- [ ] Specific capability description
- [ ] Business value/benefit
- [ ] At least 2 acceptance criteria
- [ ] Acceptance criteria are testable

**If missing critical elements:**
- Point out what's missing
- Suggest improvements
- Ask developer if they want to get clarification from PO or proceed with what they have

### Step 3: Research Codebase for Technical Context

Use the Task tool with `subagent_type=Explore` to research the codebase for relevant context.

**Research Goals:**

1. **Find Similar Implementations:**
   - Search for similar features, components, or patterns
   - Look for examples that solve similar problems
   - Identify reusable code

2. **Identify API Endpoints:**
   - Search API specification files (e.g., `docs/api/*.json`)
   - Find endpoints that match the user story requirements
   - Note request/response formats

3. **Find Relevant Libraries:**
   - Check `package.json` or equivalent for available libraries
   - Identify which libraries are already in use for similar features
   - Note versions

4. **Locate Related Files:**
   - Find files that will need to be modified
   - Find files that contain patterns to follow
   - Identify state management, API clients, components, etc.

5. **Identify Technical Constraints:**
   - Platform-specific requirements
   - Security considerations from existing code
   - Performance patterns
   - Testing patterns

**Research Strategy:**
- Start broad: search for keywords from the user story
- Get specific: look for exact component names, API routes, etc.
- Check examples: look in `examples/` directory if it exists
- Review docs: check `PRPs/ai_docs/` for library documentation

### Step 4: Ask Developer Clarifying Questions

Based on the user story and research, ask the developer:

1. **API Questions:**
   - "I found these API endpoints: [list]. Are these the correct ones to use?"
   - "Should we use [endpoint A] or [endpoint B] for [specific functionality]?"
   - "Are there any API endpoints not yet documented that this requires?"

2. **Technical Approach:**
   - "I found [similar component/pattern]. Should we follow this approach?"
   - "Should we reuse [existing component] or create a new one?"
   - "Which state management approach: [option A] or [option B]?"

3. **Scope Clarification:**
   - "The acceptance criteria mention [X]. Does this include [related functionality Y]?"
   - "Should error handling cover [specific scenarios]?"
   - "Are there platform-specific requirements (iOS vs Android, mobile vs web)?"

4. **Dependencies:**
   - "This depends on [other work]. Is that already complete?"
   - "Do we need to wait for [backend API/design/etc.]?"

### Step 5: Generate SPEC.md

Create the SPEC.md file with the following structure:

```markdown
<!-- SOURCE: ADO [WORK-ITEM-ID] -->
<!-- SPRINT: [Sprint Name/Number] -->
<!-- STORY POINTS: [Points] -->
<!-- CONVERTED: [Date] -->

## FEATURE

[Feature description from user story title]

**User Story:**
[As a... I want... So that... - verbatim from ADO]

**Acceptance Criteria:**
- [ ] [Criterion 1 - verbatim from ADO]
- [ ] [Criterion 2 - verbatim from ADO]
- [ ] [Criterion 3 - verbatim from ADO]

**Functional Requirements:**
[Derived from acceptance criteria - list specific functionality needed]
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## EXAMPLES

[Populated from codebase research]

**Similar Implementations:**
- [File path]: [Description of what to reference]
- [File path]: [Description of pattern to follow]

**Code Patterns:**
```[language]
// Example pattern from codebase
[relevant code snippet if applicable]
```

**Design References:**
- [Link to mockups/designs if provided in ADO]

## DOCUMENTATION

[Populated from codebase research]

**API Endpoints:**
- `[METHOD] [endpoint]` - [Description]
- `[METHOD] [endpoint]` - [Description]
- API Spec: [Path to API specification file]

**Libraries/Frameworks:**
- `[library-name]` ([version]) - [Usage]
- `[library-name]` ([version]) - [Usage]

**Related Files:**
- `[file-path]` - [What this file contains/does]
- `[file-path]` - [How it relates to this feature]

**External Documentation:**
- [Links to library docs, framework guides, etc.]

## OTHER CONSIDERATIONS

**Security:**
- [Security requirements specific to this feature]
- [Always include auth, validation, data protection considerations]

**User Experience:**
- [Loading states]
- [Error handling and messages]
- [Accessibility requirements]
- [Responsive design considerations]

**Testing:**
- [Unit tests needed]
- [Integration tests needed]
- [E2E test scenarios]
- [Edge cases to test]

**Dependencies:**
- [Other work items that must complete first]
- [Backend APIs that must be ready]
- [Design assets needed]
- [Configuration or infrastructure requirements]

**Technical Constraints:**
- [Platform-specific considerations]
- [Performance requirements]
- [Compatibility requirements]
- [Known limitations or gotchas]

**Additional Context from ADO:**
[Any relevant context from the ADO description or comments]
```

### Step 6: Save and Confirm

**File Naming:**
- Format: `[ado-id]-[short-description]-SPEC.md`
- Example: `US-4523-user-login-SPEC.md`
- Location: `PRPs/feature-requests/`

**After saving:**
1. Show the developer the generated SPEC.md path
2. Ask if they want to review/edit before proceeding to `/generate-prp`
3. Suggest next steps:
   ```
   ✅ Feature request created: PRPs/feature-requests/[filename]

   Next steps:
   1. Review the SPEC.md file for accuracy
   2. Make any necessary adjustments
   3. Run: /generate-prp PRPs/feature-requests/[filename]

   Or run /generate-prp now if everything looks good!
   ```

---

## Examples

### Example 1: Simple Login Story

**Developer Input:**
```
ADO Work Item ID: US-4523
Story Title: User login with email and password
User Story: As a mobile app user, I want to login with my email and password, so that I can access my account securely
Acceptance Criteria:
- Given I have a valid account, when I enter correct email/password, then I am logged in
- Given I enter incorrect password, when I submit, then I see "Invalid credentials" error
- Given I am logged in, when I restart the app, then I remain logged in
Story Points: 3
Sprint: Sprint 12
```

**Your Actions:**
1. Parse the user story ✓
2. Research codebase:
   - Search for existing auth patterns
   - Find API endpoints in `docs/api/auth-spec.json`
   - Locate form components, validation utils
   - Find secure storage implementation
3. Ask developer:
   - "I found POST /api/v1/auth/login endpoint. Is this correct?"
   - "Should we use the existing FormInput component or create a new one?"
   - "For token storage, I see expo-secure-store is already used. Continue with that?"
4. Generate `PRPs/feature-requests/US-4523-user-login-SPEC.md`
5. Prompt developer to review

### Example 2: Story with Missing Details

**Developer Input:**
```
ADO Work Item ID: US-5001
Story Title: Password reset
User Story: As a user, I want to reset my password
Acceptance Criteria: User can reset password
```

**Your Actions:**
1. Identify issues:
   - User type too generic
   - No "so that" benefit
   - Acceptance criteria not testable
   - No Given/When/Then format
2. Ask developer:
   ```
   This user story is missing some critical details:

   Issues found:
   - User type is generic ("user" instead of specific persona)
   - No business value ("so that" is missing)
   - Acceptance criteria is not testable
   - No Given/When/Then format

   Suggestions:
   - User type: "mobile app user who forgot password"?
   - Benefit: "so that I can regain access to my account"?
   - Acceptance criteria should include:
     * Requesting reset email
     * Receiving reset link
     * Submitting new password
     * Success confirmation

   Would you like to:
   A) Get clarification from the Product Owner
   B) Proceed with assumptions and I'll document them
   C) You'll provide the missing details now
   ```
3. Wait for developer input before proceeding

---

## Error Handling

### If ADO Work Item ID is Missing
- Warn developer but proceed
- Use a generated ID: `STORY-[timestamp]`
- Note in SPEC.md: `<!-- SOURCE: Manual entry - no ADO ID provided -->`

### If Research Finds No Relevant Code
- Note this in EXAMPLES section: "No similar implementations found in codebase - this is a new pattern"
- Proceed with research from AI docs and external sources
- Suggest extra caution during PRP generation

### If API Endpoints Not Found
- Check if API spec exists
- If not found, note in DOCUMENTATION: "API endpoints not yet documented - verify with backend team"
- Flag as a dependency

### If User Story is Too Large
- Warn developer: "This story seems large (estimated > 3 days). Consider breaking it down into smaller stories."
- Ask if they want to proceed or split it first
- If proceeding, note the size concern in SPEC.md

---

## Quality Checklist

Before finalizing SPEC.md, verify:

- [ ] User story is captured verbatim
- [ ] All acceptance criteria are listed as checkboxes
- [ ] Functional requirements are specific and actionable
- [ ] EXAMPLES section has at least 2-3 references (or notes why none exist)
- [ ] DOCUMENTATION section has specific API endpoints (or notes them as TBD)
- [ ] Related libraries are listed with versions
- [ ] Security considerations are included
- [ ] Testing requirements are specified
- [ ] Dependencies are identified
- [ ] File has proper metadata (ADO ID, sprint, story points, conversion date)

---

## Tips for Developers

**Make this command more effective by:**
- Providing complete user story information upfront
- Including links to mockups/designs
- Noting any known technical constraints
- Mentioning if this relates to other recent work

**After conversion:**
- Always review the generated SPEC.md
- Verify API endpoints match current specification
- Check that libraries/versions are correct
- Add any project-specific gotchas you know about

**When to skip this command:**
- Very technical work (refactoring, bug fixes) - write SPEC.md directly
- User story is too vague - get clarification first
- You're very familiar with the requirement - writing SPEC.md manually might be faster
