---
description: Generate comprehensive PRP from feature request (INITIAL.md format)
---

You are about to generate a Product Requirements Prompt (PRP) from a feature request.

**Input**: Path to feature request file in INITIAL.md format (must contain FEATURE, EXAMPLES, DOCUMENTATION, OTHER CONSIDERATIONS sections)

**Mandatory Research Phase (CRITICAL)**:
Before writing the PRP, you MUST research:

1. **Codebase Patterns** (examine examples/ folder):
   - Search `examples/` for similar implementations
   - Review `CLAUDE.md` for project conventions
   - Check existing PRPs for pattern consistency
   - **Verify API endpoints against API specification (if applicable)**

2. **External Documentation**:
   - Fetch official docs for libraries used (URLs in DOCUMENTATION section)
   - Read specific sections referenced in feature request
   - Look for code examples in official documentation

3. **User Clarification** (if needed):
   - Request clarification on integration points
   - Ask about ambiguous requirements
   - Confirm technical approach

**PRP Document Requirements**:

The generated PRP must include:

### 1. Goal (one sentence)
What are we building?

### 2. Why (business value)
User impact and business justification

### 3. What (Success Criteria)
- [ ] Specific, testable requirement 1
- [ ] Specific, testable requirement 2
[ALL requirements as checkboxes]

### 4. All Needed Context

#### API Endpoints
**CRITICAL:** Verify all endpoints against API specification BEFORE implementation (if applicable).

**Specification Sources (if applicable):**
- Full spec: `docs/api/[[YOUR_API_SPEC]].json` or `.yaml`
- AI summary: `PRPs/ai_docs/[[your-api]]-spec-summary.md` (if created)
- API documentation URL: [[YOUR_API_DOCS_URL]]

**For each endpoint, document:**
- Full path with parameters (e.g., `/api/users/{userId}`)
- HTTP method (GET/POST/PUT/DELETE/PATCH)
- Request body schema
- Response schemas (success and error cases)
- Required headers
- Authentication requirements
- Full request/response TypeScript/type examples

#### Data Models
[Complete interfaces/types]

#### UI Components (if applicable)
[UI library components to use, reference patterns from codebase]

#### Libraries/Dependencies
[Specific libraries needed, check existing dependencies]

#### Known Gotchas
[Common pitfalls, library-specific considerations from CLAUDE.md]

#### Related Files
[Exact file paths that will be created or modified]

### 5. Implementation Blueprint

Break into sequential steps (typically 8-15 steps):

**Step N: [Task Name]**
- **What**: Clear description
- **Files**: Exact paths with purpose
- **Code Pattern**: Reference working example from examples/ folder
- **Validation**: Specific command to test (e.g., npm run type-check)

### 6. Validation Loop

**Syntax/Style Check:**
```bash
npm run type-check
npm run lint
```

**Unit Tests:**
```bash
npm test src/features/[feature-name]
```

**Integration Tests:**
[Manual test steps or E2E test commands]

**Acceptance Testing:**
- [ ] User can [specific action]
- [ ] System responds with [expected behavior]
- [ ] Error case [scenario] shows [expected result]

### 7. Confidence Score (X/10)

Rate confidence that AI can implement this with current context:
- 9-10: Zero clarifying questions needed
- 7-8: 1-2 clarifications on edge cases
- 5-6: Several clarifications needed
- 3-4: Significant context gaps
- 1-2: Too vague to implement

**Quality Validation** (before saving):
✓ All necessary context included
✓ Executable validation commands present
✓ References existing code patterns from examples/
✓ Clear implementation path with pseudocode
✓ Error handling documented

**Output**: Save PRP to `PRPs/active/{feature-name}.md`

**Goal**: Enable one-pass implementation success through comprehensive context
