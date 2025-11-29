---
description: Execute PRP step-by-step with validation gates and ULTRATHINK planning
---

You are about to execute a Product Requirements Prompt (PRP).

**Input**: Path to PRP file (e.g., `PRPs/active/01-reservation-calendar.md`)

**Pre-Execution Checklist:**

Before executing PRP, verify:
- [ ] PRP header contains **Parent Task** and **Child Task** IDs
- [ ] Parent task exists in `.claude/TASK.md`
- [ ] Feature task file exists (`.claude/tasks/TASK-XXX-*.md`)
- [ ] Child subtask exists in feature task file
- [ ] Subtask is not already marked complete

**If any check fails:**
- STOP execution immediately
- Report which check failed
- Prompt user to fix task linkage first (run `/generate-prp` again or manually add task IDs)

**Process**:

## Phase 0: Skills & Feature Branch (MANDATORY)

This phase MUST be executed before any code changes. It ensures proper context management and git hygiene.

### Step 0.1: Invoke Context-Optimizer Skill

**Invoke the context-optimizer skill IMMEDIATELY:**

```typescript
// Use Skill tool to invoke context-optimizer
Skill({ skill: "context-optimizer" })
```

**This skill:**

- Optimizes token usage for large cleanup operations
- Manages context efficiently across multi-step workflows
- Enforces efficient context usage while maintaining quality
- Essential for cleanup operations that involve 10+ files

**CRITICAL**: Do not proceed until context-optimizer skill is active.

### Step 0.5.2: Create Feature Branch

**ALWAYS create a feature branch before making any code changes:**

```bash
# Get current branch name
git branch --show-current

# Create and checkout feature branch
# Branch naming convention: cleanup/<scope>-<date>
git checkout -b cleanup/[scope]-YYYY-MM-DD

# Example:
# git checkout -b cleanup/likes-page-2025-01-15
# git checkout -b cleanup/dashboard-components-2025-01-15
# git checkout -b cleanup/design-system-violations-2025-01-15
```

**Branch naming rules:**

- Prefix: `cleanup/`
- Scope: Extract from execution plan (e.g., `likes-page`, `dashboard`, `admin-panel`)
- Date: Current date in YYYY-MM-DD format
- Example: `cleanup/likes-page-2025-01-15`

**Verification:**

```bash
# Verify you're on the feature branch (not main/dev)
git branch --show-current
# Should NOT be 'main' or 'dev'
```

**If already on a cleanup branch:**

- Verify branch name follows convention
- If not, create new branch with correct naming

**CRITICAL**: Do NOT proceed with any code changes until feature branch is confirmed.

### Phase 1: Load PRP & MCP Validation
- Read the specified PRP file completely
- Understand all context and requirements

**MCP Validation (MANDATORY)**:

1. **Verify Style Guide** (local-rag):

   ```javascript
   // Query design system and conventions
   mcp__local-rag__query_documents({
     query: "design system colors spacing typography conventions",
     limit: 3
   })

   // Query specific styling for feature type
   mcp__local-rag__query_documents({
     query: "styling patterns conventions for [feature type]",
     limit: 3
   })
   ```

2. **Verify API Endpoints** (local-rag - if applicable):

   ```javascript
   // Query for specific endpoints used in PRP
   mcp__local-rag__query_documents({
     query: "[feature] API endpoints used in this PRP",
     limit: 5
   })
   // Verify: Exact paths, methods, request/response schemas, headers
   ```

3. **Find Similar Implementations** (local-rag):

   ```javascript
   // Search for existing patterns
   mcp__local-rag__query_documents({
     query: "similar component implementations patterns",
     limit: 3
   })
   // Review: Established patterns for consistency
   ```

4. **Fetch Library APIs** (context7 - if needed):

   ```javascript
   // Only if PRP uses specific library features
   mcp__context7__resolve-library-id({
     libraryName: "[library]"
   })
   mcp__context7__get-library-docs({
     context7CompatibleLibraryID: "/org/project",
     topic: "[specific API or feature]",
     tokens: 5000
   })
   ```

5. **Additional Research** (traditional methods):
   - Search codebase for patterns (Grep/Glob)
   - Review examples/ folder (Read)
   - Check CLAUDE.md conventions (Read)

### Phase 1.5: Verify Task Linkage (MANDATORY)

**Before planning implementation, verify PRP is linked to task system:**

1. **Read PRP Header:**
   - Extract Parent Task ID (e.g., `[TASK-005]`)
   - Extract Child Task ID (e.g., `[TASK-005.4]`)
   - If either missing, STOP execution and report:

     ```
     ⚠️ BLOCKED: PRP is missing task linkage in header.

     This PRP needs to be linked to the task system before execution.

     Options:
     1. Re-run /generate-prp with task linkage enabled
     2. Manually add task IDs to PRP header
     3. Create task entries in .claude/TASK.md and .claude/tasks/
     ```

2. **Verify Parent Task Exists:**
   - Read `.claude/TASK.md`
   - Confirm parent task ID exists (e.g., `[TASK-005]`)
   - If missing, STOP and report missing parent task

3. **Verify Feature Task File Exists:**
   - Check if `.claude/tasks/TASK-XXX-*.md` exists
   - Use the task ID from PRP header to find correct file
   - If missing, STOP and report missing feature task file

4. **Verify Child Subtask Exists:**
   - Read feature task file
   - Confirm child subtask ID exists (e.g., `[TASK-005.4]`)
   - Check if already marked complete `[x]`
   - If already complete, warn user but allow re-execution
   - If missing, STOP and report missing subtask

5. **Load Task Context:**
   - Read feature task file for additional context
   - Note any existing blockers or dependencies
   - Review related subtasks for consistency

**If all verifications pass:**
- Proceed to Phase 2: ULTRATHINK
- Task linkage confirmed ✅

**If any verification fails:**
- STOP execution with BLOCKED status
- Report specific failure
- Provide remediation steps

### Phase 2: ULTRATHINK (Mandatory Planning Phase)

### **CRITICAL: You must plan before coding**

1. **Break Down Tasks**:
   - Read the feature task file (`.claude/tasks/TASK-XXX-*.md`) loaded in Phase 1.5
   - Identify the specific subtask this PRP addresses (e.g., `[TASK-005.4]`)
   - Use TodoWrite tool for granular session-level tasks (ephemeral)
   - Break complex tasks into smaller steps
   - Identify dependencies between steps
   - Map tasks to PRP implementation blueprint
   - **Note:** TodoWrite is for step-by-step execution only (does not persist)
   - **Persistent tracking:** Feature task file will be updated after major milestones

2. **Identify Patterns**:
   - Which examples/ files are relevant?
   - Which CLAUDE.md rules apply?
   - Are there existing similar implementations?
   - Review related subtasks in feature task file for consistency

3. **Plan Execution Strategy**:
   - Sequential vs parallel tasks
   - Validation checkpoints
   - Potential blockers (check feature task file for known blockers)
   - Document planned approach in feature task file Notes section

### Phase 3: Execute Implementation Blueprint

For EACH major milestone step in the PRP (not every tiny step):

1. **Mark Step as in_progress** (TodoWrite - session level)

2. **Implement** following the step's guidance:
   - **Verify API contract in specification (if applicable)**
   - Match endpoint paths, methods, schemas exactly
   - Reference code patterns from examples/
   - Follow CLAUDE.md conventions
   - Use exact types from PRP (matching API spec definitions)
   - Add comments for complex logic

3. **Validate Step**:

   ```bash
   [[VALIDATION_COMMAND_1]]  # Must exit 0
   [[VALIDATION_COMMAND_2]]  # Must exit 0
   [[TEST_COMMAND]] [path]   # Must pass (if applicable)
   ```

4. **Fix Failures** (iterative loop):
   - If validation fails, analyze errors
   - Fix issues
   - Re-run validation
   - Retry up to 3 times
   - If still failing: STOP and report blocker

5. **Mark Step as completed** (TodoWrite - session level)

6. **Update Feature Task File** (persistent - after major milestones):
   - Read feature task file (`.claude/tasks/TASK-XXX-*.md`)
   - Add notes to **Notes** section about what was completed:

     ```markdown
     - [YYYY-MM-DD] Completed [step description]: [brief summary of implementation]
     ```

   - Document any important decisions or gotchas discovered
   - Update **Blockers** section if encountered any issues
   - Update **Last Updated** timestamp
   - **Do NOT mark subtask complete yet** (only in Phase 5 when entire PRP done)

7. **Proceed to Next Step**

### Phase 4: Complete

After all steps:

1. **Run Full Validation Suite**:

   ```bash
   [[VALIDATION_COMMAND_1]]
   [[VALIDATION_COMMAND_2]]
   [[TEST_COMMAND]]
   [[BUILD_COMMAND]]  # or project-specific build command
   ```

2. **Check Acceptance Criteria**:
   - Verify all checkboxes from "What (Success Criteria)"
   - Test each acceptance criterion manually

3. **Generate Summary**:
   - List all files created/modified
   - Report test results
   - Note any deviations from PRP
   - Document any discovered gotchas

4. **Add Completion Summary to PRP** (MANDATORY):
   - Append completion documentation to the PRP file itself
   - This ensures the PRP serves as a complete historical record
   - The completion summary will be ingested into local-rag via `/update-rag`

   **Required Format:**

   ```markdown
   ---

   **Last Updated**: [original date from PRP header]
   **Completed**: YYYY-MM-DD
   **Status**: ✅ COMPLETE - [brief status description]

   ## Completion Summary

   **Date Completed**: YYYY-MM-DD
   **Implementation Quality**: [High/Medium/Low] - [brief assessment]

   **Deliverables**:
   - ✅ [specific deliverable 1]
   - ✅ [specific deliverable 2]
   - ✅ [specific deliverable N]

   **Key Deviations from Original Plan**:
   1. [Deviation description]: [rationale for change]
   2. [Another deviation if applicable]

   **Testing Results**:
   - [Summary of manual testing]
   - [Summary of automated tests if applicable]
   - [Any test failures or known issues]

   **Total Implementation Time**: [realistic estimate]
   **Code Quality**: [Production-ready / Needs refinement / Prototype]
   ```

   **What to Include:**
   - **Deliverables**: Concrete list of what was actually built (endpoints, files, features)
   - **Deviations**: ANY changes from original PRP plan with rationale
   - **Testing**: Actual testing performed (manual + automated)
   - **Quality**: Honest assessment of code quality and production-readiness

   **For IN_PROGRESS or BLOCKED status:**
   - Use status: `🔄 IN_PROGRESS` or `⚠️ BLOCKED` instead of `✅ COMPLETE`
   - Document what was completed and what remains
   - Note blockers or reasons for stopping

5. **Update Context**:
   - If new patterns emerged, add to examples/
   - Update CLAUDE.md if needed
   - Add gotchas to PRP or docs (if not already in completion summary)

### Phase 5: Update Task Hierarchy (ALWAYS - For All Statuses)

**PRP STATUS Options:**
- ✅ **COMPLETED**: All requirements met, all validations pass
- ⚠️ **BLOCKED**: Cannot proceed, requires user input
- 🔄 **IN_PROGRESS**: Partial completion, continue later

**Update Task Hierarchy** (for ALL statuses):

1. **Load Task Context:**
   - Read PRP header for task IDs (Parent Task and Child Task)
   - Load feature task file (`.claude/tasks/TASK-XXX-*.md`)

2. **Verify PRP Completion Summary Added** (for COMPLETED status):
   - Confirm completion summary was added to PRP file in Phase 4, step 4
   - The completion summary in the PRP is the "source of truth" for what was delivered
   - Feature task file notes should reference the completed PRP

3. **Update Feature Task File** (based on status):

   **If status is ✅ COMPLETED:**
   - Mark subtask complete:

     ```markdown
     - [x] [TASK-XXX.Y] Subtask description
     ```

   - Update **Notes** section with completion reference:

     ```markdown
     - [YYYY-MM-DD] COMPLETED - See completion summary in PRP: PRPs/completed/[prp-name].md
     - Key achievements: [brief 1-2 line summary]
     - Any important notes: [gotchas, decisions, future work]
     ```

   - Mark **Testing Requirements** checkboxes if tests were written
   - Mark **Documentation Updates** checkboxes if docs updated
   - Update **Last Updated** timestamp
   - Update **Completion** count: `**Completion**: X/Y subtasks complete (ZZ%)`

   **If status is 🔄 IN_PROGRESS:**
   - Add notes to **Notes** section:

     ```markdown
     - [YYYY-MM-DD] IN_PROGRESS: Completed steps X-Y, stopped at step Z
     - Next steps: [what needs to be done to continue]
     ```

   - Document current progress and where execution stopped
   - Update **Last Updated** timestamp
   - Leave subtask unchecked: `- [ ] [TASK-XXX.Y] Subtask description`

   **If status is ⚠️ BLOCKED:**
   - Add blocker to **Blockers** section:

     ```markdown
     - [YYYY-MM-DD] [TASK-XXX.Y] BLOCKED: [description of blocker]
       - What's needed: [specific requirements to unblock]
       - Impact: [what this blocks]
     ```

   - Add notes about progress made before blocking
   - Update **Last Updated** timestamp
   - Leave subtask unchecked: `- [ ] [TASK-XXX.Y] Subtask description`

4. **Run Task Parser to Update Parent:**

   ```bash
   node PRPs/scripts/parse-tasks.js --update TASK-XXX
   ```

   Parser will:
   - Count completed subtasks in feature file
   - Update progress count in master `.claude/TASK.md` (e.g., `(3/7)`)
   - Auto-complete parent task if all subtasks done: `[x] [TASK-XXX] ...`
   - Auto-move to "Completed" section if fully done

5. **Commit Task Updates to Git:**
   - Feature task files are tracked in git for persistence
   - Commit changes so progress survives across sessions:

     ```bash
     git add .claude/tasks/TASK-XXX-*.md .claude/TASK.md
     git commit -m "chore(tasks): update TASK-XXX progress (status: COMPLETED|IN_PROGRESS|BLOCKED)"
     ```

**Output**: Implementation summary + PRP status + Task hierarchy update confirmation

**Example Output**:

```
PRP Execution Summary
─────────────────────────────────
PRP: 01-feature-name.md
Status: ✅ COMPLETED

Steps Executed: 12/12
Files Created: 23
Files Modified: 5
Tests Passing: 42/42
Build Status: ✅ Success

Acceptance Criteria: 15/15 ✅

Completion Summary: ✅ Added to PRP file
Task System: ✅ Updated (TASK-005.4 marked complete)

Next Steps:
1. Run /archive-prp PRPs/active/01-feature-name.md
2. Run /update-rag to ingest completed PRP into local-rag database
```
