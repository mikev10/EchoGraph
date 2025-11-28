"""Tests for doctor command."""

from pathlib import Path

from typer.testing import CliRunner

from echograph_cli.core.doctor import (
    check_directory_structure,
    check_git_repo,
    check_mcp_config,
    run_all_checks,
)
from echograph_cli.main import app

runner = CliRunner()


class TestDoctorCommand:
    """Tests for echograph doctor command."""

    def test_doctor_shows_results_table(self, temp_project_with_claude: Path) -> None:
        """Should display results in table format."""
        result = runner.invoke(app, ["doctor", str(temp_project_with_claude)])

        assert "EchoGraph Doctor" in result.output
        assert "PASS" in result.output or "FAIL" in result.output

    def test_doctor_checks_directory_structure(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should check .claude directory structure."""
        result = runner.invoke(app, ["doctor", str(temp_project_with_claude)])

        assert "Directory Structure" in result.output


class TestCheckDirectoryStructure:
    """Tests for directory structure check."""

    def test_fails_without_claude_dir(self, temp_project: Path) -> None:
        """Should fail when .claude missing."""
        check = check_directory_structure(temp_project)

        assert not check.passed
        assert ".claude directory not found" in check.message

    def test_passes_with_all_files(self, temp_project_with_claude: Path) -> None:
        """Should pass with all required files."""
        check = check_directory_structure(temp_project_with_claude)

        assert check.passed
        assert "All required files present" in check.message

    def test_fails_with_missing_files(self, temp_project: Path) -> None:
        """Should fail when required files missing."""
        claude_dir = temp_project / ".claude"
        claude_dir.mkdir()
        (claude_dir / "CLAUDE.md").write_text("# Test")
        # Missing PLANNING.md and TASK.md

        check = check_directory_structure(temp_project)

        assert not check.passed
        assert "Missing files" in check.message


class TestCheckMcpConfig:
    """Tests for MCP configuration check."""

    def test_passes_without_config(self, temp_project: Path) -> None:
        """Should pass when no MCP config (optional)."""
        check = check_mcp_config(temp_project)

        assert check.passed
        assert "optional" in check.message.lower()

    def test_passes_with_valid_config(self, temp_project: Path) -> None:
        """Should pass with valid MCP config."""
        mcp_file = temp_project / ".mcp.json"
        mcp_file.write_text('{"servers": {}}')

        check = check_mcp_config(temp_project)

        assert check.passed

    def test_fails_with_invalid_json(self, temp_project: Path) -> None:
        """Should fail with invalid JSON config."""
        mcp_file = temp_project / ".mcp.json"
        mcp_file.write_text("not valid json")

        check = check_mcp_config(temp_project)

        assert not check.passed
        assert "Invalid JSON" in check.message


class TestCheckGitRepo:
    """Tests for git repository check."""

    def test_fails_without_git(self, temp_project: Path) -> None:
        """Should fail when not a git repo."""
        check = check_git_repo(temp_project)

        assert not check.passed

    def test_passes_with_git(self, temp_project_with_git: Path) -> None:
        """Should pass with git initialized."""
        check = check_git_repo(temp_project_with_git)

        assert check.passed


class TestRunAllChecks:
    """Tests for running all checks."""

    def test_returns_all_checks(self, temp_project: Path) -> None:
        """Should return results for all checks."""
        checks = run_all_checks(temp_project)

        # Should have at least 4 checks
        assert len(checks) >= 4

        # Check that expected checks are present
        check_names = [c.name for c in checks]
        assert "Claude Code CLI" in check_names
        assert "Directory Structure" in check_names
        assert "MCP Configuration" in check_names
        assert "Git Repository" in check_names
