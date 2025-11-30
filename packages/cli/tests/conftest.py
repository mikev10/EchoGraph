"""Pytest fixtures for EchoGraph CLI tests."""

from pathlib import Path

import pytest


@pytest.fixture
def temp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def temp_project_with_claude(tmp_path: Path) -> Path:
    """Create a temporary project with CLAUDE.md and .claude/ directory."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    # CLAUDE.md goes at project root
    (tmp_path / "CLAUDE.md").write_text("# Test Project\n\n## Project Context\n")
    # PLANNING.md and TASK.md go in .claude/
    (claude_dir / "PLANNING.md").write_text("# Test\n\n## Goals\n")
    (claude_dir / "TASK.md").write_text(
        "# Tasks\n\n## In Progress\n\n## Pending\n\n## Completed\n"
    )

    return tmp_path


@pytest.fixture
def temp_project_with_git(tmp_path: Path) -> Path:
    """Create a temporary project with git initialized."""
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    return tmp_path
