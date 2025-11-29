#!/usr/bin/env python3
"""Sync .claude/ templates to CLI package before publishing.

This script copies the main project's .claude/ folder to the CLI templates,
ensuring the published package has the latest commands and configuration.

Project-specific files (in _project/ folders or listed in EXCLUDE_PATTERNS)
are NOT synced - they stay only in EchoGraph's own .claude/ folder.

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

# Files/folders to EXCLUDE from sync (project-specific, not for distribution)
EXCLUDE_PATTERNS = [
    # Project-specific folders (convention: prefix with underscore)
    "_project/",           # .claude/commands/_project/ - EchoGraph-specific commands

    # Task tracking (project-specific)
    "tasks/",              # .claude/tasks/ - EchoGraph task files
    "TASK.md",             # Project task tracking

    # Common excludes
    "*.pyc",
    "__pycache__",
    ".DS_Store",
]


def should_exclude(path: Path, base: Path) -> bool:
    """Check if path should be excluded from sync."""
    rel_path = str(path.relative_to(base)).replace("\\", "/")

    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith("/"):
            # Directory pattern - check if path is inside this directory
            dir_name = pattern.rstrip("/")
            if f"/{dir_name}/" in f"/{rel_path}" or rel_path.startswith(f"{dir_name}/"):
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

    print("=" * 60)
    print("EchoGraph CLI Template Sync")
    print("=" * 60)
    print(f"\nSource: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print(f"\nExcluded patterns:")
    for pattern in EXCLUDE_PATTERNS:
        print(f"  - {pattern}")
    print()

    if dry_run:
        print(">>> DRY RUN - No changes will be made <<<\n")

    # Collect files to sync
    files_to_copy = []
    files_to_delete = []
    excluded_files = []

    # Find all source files
    for src_file in SOURCE_DIR.rglob("*"):
        if src_file.is_file():
            if should_exclude(src_file, SOURCE_DIR):
                excluded_files.append(src_file)
            else:
                rel_path = src_file.relative_to(SOURCE_DIR)
                target_file = TARGET_DIR / rel_path
                files_to_copy.append((src_file, target_file))

    # Find orphaned target files (exist in target but not source)
    if TARGET_DIR.exists():
        for target_file in TARGET_DIR.rglob("*"):
            if target_file.is_file():
                rel_path = target_file.relative_to(TARGET_DIR)
                src_file = SOURCE_DIR / rel_path
                # Delete if: doesn't exist in source AND isn't in an excluded pattern
                if not src_file.exists() and not should_exclude(target_file, TARGET_DIR):
                    files_to_delete.append(target_file)

    # Report
    print(f"Files to sync:    {len(files_to_copy)}")
    print(f"Files to delete:  {len(files_to_delete)}")
    print(f"Files excluded:   {len(excluded_files)}")
    print()

    # Show excluded files
    if excluded_files:
        print("Excluded (project-specific):")
        for f in excluded_files[:10]:  # Show first 10
            print(f"  [SKIP] {f.relative_to(SOURCE_DIR)}")
        if len(excluded_files) > 10:
            print(f"  ... and {len(excluded_files) - 10} more")
        print()

    # Copy files
    print("Syncing files:")
    for src_file, target_file in files_to_copy:
        rel_path = src_file.relative_to(SOURCE_DIR)

        # Check if file changed
        if target_file.exists():
            if src_file.read_bytes() == target_file.read_bytes():
                continue  # Skip unchanged files
            action = "UPDATE"
        else:
            action = "ADD"

        print(f"  [{action}] {rel_path}")

        if not dry_run:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, target_file)

    # Delete orphaned files
    if files_to_delete:
        print("\nDeleting orphaned files:")
        for target_file in files_to_delete:
            rel_path = target_file.relative_to(TARGET_DIR)
            print(f"  [DELETE] {rel_path}")

            if not dry_run:
                target_file.unlink()

    print()
    print("=" * 60)
    if dry_run:
        print("DRY RUN COMPLETE - Run without --dry-run to apply changes")
    else:
        print("Sync complete!")
        print()
        print("Next steps:")
        print("  1. Review changes: git diff packages/cli/")
        print("  2. Run: /workflow:publish-cli  (or manually bump, build, publish)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Sync .claude/ templates to CLI package",
        epilog="Files in _project/ folders are excluded (project-specific)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    args = parser.parse_args()

    sync_templates(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
