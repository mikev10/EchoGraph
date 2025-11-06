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

2. **Add Metadata**:
   ```markdown
   ---
   status: completed
   completed_date: 2025-01-15
   implemented_by: Claude
   ---
   ```

3. **Move File**:
   ```bash
   mv PRPs/[prp-name].md PRPs/completed/[prp-name].md
   ```

4. **Extract New Patterns**:
   - Review implementation for reusable code
   - Add new patterns to examples/
   - Update CLAUDE.md if new conventions emerged

5. **Update Task Hierarchy**:
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
PRPs/01-reservation-calendar.md

# After
PRPs/completed/01-reservation-calendar.md
```

The PRP is now archived and can serve as reference for future similar features.
