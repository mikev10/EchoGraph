"""Doctor command - verify Claude Code setup."""

from pathlib import Path
from typing import Annotated

import typer

from echograph_cli.core.doctor import run_all_checks
from echograph_cli.output import console, print_doctor_results


def doctor_command(
    path: Annotated[
        Path,
        typer.Argument(
            help="Project directory to check",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
) -> None:
    """Verify Claude Code setup and diagnose issues.

    Checks:
    - Claude Code CLI is installed and available
    - .claude/ directory structure is correct
    - MCP configuration is valid (if present)
    - Project is a git repository
    - Template version is up to date
    """
    console.print(f"[dim]Checking {path}...[/dim]\n")

    checks = run_all_checks(path)
    print_doctor_results(checks)

    # Summary
    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    console.print()

    if passed == total:
        console.print("[bold green]All checks passed![/bold green]")
    else:
        console.print(f"[bold yellow]{passed}/{total} checks passed[/bold yellow]")
        console.print("\n[dim]Fix the issues above and run doctor again.[/dim]")
        raise typer.Exit(1)
