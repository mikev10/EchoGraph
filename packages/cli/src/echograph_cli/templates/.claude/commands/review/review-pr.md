---
description: Review a GitHub PR for code quality, patterns, and security before merging
---

You are about to review a **GitHub Pull Request** using the `pattern-enforcer` agent.

**Input Format**:

```
/review-pr [pr-number|branch] [--strict] [--security] [--quick] [--no-post]
```

**Arguments**:

- `pr-number` (optional): PR number to review (e.g., `123`). Default: current branch's PR
- `branch` (optional): Branch name to review against main
- `--strict` (optional): Fail on any pattern deviation (for CI)
- `--security` (optional): Include security-focused review
- `--quick` (optional): Fast review, skip deep analysis
- `--no-post` (optional): Skip posting review to GitHub (default: always posts)

**Examples**:

```bash
# Review current branch's PR
/review-pr

# Review specific PR by number
/review-pr 42

# Strict review for CI (exits non-zero on issues)
/review-pr --strict

# Security-focused review
/review-pr --security

# Quick review (faster, less thorough)
/review-pr --quick

# Combine options
/review-pr 42 --strict --security

# Review without posting to GitHub
/review-pr --no-post
```

---

## Phase 0: Parse Arguments & Gather PR Info

### Step 0.1: Determine PR to Review

```bash
# If PR number provided, use it
gh pr view [pr-number] --json number,title,headRefName,baseRefName,additions,deletions,changedFiles

# If no PR number, find PR for current branch
gh pr view --json number,title,headRefName,baseRefName,additions,deletions,changedFiles

# If branch name provided, find its PR
gh pr list --head [branch] --json number,title
```

**Display:**

```
PR Review Request
─────────────────────────────────
PR: #[number] - [title]
Branch: [head] -> [base]
Changes: +[additions] / -[deletions] in [changedFiles] files
Mode: [strict|normal] {{IF security}}+ Security{{END IF}}
```

### Step 0.2: Fetch PR Diff and Files

```bash
# Get the full diff
gh pr diff [number]

# Get list of changed files
gh pr view [number] --json files --jq '.files[].path'

# Get PR description and commits
gh pr view [number] --json body,commits
```

---

## Phase 1: Invoke Pattern-Enforcer Agent

### Step 1.1: Prepare Review Context

**Build agent prompt with PR details:**

```markdown
You are reviewing PR #[number]: [title]

**Branch**: [head] -> [base]
**Files Changed**: [count]
**Lines**: +[additions] / -[deletions]

**PR Description**:
[body]

**Changed Files**:
[list of files]

**Diff**:
[full diff content]
```

### Step 1.2: Launch Pattern-Enforcer Agent

Use the Task tool to invoke the `pattern-enforcer` agent:

```typescript
Task({
  subagent_type: "pattern-enforcer",
  description: "Review PR #[number]",
  prompt: `
You are conducting a code review for PR #[number]: [title]

## Your Mission

Review all changes in this PR against the project's documented patterns and conventions.

## Review Checklist

### 1. Pattern Compliance (CLAUDE.md)
- [ ] File naming conventions followed (snake_case.py)
- [ ] Class/function naming conventions (PascalCase/snake_case)
- [ ] Import order correct (stdlib, third-party, internal, relative)
- [ ] Code structure matches project patterns
- [ ] No violations of "What NOT to Do" section

### 2. Code Quality
- [ ] Functions are focused and single-purpose
- [ ] No code duplication
- [ ] Appropriate error handling
- [ ] Clear variable/function names
- [ ] Comments explain "why" not "what"

### 3. Testing
- [ ] New code has corresponding tests
- [ ] Tests follow project patterns (Arrange/Act/Assert)
- [ ] Edge cases covered
- [ ] Test naming is descriptive

### 4. Documentation
- [ ] Public functions have docstrings (Google style)
- [ ] Complex logic is commented
- [ ] README updated if needed

{{IF security}}
### 5. Security Review
- [ ] No hardcoded secrets/tokens
- [ ] Input validation present
- [ ] No SQL injection vectors
- [ ] No command injection vectors
- [ ] Proper authentication checks
- [ ] Sensitive data not logged
{{END IF}}

## Files to Review

[list changed files]

## Diff Content

[full diff]

## Output Format

Provide your review in this exact format:

### Summary
[1-2 sentence overall assessment]

### Issues Found

#### Critical (Must Fix)
- [file:line] [issue description]

#### Warnings (Should Fix)
- [file:line] [issue description]

#### Suggestions (Nice to Have)
- [file:line] [suggestion]

### Pattern Compliance
- CLAUDE.md: [PASS/FAIL] - [details]
- Naming: [PASS/FAIL] - [details]
- Structure: [PASS/FAIL] - [details]
- Tests: [PASS/FAIL] - [details]

### Verdict
[APPROVE / REQUEST_CHANGES / COMMENT]

### Recommended Actions
1. [action 1]
2. [action 2]
`
})
```

---

## Phase 2: Process Review Results

### Step 2.1: Parse Agent Response

Extract from agent response:
- Summary
- Critical issues (blockers)
- Warnings
- Suggestions
- Pattern compliance results
- Verdict

### Step 2.2: Format Review Output

```
PR Review Complete
═══════════════════════════════════════════════════════

PR: #[number] - [title]
Reviewer: Claude Code (pattern-enforcer agent)
Mode: [strict|normal]

Summary
───────────────────────────────────────────────────────
[agent summary]

Issues Found
───────────────────────────────────────────────────────
Critical: [count] | Warnings: [count] | Suggestions: [count]

{{IF critical issues}}
CRITICAL (Must Fix Before Merge):
{{FOR each critical}}
  ❌ [file]:[line]
     [issue description]
{{END FOR}}
{{END IF}}

{{IF warnings}}
WARNINGS (Should Address):
{{FOR each warning}}
  ⚠️  [file]:[line]
     [issue description]
{{END FOR}}
{{END IF}}

{{IF suggestions}}
SUGGESTIONS (Nice to Have):
{{FOR each suggestion}}
  💡 [file]:[line]
     [suggestion]
{{END FOR}}
{{END IF}}

Pattern Compliance
───────────────────────────────────────────────────────
CLAUDE.md:  [✅ PASS | ❌ FAIL]
Naming:     [✅ PASS | ❌ FAIL]
Structure:  [✅ PASS | ❌ FAIL]
Tests:      [✅ PASS | ❌ FAIL]
{{IF security}}
Security:   [✅ PASS | ❌ FAIL]
{{END IF}}

Verdict
───────────────────────────────────────────────────────
{{IF verdict == APPROVE}}
✅ APPROVED - Ready to merge
{{ELSE IF verdict == REQUEST_CHANGES}}
❌ CHANGES REQUESTED - Address critical issues before merge
{{ELSE}}
💬 COMMENT - Review suggestions, merge at your discretion
{{END IF}}

{{IF strict AND (critical > 0 OR verdict == REQUEST_CHANGES)}}
⚠️  STRICT MODE: Review failed. Fix issues before merging.
{{END IF}}

Recommended Actions
───────────────────────────────────────────────────────
{{FOR each action}}
[N]. [action]
{{END FOR}}

═══════════════════════════════════════════════════════
```

### Step 2.3: Submit GitHub Review with Approval (if applicable)

**IMPORTANT**: When the verdict is APPROVE, submit an official GitHub review approval.
This satisfies branch protection rules requiring reviews. For solo developers who cannot
self-approve their own PRs, this step will be skipped with a note.

{{IF verdict == APPROVE}}

```bash
# Submit official approval review
gh pr review [number] --approve --body "$(cat <<'EOF'
## PR Review: APPROVED ✅

**Reviewed by**: Claude Code (pattern-enforcer agent)

### Summary
[agent summary]

### Review Checklist
- ✅ Pattern compliance verified
- ✅ Code quality standards met
- ✅ Tests present and passing
- ✅ No security issues found

This PR is ready to merge.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**If approval fails** (e.g., reviewing own PR):
```
ℹ️  Cannot submit approval: GitHub does not allow self-approval.
   For solo projects, proceed with merge directly.
```

{{ELSE IF verdict == REQUEST_CHANGES}}

```bash
# Submit review requesting changes
gh pr review [number] --request-changes --body "$(cat <<'EOF'
## PR Review: Changes Requested ❌

**Reviewed by**: Claude Code (pattern-enforcer agent)

### Summary
[agent summary]

### Critical Issues to Address
[list critical issues]

Please address the issues above before this PR can be merged.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

{{ELSE}}

```bash
# Submit comment-only review
gh pr review [number] --comment --body "$(cat <<'EOF'
## PR Review: Comment 💬

**Reviewed by**: Claude Code (pattern-enforcer agent)

### Summary
[agent summary]

### Suggestions
[list suggestions]

This PR can be merged at your discretion.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

{{END IF}}

### Step 2.4: Post Detailed Review Comment (Automatic)

**IMPORTANT**: Always post the detailed review to GitHub unless `--no-post` flag is provided.
This creates a documented history of all PR reviews for the project.

{{IF NOT no-post}}

```bash
# Post review as PR comment with markdown formatting
gh pr comment [number] --body "$(cat <<'EOF'
## PR Review Complete

**Reviewer**: Claude Code (pattern-enforcer agent)
**Mode**: [strict|normal]

### Summary

[agent summary]

### Issues Found

| Severity | Count |
|----------|-------|
| Critical | [count] |
| Warnings | [count] |
| Suggestions | [count] |

#### Critical (Must Fix Before Merge)

[list critical issues with file:line references]

#### Warnings (Should Address)

[list warnings with file:line references]

#### Suggestions (Nice to Have)

[list suggestions]

### Pattern Compliance

| Category | Status | Details |
|----------|--------|---------|
| CLAUDE.md | [✅/❌] | [details] |
| Naming | [✅/❌] | [details] |
| Structure | [✅/❌] | [details] |
| Tests | [✅/❌] | [details] |

### Verdict

[verdict with emoji and explanation]

### Recommended Actions

[numbered list of actions]

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Confirm post success:**
```
✅ Detailed review posted to PR #[number]: [GitHub comment URL]
```

{{ELSE}}

```
ℹ️  --no-post flag provided. Review not posted to GitHub.
```

{{END IF}}

---

## Phase 3: Handle Strict Mode

{{IF strict}}

### Exit Code for CI Integration

```typescript
if (criticalIssues > 0 || verdict === 'REQUEST_CHANGES') {
  // Exit with error code for CI
  process.exit(1)
} else {
  process.exit(0)
}
```

**CI Usage:**

```yaml
# In GitHub Actions
- name: Review PR
  run: claude "/review-pr --strict"
  # Fails the build if review finds critical issues
```

{{END IF}}

---

## Error Handling

### No PR Found

```
No PR found for current branch.

Options:
1. Specify PR number: /review-pr 42
2. Create a PR first: /create-pr
3. Check branch has been pushed
```

### PR Too Large

```
PR has [N] changed files ([M] lines).
This may take a while to review thoroughly.

Options:
1. Continue with full review
2. Use --quick for faster review
3. Review specific files only

Proceeding with full review...
```

---

## Goal

Provide thorough, consistent code review that:

- Enforces project patterns from CLAUDE.md
- Catches bugs and security issues early
- Suggests improvements aligned with project conventions
- Integrates with CI for automated quality gates

**Key Features:**

- Uses `pattern-enforcer` agent for deep analysis
- Checks against documented patterns (not generic best practices)
- Supports strict mode for CI integration
- Optional security-focused review
- Can post review directly to GitHub
