"""Rich output helpers for CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


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


def print_doctor_results(checks: list) -> None:  # type: ignore[type-arg]
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


def print_validation_results(results: list) -> None:  # type: ignore[type-arg]
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
