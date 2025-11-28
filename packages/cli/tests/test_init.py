"""Tests for init command."""

from pathlib import Path

from typer.testing import CliRunner

from echograph_cli.main import app

runner = CliRunner()


class TestInitCommand:
    """Tests for echograph init command."""

    def test_init_creates_claude_directory(self, temp_project: Path) -> None:
        """Should create .claude directory."""
        result = runner.invoke(app, ["init", str(temp_project), "--minimal"])

        assert result.exit_code == 0
        assert (temp_project / ".claude").exists()

    def test_init_minimal_creates_core_files(self, temp_project: Path) -> None:
        """Should create CLAUDE.md, PLANNING.md, TASK.md in minimal mode."""
        result = runner.invoke(app, ["init", str(temp_project), "--minimal"])

        assert result.exit_code == 0
        assert (temp_project / ".claude" / "CLAUDE.md").exists()
        assert (temp_project / ".claude" / "PLANNING.md").exists()
        assert (temp_project / ".claude" / "TASK.md").exists()

    def test_init_detects_existing_directory(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should prompt when .claude already exists."""
        result = runner.invoke(
            app, ["init", str(temp_project_with_claude)], input="n\n"
        )

        assert result.exit_code == 1
        assert "already exists" in result.output

    def test_init_force_overwrites(self, temp_project_with_claude: Path) -> None:
        """Should overwrite with --force flag."""
        result = runner.invoke(
            app, ["init", str(temp_project_with_claude), "--force", "--minimal"]
        )

        assert result.exit_code == 0

    def test_init_creates_metadata_file(self, temp_project: Path) -> None:
        """Should create .echograph-meta.json for updates."""
        runner.invoke(app, ["init", str(temp_project), "--minimal"])

        metadata_file = temp_project / ".claude" / ".echograph-meta.json"
        assert metadata_file.exists()

    def test_init_cannot_use_both_minimal_and_full(self, temp_project: Path) -> None:
        """Should error when both --minimal and --full specified."""
        result = runner.invoke(
            app, ["init", str(temp_project), "--minimal", "--full"]
        )

        assert result.exit_code == 1
        assert "Cannot use both" in result.output
