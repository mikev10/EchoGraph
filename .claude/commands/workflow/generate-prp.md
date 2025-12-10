---
description: Generate comprehensive PRP from feature request (SPEC.md format)
---

You are about to generate a Product Requirements Prompt (PRP) from a feature request.

**Input**: Path to feature request file in SPEC.md format (must contain FEATURE, EXAMPLES, DOCUMENTATION, OTHER CONSIDERATIONS sections)

**Mandatory Research Phase (CRITICAL)**:
Before writing the PRP, you MUST use MCP servers to gather accurate context:

1. **Query local-rag for Project Context** (MANDATORY):
   ```javascript
   // Find existing patterns
   mcp__local-rag__query_documents({
     query: "similar features and implementations related to [feature name]",
     limit: 5
   })

   // Verify style guide and conventions
   mcp__local-rag__query_documents({
     query: "design patterns styling conventions for [feature type]",
     limit: 3
   })

   // Check API endpoints (if applicable - CRITICAL!)
   mcp__local-rag__query_documents({
     query: "[feature] API endpoints methods request response",
     limit: 5
   })
   // Verify: Exact paths, methods, schemas, headers

   // Find component/code patterns
   mcp__local-rag__query_documents({
     query: "component patterns best practices for [feature type]",
     limit: 3
   })
   ```

2. **Fetch Library Documentation** (context7) (MANDATORY):
   ```javascript
   // Resolve library names to Context7 IDs
   mcp__context7__resolve-library-id({
     libraryName: "[primary library]"  // e.g., "next.js", "react"
   })

   // Fetch documentation with topic focus
   mcp__context7__get-library-docs({
     context7CompatibleLibraryID: "/org/project",
     topic: "[specific topic]",  // e.g., "server actions", "app router"
     tokens: 5000-7000
   })
   // Returns: Accurate API signatures, current patterns, real examples
   ```

3. **Research Best Practices** (perplexity) (RECOMMENDED):
   ```javascript
   // Use 'reason' model for complex analysis
   mcp__perplexity__reason({
     query: "How to implement [feature] in [tech stack]?
            Consider: [specific requirements]
            Environment: [framework versions, key dependencies]
            Include: Architecture patterns, best practices, code examples"
   })

   // Use 'deep_research' for comprehensive evaluation (if time permits)
   mcp__perplexity__deep_research({
     query: "[feature] implementation strategies and tradeoffs",
     focus_areas: ["performance", "scalability", "user experience"]
   })
   ```

4. **Review Codebase** (traditional methods):
   - Search `examples/` for similar implementations (use Grep/Glob)
   - Review `CLAUDE.md` for project conventions (use Read)
   - Check existing PRPs for pattern consistency (use Glob *.md)

5. **User Clarification** (if needed):
   - Use AskUserQuestion for ambiguous requirements
   - Request clarification on integration points
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

### Task Creation (Mandatory)

**When generating a PRP, AUTOMATICALLY create a corresponding task:**

1. **Determine Next Task ID:**
   - Read `.claude/TASK.md` to find highest existing TASK-XXX number
   - Increment by 1 for new task (e.g., if TASK-007 exists, use TASK-008)

2. **Create Task Entry in TASK.md:**
   - Add new entry to "Pending" section:
     ```markdown
     - [ ] [TASK-XXX] Brief description from PRP goal → @.claude/tasks/TASK-XXX-feature-name.md
     ```
   - Use feature name from PRP filename (e.g., `project-setup.md` → `TASK-008-project-setup.md`)

3. **Create Task File:**
   - Create `.claude/tasks/TASK-XXX-feature-name.md` with this structure:
     ```markdown
     # [TASK-XXX] Feature Name

     **Status**: Pending
     **Parent Task**: References `.claude/TASK.md` entry for TASK-XXX
     **Started**: Not yet
     **Completed**: Not yet

     ## Context

     [Copy from PRP Goal and Why sections]

     ## Feature Request

     **Location**: `[Path to original feature request file]`

     ## Implementation

     **PRP Location**: `PRPs/active/[feature-name]-PRP.md` (move to `PRPs/completed/` when done)

     ## Subtasks

     [Break down from Implementation Blueprint - 3-10 items]
     - [ ] [TASK-XXX.1] First implementation step
     - [ ] [TASK-XXX.2] Second implementation step
     - [ ] [TASK-XXX.3] Third implementation step
     ...

     ## Dependencies

     [List any prerequisite tasks or related features]

     ## Notes

     [Any important context from feature request]

     ---

     **Last Updated**: [Today's date]
     ```

4. **Add Task Reference to PRP Header:**
   - At the very top of the PRP (above Goal section), add:
     ```markdown
     **Task**: [TASK-XXX] Feature name (from `.claude/TASK.md`)
     **Task File**: @.claude/tasks/TASK-XXX-feature-name.md
     ```

5. **Verify Task Creation:**
   - Confirm task entry exists in `.claude/TASK.md` under "Pending"
   - Confirm task file `.claude/tasks/TASK-XXX-feature-name.md` was created
   - Confirm PRP header contains task reference
   - If any missing, STOP and complete task creation before saving PRP

**Result**: Each PRP has exactly ONE corresponding task. Simple 1:1 mapping.

**Output**: Save PRP to `PRPs/active/{feature-name}-PRP.md`

**Goal**: Enable one-pass implementation success through comprehensive context
