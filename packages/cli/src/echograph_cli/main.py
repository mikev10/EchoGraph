"""Main CLI entry point for EchoGraph."""

import typer
from typing_extensions import Annotated

from echograph_cli import __version__
from echograph_cli.output import console

app = typer.Typer(
    name="echograph",
    help="EchoGraph - Context Engineering for Claude Code",
    add_completion=False,
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"echograph {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """EchoGraph - Context Engineering for Claude Code."""
    pass


# Import and register commands after app is created to avoid circular imports
def _register_commands() -> None:
    """Register all commands with the app."""
    from echograph_cli.commands import doctor, init, placeholders, update, validate

    app.command(name="init")(init.init_command)
    app.command(name="update")(update.update_command)
    app.command(name="validate")(validate.validate_command)
    app.command(name="doctor")(doctor.doctor_command)

    # Register placeholder command groups
    app.add_typer(
        placeholders.search_app,
        name="search",
        help="Search your codebase (coming soon)",
    )
    app.add_typer(
        placeholders.sync_app,
        name="sync",
        help="Sync external sources (coming soon)",
    )
    app.add_typer(
        placeholders.decision_app,
        name="decision",
        help="Track architectural decisions (coming soon)",
    )


_register_commands()


if __name__ == "__main__":
    app()
