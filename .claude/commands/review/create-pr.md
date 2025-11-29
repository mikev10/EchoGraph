---
description: Create pull request with summary, test plan, and screenshots
---

You are about to create a **GitHub Pull Request** using the `gh` CLI.

**Input Format**:

```
/create-pr [--base=branch] [--skip-tests] [--draft] [--title="custom title"]
```

**Arguments**:

- `--base=branch` (optional): Target branch to merge into (default: `dev`)
- `--skip-tests` (optional): Skip running tests before creating PR
- `--draft` (optional): Create as draft PR
- `--title="text"` (optional): Custom PR title (default: auto-generated from commits)

**Examples**:

```bash
# Basic PR to dev branch (default)
/create-pr

# PR to main branch
/create-pr --base=main

# Draft PR without running tests
/create-pr --draft --skip-tests

# PR with custom title
/create-pr --title="feat: Add user authentication"

# Combine options
/create-pr --base=main --draft --title="fix: Resolve memory leak"
```

---

## Phase 0: Parse Arguments

### Step 0.1: Extract Configuration

```typescript
interface PRConfig {
  baseBranch: string      // default: "dev"
  skipTests: boolean      // default: false
  isDraft: boolean        // default: false
  customTitle: string | null  // default: null (auto-generate)
}
```

**Display parsed configuration:**

```
PR Configuration
─────────────────────────────────
Target: GitHub (using gh CLI)
Base Branch: [baseBranch]
Draft: [isDraft ? 'Yes' : 'No']
Skip Tests: [skipTests ? 'Yes' : 'No']
{{IF customTitle}}
Custom Title: "{customTitle}"
{{END IF}}
```

---

## Phase 1: Pre-Flight Checks

### Step 1.1: Verify Prerequisites

**Run these checks:**

```bash
# Check gh CLI is available
gh --version

# Check authenticated with GitHub
gh auth status

# Check we're in a git repo
git rev-parse --git-dir

# Get current branch
git branch --show-current
```

**Validation:**

- [ ] `gh` CLI is installed
- [ ] Authenticated with GitHub
- [ ] Current branch is NOT the base branch (can't PR into itself)
- [ ] Current branch has commits ahead of base branch

**If any check fails:**

```
Cannot create PR:

[specific issue]

Fix: [how to fix]
```

### Step 1.2: Check for Uncommitted Changes

```bash
git status --porcelain
```

**If uncommitted changes exist:**

```
Warning: You have uncommitted changes:
[list files]

Options:
1. Commit changes first (recommended)
2. Stash changes and continue
3. Continue anyway (changes won't be in PR)

Proceeding with option 3...
```

---

## Phase 2: Run Validation (unless --skip-tests)

{{IF NOT skipTests}}

### Step 2.1: Run Project Tests

**Detect and run appropriate validation:**

```bash
# Python projects
uv run ruff check .
uv run ruff format --check .
uv run mypy packages/
uv run pytest

# Node projects
npm run lint
npm run typecheck
npm run test
npm run build
```

**If validation fails:**

```
Validation failed:

[error output]

Options:
1. Fix issues and retry: /create-pr
2. Skip validation: /create-pr --skip-tests

Cannot create PR with failing tests.
```

{{END IF}}

---

## Phase 3: Gather PR Information

### Step 3.1: Analyze Changes

**Run in parallel:**

```bash
# Get current branch
git branch --show-current

# Get commits to include
git log [baseBranch]..HEAD --oneline

# Get full diff summary
git diff [baseBranch]...HEAD --stat

# Get changed files
git diff [baseBranch]...HEAD --name-only

# Check if branch is pushed
git status -sb
```

### Step 3.2: Determine PR Type

**From commit messages, determine type:**

- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation
- `test:` - Tests
- `chore:` - Maintenance
- `perf:` - Performance
- `style:` - Formatting

### Step 3.3: Generate PR Title

{{IF customTitle}}
Use: `{customTitle}`
{{ELSE}}
**Auto-generate from commits:**

- Single commit: Use commit message
- Multiple commits: Summarize (e.g., "feat: Add authentication system")
- Follow conventional commits format
{{END IF}}

### Step 3.4: Generate PR Body

**Template:**

```markdown
## Summary

[1-3 bullet points describing what this PR does]

## Changes

- [Change 1]
- [Change 2]
- [Change 3]

## Test Plan

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested edge cases

## Files Changed

[List key files, or "See diff for full list" if >10]

## Breaking Changes

[None / List any breaking changes]

## Related Issues

[Closes #XXX / Related to #XXX / None]

---

Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Phase 4: Push and Create PR

### Step 4.1: Push Branch (if needed)

```bash
# Check if branch needs pushing
git status -sb

# Push with upstream tracking
git push -u origin [current-branch]
```

### Step 4.2: Create Pull Request

```bash
gh pr create \
  --base [baseBranch] \
  {{IF isDraft}}--draft{{END IF}} \
  --title "[generated or custom title]" \
  --body "$(cat <<'EOF'
[generated PR body]
EOF
)"
```

### Step 4.3: Report Success

```
Pull Request Created Successfully
─────────────────────────────────
Title: [PR title]
Branch: [current-branch] -> [baseBranch]
URL: [PR URL]
Status: {{IF isDraft}}Draft{{ELSE}}Ready for Review{{END IF}}

Next steps:
1. Review the PR: [URL]
2. Request reviewers if needed
3. Address any CI failures
{{IF isDraft}}
4. Mark as "Ready for Review" when done
{{END IF}}
```

---

## Error Handling

### If gh CLI not authenticated

```
GitHub CLI not authenticated.

To authenticate:
  gh auth login

Then retry: /create-pr
```

### If branch not pushed

```
Branch not on remote. Pushing now...
[push output]
```

### If PR already exists

```
A PR already exists for this branch:
[existing PR URL]

Options:
1. View existing PR
2. Close existing and create new (not recommended)
```

---

## Goal

Create a well-documented GitHub Pull Request with:

- Clear summary of changes
- Test plan checklist
- Breaking change notices
- Proper conventional commit title
- Links to related issues

**Key Features:**

- Defaults to `dev` branch (configurable with --base)
- Runs validation before creating (skip with --skip-tests)
- Supports draft PRs (--draft)
- Auto-generates title or accepts custom (--title)
- Uses `gh` CLI for GitHub integration
