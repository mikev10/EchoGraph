# Validate Task System

Validates the hierarchical task management system and updates progress automatically.

## Purpose

This command:
1. Validates task file structure and format
2. Checks task ID uniqueness and format
3. Verifies file references exist
4. Detects progress mismatches
5. Finds orphaned task files
6. Auto-updates parent task progress
7. Auto-completes parent tasks when all subtasks done

## Usage

```bash
/validate-tasks
```

## What It Does

### 1. Structural Validation

**Master TASK.md:**
- ✓ File exists and is readable
- ✓ All task IDs unique
- ✓ Task IDs follow format (TASK-XXX)
- ✓ Three sections exist (In Progress, Pending, Completed)
- ✓ File references are valid paths

**Feature Task Files:**
- ✓ Referenced files exist at specified paths
- ✓ Subtask IDs match parent (TASK-001.1, TASK-001.2, etc.)
- ✓ Completion counts are accurate
- ✓ No orphaned files (files not referenced in master)

### 2. Progress Validation

For each task:
- Compare progress in master TASK.md vs feature task file
- Flag mismatches (e.g., master shows 2/5 but file shows 3/5)
- Suggest running update command if mismatch found

### 3. Auto-Update Mode

**When running validation:**
1. Read all task files
2. Calculate actual completion for each task
3. Update master TASK.md with correct progress
4. Auto-complete tasks [x] when all subtasks done
5. Auto-move completed tasks to "Completed" section

## Validation Checks

### ✓ Pass Conditions

- Task IDs are unique and follow TASK-XXX format
- All file references resolve to existing files
- Progress counts match actual subtask completion
- No duplicate task IDs across sections
- Subtask IDs properly namespaced (TASK-001.1, TASK-001.2)

### ⚠️ Warning Conditions

- Task has no feature file reference (flat task, acceptable)
- Orphaned task file exists (file not referenced in master)
- Progress mismatch (master vs file) - will be auto-corrected

### ✗ Error Conditions

- Duplicate task ID found
- Invalid task ID format (not TASK-XXX)
- Referenced file does not exist
- Subtask ID doesn't match parent (e.g., TASK-002.1 in TASK-001 file)

## Example Output

```
=== Task Validation ===

✓ Master TASK.md found
✓ Parsed 15 tasks from master TASK.md
✓ All task IDs are unique
✓ Updated TASK-001: 3/5 complete
✓ Updated TASK-002: 7/7 complete
✓ All subtasks complete! Moving TASK-002 to Completed section...
✓ Moved TASK-002 to Completed section
⚠ Progress mismatch for TASK-003
⚠ Orphaned task file: TASK-999-old-feature.md

=== Validation Summary ===
Tasks validated: 15
Errors: 0
Warnings: 2

✓ All validations passed!

Next Steps:
- TASK-002 is complete! Run /archive-prp if PRP exists
- Review orphaned file: .claude/tasks/TASK-999-old-feature.md
```

## When to Run

**Automatically:**
- After completing a PRP (`/execute-prp`)
- After archiving a PRP (`/archive-prp`)
- Before committing changes

**Manually:**
- After manually updating task files
- When progress seems out of sync
- Before planning session to see current state
- After creating new task files

## Implementation

The command runs the task parser utility:

```bash
node PRPs/scripts/parse-tasks.js --validate
```

For auto-updating a specific task:

```bash
node PRPs/scripts/parse-tasks.js --update TASK-XXX
```

## Troubleshooting

### "Progress mismatch" Warning

**Cause**: Master TASK.md shows different progress than feature task file

**Fix**: Validation auto-corrects this. If you want to manually fix:
1. Count completed subtasks in feature file
2. Update progress in master TASK.md to match
3. Or run `/validate-tasks` to auto-fix

### "Orphaned task file" Warning

**Cause**: Task file exists but not referenced in master TASK.md

**Fix Options**:
1. Add reference to master TASK.md if task is active
2. Delete file if task was completed and archived
3. Keep file for historical reference (warning will persist)

### "Invalid task ID format" Error

**Cause**: Task ID doesn't match TASK-XXX pattern

**Fix**:
1. Rename task ID to follow pattern (TASK-001, TASK-002, etc.)
2. Update both master TASK.md and feature file
3. Ensure 3-digit zero-padded format (001, not 1)

### "Referenced file not found" Error

**Cause**: Master TASK.md references a file that doesn't exist

**Fix**:
1. Create the missing feature task file
2. Or remove the file reference from master TASK.md
3. Or correct the file path if typo

## Integration with Workflow

### During Development

```bash
# 1. Start work on subtask
# 2. Mark subtask complete in feature file
# 3. Validate and update:
/validate-tasks

# 4. Commit changes
git add .
git commit -m "[TASK-001.3] Implemented token refresh"
```

### After PRP Completion

```bash
# 1. Complete PRP execution
/execute-prp PRPs/001-feature.md

# 2. Validation runs automatically
# 3. If all subtasks done, parent auto-completes

# 4. Archive PRP
/archive-prp PRPs/001-feature.md
```

### Before Planning Session

```bash
# Check current state before planning
/validate-tasks

# Review output to see:
# - What's in progress
# - What's blocked
# - What's ready to complete
```

## Files Modified

This command may modify:
- `.claude/TASK.md` (progress updates, task completion, section moves)

This command reads:
- `.claude/TASK.md`
- `.claude/tasks/TASK-*.md`

## See Also

- `.claude/tasks/README.md` - Task system documentation
- `.claude/TASK.md` - Master task list
- `PRPs/scripts/parse-tasks.js` - Task parser utility
- `/execute-prp` - PRP execution with auto-task-updates
- `/archive-prp` - PRP archival with task completion
