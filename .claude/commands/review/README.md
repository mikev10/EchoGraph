# Review Commands

Commands for code review workflows.

## Available Commands

| Command | Description |
|---------|-------------|
| `/review:review-pr` | Review a PR using pattern-enforcer agent |
| `/review:review-staged` | Review staged git changes before commit |
| `/review:review-general` | General code review with security/performance checks |
| `/review:create-pr` | Create a GitHub PR with summary and test plan |

## PR Review Workflow

```
Code Changes
    ↓
/review:review-staged     ← Before commit
    ↓
git commit
    ↓
/review:create-pr         ← Create PR
    ↓
/review:review-pr         ← Review PR (or automated via GH Actions)
    ↓
Address Feedback
    ↓
Merge
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
        run: |
          claude "/review-pr ${{ github.event.pull_request.number }} --strict" \
            --output-format json > review.json

          # Post review as PR comment
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "$(cat review.json | jq -r '.summary')"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Requirements:**
- `ANTHROPIC_API_KEY` secret in repo settings
- GitHub token has PR comment permissions

**Cost Considerations:**
- Each review uses ~10-50K tokens depending on PR size
- Consider using `--quick` flag for large PRs
- Set up branch protection to only review on specific paths

## Local Usage

```bash
# Review current branch's PR
/review-pr

# Review specific PR
/review-pr 42

# Strict mode (for CI - fails on issues)
/review-pr --strict

# Include security analysis
/review-pr --security

# Quick review (less thorough, faster)
/review-pr --quick
```
