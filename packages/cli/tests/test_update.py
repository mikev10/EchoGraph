"""Tests for update command."""

import json
from pathlib import Path

from typer.testing import CliRunner

from echograph_cli import __version__
from echograph_cli.main import app

runner = CliRunner()


class TestUpdateCommand:
    """Tests for echograph update command."""

    def test_update_fails_without_claude_dir(self, temp_project: Path) -> None:
        """Should fail when .claude directory missing."""
        result = runner.invoke(app, ["update", str(temp_project)])

        assert result.exit_code == 1
        assert ".claude directory not found" in result.output

    def test_update_fails_without_metadata(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should fail when no metadata file."""
        result = runner.invoke(app, ["update", str(temp_project_with_claude)])

        assert result.exit_code == 1
        assert "No template metadata found" in result.output

    def test_update_reports_up_to_date(self, temp_project_with_claude: Path) -> None:
        """Should report when templates are current."""
        # Create metadata with current version
        metadata_file = temp_project_with_claude / ".claude" / ".echograph-meta.json"
        metadata_file.write_text(
            json.dumps({"template_version": __version__, "files": {}})
        )

        result = runner.invoke(app, ["update", str(temp_project_with_claude)])

        assert result.exit_code == 0
        assert "up to date" in result.output.lower()

    def test_update_dry_run_no_changes(self, temp_project_with_claude: Path) -> None:
        """Should not modify files in dry run mode."""
        # Create metadata with old version
        metadata_file = temp_project_with_claude / ".claude" / ".echograph-meta.json"
        metadata_file.write_text(json.dumps({"template_version": "0.0.1", "files": {}}))

        claude_md = temp_project_with_claude / ".claude" / "CLAUDE.md"
        original_content = claude_md.read_text()

        result = runner.invoke(
            app, ["update", str(temp_project_with_claude), "--dry-run"]
        )

        assert "Dry run" in result.output
        assert claude_md.read_text() == original_content
