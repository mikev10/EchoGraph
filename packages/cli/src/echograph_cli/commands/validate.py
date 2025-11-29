"""Validate command - check context files for completeness."""

from pathlib import Path
from typing import Annotated

import typer

from echograph_cli.core.validation import validate_directory
from echograph_cli.output import console, print_validation_results


def validate_command(
    path: Annotated[
        Path,
        typer.Argument(
            help="Project directory to validate",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
    strict: Annotated[
        bool,
        typer.Option(
            "--strict",
            "-s",
            help="Treat warnings as errors",
        ),
    ] = False,
) -> None:
    """Check context files for required fields and valid references.

    Validates:
    - Required files exist (.claude/CLAUDE.md, PLANNING.md, TASK.md)
    - CLAUDE.md has Project Context section
    - @ imports reference existing files
    - TASK.md has required sections (In Progress, Pending, Completed)
    """
    console.print(f"[dim]Validating {path}...[/dim]\n")

    results = validate_directory(path)

    # Filter by severity for strict mode
    if strict:
        # Upgrade warnings to errors in strict mode
        for result in results:
            if result.severity == "warning":
                result.severity = "error"

    print_validation_results(results)

    # Exit with error code if there are errors
    errors = [r for r in results if r.severity == "error"]
    if errors:
        raise typer.Exit(1)
