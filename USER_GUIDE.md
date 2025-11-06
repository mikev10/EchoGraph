# User Guide: Feature Development Workflow

This guide explains how to request, plan, and implement features using the Feature Request → PRP → Implementation workflow.

## Table of Contents

1. [Overview](#overview)
2. [The Three-Stage Workflow](#the-three-stage-workflow)
3. [Stage 1: Create Feature Request](#stage-1-create-feature-request)
4. [Stage 2: Generate PRP](#stage-2-generate-prp)
5. [Stage 3: Execute PRP](#stage-3-execute-prp)
6. [File Structure](#file-structure)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This workflow separates **what** you want built (feature request) from **how** it will be built (PRP) and the actual **implementation** (execution). This ensures comprehensive planning before coding begins.

**Benefits:**
- Reduces implementation errors
- Ensures all context is gathered upfront
- Creates documentation trail
- Enables reusable feature templates
- Provides confidence scoring before implementation

---

## The Three-Stage Workflow

```
┌─────────────────────┐
│ 1. Feature Request  │  You create INITIAL.md
│    (INITIAL.md)     │  describing what to build
└──────────┬──────────┘
           │
           │ /generate-prp
           ▼
┌─────────────────────┐
│ 2. Generate PRP     │  AI researches codebase,
│    (feature.md)     │  fetches docs, creates plan
└──────────┬──────────┘
           │
           │ /execute-prp
           ▼
┌─────────────────────┐
│ 3. Execute PRP      │  AI implements step-by-step
│    (implementation) │  with validation gates
└─────────────────────┘
```

---

## Stage 1: Create Feature Request

### Location
Save feature requests in: `PRPs/feature-requests/`

### Naming Convention
`feature-name-INITIAL.md`

Example: `user-authentication-INITIAL.md`

### Required Structure

Your INITIAL.md file MUST contain these 4 sections:

#### 1. FEATURE
**What to include:**
- Specific functionality to implement
- User capabilities/actions
- Expected behavior

**Example:**
```markdown
## FEATURE

Implement user authentication system with login, logout, and token refresh capabilities.

Users should be able to:
- Login with email and password
- Receive JWT token on successful authentication
- Automatically refresh tokens before expiry
- Logout and clear session
- See appropriate error messages for failed login attempts
```

#### 2. EXAMPLES
**What to include:**
- Code examples showing expected structure
- Screenshots or mockups (if UI-related)
- Links to similar implementations

**Example:**
```markdown
## EXAMPLES

**Login Flow:**
```typescript
// User enters credentials
const credentials = { email: 'user@example.com', password: 'secret123' }

// System authenticates
const response = await api.post('/auth/login', credentials)
// Returns: { token: 'jwt...', refreshToken: 'refresh...', user: {...} }

// Token stored securely and used for subsequent requests
```

**Error Handling:**
```typescript
// Invalid credentials
try {
  await api.post('/auth/login', invalidCredentials)
} catch (error) {
  // Show: "Invalid email or password"
}
```
```

#### 3. DOCUMENTATION
**What to include:**
- Links to official library documentation
- API specification references
- Related examples in your codebase

**Example:**
```markdown
## DOCUMENTATION

- JWT Best Practices: https://jwt.io/introduction
- Token Storage Security: https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#local-storage
- React Authentication Patterns: https://reactjs.org/docs/context.html
- Internal API: PRPs/ai_docs/auth-api-spec-summary.md
- Related patterns: examples/integrations/auth/
```

#### 4. OTHER CONSIDERATIONS
**What to include:**
- Security requirements
- Performance constraints
- Compatibility requirements
- Known gotchas
- References to CLAUDE.md sections

**Example:**
```markdown
## OTHER CONSIDERATIONS

- Tokens should be stored securely (not localStorage)
- Auto-refresh tokens 5 minutes before expiry
- Redirect to login page on 401 responses
- Clear all user data on logout
- Add loading states for all auth operations
- Consider rate limiting for login attempts
- See CLAUDE.md for Security Rules section
```

### Template
Use the template at: `PRPs/feature-requests/user-authentication-INITIAL.md`

Copy and customize it for new feature requests.

---

## Stage 2: Generate PRP

### Command
```bash
/generate-prp PRPs/feature-requests/your-feature-INITIAL.md
```

### What Happens
The AI will:
1. **Research your codebase** - Examines `examples/` folder for patterns
2. **Review conventions** - Reads `CLAUDE.md` for project rules
3. **Fetch documentation** - Retrieves docs from URLs you provided
4. **Verify API specs** - Checks endpoints against API specifications (if applicable)
5. **Ask clarifications** - Requests additional info if needed
6. **Generate comprehensive PRP** - Creates detailed implementation plan

### Output
The generated PRP will be saved as: `PRPs/your-feature.md`

### PRP Contents
The generated PRP includes:

1. **Goal** - One sentence summary
2. **Why** - Business value and user impact
3. **What (Success Criteria)** - Testable requirements as checkboxes
4. **All Needed Context** - API endpoints, data models, UI components, libraries, gotchas
5. **Implementation Blueprint** - 8-15 sequential steps with validation
6. **Validation Loop** - Commands to test (lint, type-check, tests)
7. **Confidence Score** - X/10 rating on implementability

### Confidence Score Guide
- **9-10**: Zero clarifying questions needed - ready to implement
- **7-8**: 1-2 clarifications on edge cases
- **5-6**: Several clarifications needed
- **3-4**: Significant context gaps
- **1-2**: Too vague to implement

If score is below 7, review the PRP and add missing context before executing.

---

## Stage 3: Execute PRP

### Command
```bash
/execute-prp PRPs/your-feature.md
```

### What Happens
The AI will:
1. Break down PRP into granular todos (using TodoWrite tool)
2. Execute step-by-step with validation gates
3. Run tests and validation commands after each major step
4. Mark tasks complete as they finish
5. Update task progress in `.claude/TASK.md` (if applicable)

### Monitoring Progress
Watch the todo list updates during execution:
- `pending` - Task not yet started
- `in_progress` - Currently working (only one at a time)
- `completed` - Task finished successfully

### Validation
At each major milestone, the AI will run:
```bash
npm run type-check  # or equivalent for your project
npm run lint
npm test
```

These ensure code quality before proceeding.

---

## File Structure

```
PRPs/
├── feature-requests/          # Your feature request files
│   ├── user-authentication-INITIAL.md
│   ├── payment-integration-INITIAL.md
│   └── dashboard-widget-INITIAL.md
│
├── user-authentication.md     # Generated PRPs
├── payment-integration.md
├── dashboard-widget.md
│
└── ai_docs/                   # AI-friendly documentation summaries
    ├── stripe-api-summary.md
    └── react-query-patterns.md

examples/                      # Reference implementations
├── integrations/
├── state/
└── testing/

.claude/
├── CLAUDE.md                  # Project conventions (auto-loaded)
├── PLANNING.md                # Architecture (auto-loaded)
├── TASK.md                    # Master task list
└── tasks/                     # Feature-level task files
    ├── TASK-001-auth.md
    └── TASK-002-payment.md
```

---

## Best Practices

### Writing Feature Requests

**DO:**
- Be specific about functionality and behavior
- Include code examples showing expected structure
- Link to official documentation
- Mention security/performance requirements
- Reference existing patterns in your codebase

**DON'T:**
- Be vague ("add some auth stuff")
- Skip sections (all 4 are required)
- Assume AI knows your specific API
- Forget error handling scenarios
- Leave out constraints/gotchas

### PRP Generation

**Before generating:**
- Ensure all 4 sections are complete
- Verify documentation URLs are accessible
- Check that similar examples exist in `examples/` folder

**After generating:**
- Review the confidence score
- Check that API endpoints match your specification
- Verify the implementation steps make sense
- Ensure validation commands are correct for your project

### PRP Execution

**Before executing:**
- Commit any uncommitted changes
- Ensure your working directory is clean
- Review the PRP one more time

**During execution:**
- Monitor the todo list progress
- Watch for validation failures
- Be ready to provide clarifications if AI asks

---

## Troubleshooting

### "Cannot read INITIAL.md file"
**Cause**: File path is incorrect or file doesn't exist

**Solution**:
- Check file exists at the path specified
- Use full path: `PRPs/feature-requests/your-feature-INITIAL.md`
- Verify you're in project root directory

### "Missing required section: FEATURE"
**Cause**: INITIAL.md file is incomplete

**Solution**:
- Ensure all 4 sections exist: FEATURE, EXAMPLES, DOCUMENTATION, OTHER CONSIDERATIONS
- Check section headers match exactly (case-sensitive)

### Low Confidence Score (below 7)
**Cause**: Insufficient context or unclear requirements

**Solution**:
- Add more code examples to EXAMPLES section
- Include more detailed documentation links
- Add references to existing patterns in your codebase
- Specify API endpoints and data structures
- Clarify ambiguous requirements

### PRP execution fails validation
**Cause**: Generated code doesn't pass tests/lint/type-check

**Solution**:
- AI will automatically attempt to fix validation errors
- If stuck, AI may ask for clarification
- Check that validation commands in PRP match your project setup

### AI asks too many questions during generation
**Cause**: Feature request lacks necessary details

**Solution**:
- Make FEATURE section more specific
- Add more code examples to EXAMPLES
- Include complete documentation links
- Specify all constraints in OTHER CONSIDERATIONS

### Generated PRP doesn't match my architecture
**Cause**: AI doesn't have enough context about your project patterns

**Solution**:
- Add reference implementations to `examples/` folder
- Update `CLAUDE.md` with project-specific conventions
- Update `PLANNING.md` with architectural decisions
- Reference these in your INITIAL.md file

---

## Quick Reference

### Commands
```bash
# Generate PRP from feature request
/generate-prp PRPs/feature-requests/your-feature-INITIAL.md

# Execute the PRP
/execute-prp PRPs/your-feature.md

# Validate tasks (after manual updates)
/validate-tasks
```

### File Naming
- Feature requests: `feature-name-INITIAL.md`
- Generated PRPs: `feature-name.md`
- Task files: `TASK-XXX-feature-name.md`

### Required Sections (INITIAL.md)
1. `## FEATURE` - What to build
2. `## EXAMPLES` - Code examples
3. `## DOCUMENTATION` - Links and references
4. `## OTHER CONSIDERATIONS` - Requirements and constraints

---

## Additional Resources

- **Project Conventions**: `.claude/CLAUDE.md`
- **Architecture**: `.claude/PLANNING.md`
- **Current Tasks**: `.claude/TASK.md`
- **Example Patterns**: `examples/` folder
- **API Documentation**: `PRPs/ai_docs/` folder

---

## Need Help?

If you encounter issues not covered in this guide:
1. Check `.claude/CLAUDE.md` for project-specific guidance
2. Review existing PRPs for examples
3. Ask AI for clarification using natural language
4. Report issues at: https://github.com/anthropics/claude-code/issues
