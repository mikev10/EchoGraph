# Task Management System - Feature Task Files

## Overview

This directory contains **feature-level task files** that break down high-level tasks from the master TASK.md into concrete, actionable subtasks.

## File Naming Convention

**Format**: `TASK-XXX-feature-name.md`

**Examples**:
- `TASK-001-oauth-authentication.md`
- `TASK-002-payment-gateway.md`
- `TASK-015-user-profile-management.md`

**Rules**:
- Use zero-padded 3-digit task IDs (001, 002, ... 999)
- Use kebab-case for feature names
- Keep names concise but descriptive

## Task File Structure

Each task file should follow this template:

```markdown
# [TASK-XXX] Feature Name

**Status**: In Progress | Pending | Completed
**PRP**: @PRPs/xxx-feature-name.md (if applicable)
**Parent Task**: References master TASK.md entry
**Started**: YYYY-MM-DD
**Completed**: YYYY-MM-DD (when done)

## Context

Brief description of what this feature accomplishes and why it's important.

## Subtasks

- [ ] [TASK-XXX.1] First concrete subtask
- [ ] [TASK-XXX.2] Second concrete subtask
- [ ] [TASK-XXX.3] Third concrete subtask
- [x] [TASK-XXX.4] Completed subtask example

## Progress

**Completion**: X/Y subtasks complete (ZZ%)

## Notes

- Any important decisions made
- Blockers or dependencies
- Links to related tasks or documentation
- Technical considerations

## Testing Requirements

- [ ] Unit tests written
- [ ] Integration tests passing
- [ ] Manual testing completed

## Documentation Updates

- [ ] Code comments added
- [ ] API documentation updated (if applicable)
- [ ] User-facing documentation updated (if applicable)

---

**Last Updated**: YYYY-MM-DD
```

## Three-Level Task Hierarchy

### Level 1: Master TASK.md (Epic/Feature Level)
High-level features that represent major milestones.

**Example**: `- [ ] [TASK-001] Build OAuth authentication system (3/5) → @.claude/tasks/TASK-001-oauth-auth.md`

### Level 2: Feature Task File (Subtask Level)
Concrete implementation steps that persist across sessions.

**Example** (in `TASK-001-oauth-auth.md`):
```markdown
- [ ] [TASK-001.1] Create auth service structure
- [ ] [TASK-001.2] Implement login endpoint
- [x] [TASK-001.3] Add token storage
```

### Level 3: TodoWrite (Session Level)
Granular execution steps managed during active work (ephemeral).

**Example** (during session):
```
[in_progress] Read auth.service.ts and understand current structure
[pending] Create new OAuth provider class
[pending] Add unit tests for OAuth flow
```

## Workflow

### Creating a New Task

1. **Add to master TASK.md**:
   ```markdown
   - [ ] [TASK-042] Implement feature X → @.claude/tasks/TASK-042-feature-x.md
   ```

2. **Create feature task file**: `TASK-042-feature-x.md`
   - Use template above
   - Break down into 3-10 subtasks
   - Link to related PRP if exists

3. **Start work**:
   - Update status to "In Progress" in both master and feature file
   - Use TodoWrite for granular session tasks

### Completing a Task

1. **Mark subtask complete** in feature task file:
   ```markdown
   - [x] [TASK-042.1] Completed subtask
   ```

2. **Update progress count**:
   ```markdown
   **Completion**: 4/5 subtasks complete (80%)
   ```

3. **When all subtasks done**:
   - Mark feature task status as "Completed"
   - Update master TASK.md (auto-completed by Claude):
     ```markdown
     - [x] [TASK-042] Implement feature X (5/5) → @.claude/tasks/TASK-042-feature-x.md
     ```
   - Move to "Completed" section in master TASK.md

### Task Dependencies

If Task B depends on Task A, note it in the feature task file:

```markdown
## Dependencies
- Blocked by: [TASK-001] OAuth authentication (must complete first)
- Blocks: [TASK-015] User profile (this must complete first)
```

## Task ID Assignment

**Manual Numbering**: Task IDs are assigned sequentially as tasks are created.

**Finding next available ID**:
1. Check master TASK.md for highest TASK-XXX number
2. Increment by 1
3. Create task file with new ID

**Example**: If highest ID is TASK-023, next task is TASK-024.

## Validation

Run validation before committing changes:

```bash
/validate-tasks
```

**Checks**:
- Task IDs are unique
- File references are valid
- Progress counts match actual subtasks
- No orphaned task files
- Proper markdown format

## Best Practices

### DO:
✅ Keep subtasks concrete and actionable
✅ Update progress counts after each subtask completion
✅ Link to related PRPs for context
✅ Note blockers and dependencies
✅ Update "Last Updated" timestamp

### DON'T:
❌ Create task files without master TASK.md entry
❌ Nest more than 2 levels (master → feature → subtask)
❌ Create overly granular subtasks (use TodoWrite instead)
❌ Leave stale "In Progress" tasks without updates
❌ Skip progress count updates

## Example: Complete Task Lifecycle

### 1. Initial Creation
**Master TASK.md**:
```markdown
## Pending
- [ ] [TASK-005] Add user profile management → @.claude/tasks/TASK-005-user-profiles.md
```

**File**: `.claude/tasks/TASK-005-user-profiles.md`
```markdown
# [TASK-005] User Profile Management

**Status**: Pending
**PRP**: @PRPs/005-user-profiles.md
**Started**: Not started

## Subtasks
- [ ] [TASK-005.1] Create profile data model
- [ ] [TASK-005.2] Build profile API endpoints
- [ ] [TASK-005.3] Create profile UI components
- [ ] [TASK-005.4] Add profile image upload
- [ ] [TASK-005.5] Write tests

**Completion**: 0/5 subtasks complete (0%)
```

### 2. Work In Progress
**Master TASK.md**:
```markdown
## In Progress
- [ ] [TASK-005] Add user profile management (2/5) → @.claude/tasks/TASK-005-user-profiles.md
```

**Feature file** (updated):
```markdown
**Status**: In Progress
**Started**: 2025-11-05

## Subtasks
- [x] [TASK-005.1] Create profile data model
- [x] [TASK-005.2] Build profile API endpoints
- [ ] [TASK-005.3] Create profile UI components
- [ ] [TASK-005.4] Add profile image upload
- [ ] [TASK-005.5] Write tests

**Completion**: 2/5 subtasks complete (40%)
```

### 3. Completed
**Master TASK.md**:
```markdown
## Completed
- [x] [TASK-005] Add user profile management (5/5) → @.claude/tasks/TASK-005-user-profiles.md
```

**Feature file** (final):
```markdown
**Status**: Completed
**Completed**: 2025-11-08

## Subtasks
- [x] [TASK-005.1] Create profile data model
- [x] [TASK-005.2] Build profile API endpoints
- [x] [TASK-005.3] Create profile UI components
- [x] [TASK-005.4] Add profile image upload
- [x] [TASK-005.5] Write tests

**Completion**: 5/5 subtasks complete (100%)

**Last Updated**: 2025-11-08
```

## Migration from Old System

Existing flat tasks in master TASK.md can remain as-is. New tasks should use the hierarchical system. Over time, convert high-level tasks to feature files when breaking them down for implementation.

## Questions?

See `.claude/CLAUDE.md` for overall task management philosophy and workflow integration.
