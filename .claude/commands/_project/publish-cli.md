---
description: Sync templates, build, and publish echograph CLI to PyPI
---

# Publish CLI to PyPI

Automates the full release workflow for the `echograph` CLI package.

## Phase 0: Sync Templates (CRITICAL)

**First, sync your `.claude/` changes to the CLI templates:**

```bash
python scripts/sync-cli-templates.py --dry-run  # Preview changes
python scripts/sync-cli-templates.py            # Apply changes
```

This copies commands/templates from `.claude/` to `packages/cli/.../templates/.claude/`, excluding:
- `_project/` folders (EchoGraph-specific commands like this one)
- `tasks/` and `TASK.md` (project task tracking)

Review the synced changes:
```bash
git diff packages/cli/
```

## Phase 1: Pre-flight Checks

1. **Check git status** - ensure changes are intentional
2. **Check current version** in `packages/cli/pyproject.toml`

## Phase 2: Version Bump

Ask user for version bump type:
- **patch** (0.2.1 → 0.2.2) - bug fixes, template updates
- **minor** (0.2.1 → 0.3.0) - new commands, features
- **major** (0.2.1 → 1.0.0) - breaking changes

Update version in BOTH files:
- `packages/cli/pyproject.toml`
- `packages/cli/src/echograph_cli/__init__.py`

## Phase 3: Build

```bash
cd packages/cli && rm -rf dist/ && uv run python -m build
```

Verify output shows both `.whl` and `.tar.gz` files.

## Phase 4: Publish

**If credentials configured (.pypirc or TWINE_* env vars):**
```bash
cd packages/cli && uv run python -m twine upload dist/*
```

**If not configured**, user runs manually and enters PyPI API token.

**Tip:** Create API token at https://pypi.org/manage/account/token/

## Phase 5: Post-Publish

1. **Commit all changes:**
   ```bash
   git add -A
   git commit -m "chore: Release echograph v{VERSION}"
   ```

2. **Tag release** (optional):
   ```bash
   git tag -a v{VERSION} -m "Release v{VERSION}"
   git push origin v{VERSION}
   ```

3. **Verify on PyPI:** https://pypi.org/project/echograph/

## Quick Checklist

- [ ] Run sync script (`python scripts/sync-cli-templates.py`)
- [ ] Review `git diff packages/cli/`
- [ ] Bump version (both files)
- [ ] Build package
- [ ] Publish to PyPI
- [ ] Commit and tag

## Full Command Sequence

```bash
# 1. Sync templates
python scripts/sync-cli-templates.py

# 2. Review changes
git diff packages/cli/

# 3. Bump version (edit pyproject.toml and __init__.py)

# 4. Build
cd packages/cli && rm -rf dist/ && uv run python -m build

# 5. Publish
uv run python -m twine upload dist/*

# 6. Commit and tag
git add -A && git commit -m "chore: Release echograph vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

## Quick Reference

| Step | Command |
|------|---------|
| Sync | `python scripts/sync-cli-templates.py` |
| Check version | `grep version packages/cli/pyproject.toml` |
| Build | `cd packages/cli && uv run python -m build` |
| Publish | `cd packages/cli && uv run python -m twine upload dist/*` |
| Verify | `pip index versions echograph` |

## Troubleshooting

**"File already exists"**: Version already published. Bump version and rebuild.

**"Invalid credentials"**: Check `.pypirc` or set `TWINE_USERNAME=__token__` and `TWINE_PASSWORD=pypi-xxx`.

**"Trusted publishing not supported"**: This warning is normal for token-based auth. Ignore it.
