---
description: Merge an approved PR, post completion comment, and clean up feature branch
---

You are about to **merge a Pull Request** using the `gh` CLI.

**Input Format**:

```
/merge-pr [pr-number] [--squash] [--rebase] [--delete-branch] [--no-delete]
```

**Arguments**:

- `pr-number` (optional): PR number to merge. Default: current branch's PR
- `--squash` (optional): Squash commits into single commit (default)
- `--rebase` (optional): Rebase commits onto base branch
- `--delete-branch` (optional): Delete feature branch after merge (default: true)
- `--no-delete` (optional): Keep feature branch after merge

**Examples**:

```bash
# Merge current branch's PR (squash, delete branch)
/merge-pr

# Merge specific PR
/merge-pr 42

# Merge with rebase instead of squash
/merge-pr --rebase

# Keep feature branch after merge
/merge-pr --no-delete
```

---

## Phase 0: Pre-Merge Checks

### Step 0.1: Identify PR and Validate

```bash
# Get PR details
gh pr view [pr-number] --json number,title,state,mergeable,headRefName,baseRefName,reviewDecision,statusCheckRollup
```

**Validation Checklist:**

- [ ] PR exists and is open (`state == "OPEN"`)
- [ ] PR is mergeable (`mergeable == "MERGEABLE"`)
- [ ] No merge conflicts
- [ ] CI checks passed (if any)

**Display:**

```
Merge Request
─────────────────────────────────
PR: #[number] - [title]
Branch: [head] -> [base]
Status: [OPEN/CLOSED/MERGED]
Mergeable: [YES/NO/CONFLICTED]
Review: [APPROVED/CHANGES_REQUESTED/PENDING]
CI Checks: [PASSING/FAILING/PENDING]
```

### Step 0.2: Validate Merge Readiness

**If PR is not mergeable:**

```
Cannot merge PR #[number]:

Reason: [specific reason]

{{IF conflicts}}
Resolve merge conflicts first:
  git checkout [head-branch]
  git merge [base-branch]
  # Resolve conflicts
  git push
{{END IF}}

{{IF checks failing}}
CI checks are failing. Review and fix:
  gh pr checks [number]
{{END IF}}

{{IF changes requested}}
Changes have been requested. Address review feedback first.
{{END IF}}
```

**Exit without merging if not ready.**

---

## Phase 1: Execute Merge

### Step 1.1: Perform Merge

```bash
# Default: Squash merge (cleaner history)
gh pr merge [number] --squash --body "$(cat <<'EOF'
Merged via Claude Code /merge-pr command.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"

# Alternative: Rebase merge (if --rebase flag)
gh pr merge [number] --rebase

# Alternative: Standard merge (if neither flag)
gh pr merge [number] --merge
```

### Step 1.2: Verify Merge Success

```bash
# Check PR is now merged
gh pr view [number] --json state,mergedAt,mergedBy
```

**If merge failed:**

```
Merge failed:

[error message]

Please resolve the issue and try again.
```

---

## Phase 2: Post-Merge Actions

### Step 2.1: Post Completion Comment

**ALWAYS post a merge completion comment to the PR:**

```bash
gh pr comment [number] --body "$(cat <<'EOF'
## PR Merged Successfully

**Merged**: [head-branch] -> [base-branch]
**Method**: [squash/rebase/merge]
**Merged By**: Claude Code

### Post-Merge Checklist

- [x] Code reviewed and approved
- [x] All CI checks passed
- [x] Merged to [base-branch]
{{IF delete-branch}}
- [x] Feature branch `[head-branch]` deleted
{{ELSE}}
- [ ] Feature branch `[head-branch]` retained
{{END IF}}

### Next Steps

{{IF base == "dev"}}
- Deploy to staging environment
- Run integration tests
- When ready, create PR from `dev` -> `main`
{{ELSE IF base == "main"}}
- Deploy to production
- Monitor for issues
- Tag release if applicable
{{END IF}}

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 2.2: Delete Feature Branch (Default)

{{IF NOT no-delete}}

```bash
# Delete remote branch
gh api -X DELETE repos/{owner}/{repo}/git/refs/heads/[head-branch]

# Or using git
git push origin --delete [head-branch]
```

**Confirm deletion:**

```
✅ Feature branch '[head-branch]' deleted from remote.
```

{{ELSE}}

```
ℹ️  --no-delete flag provided. Feature branch '[head-branch]' retained.
```

{{END IF}}

### Step 2.3: Update Local Repository

```bash
# Switch to base branch
git checkout [base-branch]

# Pull latest changes
git pull origin [base-branch]

# Delete local feature branch (if exists)
git branch -d [head-branch] 2>/dev/null || true
```

---

## Phase 3: Final Report

### Step 3.1: Display Summary

```
PR Merge Complete
═══════════════════════════════════════════════════════

PR: #[number] - [title]
Merged: [head-branch] -> [base-branch]
Method: [squash/rebase/merge]

Actions Taken
───────────────────────────────────────────────────────
✅ PR merged successfully
✅ Completion comment posted
{{IF branch deleted}}
✅ Feature branch deleted
{{ELSE}}
ℹ️  Feature branch retained
{{END IF}}
✅ Local repository updated

{{IF base == "dev"}}
Next: Deploy to staging or create PR to main when ready.
{{ELSE IF base == "main"}}
Next: Monitor deployment and tag release if needed.
{{END IF}}

═══════════════════════════════════════════════════════
```

---

## Error Handling

### PR Not Found

```
No PR found.

Options:
1. Specify PR number: /merge-pr 42
2. Check you're on a feature branch with an open PR
```

### Merge Conflicts

```
PR has merge conflicts.

To resolve:
1. git checkout [head-branch]
2. git merge origin/[base-branch]
3. Resolve conflicts in affected files
4. git add . && git commit
5. git push
6. Retry: /merge-pr [number]
```

### Branch Protection Rules

```
Cannot merge: Branch protection rules prevent this action.

Required:
{{IF requires approval}}
- [ ] At least [N] approving review(s)
{{END IF}}
{{IF requires checks}}
- [ ] Required status checks must pass
{{END IF}}
{{IF requires linear history}}
- [ ] Linear history required (use --rebase or --squash)
{{END IF}}

Contact repository admin if you believe this is an error.
```

---

## Goal

Safely merge approved PRs with:

- Pre-merge validation (conflicts, checks, approval)
- Clean merge commit messages
- Documented merge via PR comment
- Automatic feature branch cleanup
- Local repository sync

**Key Features:**

- Validates PR is ready to merge before attempting
- Defaults to squash merge for clean history
- Always posts merge completion comment for documentation
- Deletes feature branch by default (use --no-delete to retain)
- Updates local repository after merge
- Future-proof: works with any base branch (dev, main, etc.)
