"""Init command - scaffold .claude/ directory."""

from pathlib import Path

import typer
from typing_extensions import Annotated

from echograph_cli.core.templates import copy_templates, get_project_config
from echograph_cli.output import (
    console,
    create_progress,
    print_error,
    print_success,
    print_warning,
    print_welcome_banner,
)


def init_command(
    path: Annotated[
        Path,
        typer.Argument(
            help="Project directory to initialize",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
    minimal: Annotated[
        bool,
        typer.Option(
            "--minimal",
            "-m",
            help="Create only CLAUDE.md, PLANNING.md, TASK.md",
        ),
    ] = False,
    full: Annotated[
        bool,
        typer.Option(
            "--full",
            "-f",
            help="Create complete directory structure with all commands",
        ),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Overwrite existing files without prompting",
        ),
    ] = False,
) -> None:
    """Scaffold Context Engineering structure in your project.

    Creates a .claude/ directory with templates for CLAUDE.md,
    PLANNING.md, TASK.md, and optionally slash commands.
    """
    print_welcome_banner()

    # Check for existing .claude directory
    claude_dir = path / ".claude"
    if claude_dir.exists() and not force:
        if not typer.confirm(
            f"\n[yellow].claude/ already exists at {path}[/yellow]\n"
            "Do you want to continue and merge templates?",
            default=False,
        ):
            print_warning("Init cancelled.")
            raise typer.Exit(1)

    # Determine mode
    if minimal and full:
        print_error("Cannot use both --minimal and --full")
        raise typer.Exit(1)

    mode = "minimal" if minimal else "full"
    if not minimal and not full:
        # Interactive mode - ask user
        mode = (
            "minimal"
            if typer.confirm(
                "\nCreate minimal setup (CLAUDE.md, PLANNING.md, TASK.md only)?",
                default=False,
            )
            else "full"
        )

    # Get project configuration
    config = get_project_config(path)
    console.print(f"\n[dim]Project: {config.project_name}[/dim]")

    # Copy templates
    with create_progress() as progress:
        task = progress.add_task("Creating files...", total=None)
        files_created = copy_templates(path, mode, config, force)
        progress.update(task, completed=True)

    # Report results
    console.print()
    for file_path in files_created:
        print_success(f"Created {file_path.relative_to(path)}")

    console.print(f"\n[bold green]Initialized {len(files_created)} files![/bold green]")
    console.print("\n[dim]Next steps:[/dim]")
    console.print("  1. Review and customize CLAUDE.md")
    console.print("  2. Run [cyan]echograph validate[/cyan] to check your setup")
    console.print("  3. Run [cyan]echograph doctor[/cyan] to verify Claude Code")
