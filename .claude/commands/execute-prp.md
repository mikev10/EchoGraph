---
description: Execute PRP step-by-step with validation gates and ULTRATHINK planning
---

You are about to execute a Product Requirements Prompt (PRP).

**Input**: Path to PRP file (e.g., `PRPs/01-reservation-calendar.md`)

**Process**:

### Phase 1: Load PRP
- Read the specified PRP file completely
- Understand all context and requirements
- **Verify API endpoints against API specification (if applicable)**
- Conduct additional research if needed:
  - Search codebase for patterns
  - Fetch live API documentation if endpoints not in static spec
  - Review examples/ folder

### Phase 2: ULTRATHINK (Mandatory Planning Phase)
**CRITICAL: You must plan before coding**

1. **Break Down Tasks**:
   - Use TodoWrite tool to create task list
   - Break complex tasks into smaller steps
   - Identify dependencies between steps
   - Map tasks to PRP implementation blueprint

2. **Identify Patterns**:
   - Which examples/ files are relevant?
   - Which CLAUDE.md rules apply?
   - Are there existing similar implementations?

3. **Plan Execution Strategy**:
   - Sequential vs parallel tasks
   - Validation checkpoints
   - Potential blockers

### Phase 3: Execute Implementation Blueprint

For EACH step in the PRP:

1. **Mark Step as in_progress** (TodoWrite)

2. **Implement** following the step's guidance:
   - **Verify API contract in specification (if applicable)**
   - Match endpoint paths, methods, schemas exactly
   - Reference code patterns from examples/
   - Follow CLAUDE.md conventions
   - Use exact TypeScript types from PRP (matching API spec definitions)
   - Add comments for complex logic

3. **Validate Step**:
   ```bash
   npm run type-check  # Must exit 0
   npm run lint        # Must exit 0
   npm test [path]     # Must pass (if applicable)
   ```

4. **Fix Failures** (iterative loop):
   - If validation fails, analyze errors
   - Fix issues
   - Re-run validation
   - Retry up to 3 times
   - If still failing: STOP and report blocker

5. **Mark Step as completed** (TodoWrite)

6. **Proceed to Next Step**

### Phase 4: Complete

After all steps:

1. **Run Full Validation Suite**:
   ```bash
   npm run type-check
   npm run lint
   npm test
   npx expo export --platform ios
   ```

2. **Check Acceptance Criteria**:
   - Verify all checkboxes from "What (Success Criteria)"
   - Test each acceptance criterion manually

3. **Generate Summary**:
   - List all files created/modified
   - Report test results
   - Note any deviations from PRP
   - Document any discovered gotchas

4. **Update Context**:
   - If new patterns emerged, add to examples/
   - Update CLAUDE.md if needed
   - Add gotchas to PRP or docs

### Phase 5: Mark PRP Complete

**PRP STATUS Options:**
- ✅ **COMPLETED**: All requirements met, all validations pass
- ⚠️ **BLOCKED**: Cannot proceed, requires user input
- 🔄 **IN_PROGRESS**: Partial completion, continue later

**Update Task Hierarchy** (if COMPLETED):
1. Find task ID from PRP header (e.g., **Parent Task**: [TASK-001])
2. Mark corresponding subtask complete in feature task file (`.claude/tasks/TASK-XXX-*.md`)
3. Update completion count in feature file
4. Run task parser to update parent:
   ```bash
   node PRPs/scripts/parse-tasks.js --update TASK-XXX
   ```
5. Parser auto-updates master TASK.md progress and completion status

**Output**: Implementation summary + PRP status + Task hierarchy update confirmation

**Example Output**:
```
PRP Execution Summary
─────────────────────────────────
PRP: 01-reservation-calendar.md
Status: ✅ COMPLETED

Steps Executed: 12/12
Files Created: 23
Files Modified: 5
Tests Passing: 42/42
Build Status: ✅ Success

Acceptance Criteria: 15/15 ✅

Next Steps:
Run /archive-prp PRPs/01-reservation-calendar.md
```
