"""Placeholder commands for features coming soon."""

import typer

from echograph_cli.output import print_coming_soon

# Search commands
search_app = typer.Typer(
    help="Search your codebase semantically (coming soon)",
    no_args_is_help=True,
)


@search_app.callback(invoke_without_command=True)
def search_callback(ctx: typer.Context) -> None:
    """Search your codebase semantically."""
    if ctx.invoked_subcommand is None:
        print_coming_soon("Semantic Search")


@search_app.command(name="query")
def search_query(query: str = typer.Argument(..., help="Search query")) -> None:
    """Search for code and documentation."""
    print_coming_soon("Semantic Search")


# Sync commands
sync_app = typer.Typer(
    help="Sync external sources (coming soon)",
    no_args_is_help=True,
)


@sync_app.callback(invoke_without_command=True)
def sync_callback(ctx: typer.Context) -> None:
    """Sync external sources."""
    if ctx.invoked_subcommand is None:
        print_coming_soon("Source Sync")


@sync_app.command(name="github")
def sync_github(
    repo: str = typer.Argument(..., help="Repository in owner/repo format"),
) -> None:
    """Sync a GitHub repository."""
    print_coming_soon("GitHub Sync")


@sync_app.command(name="local")
def sync_local(
    path: str = typer.Argument(".", help="Path to local directory"),
) -> None:
    """Sync a local directory."""
    print_coming_soon("Local Sync")


# Decision commands
decision_app = typer.Typer(
    help="Track architectural decisions (coming soon)",
    no_args_is_help=True,
)


@decision_app.callback(invoke_without_command=True)
def decision_callback(ctx: typer.Context) -> None:
    """Track architectural decisions."""
    if ctx.invoked_subcommand is None:
        print_coming_soon("Decision Tracking")


@decision_app.command(name="create")
def decision_create(
    title: str = typer.Argument(..., help="Decision title"),
) -> None:
    """Create a new architectural decision record."""
    print_coming_soon("Decision Tracking")


@decision_app.command(name="list")
def decision_list() -> None:
    """List all decision records."""
    print_coming_soon("Decision Tracking")
