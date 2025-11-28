"""Validation rules for context files."""

import re
from pathlib import Path

from echograph_cli.core.models import ValidationResult


def validate_claude_md(content: str, file_path: Path) -> list[ValidationResult]:
    """Validate CLAUDE.md file."""
    results: list[ValidationResult] = []

    # Rule: Must have project context section
    if (
        "## Project Context" not in content
        and "## project context" not in content.lower()
    ):
        results.append(
            ValidationResult(
                file_path=file_path,
                line_number=None,
                rule="claude-md-context",
                message="CLAUDE.md should have a '## Project Context' section",
                severity="warning",
            )
        )

    # Rule: Check @ imports reference existing files
    import_pattern = r"@([^\s\]]+\.md)"
    for i, line in enumerate(content.splitlines(), 1):
        for match in re.finditer(import_pattern, line):
            import_path = match.group(1)
            # Handle both absolute and relative paths
            if import_path.startswith(".claude/"):
                full_path = file_path.parent.parent / import_path
            else:
                full_path = file_path.parent / import_path

            if not full_path.exists():
                results.append(
                    ValidationResult(
                        file_path=file_path,
                        line_number=i,
                        rule="import-exists",
                        message=f"Import '@{import_path}' references non-existent file",
                        severity="error",
                    )
                )

    return results


def validate_planning_md(content: str, file_path: Path) -> list[ValidationResult]:
    """Validate PLANNING.md file."""
    results: list[ValidationResult] = []

    # Rule: Should have at least one section
    if "## " not in content:
        results.append(
            ValidationResult(
                file_path=file_path,
                line_number=None,
                rule="planning-structure",
                message="PLANNING.md should have at least one section (## heading)",
                severity="warning",
            )
        )

    # Rule: Should have goals or objectives
    goals_patterns = ["goal", "objective", "purpose", "vision"]
    content_lower = content.lower()
    has_goals = any(pattern in content_lower for pattern in goals_patterns)
    if not has_goals:
        results.append(
            ValidationResult(
                file_path=file_path,
                line_number=None,
                rule="planning-goals",
                message="PLANNING.md should describe project goals or objectives",
                severity="info",
            )
        )

    return results


def validate_task_md(content: str, file_path: Path) -> list[ValidationResult]:
    """Validate TASK.md file."""
    results: list[ValidationResult] = []

    # Rule: Should have status sections
    required_sections = ["In Progress", "Pending", "Completed"]
    for section in required_sections:
        if f"## {section}" not in content:
            results.append(
                ValidationResult(
                    file_path=file_path,
                    line_number=None,
                    rule="task-sections",
                    message=f"TASK.md should have '## {section}' section",
                    severity="warning",
                )
            )

    # Rule: Check task file references exist
    task_ref_pattern = r"@\.claude/tasks/([^\s\]]+\.md)"
    for i, line in enumerate(content.splitlines(), 1):
        for match in re.finditer(task_ref_pattern, line):
            task_path = match.group(1)
            full_path = file_path.parent / "tasks" / task_path

            if not full_path.exists():
                results.append(
                    ValidationResult(
                        file_path=file_path,
                        line_number=i,
                        rule="task-file-exists",
                        message=f"Task file reference '.claude/tasks/{task_path}' "
                        "does not exist",
                        severity="error",
                    )
                )

    return results


def validate_directory(path: Path) -> list[ValidationResult]:
    """Validate entire .claude directory structure."""
    results: list[ValidationResult] = []
    claude_dir = path / ".claude"

    if not claude_dir.exists():
        results.append(
            ValidationResult(
                file_path=path,
                line_number=None,
                rule="claude-dir-exists",
                message=".claude directory does not exist",
                severity="error",
            )
        )
        return results

    # Check required files
    required_files = [
        ("CLAUDE.md", validate_claude_md),
        ("PLANNING.md", validate_planning_md),
        ("TASK.md", validate_task_md),
    ]

    for filename, validator in required_files:
        # Check both .claude/ and root
        claude_file = claude_dir / filename
        root_file = path / filename

        if not claude_file.exists() and not root_file.exists():
            results.append(
                ValidationResult(
                    file_path=path,
                    line_number=None,
                    rule="required-file",
                    message=f"Required file {filename} not found "
                    "in .claude/ or project root",
                    severity="error",
                )
            )
        else:
            # Validate the file that exists
            target = claude_file if claude_file.exists() else root_file
            try:
                content = target.read_text(encoding="utf-8")
                results.extend(validator(content, target))
            except UnicodeDecodeError:
                results.append(
                    ValidationResult(
                        file_path=target,
                        line_number=None,
                        rule="file-encoding",
                        message=f"Could not read {filename} - invalid encoding",
                        severity="error",
                    )
                )

    return results
