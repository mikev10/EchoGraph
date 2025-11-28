"""Tests for main CLI entry point."""

from typer.testing import CliRunner

from echograph_cli import __version__
from echograph_cli.main import app

runner = CliRunner()


class TestMainCli:
    """Tests for main CLI functionality."""

    def test_version_flag(self) -> None:
        """Should show version with --version flag."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert __version__ in result.output

    def test_version_short_flag(self) -> None:
        """Should show version with -v flag."""
        result = runner.invoke(app, ["-v"])

        assert result.exit_code == 0
        assert __version__ in result.output

    def test_help_flag(self) -> None:
        """Should show help with --help flag."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "EchoGraph" in result.output
        assert "init" in result.output
        assert "validate" in result.output
        assert "doctor" in result.output

    def test_no_args_shows_help(self) -> None:
        """Should show help when no arguments provided."""
        result = runner.invoke(app, [])

        assert result.exit_code == 0
        assert "EchoGraph" in result.output


class TestPlaceholderCommands:
    """Tests for placeholder commands."""

    def test_search_shows_coming_soon(self) -> None:
        """Should show coming soon for search command."""
        result = runner.invoke(app, ["search"])

        assert result.exit_code == 0
        assert "coming soon" in result.output.lower()

    def test_sync_shows_coming_soon(self) -> None:
        """Should show coming soon for sync command."""
        result = runner.invoke(app, ["sync"])

        assert result.exit_code == 0
        assert "coming soon" in result.output.lower()

    def test_decision_shows_coming_soon(self) -> None:
        """Should show coming soon for decision command."""
        result = runner.invoke(app, ["decision"])

        assert result.exit_code == 0
        assert "coming soon" in result.output.lower()

    def test_search_query_shows_coming_soon(self) -> None:
        """Should show coming soon for search query subcommand."""
        result = runner.invoke(app, ["search", "query", "test"])

        assert result.exit_code == 0
        assert "coming soon" in result.output.lower()

    def test_sync_github_shows_coming_soon(self) -> None:
        """Should show coming soon for sync github subcommand."""
        result = runner.invoke(app, ["sync", "github", "owner/repo"])

        assert result.exit_code == 0
        assert "coming soon" in result.output.lower()
