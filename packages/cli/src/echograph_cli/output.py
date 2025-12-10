"""Rich output helpers for CLI."""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from echograph_cli.core.models import DoctorCheck, ValidationResult

# Use UTF-8 encoding for console output on Windows
# This prevents UnicodeEncodeError with emoji characters
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# force_terminal=True ensures colors work on Windows PowerShell
# where Rich's auto-detection may fail
console = Console(force_terminal=True)


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green][bold]\u2713[/bold][/green] {message}")


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red][bold]\u2717[/bold][/red] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow][bold]![/bold][/yellow] {message}")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue][bold]i[/bold][/blue] {message}")


def print_doctor_results(checks: list[DoctorCheck]) -> None:
    """Print doctor check results in a table."""
    table = Table(title="EchoGraph Doctor", show_header=True)
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    for check in checks:
        status = "[green]PASS[/green]" if check.passed else "[red]FAIL[/red]"
        details = check.message
        if check.fix_hint and not check.passed:
            details += f"\n[dim]{check.fix_hint}[/dim]"
        table.add_row(check.name, status, details)

    console.print(table)


def print_validation_results(results: list[ValidationResult]) -> None:
    """Print validation results."""
    if not results:
        print_success("All validation checks passed!")
        return

    errors = [r for r in results if r.severity == "error"]
    warnings = [r for r in results if r.severity == "warning"]

    if errors:
        console.print(
            Panel(
                "\n".join(
                    f"[red]{r.file_path}:{r.line_number or 0}[/red] {r.message}"
                    for r in errors
                ),
                title="[red]Errors[/red]",
                border_style="red",
            )
        )

    if warnings:
        console.print(
            Panel(
                "\n".join(
                    f"[yellow]{r.file_path}:{r.line_number or 0}[/yellow] {r.message}"
                    for r in warnings
                ),
                title="[yellow]Warnings[/yellow]",
                border_style="yellow",
            )
        )


def create_progress() -> Progress:
    """Create progress bar for file operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )


def print_welcome_banner() -> None:
    """Print welcome banner for init command."""
    console.print(
        Panel(
            "[bold cyan]EchoGraph[/bold cyan]\n"
            "[dim]Context Engineering for Claude Code[/dim]",
            border_style="cyan",
        )
    )


def print_coming_soon(feature: str) -> None:
    """Print coming soon message for placeholder commands."""
    console.print(
        Panel(
            f"[yellow]{feature}[/yellow] is coming soon!\n\n"
            "[dim]This feature will be available in a future release.\n"
            "Follow development at: https://github.com/echograph/echograph[/dim]",
            title="[yellow]Coming Soon[/yellow]",
            border_style="yellow",
        )
    )


# Diff display color constants
DIFF_COLORS = {
    "added": "green",
    "removed": "red",
    "modified": "yellow",
    "context": "dim",
    "conflict": "bold red",
}


def print_unified_diff(
    old_content: str,
    new_content: str,
    filename: str,
) -> None:
    """Display unified diff with syntax highlighting.

    Args:
        old_content: The existing/user content
        new_content: The new/template content
        filename: Name of the file being compared
    """
    import difflib

    from rich.syntax import Syntax

    diff_lines = difflib.unified_diff(
        old_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"existing/{filename}",
        tofile=f"template/{filename}",
    )
    diff_text = "".join(diff_lines)

    if not diff_text:
        console.print("[dim]No differences found[/dim]")
        return

    console.print(
        Panel(
            Syntax(diff_text, "diff", theme="monokai", line_numbers=True),
            title=f"[cyan]Diff: {filename}[/cyan]",
            border_style="cyan",
        )
    )


def print_three_panel_merge(
    yours: str,
    base: str | None,
    theirs: str,
    title: str,
) -> None:
    """Display three-panel merge view using Rich Columns.

    Args:
        yours: User's current content
        base: Original base content (may be None)
        theirs: New template content
        title: Title for the panel
    """
    from rich.columns import Columns

    panels = [
        Panel(
            yours or "[dim](empty)[/dim]",
            title="[green]YOURS[/green]",
            border_style="green",
        ),
    ]

    if base is not None:
        panels.append(
            Panel(
                base or "[dim](empty)[/dim]",
                title="[dim]BASE[/dim]",
                border_style="dim",
            )
        )

    panels.append(
        Panel(
            theirs or "[dim](empty)[/dim]",
            title="[yellow]THEIRS[/yellow]",
            border_style="yellow",
        )
    )

    console.print(
        Panel(
            Columns(panels, equal=True, expand=True),
            title=title,
            border_style="blue",
        )
    )
