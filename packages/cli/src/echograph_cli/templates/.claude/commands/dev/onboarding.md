---
description: Onboard new developer to project with guided tour
---

Provides:
- Project overview from PLANNING.md
- Key conventions from CLAUDE.md
- Tour of examples/ folder
- How to use PRPs
- How to run validation commands

**Onboarding Checklist**:

## 1. Project Overview
- Review PLANNING.md for architecture
- Understand feature hierarchy
- Learn tech stack rationale

## 2. Development Workflow
- How to create PRPs
- How to execute PRPs
- Using slash commands
- Validation process

## 3. Code Conventions
- Read CLAUDE.md thoroughly
- Review examples/ folder
- Understand naming conventions
- Learn tech stack patterns

## 4. Setup Environment
- Install dependencies
- Configure environment variables
- Set up dev tools (ESLint, Prettier)

## 5. Run First Task

**Understanding Task Hierarchy**:
- **Master TASK.md**: High-level features (epics) with task IDs [TASK-001]
- **Feature Task Files** (`.claude/tasks/`): Detailed subtasks for each feature
- **TodoWrite**: Session-level granular steps (managed by Claude)

**Selecting Your First Task**:
1. Review master `.claude/TASK.md` for "In Progress" or "Pending" tasks
2. Choose a task and open its feature task file (`.claude/tasks/TASK-XXX-*.md`)
3. **Important**: Pick a SUBTASK (TASK-XXX.1, TASK-XXX.2), not the parent task
4. Understand parent context before starting (read feature file's Context section)
5. Follow PRP workflow if available, or create one with `/generate-prp`
6. Mark subtask complete when done
7. Run `/validate-tasks` to update progress
8. Run validation commands
9. Submit PR referencing task ID in commit message

**Example**:
```
# In master TASK.md:
- [ ] [TASK-001] Build authentication (2/5) → @.claude/tasks/TASK-001-auth.md

# In .claude/tasks/TASK-001-auth.md:
- [x] [TASK-001.1] Create auth service  ← Done
- [x] [TASK-001.2] Add login endpoint   ← Done
- [ ] [TASK-001.3] Add token refresh    ← Pick this one!
- [ ] [TASK-001.4] Add logout
- [ ] [TASK-001.5] Write tests

# Your first task: Implement TASK-001.3 (token refresh)
```

**Tip**: Start with a subtask that's straightforward but meaningful. Avoid picking parent tasks - they're containers, not actionable items.

Welcome to [[PROJECT_NAME]]! 🎉
