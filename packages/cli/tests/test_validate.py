"""Tests for validate command."""

from pathlib import Path

from typer.testing import CliRunner

from echograph_cli.core.validation import (
    validate_claude_md,
    validate_directory,
    validate_planning_md,
    validate_task_md,
)
from echograph_cli.main import app

runner = CliRunner()


class TestValidateCommand:
    """Tests for echograph validate command."""

    def test_validate_passes_with_valid_structure(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should pass with valid .claude structure."""
        result = runner.invoke(app, ["validate", str(temp_project_with_claude)])

        assert result.exit_code == 0
        assert "passed" in result.output.lower()

    def test_validate_fails_without_claude_dir(self, temp_project: Path) -> None:
        """Should fail when .claude directory missing."""
        result = runner.invoke(app, ["validate", str(temp_project)])

        assert result.exit_code == 1
        assert ".claude directory does not exist" in result.output

    def test_validate_reports_missing_files(self, temp_project: Path) -> None:
        """Should report missing required files."""
        claude_dir = temp_project / ".claude"
        claude_dir.mkdir()

        result = runner.invoke(app, ["validate", str(temp_project)])

        assert result.exit_code == 1
        assert "CLAUDE.md" in result.output


class TestValidateClaudeMd:
    """Tests for CLAUDE.md validation."""

    def test_warns_missing_project_context(self, tmp_path: Path) -> None:
        """Should warn when Project Context section missing."""
        file_path = tmp_path / "CLAUDE.md"
        content = "# My Project\n\nSome content without context section."

        results = validate_claude_md(content, file_path)

        assert len(results) == 1
        assert results[0].rule == "claude-md-context"
        assert results[0].severity == "warning"

    def test_passes_with_project_context(self, tmp_path: Path) -> None:
        """Should pass with Project Context section."""
        file_path = tmp_path / "CLAUDE.md"
        content = "# My Project\n\n## Project Context\n\nContext here."

        results = validate_claude_md(content, file_path)

        context_results = [r for r in results if r.rule == "claude-md-context"]
        assert len(context_results) == 0

    def test_errors_on_invalid_import(self, tmp_path: Path) -> None:
        """Should error when @ import references missing file."""
        file_path = tmp_path / "CLAUDE.md"
        content = "# My Project\n\n@nonexistent.md"

        results = validate_claude_md(content, file_path)

        import_results = [r for r in results if r.rule == "import-exists"]
        assert len(import_results) == 1
        assert import_results[0].severity == "error"


class TestValidatePlanningMd:
    """Tests for PLANNING.md validation."""

    def test_warns_missing_sections(self, tmp_path: Path) -> None:
        """Should warn when no sections present."""
        file_path = tmp_path / "PLANNING.md"
        content = "Just some text without any headings."

        results = validate_planning_md(content, file_path)

        assert any(r.rule == "planning-structure" for r in results)


class TestValidateTaskMd:
    """Tests for TASK.md validation."""

    def test_warns_missing_status_sections(self, tmp_path: Path) -> None:
        """Should warn when status sections missing."""
        file_path = tmp_path / "TASK.md"
        content = "# Tasks\n\nSome tasks here."

        results = validate_task_md(content, file_path)

        section_results = [r for r in results if r.rule == "task-sections"]
        assert len(section_results) == 3  # In Progress, Pending, Completed

    def test_passes_with_all_sections(self, tmp_path: Path) -> None:
        """Should pass with all required sections."""
        file_path = tmp_path / "TASK.md"
        content = "# Tasks\n\n## In Progress\n\n## Pending\n\n## Completed\n"

        results = validate_task_md(content, file_path)

        section_results = [r for r in results if r.rule == "task-sections"]
        assert len(section_results) == 0


class TestValidateDirectory:
    """Tests for directory validation."""

    def test_validates_complete_structure(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should pass with complete structure."""
        results = validate_directory(temp_project_with_claude)

        errors = [r for r in results if r.severity == "error"]
        assert len(errors) == 0
