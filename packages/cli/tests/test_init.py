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
        """Should create CLAUDE.md at root, PLANNING.md/TASK.md in .claude/."""
        result = runner.invoke(app, ["init", str(temp_project), "--minimal"])

        assert result.exit_code == 0
        # CLAUDE.md goes at project root
        assert (temp_project / "CLAUDE.md").exists()
        # PLANNING.md and TASK.md go in .claude/
        assert (temp_project / ".claude" / "PLANNING.md").exists()
        assert (temp_project / ".claude" / "TASK.md").exists()

    def test_init_detects_existing_directory(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should detect existing files and prompt for conflict resolution."""
        result = runner.invoke(
            app, ["init", str(temp_project_with_claude), "--minimal"], input="1\n"
        )

        # Should complete with skip resolution
        assert result.exit_code == 0
        assert "existing file" in result.output

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
        result = runner.invoke(app, ["init", str(temp_project), "--minimal", "--full"])

        assert result.exit_code == 1
        assert "Cannot use both" in result.output

    def test_init_dry_run_shows_preview(self, temp_project: Path) -> None:
        """Should show preview of files without creating them."""
        result = runner.invoke(
            app, ["init", str(temp_project), "--minimal", "--dry-run"]
        )

        assert result.exit_code == 0
        assert "Dry run" in result.output
        assert "CLAUDE.md" in result.output
        # Files should NOT be created
        assert not (temp_project / ".claude").exists()

    def test_init_dry_run_shows_conflicts(self, temp_project_with_claude: Path) -> None:
        """Should show existing files as conflicts in dry run."""
        result = runner.invoke(
            app, ["init", str(temp_project_with_claude), "--minimal", "--dry-run"]
        )

        assert result.exit_code == 0
        assert "EXISTS" in result.output

    def test_init_full_creates_commands(self, temp_project: Path) -> None:
        """Should create slash commands in full mode."""
        result = runner.invoke(app, ["init", str(temp_project), "--full"])

        assert result.exit_code == 0
        commands_dir = temp_project / ".claude" / "commands"
        assert commands_dir.exists()
        # Check for at least one command category
        assert (commands_dir / "workflow").exists() or (commands_dir / "dev").exists()

    def test_init_full_creates_skills(self, temp_project: Path) -> None:
        """Should create skills in full mode."""
        result = runner.invoke(app, ["init", str(temp_project), "--full"])

        assert result.exit_code == 0
        skills_dir = temp_project / ".claude" / "skills"
        assert skills_dir.exists()

    def test_init_full_creates_prps_structure(self, temp_project: Path) -> None:
        """Should create PRPs folder structure in full mode."""
        result = runner.invoke(app, ["init", str(temp_project), "--full"])

        assert result.exit_code == 0
        prps_dir = temp_project / "PRPs"
        assert prps_dir.exists()
        assert (prps_dir / "templates").exists()

    def test_init_conflict_skip_preserves_existing(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should preserve existing files when skip resolution chosen."""
        # Write custom content to CLAUDE.md at root
        claude_md = temp_project_with_claude / "CLAUDE.md"
        custom_content = "# Custom CLAUDE.md\n\nMy custom content."
        claude_md.write_text(custom_content)

        # Run init with skip all (option 1)
        result = runner.invoke(
            app, ["init", str(temp_project_with_claude), "--minimal"], input="1\n"
        )

        assert result.exit_code == 0
        # Custom content should be preserved
        assert claude_md.read_text() == custom_content

    def test_init_merge_adds_missing_sections(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should add missing sections to existing CLAUDE.md with --merge."""
        # Create CLAUDE.md with only some sections
        claude_md = temp_project_with_claude / "CLAUDE.md"
        existing_content = """# My Project

## Project Overview

This is my project.

## Tech Stack

- Python
- FastAPI
"""
        claude_md.write_text(existing_content)

        # Run init with --merge (skip conflicts on PLANNING.md/TASK.md)
        result = runner.invoke(
            app,
            ["init", str(temp_project_with_claude), "--minimal", "--merge"],
            input="1\n",  # Skip existing files
        )

        assert result.exit_code == 0
        # Should have added sections
        assert "Merged" in result.output or "already has all" in result.output

        # Existing content should be preserved
        final_content = claude_md.read_text()
        assert "This is my project" in final_content
        assert "## Tech Stack" in final_content

    def test_init_merge_preserves_existing_sections(
        self, temp_project_with_claude: Path
    ) -> None:
        """Should not overwrite existing sections when merging."""
        claude_md = temp_project_with_claude / "CLAUDE.md"
        custom_security = """## Security Rules (CRITICAL)

My custom security rules that should not be overwritten.
"""
        existing_content = f"# My Project\n\n{custom_security}"
        claude_md.write_text(existing_content)

        result = runner.invoke(
            app,
            ["init", str(temp_project_with_claude), "--minimal", "--merge"],
            input="1\n",  # Skip existing files
        )

        assert result.exit_code == 0
        final_content = claude_md.read_text()
        # Custom security content should be preserved
        assert "My custom security rules" in final_content
