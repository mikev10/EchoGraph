"""Update command - update templates with three-way merge."""

from pathlib import Path
from typing import Annotated

import typer

from echograph_cli import __version__
from echograph_cli.core.merge import three_way_merge
from echograph_cli.core.templates import (
    get_bundled_template,
    get_template_metadata,
    list_template_files,
)
from echograph_cli.output import (
    console,
    create_progress,
    print_error,
    print_info,
    print_success,
    print_warning,
)


def update_command(
    path: Annotated[
        Path,
        typer.Argument(
            help="Project directory to update",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("."),
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-n",
            help="Show what would be updated without making changes",
        ),
    ] = False,
) -> None:
    """Update templates preserving your customizations.

    Uses three-way merge to integrate template updates while
    preserving your changes. Conflicts are marked for manual resolution.
    """
    claude_dir = path / ".claude"
    if not claude_dir.exists():
        print_error(".claude directory not found. Run 'echograph init' first.")
        raise typer.Exit(1)

    # Check template metadata for base version
    metadata_file = claude_dir / ".echograph-meta.json"
    if not metadata_file.exists():
        print_warning(
            "No template metadata found. Cannot perform three-way merge.\n"
            "This project may have been initialized manually or with an "
            "older version.\n"
            "Consider running 'echograph init --force' to reset templates."
        )
        raise typer.Exit(1)

    metadata = get_template_metadata(metadata_file)
    base_version = metadata.get("template_version", "unknown")
    current_version = __version__

    if base_version == current_version:
        print_info("Templates are already up to date.")
        return

    console.print(
        f"[dim]Updating templates from {base_version} to {current_version}[/dim]\n"
    )

    template_files = list_template_files("full")
    updated_count = 0
    conflict_count = 0

    with create_progress() as progress:
        task = progress.add_task("Checking files...", total=len(template_files))

        for template_rel_path in template_files:
            progress.advance(task)
            user_file = path / template_rel_path

            if not user_file.exists():
                # New file in template - just copy
                if not dry_run:
                    user_file.parent.mkdir(parents=True, exist_ok=True)
                    content = get_bundled_template(template_rel_path)
                    user_file.write_text(content, encoding="utf-8")
                print_success(f"Added {template_rel_path}")
                updated_count += 1
                continue

            # Get base, user, and new content
            base_content = metadata.get("files", {}).get(template_rel_path, "")
            user_content = user_file.read_text(encoding="utf-8")
            new_content = get_bundled_template(template_rel_path)

            # Skip if no changes in template
            if base_content == new_content:
                continue

            # Skip if user hasn't modified
            if user_content == base_content:
                if not dry_run:
                    user_file.write_text(new_content, encoding="utf-8")
                print_success(f"Updated {template_rel_path}")
                updated_count += 1
                continue

            # Three-way merge needed
            merged, conflicts = three_way_merge(base_content, user_content, new_content)

            if conflicts:
                if not dry_run:
                    user_file.write_text(merged, encoding="utf-8")
                print_warning(
                    f"Updated {template_rel_path} with {len(conflicts)} conflict(s)"
                )
                conflict_count += len(conflicts)
            else:
                if not dry_run:
                    user_file.write_text(merged, encoding="utf-8")
                print_success(f"Merged {template_rel_path}")
            updated_count += 1

    # Summary
    console.print()
    if dry_run:
        console.print("[dim]Dry run - no changes made[/dim]")

    if updated_count == 0:
        print_info("No updates needed.")
    else:
        console.print(f"[bold]Updated {updated_count} file(s)[/bold]")
        if conflict_count > 0:
            print_warning(
                f"\n{conflict_count} conflict(s) need manual resolution.\n"
                "Look for <<<<<<< YOUR CHANGES markers in affected files."
            )
