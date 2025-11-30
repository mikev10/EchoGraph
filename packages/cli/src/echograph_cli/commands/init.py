"""Init command - scaffold .claude/ directory."""

from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from echograph_cli.core.merge import merge_claude_md_sections
from echograph_cli.core.models import ConflictResolution
from echograph_cli.core.templates import (
    copy_templates,
    detect_conflicts,
    get_project_config,
    preview_templates,
    render_template,
)
from echograph_cli.output import (
    console,
    create_progress,
    print_error,
    print_info,
    print_success,
    print_warning,
    print_welcome_banner,
)


def _resolve_conflicts_interactive(
    conflicts: list[tuple[str, Path]],
) -> dict[str, ConflictResolution]:
    """Prompt user for conflict resolution strategy."""
    resolutions: dict[str, ConflictResolution] = {}

    console.print(f"\n[yellow]Found {len(conflicts)} existing file(s):[/yellow]")

    # Ask for global strategy first
    console.print("\nHow would you like to handle conflicts?")
    console.print("  [1] Skip all existing files (keep your changes)")
    console.print("  [2] Overwrite all existing files (use new templates)")
    console.print("  [3] Rename existing files (backup as .bak)")
    console.print("  [4] Decide for each file individually")

    choice = typer.prompt("Choose option", default="1")

    if choice == "1":
        return {c[0]: ConflictResolution.SKIP for c in conflicts}
    elif choice == "2":
        return {c[0]: ConflictResolution.OVERWRITE for c in conflicts}
    elif choice == "3":
        return {c[0]: ConflictResolution.RENAME for c in conflicts}
    else:
        # Individual resolution
        for template_path, target_path in conflicts:
            console.print(f"\n[yellow]{template_path}[/yellow] already exists")
            console.print("  [s] Skip (keep existing)")
            console.print("  [o] Overwrite (use template)")
            console.print("  [r] Rename existing to .bak")

            file_choice = typer.prompt("Choose", default="s").lower()
            if file_choice == "o":
                resolutions[template_path] = ConflictResolution.OVERWRITE
            elif file_choice == "r":
                resolutions[template_path] = ConflictResolution.RENAME
            else:
                resolutions[template_path] = ConflictResolution.SKIP

    return resolutions


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
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-n",
            help="Preview what would be created without making changes",
        ),
    ] = False,
    merge: Annotated[
        bool,
        typer.Option(
            "--merge",
            help="Merge missing sections into existing CLAUDE.md",
        ),
    ] = False,
) -> None:
    """Scaffold Context Engineering structure in your project.

    Creates a .claude/ directory with templates for CLAUDE.md,
    PLANNING.md, TASK.md, and optionally slash commands and skills.

    Use --dry-run to preview what files would be created.
    """
    print_welcome_banner()

    # Determine mode
    if minimal and full:
        print_error("Cannot use both --minimal and --full")
        raise typer.Exit(1)

    mode = "minimal" if minimal else "full"
    if not minimal and not full and not dry_run:
        # Interactive mode - show clear menu
        console.print("\n[bold]What would you like to set up?[/bold]\n")
        console.print("  [1] [green]Full setup[/green] (recommended)")
        console.print("      Core files + slash commands, skills, tasks")
        console.print()
        console.print("  [2] Minimal setup")
        console.print("      CLAUDE.md, PLANNING.md, TASK.md only")
        console.print()

        choice = typer.prompt("Choose option", default="1")
        mode = "minimal" if choice == "2" else "full"

    # Handle --dry-run
    if dry_run:
        console.print(f"\n[bold]Dry run - previewing {mode} setup[/bold]\n")
        preview = preview_templates(path, mode)

        table = Table(title="Files to be created")
        table.add_column("File", style="cyan")
        table.add_column("Status")

        new_count = 0
        conflict_count = 0
        for rel_path, exists in preview:
            if exists:
                table.add_row(rel_path, "[yellow]EXISTS (would skip)[/yellow]")
                conflict_count += 1
            else:
                table.add_row(rel_path, "[green]NEW[/green]")
                new_count += 1

        console.print(table)
        console.print(f"\n[green]{new_count} new files[/green]", end="")
        if conflict_count:
            console.print(f", [yellow]{conflict_count} conflicts[/yellow]")
        else:
            console.print()
        print_info("Run without --dry-run to create files")
        return

    # Get project configuration
    config = get_project_config(path)
    console.print(f"\n[dim]Project: {config.project_name}[/dim]")

    # Handle CLAUDE.md merge if it exists and --merge is used
    claude_md_path = path / "CLAUDE.md"
    merged_claude_md = False
    if claude_md_path.exists() and merge:
        existing_content = claude_md_path.read_text(encoding="utf-8")
        # Render template with project config
        context = {
            "project_name": config.project_name,
            "tech_stack": config.tech_stack,
            "has_tests": config.has_tests,
            "test_framework": config.test_framework,
            "formatter": config.formatter,
            "linter": config.linter,
        }
        template_content = render_template("CLAUDE.md.j2", context)

        merged_content, added_sections = merge_claude_md_sections(
            existing_content, template_content
        )

        if added_sections:
            claude_md_path.write_text(merged_content, encoding="utf-8")
            console.print()
            print_success(f"Merged {len(added_sections)} sections into CLAUDE.md:")
            for section in added_sections:
                console.print(f"  [green]+[/green] {section}")
            merged_claude_md = True
        else:
            print_info("CLAUDE.md already has all template sections")

    # Detect conflicts
    conflict_resolutions: dict[str, ConflictResolution] = {}
    if not force:
        conflicts = detect_conflicts(path, mode)
        # If we merged CLAUDE.md, skip it in conflict detection
        if merged_claude_md:
            conflicts = [c for c in conflicts if c.template_path != "CLAUDE.md"]
        if conflicts:
            conflict_resolutions = _resolve_conflicts_interactive(
                [(c.template_path, c.target_path) for c in conflicts]
            )
    # If CLAUDE.md was merged, mark it to skip in copy_templates
    if merged_claude_md:
        conflict_resolutions["CLAUDE.md"] = ConflictResolution.SKIP

    # Copy templates
    with create_progress() as progress:
        task = progress.add_task("Creating files...", total=None)
        files_created = copy_templates(path, mode, config, force, conflict_resolutions)
        progress.update(task, completed=True)

    # Report results
    console.print()
    for file_path in files_created:
        print_success(f"Created {file_path.relative_to(path)}")

    if not files_created:
        print_warning("No files created (all conflicts skipped)")
        return

    console.print(f"\n[bold green]Initialized {len(files_created)} files![/bold green]")
    console.print("\n[dim]Next steps:[/dim]")
    console.print("  1. Review and customize CLAUDE.md")
    console.print("  2. Run [cyan]echograph validate[/cyan] to check your setup")
    console.print("  3. Run [cyan]echograph doctor[/cyan] to verify Claude Code")
