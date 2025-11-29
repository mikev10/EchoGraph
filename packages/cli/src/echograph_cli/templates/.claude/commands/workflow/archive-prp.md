---
description: Archive completed PRP to PRPs/completed/
---

Process:
1. Move PRP to `PRPs/completed/`
2. Add completion date to PRP header
3. Update implementation log
4. Extract any new patterns to examples/

**Steps**:

1. **Verify Completion**:
   - All acceptance criteria met
   - All validation commands pass
   - Tests passing
   - No open issues
   - **Completion Summary added to PRP** (should be done during `/execute-prp` Phase 4)

2. **Verify Completion Summary Exists**:
   - Check PRP file has "## Completion Summary" section at the end
   - If missing, add it now following the format in `/execute-prp` workflow
   - Completion summary is REQUIRED before archiving
   - This ensures the PRP is a complete historical record for local-rag

3. **Add Metadata** (Optional - frontmatter):
   ```markdown
   ---
   status: completed
   completed_date: 2025-01-15
   implemented_by: Claude
   ---
   ```
   Note: The completion summary at the end is more important than frontmatter metadata

4. **Move File**:
   ```bash
   mv PRPs/active/[prp-name].md PRPs/completed/[prp-name].md
   ```

5. **Extract New Patterns**:
   - Review implementation for reusable code
   - Add new patterns to examples/
   - Update CLAUDE.md if new conventions emerged

6. **Update Task Hierarchy**:
   - Mark corresponding subtask as complete in feature task file (`.claude/tasks/TASK-XXX-*.md`)
   - Update subtask completion count in feature file
   - Run task parser to update parent task in master TASK.md:
     ```bash
     node PRPs/scripts/parse-tasks.js --update TASK-XXX
     ```
   - Parser will:
     - Update progress count (X/Y) in master TASK.md
     - Auto-complete parent task [x] if all subtasks done
     - Auto-move parent to "Completed" section if fully done
   - Update relevant docs/ files
   - Add entry to changelog (if exists)

   **Important**: Find the task ID in the PRP header before updating

**Example**:
```bash
# Before
PRPs/active/01-reservation-calendar.md

# After
PRPs/completed/01-reservation-calendar.md
```

The PRP is now archived and can serve as reference for future similar features.
