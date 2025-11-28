# Current Tasks

This file tracks **high-level features and milestones** (epics). Each task can reference a detailed feature task file in `.claude/tasks/` that contains persistent subtasks.

## In Progress

- [ ] [TASK-002] Context Engineering CLI (8/9) → @.claude/tasks/TASK-002-context-engineering-cli.md

## Pending

## Completed

### Completed tasks will be moved here automatically when all subtasks are done

- [x] [TASK-001] Example feature implementation (7/7) → @.claude/tasks/TASK-001-example-feature.md

---

**Last Updated**: 2025-11-27

## Task Format

Each task follows this format:

```
- [ ] [TASK-XXX] Feature description (completed/total) → @.claude/tasks/TASK-XXX-feature-name.md
```

**Components**:
- `[ ]` or `[x]`: Checkbox (auto-completed when all subtasks done)
- `[TASK-XXX]`: Unique 3-digit task ID
- Feature description: Brief summary of the task
- `(X/Y)`: Progress indicator (auto-updated by validation script)
- `→ @.claude/tasks/...`: Reference to detailed feature task file

## Instructions

**Three-Level Task Hierarchy**:

1. **Master TASK.md** (this file) - Epic/feature level
   - High-level milestones that persist across sessions
   - References detailed feature task files
   - Auto-updated by Claude and validation scripts

2. **Feature Task Files** (`.claude/tasks/TASK-XXX-*.md`) - Subtask level
   - Concrete implementation steps (3-10 subtasks per feature)
   - Persists across sessions, tracked in git
   - Contains context, notes, testing requirements

3. **TodoWrite** (session-level) - Granular execution
   - Step-by-step work during active session
   - Ephemeral, does not persist
   - One task `in_progress` at a time

**When Claude Updates This File**:
- After completing PRPs
- At session end
- After major milestones
- When running `/validate-tasks` command

**Progress Auto-Update**:
- Progress counts `(X/Y)` are automatically updated by validation scripts
- Tasks auto-complete `[x]` when all subtasks in feature file are done
- Completed tasks auto-move to "Completed" section

**Creating New Tasks**:

1. Assign next available TASK-XXX ID
2. Add entry to this file with task description
3. Create feature task file: `.claude/tasks/TASK-XXX-feature-name.md`
4. Break down into subtasks in the feature file
5. Link to related PRP if applicable

**Validation**:
Run `/validate-tasks` to check:
- Task ID uniqueness and format
- File reference validity
- Progress count accuracy
- No orphaned files

**See Also**:
- `.claude/tasks/README.md` - Detailed task system documentation
- `.claude/tasks/TASK-001-example-feature.md` - Example task file template
- `PRPs/scripts/parse-tasks.js` - Task parser and validator utility
