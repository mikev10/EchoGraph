# Review Commands

Commands for code review and PR management workflows.

## Available Commands

| Command | Description |
|---------|-------------|
| `/review:review-pr` | Review a PR using pattern-enforcer agent (auto-posts to GitHub) |
| `/review:merge-pr` | Merge approved PR, post completion comment, delete feature branch |
| `/review:review-staged` | Review staged git changes before commit |
| `/review:review-general` | General code review with security/performance checks |
| `/review:create-pr` | Create a GitHub PR with summary and test plan |

## Complete PR Workflow

```
Code Changes
    ↓
/review:review-staged     ← Before commit (optional)
    ↓
git commit
    ↓
/review:create-pr         ← Create PR (defaults to dev branch)
    ↓
/review:review-pr         ← Review PR (auto-posts to GitHub)
    ↓
Address Feedback (if any)
    ↓
/review:merge-pr          ← Merge, comment, cleanup branch
    ↓
Done! (local repo updated)
```

## Command Quick Reference

### Review PR

```bash
# Review current branch's PR (posts review to GitHub)
/review-pr

# Review specific PR
/review-pr 42

# Strict mode (for CI - fails on issues)
/review-pr --strict

# Include security analysis
/review-pr --security

# Review without posting to GitHub
/review-pr --no-post
```

### Merge PR

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

### Create PR

```bash
# Create PR to dev branch (default)
/create-pr

# Create PR to main branch
/create-pr --base=main

# Create draft PR
/create-pr --draft

# Skip running tests before creating
/create-pr --skip-tests
```

## GitHub Actions Integration (Optional)

To automate PR reviews with Claude Code, add this workflow:

```yaml
# .github/workflows/pr-review.yml
name: PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          claude "/review-pr ${{ github.event.pull_request.number }} --strict"
```

**Requirements:**
- `ANTHROPIC_API_KEY` secret in repo settings
- GitHub token has PR comment permissions

**Cost Considerations:**
- Each review uses ~10-50K tokens depending on PR size
- Consider using `--quick` flag for large PRs
- Set up branch protection to only review on specific paths

## Workflow Features

### Review Posts to GitHub with Approval

`/review-pr` automatically:
1. **Submits official GitHub review** - APPROVE, REQUEST_CHANGES, or COMMENT
   - Satisfies branch protection rules requiring reviews
   - Note: GitHub doesn't allow self-approval on your own PRs
2. **Posts detailed review comment** with:
   - Summary of findings
   - Critical issues, warnings, and suggestions
   - Pattern compliance status
   - Recommended actions

### Merge with Documentation

`/merge-pr` handles the complete merge workflow:
- Pre-merge validation (conflicts, CI, approval status)
- Squash merge by default (clean history)
- Posts completion comment with checklist
- Deletes feature branch (configurable)
- Updates local repository

### Branch Strategy

Commands support any branching strategy:
- `main` only: PRs go directly to main
- `dev` -> `main`: PRs target dev, then promote to main
- Custom: Specify base branch with `--base=`
