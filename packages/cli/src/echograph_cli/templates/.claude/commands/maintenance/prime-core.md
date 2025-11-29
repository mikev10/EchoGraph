---
description: Load all project context into Claude's memory
---

You are loading the complete project context into memory.

**Purpose**: Ensure you have full awareness of the project before starting work.

**Process**:

### 1. Load Core Documentation
Read and internalize the following files:

```bash
# Project foundation
.claude/CLAUDE.md         # Global conventions (MOST IMPORTANT)
.claude/PLANNING.md       # Architecture and goals
.claude/TASK.md           # Current work priorities
```

### 2. Survey Code Patterns
Review all example files to understand established patterns:

```bash
examples/integrations/     # API client, React Query patterns
examples/components/       # UI component patterns
examples/hooks/            # Custom hook patterns
examples/state/            # Zustand store patterns
examples/security/         # Auth and security patterns
examples/offline/          # Offline queue patterns
examples/testing/          # Test patterns
```

### 3. Review Library Documentation
Refresh knowledge of key libraries:

```bash
PRPs/ai_docs/react-native.md
PRPs/ai_docs/expo.md
PRPs/ai_docs/tamagui.md
PRPs/ai_docs/react-query.md
PRPs/ai_docs/zustand.md
```

### 4. Scan Project Structure
Understand the current file organization:

```bash
# List all source directories
find src -type d | sort

# List all component files
find src -name "*.tsx" | sort

# List all type definition files
find src -name "*.ts" -o -name "types.ts" | sort
```

### 5. Check Dependencies
Review installed packages and versions:

```bash
# If package.json exists
cat package.json | jq '.dependencies'
cat package.json | jq '.devDependencies'
```

### 6. Review Recent Work
Check what's been completed and what's next:

```bash
# Master task list (high-level features)
cat .claude/TASK.md

# Feature task files (detailed subtasks for in-progress tasks)
# Read any tasks currently in progress from .claude/tasks/
ls .claude/tasks/TASK-*.md 2>/dev/null || echo "No feature task files yet"

# If there are in-progress tasks, read their feature files:
# cat .claude/tasks/TASK-XXX-feature-name.md

# Recent PRPs
ls -lt PRPs/*.md | head -5
```

**Note**: For each task in the "In Progress" section of TASK.md, read its corresponding feature task file to understand current subtask status

### 7. Summary Report

After loading context, provide a brief summary:

```
Context Loading Complete ✅

Loaded:
- Global conventions (CLAUDE.md)
- Project architecture (PLANNING.md)
- Code patterns from examples/
- Library documentation
- Current file structure

Current Focus:
- [Summary of TASK.md priorities]

Key Conventions:
- [Top 3 most important rules from CLAUDE.md]

Ready to proceed with development.
```

**Use Case**: Run this command at the start of each coding session to ensure full context awareness.
