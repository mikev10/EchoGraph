#!/usr/bin/env python3
"""Sync .claude/ templates to CLI package before publishing.

This script copies the main project's .claude/ folder to the CLI templates,
ensuring the published package has the latest commands and configuration.

Usage:
    python scripts/sync-cli-templates.py [--dry-run]

Run this BEFORE bumping version and publishing to PyPI.
"""

import argparse
import shutil
from pathlib import Path


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIR = PROJECT_ROOT / ".claude"
TARGET_DIR = PROJECT_ROOT / "packages" / "cli" / "src" / "echograph_cli" / "templates" / ".claude"

# Files/folders to exclude from sync (project-specific, not for distribution)
EXCLUDE_PATTERNS = [
    "tasks/",           # Project task files, not template
    "TASK.md",          # Project-specific task tracking
    "*.pyc",
    "__pycache__",
    ".DS_Store",
]


def should_exclude(path: Path, base: Path) -> bool:
    """Check if path should be excluded from sync."""
    rel_path = str(path.relative_to(base))
    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith("/"):
            # Directory pattern
            if rel_path.startswith(pattern) or f"/{pattern}" in rel_path:
                return True
        elif "*" in pattern:
            # Glob pattern
            if path.match(pattern):
                return True
        else:
            # Exact match
            if rel_path == pattern or path.name == pattern:
                return True
    return False


def sync_templates(dry_run: bool = False) -> None:
    """Sync .claude/ to CLI templates."""
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        return

    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print()

    if dry_run:
        print("=== DRY RUN - No changes will be made ===\n")

    # Collect files to sync
    files_to_copy = []
    files_to_delete = []

    # Find all source files
    for src_file in SOURCE_DIR.rglob("*"):
        if src_file.is_file() and not should_exclude(src_file, SOURCE_DIR):
            rel_path = src_file.relative_to(SOURCE_DIR)
            target_file = TARGET_DIR / rel_path
            files_to_copy.append((src_file, target_file))

    # Find orphaned target files (exist in target but not source)
    if TARGET_DIR.exists():
        for target_file in TARGET_DIR.rglob("*"):
            if target_file.is_file():
                rel_path = target_file.relative_to(TARGET_DIR)
                src_file = SOURCE_DIR / rel_path
                if not src_file.exists() and not should_exclude(target_file, TARGET_DIR):
                    files_to_delete.append(target_file)

    # Report changes
    print(f"Files to copy: {len(files_to_copy)}")
    print(f"Files to delete: {len(files_to_delete)}")
    print()

    # Copy files
    for src_file, target_file in files_to_copy:
        rel_path = src_file.relative_to(SOURCE_DIR)
        action = "COPY" if not target_file.exists() else "UPDATE"
        print(f"  {action}: {rel_path}")

        if not dry_run:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, target_file)

    # Delete orphaned files
    for target_file in files_to_delete:
        rel_path = target_file.relative_to(TARGET_DIR)
        print(f"  DELETE: {rel_path}")

        if not dry_run:
            target_file.unlink()

    print()
    if dry_run:
        print("=== DRY RUN COMPLETE - Run without --dry-run to apply changes ===")
    else:
        print("Sync complete!")
        print()
        print("Next steps:")
        print("  1. Review changes: git diff packages/cli/")
        print("  2. Bump version in packages/cli/pyproject.toml")
        print("  3. Build: cd packages/cli && uv run python -m build")
        print("  4. Publish: cd packages/cli && uv run python -m twine upload dist/*")


def main():
    parser = argparse.ArgumentParser(description="Sync .claude/ templates to CLI package")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()

    sync_templates(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
