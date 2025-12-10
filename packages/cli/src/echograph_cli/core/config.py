"""Configuration management for EchoGraph CLI."""

import os
from pathlib import Path

import typer
import yaml
from rich.console import Console

# Default config directory follows XDG spec on Linux, AppData on Windows
if os.name == "nt":
    CONFIG_DIR = Path(os.environ.get("APPDATA", "~")) / "echograph"
else:
    CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")) / "echograph"

CONFIG_FILE = CONFIG_DIR.expanduser() / "config.yaml"

console = Console()


def load_config() -> dict:
    """Load configuration from config file.

    Returns:
        Dict with configuration values, empty dict if file doesn't exist.
    """
    config_path = CONFIG_FILE.expanduser()
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, OSError):
            return {}
    return {}


def save_config(config: dict) -> None:
    """Save configuration to config file.

    Args:
        config: Dict with configuration values to save.
    """
    config_path = CONFIG_FILE.expanduser()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False)


def get_api_key(key_name: str = "anthropic_api_key") -> str | None:
    """Get API key from environment or config file.

    Priority:
    1. Environment variable (ANTHROPIC_API_KEY)
    2. Config file (~/.echograph/config.yaml)

    Args:
        key_name: Name of the key in config file.

    Returns:
        API key string or None if not found.
    """
    # Check environment first
    env_var = key_name.upper()
    if env_var == "ANTHROPIC_API_KEY":
        env_key = os.environ.get("ANTHROPIC_API_KEY")
        if env_key:
            return env_key

    # Fall back to config file
    config = load_config()
    return config.get(key_name)


def set_api_key(key_name: str, value: str) -> None:
    """Save API key to config file.

    Args:
        key_name: Name of the key to save.
        value: API key value.
    """
    config = load_config()
    config[key_name] = value
    save_config(config)


def prompt_for_api_key(
    key_name: str = "anthropic_api_key",
    service_name: str = "Anthropic",
    console_url: str = "https://console.anthropic.com/",
) -> str | None:
    """Interactively prompt user for API key if not set.

    Args:
        key_name: Name of the key in config file.
        service_name: Display name of the service.
        console_url: URL where user can get their API key.

    Returns:
        API key string or None if user skipped.
    """
    # Check if already set
    existing_key = get_api_key(key_name)
    if existing_key:
        return existing_key

    console.print(f"\n[yellow]{service_name} API key not found.[/yellow]")
    console.print(f"Get your API key from: [cyan]{console_url}[/cyan]")
    console.print()

    console.print("[bold]Options:[/bold]")
    console.print("  [1] Enter API key now (will be saved for future use)")
    console.print("  [2] Skip (smart merge will be unavailable)")
    console.print()

    choice = typer.prompt("Choose option", default="1")

    if choice != "1":
        console.print("[dim]Skipped - you can set it later with:[/dim]")
        console.print("  [cyan]export ANTHROPIC_API_KEY=your-key[/cyan]")
        return None

    # Prompt for the key
    api_key = typer.prompt(
        f"Enter your {service_name} API key",
        hide_input=True,
    )

    if not api_key or not api_key.strip():
        console.print("[yellow]No key entered, skipping.[/yellow]")
        return None

    api_key = api_key.strip()

    # Ask if they want to save it
    save_key = typer.confirm(
        "Save this key for future use?",
        default=True,
    )

    if save_key:
        set_api_key(key_name, api_key)
        config_path = CONFIG_FILE.expanduser()
        console.print(f"[green]Saved to {config_path}[/green]")
    else:
        console.print("[dim]Key will be used for this session only.[/dim]")

    return api_key


def ensure_api_key(
    key_name: str = "anthropic_api_key",
    service_name: str = "Anthropic",
    console_url: str = "https://console.anthropic.com/",
) -> str:
    """Get API key, prompting if necessary. Raises if unavailable.

    Args:
        key_name: Name of the key in config file.
        service_name: Display name of the service.
        console_url: URL where user can get their API key.

    Returns:
        API key string.

    Raises:
        ValueError: If no API key is available.
    """
    api_key = prompt_for_api_key(key_name, service_name, console_url)
    if not api_key:
        raise ValueError(
            f"{service_name} API key required for this feature.\n"
            f"Set it with: export {key_name.upper()}=your-key"
        )
    return api_key
