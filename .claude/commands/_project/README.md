# Project-Specific Commands

This folder contains commands that are **specific to EchoGraph development** and should NOT be distributed to users via `echograph init`.

## Convention

Any folder named `_project/` (prefixed with underscore) is excluded from CLI template sync.

## Commands in this folder

- `publish-cli.md` - Build and publish echograph CLI to PyPI

## How sync works

When running `python scripts/sync-cli-templates.py`:
1. Files from `.claude/` are copied to `packages/cli/.../templates/.claude/`
2. Files in `_project/` folders are EXCLUDED
3. Files in `tasks/` and `TASK.md` are also excluded

This allows EchoGraph to have its own commands while sharing general-purpose commands with all users.
