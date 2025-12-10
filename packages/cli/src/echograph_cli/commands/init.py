"""Init command - scaffold .claude/ directory."""

from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer
from jinja2.exceptions import TemplateNotFound
from rich.table import Table

from echograph_cli.core.ai_merge import smart_merge_file
from echograph_cli.core.merge import (
    ConflictMarkerStyle,
    merge_claude_md_sections,
    three_way_merge_sections,
)
from echograph_cli.core.models import ConflictResolution
from echograph_cli.core.templates import (
    copy_templates,
    detect_conflicts,
    get_bundled_template,
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
    print_unified_diff,
    print_warning,
    print_welcome_banner,
)

# Sentinel value for smart merge resolution
SMART_MERGE_SENTINEL = "SMART_MERGE"


def _handle_claude_md_migration(path: Path) -> bool:
    """Handle migration of CLAUDE.md from old to new location.

    Returns True if migration was handled (user made a choice),
    False if no migration needed.
    """
    old_location = path / ".claude" / "CLAUDE.md"
    new_location = path / "CLAUDE.md"

    old_exists = old_location.exists()
    new_exists = new_location.exists()

    # Scenario 1: Neither exists - no migration needed
    if not old_exists and not new_exists:
        return False

    # Scenario 2: Only new location - no migration needed
    if not old_exists and new_exists:
        return False

    # Scenario 3: Only old location - offer to move
    if old_exists and not new_exists:
        console.print("\n[yellow]Migration needed:[/yellow]")
        console.print("  Found CLAUDE.md at old location: [dim].claude/CLAUDE.md[/dim]")
        console.print("  New location is project root: [dim]./CLAUDE.md[/dim]")
        console.print()

        if typer.confirm("Move CLAUDE.md to root?", default=True):
            old_content = old_location.read_text(encoding="utf-8")
            new_location.write_text(old_content, encoding="utf-8")
            old_location.unlink()
            print_success("Moved CLAUDE.md to project root")
            return True
        else:
            print_warning("Skipped migration - CLAUDE.md remains at old location")
            return True

    # Scenario 4: Both exist - let user decide
    console.print("\n[yellow]Found CLAUDE.md in both locations:[/yellow]")
    console.print("  [green]./CLAUDE.md[/green] (root - correct location)")
    console.print("  [dim].claude/CLAUDE.md[/dim] (old location)")
    console.print()
    console.print("What would you like to do?")
    console.print("  [1] Keep root, delete old (recommended)")
    console.print("  [2] Merge old content into root, then delete old")
    console.print("  [3] Keep both (not recommended)")

    choice = typer.prompt("Choose option", default="1")

    if choice == "1":
        old_location.unlink()
        print_success("Deleted old .claude/CLAUDE.md")
    elif choice == "2":
        # Merge old into new
        old_content = old_location.read_text(encoding="utf-8")
        new_content = new_location.read_text(encoding="utf-8")

        from echograph_cli.core.merge import merge_claude_md_sections

        merged, added = merge_claude_md_sections(new_content, old_content)
        if added:
            new_location.write_text(merged, encoding="utf-8")
            print_success(f"Merged {len(added)} sections from old file")
        else:
            print_info("No new sections to merge from old file")

        old_location.unlink()
        print_success("Deleted old .claude/CLAUDE.md")
    else:
        print_warning("Keeping both files - remember to clean up .claude/CLAUDE.md")

    return True


def _resolve_conflicts_interactive(
    conflicts: list[tuple[str, Path]],
    get_template_content: Callable[[str], str] | None = None,
    smart_merge_available: bool = False,
) -> dict[str, ConflictResolution | str]:
    """Prompt user for conflict resolution strategy.

    Args:
        conflicts: List of (template_path, target_path) tuples
        get_template_content: Optional callable to get template content for diff display
        smart_merge_available: Whether AI merge is available (anthropic installed)

    Returns:
        Dict mapping template_path to resolution (or SMART_MERGE_SENTINEL for AI merge)
    """
    resolutions: dict[str, ConflictResolution | str] = {}

    console.print(f"\n[yellow]Found {len(conflicts)} existing file(s):[/yellow]")

    # Ask for global strategy first
    console.print("\nHow would you like to handle conflicts?")
    console.print("  [1] Skip all existing files (keep your changes)")
    console.print("  [2] Overwrite all existing files (use new templates)")
    console.print("  [3] Rename existing files (backup as .bak)")
    console.print("  [4] Decide for each file individually")
    console.print("  [5] [cyan]Smart merge (AI-assisted)[/cyan]")
    console.print("      [dim]AI merges your customizations with new templates[/dim]")
    console.print()

    # Loop until valid choice
    while True:
        choice = typer.prompt("Choose option (1-5)")
        if choice in ("1", "2", "3", "4", "5"):
            break
        console.print("[red]Please enter 1, 2, 3, 4, or 5[/red]")

    if choice == "1":
        return {c[0]: ConflictResolution.SKIP for c in conflicts}
    elif choice == "2":
        return {c[0]: ConflictResolution.OVERWRITE for c in conflicts}
    elif choice == "3":
        return {c[0]: ConflictResolution.RENAME for c in conflicts}
    elif choice == "5":
        # Smart merge - mark all files for AI-assisted merge
        return {c[0]: SMART_MERGE_SENTINEL for c in conflicts}
    else:  # choice == "4"
        # Individual resolution with diff support
        for template_path, target_path in conflicts:
            is_markdown = target_path.suffix == ".md"

            while True:
                console.print(f"\n[yellow]{template_path}[/yellow] already exists")
                console.print("  (s) Skip (keep existing)")
                console.print("  (o) Overwrite (use template)")
                console.print("  (r) Rename existing to .bak")
                if get_template_content is not None:
                    console.print("  (d) Show diff")
                    if is_markdown:
                        console.print("  (m) Section merge (markdown)")
                    console.print("  (a) [cyan]AI smart merge[/cyan]")

                file_choice = typer.prompt("Choose", default="s").lower()

                if file_choice == "d" and get_template_content is not None:
                    # Show diff and re-prompt
                    try:
                        existing_content = target_path.read_text(encoding="utf-8")
                        template_content = get_template_content(template_path)
                        print_unified_diff(
                            existing_content,
                            template_content,
                            target_path.name,
                        )
                    except Exception as e:
                        console.print(f"[red]Error reading file: {e}[/red]")
                    continue  # Re-prompt after showing diff

                if (
                    file_choice == "m"
                    and is_markdown
                    and get_template_content is not None
                ):
                    # Section-level merge for markdown files
                    try:
                        existing_content = target_path.read_text(encoding="utf-8")
                        template_content = get_template_content(template_path)

                        # Use empty string as base (no three-way, just merge sections)
                        merged, section_conflicts = three_way_merge_sections(
                            "",  # No base version available
                            existing_content,
                            template_content,
                            ConflictMarkerStyle.HTML_COMMENT,
                        )

                        target_path.write_text(merged, encoding="utf-8")

                        if section_conflicts:
                            console.print(
                                f"  [yellow]Merged with {len(section_conflicts)} "
                                f"conflict(s) - review markers in file[/yellow]"
                            )
                        else:
                            console.print(
                                "  [green]Sections merged successfully[/green]"
                            )

                        # Already handled - skip in copy_templates
                        resolutions[template_path] = ConflictResolution.SKIP
                    except Exception as e:
                        console.print(f"[red]Error merging: {e}[/red]")
                        continue
                    break

                if (
                    file_choice == "a"
                    and get_template_content is not None
                ):
                    # AI-assisted smart merge
                    try:
                        existing_content = target_path.read_text(encoding="utf-8")
                        template_content = get_template_content(template_path)

                        result = smart_merge_file(
                            user_content=existing_content,
                            template_content=template_content,
                            filename=target_path.name,
                            console=console,
                            auto_approve=False,
                        )

                        if result.user_approved:
                            target_path.write_text(
                                result.merged_content, encoding="utf-8"
                            )
                            console.print("  [green]Smart merge applied[/green]")
                        else:
                            console.print("  [yellow]Kept original file[/yellow]")

                        # Already handled - skip in copy_templates
                        resolutions[template_path] = ConflictResolution.SKIP
                    except Exception as e:
                        console.print(f"[red]Error in AI merge: {e}[/red]")
                        continue
                    break

                if file_choice == "o":
                    resolutions[template_path] = ConflictResolution.OVERWRITE
                elif file_choice == "r":
                    resolutions[template_path] = ConflictResolution.RENAME
                else:
                    resolutions[template_path] = ConflictResolution.SKIP
                break  # Exit the while loop

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
    auto_merge: Annotated[
        bool,
        typer.Option(
            "--auto-merge",
            help="Auto-merge non-conflicting sections in markdown files",
        ),
    ] = False,
    smart_merge: Annotated[
        bool,
        typer.Option(
            "--smart-merge",
            help="Use AI-assisted merge for all conflicting files",
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

    # Handle migration from old CLAUDE.md location
    if not dry_run:
        _handle_claude_md_migration(path)

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
    conflict_resolutions: dict[str, ConflictResolution | str] = {}
    smart_merge_files: list[tuple[str, Path]] = []  # Files marked for smart merge

    if not force:
        conflicts = detect_conflicts(path, mode)
        # If we merged CLAUDE.md, skip it in conflict detection
        if merged_claude_md:
            conflicts = [c for c in conflicts if c.template_path != "CLAUDE.md"]
        if conflicts:
            # Create a getter function for template content (for diff display)
            def get_template_content(template_path: str) -> str:
                """Get rendered template content for a given template path."""
                context = {
                    "project_name": config.project_name,
                    "tech_stack": config.tech_stack,
                    "has_tests": config.has_tests,
                    "test_framework": config.test_framework,
                    "formatter": config.formatter,
                    "linter": config.linter,
                }
                # Try .j2 template first, fall back to raw file
                try:
                    return render_template(f"{template_path}.j2", context)
                except TemplateNotFound:
                    return get_bundled_template(template_path)

            if smart_merge:
                # --smart-merge flag: mark all conflicts for AI merge
                conflict_resolutions = {
                    c.template_path: SMART_MERGE_SENTINEL for c in conflicts
                }
            else:
                conflict_resolutions = _resolve_conflicts_interactive(
                    [(c.template_path, c.target_path) for c in conflicts],
                    get_template_content=get_template_content,
                )

            # Process smart merge files
            for c in conflicts:
                if conflict_resolutions.get(c.template_path) == SMART_MERGE_SENTINEL:
                    smart_merge_files.append((c.template_path, c.target_path))

    # If CLAUDE.md was merged, mark it to skip in copy_templates
    if merged_claude_md:
        conflict_resolutions["CLAUDE.md"] = ConflictResolution.SKIP

    # Handle smart merge files before copy_templates
    if smart_merge_files:
        # Check for anthropic package and API key upfront
        from echograph_cli.core.config import prompt_for_api_key

        try:
            import anthropic  # noqa: F401
        except ImportError:
            console.print()
            console.print("[red]" + "=" * 50 + "[/red]")
            console.print("[bold red]  ⚠ MISSING DEPENDENCY[/bold red]")
            console.print("[red]" + "=" * 50 + "[/red]")
            console.print()
            console.print("  Smart merge requires the [bold]anthropic[/bold] package.")
            console.print()
            console.print("  [bold]To install:[/bold]")
            console.print("    [green]uv tool install echograph\\[ai][/green]")
            console.print()
            console.print("  Then run [cyan]echograph init[/cyan] again.")
            console.print()
            console.print("[red]" + "=" * 50 + "[/red]")
            console.print()

            # Ask user what to do
            console.print("[bold]What would you like to do?[/bold]")
            console.print("  [1] Skip all conflicts (keep existing files)")
            console.print("  [2] Abort and install package first (recommended)")
            fallback_choice = typer.prompt("Choose option", default="2")

            if fallback_choice == "1":
                for template_path, _ in smart_merge_files:
                    conflict_resolutions[template_path] = ConflictResolution.SKIP
                smart_merge_files = []
            else:
                raise typer.Exit(0)

        if smart_merge_files:
            # Prompt for API key if not set
            api_key = prompt_for_api_key(
                key_name="anthropic_api_key",
                service_name="Anthropic",
                console_url="https://console.anthropic.com/",
            )
            if not api_key:
                console.print("\n[yellow]No API key provided.[/yellow]")

                # Ask user what to do
                console.print("\n[bold]What would you like to do?[/bold]")
                console.print("  [1] Skip all conflicts (keep existing files)")
                console.print("  [2] Abort and set up API key first")
                fallback_choice = typer.prompt("Choose option", default="2")

                if fallback_choice == "1":
                    for template_path, _ in smart_merge_files:
                        conflict_resolutions[template_path] = ConflictResolution.SKIP
                    smart_merge_files = []
                else:
                    raise typer.Exit(0)

    if smart_merge_files:
        console.print(
            f"\n[cyan]Processing {len(smart_merge_files)} file(s) "
            f"with AI-assisted merge...[/cyan]"
        )

        def get_template_content_for_merge(template_path: str) -> str:
            """Get rendered template content for smart merge."""
            context = {
                "project_name": config.project_name,
                "tech_stack": config.tech_stack,
                "has_tests": config.has_tests,
                "test_framework": config.test_framework,
                "formatter": config.formatter,
                "linter": config.linter,
            }
            # Try .j2 template first, fall back to raw file
            try:
                return render_template(f"{template_path}.j2", context)
            except TemplateNotFound:
                return get_bundled_template(template_path)

        for template_path, target_path in smart_merge_files:
            try:
                existing_content = target_path.read_text(encoding="utf-8")
                template_content = get_template_content_for_merge(template_path)

                result = smart_merge_file(
                    user_content=existing_content,
                    template_content=template_content,
                    filename=target_path.name,
                    console=console,
                    auto_approve=smart_merge,  # Auto-approve with --smart-merge flag
                )

                if result.user_approved:
                    if not result.was_skipped_whitespace:
                        # Only write if there were actual changes
                        target_path.write_text(result.merged_content, encoding="utf-8")
                        print_success(f"Smart merged: {template_path}")
                    # else: whitespace skip already printed message, no action needed
                else:
                    print_warning(f"Skipped: {template_path}")

                # Mark as handled
                conflict_resolutions[template_path] = ConflictResolution.SKIP
            except Exception as e:
                print_error(f"Smart merge failed for {template_path}: {e}")
                conflict_resolutions[template_path] = ConflictResolution.SKIP

    # Convert any remaining SMART_MERGE_SENTINEL to SKIP
    final_resolutions: dict[str, ConflictResolution] = {}
    for k, v in conflict_resolutions.items():
        if isinstance(v, ConflictResolution):
            final_resolutions[k] = v
        else:
            final_resolutions[k] = ConflictResolution.SKIP

    # Copy templates
    with create_progress() as progress:
        task = progress.add_task("Creating files...", total=None)
        files_created = copy_templates(path, mode, config, force, final_resolutions)
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
