"""Doctor checks for Claude Code setup."""

import json
import shutil
from pathlib import Path

from echograph_cli import __version__
from echograph_cli.core.models import DoctorCheck


def check_claude_cli() -> DoctorCheck:
    """Check if Claude Code CLI is available."""
    claude_path = shutil.which("claude")
    if claude_path:
        return DoctorCheck(
            name="Claude Code CLI",
            passed=True,
            message=f"Found at {claude_path}",
        )
    return DoctorCheck(
        name="Claude Code CLI",
        passed=False,
        message="'claude' command not found in PATH",
        fix_hint="Install Claude Code: https://docs.anthropic.com/claude-code/installation",
    )


def check_directory_structure(path: Path) -> DoctorCheck:
    """Check .claude directory structure."""
    claude_dir = path / ".claude"

    if not claude_dir.exists():
        return DoctorCheck(
            name="Directory Structure",
            passed=False,
            message=".claude directory not found",
            fix_hint="Run 'echograph init' to create the directory structure",
        )

    required = ["CLAUDE.md", "PLANNING.md", "TASK.md"]
    missing = [
        f
        for f in required
        if not (claude_dir / f).exists() and not (path / f).exists()
    ]

    if missing:
        return DoctorCheck(
            name="Directory Structure",
            passed=False,
            message=f"Missing files: {', '.join(missing)}",
            fix_hint="Run 'echograph init' to create missing files",
        )

    return DoctorCheck(
        name="Directory Structure",
        passed=True,
        message="All required files present",
    )


def check_mcp_config(path: Path) -> DoctorCheck:
    """Check MCP configuration."""
    # Check project-level config first
    project_mcp = path / ".mcp.json"
    home_mcp = Path.home() / ".claude" / "mcp.json"

    if project_mcp.exists():
        try:
            json.loads(project_mcp.read_text())
            return DoctorCheck(
                name="MCP Configuration",
                passed=True,
                message=f"Project config found at {project_mcp}",
            )
        except json.JSONDecodeError:
            return DoctorCheck(
                name="MCP Configuration",
                passed=False,
                message=f"Invalid JSON in {project_mcp}",
                fix_hint="Fix JSON syntax errors in .mcp.json",
            )

    if home_mcp.exists():
        try:
            json.loads(home_mcp.read_text())
            return DoctorCheck(
                name="MCP Configuration",
                passed=True,
                message=f"Global config found at {home_mcp}",
            )
        except json.JSONDecodeError:
            return DoctorCheck(
                name="MCP Configuration",
                passed=False,
                message=f"Invalid JSON in {home_mcp}",
                fix_hint="Fix JSON syntax errors in ~/.claude/mcp.json",
            )

    return DoctorCheck(
        name="MCP Configuration",
        passed=True,
        message="No MCP config found (optional)",
    )


def check_git_repo(path: Path) -> DoctorCheck:
    """Check if project is a git repository."""
    git_dir = path / ".git"

    if git_dir.exists():
        return DoctorCheck(
            name="Git Repository",
            passed=True,
            message="Project is a git repository",
        )

    return DoctorCheck(
        name="Git Repository",
        passed=False,
        message="Project is not a git repository",
        fix_hint="Run 'git init' to initialize a repository (recommended)",
    )


def check_template_version(path: Path) -> DoctorCheck:
    """Check if templates are up to date."""
    metadata_file = path / ".claude" / ".echograph-meta.json"

    if not metadata_file.exists():
        return DoctorCheck(
            name="Template Version",
            passed=True,
            message="No template metadata (manual setup or old version)",
        )

    try:
        metadata = json.loads(metadata_file.read_text())
        template_version = metadata.get("template_version", "unknown")

        if template_version == __version__:
            return DoctorCheck(
                name="Template Version",
                passed=True,
                message=f"Templates are up to date (v{template_version})",
            )
        return DoctorCheck(
            name="Template Version",
            passed=False,
            message=f"Templates are v{template_version}, latest is v{__version__}",
            fix_hint="Run 'echograph update' to update templates",
        )
    except (json.JSONDecodeError, KeyError):
        return DoctorCheck(
            name="Template Version",
            passed=False,
            message="Invalid template metadata",
            fix_hint="Run 'echograph init --force' to reset templates",
        )


def run_all_checks(path: Path) -> list[DoctorCheck]:
    """Run all doctor checks."""
    return [
        check_claude_cli(),
        check_directory_structure(path),
        check_mcp_config(path),
        check_git_repo(path),
        check_template_version(path),
    ]
