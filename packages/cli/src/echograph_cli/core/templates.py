"""Template loading and rendering."""

import json
import subprocess
from importlib import resources
from pathlib import Path
from typing import Any

from jinja2 import BaseLoader, Environment, TemplateNotFound

from echograph_cli import __version__
from echograph_cli.core.models import ConflictResolution, FileConflict, ProjectConfig

# Minimal templates - core files only
MINIMAL_TEMPLATES = [
    ".claude/CLAUDE.md",
    ".claude/PLANNING.md",
    ".claude/TASK.md",
]


class PackageTemplateLoader(BaseLoader):
    """Load templates from package resources."""

    def __init__(self, package: str, template_dir: str = "templates") -> None:
        """Initialize loader."""
        self.package = package
        self.template_dir = template_dir

    def get_source(
        self, environment: Environment, template: str
    ) -> tuple[str, str, Any]:
        """Load template source."""
        template_path = f"{self.template_dir}/{template}"
        try:
            files = resources.files(self.package)
            content = (files / template_path).read_text(encoding="utf-8")
            return content, template_path, lambda: True
        except (FileNotFoundError, TypeError):
            raise TemplateNotFound(template)


def create_template_env() -> Environment:
    """Create Jinja2 environment for template rendering."""
    loader = PackageTemplateLoader("echograph_cli")
    return Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,  # Not HTML, don't escape
    )


def render_template(template_name: str, context: dict[str, Any]) -> str:
    """Render a template with the given context."""
    env = create_template_env()
    template = env.get_template(template_name)
    return template.render(**context)


def list_template_files(mode: str = "full") -> list[str]:
    """List all template files for the given mode."""
    try:
        files = resources.files("echograph_cli") / "templates"
        templates: list[str] = []

        def _walk_templates(base: Any, prefix: str = "") -> None:
            """Recursively walk template directory."""
            try:
                for item in base.iterdir():
                    rel_path = f"{prefix}/{item.name}" if prefix else item.name
                    if item.is_file():
                        # Remove .j2 extension for output path
                        if rel_path.endswith(".j2"):
                            rel_path = rel_path[:-3]
                        templates.append(rel_path)
                    else:
                        _walk_templates(item, rel_path)
            except (TypeError, AttributeError):
                pass

        _walk_templates(files)

        if mode == "minimal":
            return [t for t in templates if t in MINIMAL_TEMPLATES]
        return templates
    except Exception:
        return MINIMAL_TEMPLATES if mode == "minimal" else []


def get_bundled_template(template_path: str) -> str:
    """Get content of a bundled template file."""
    # Try with .j2 extension first
    try:
        env = create_template_env()
        return env.get_template(f"{template_path}.j2").render()
    except TemplateNotFound:
        pass

    # Try without extension
    try:
        files = resources.files("echograph_cli") / "templates"
        return (files / template_path).read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError):
        return ""


def get_project_config(path: Path) -> ProjectConfig:
    """Detect project configuration from directory."""
    project_name = _detect_project_name(path)
    tech_stack = _detect_tech_stack(path)

    # Detect test framework
    test_framework = None
    if (path / "pytest.ini").exists() or (path / "pyproject.toml").exists():
        test_framework = "pytest"
    elif (path / "package.json").exists():
        test_framework = "jest"  # Common default for JS projects

    return ProjectConfig(
        project_name=project_name,
        tech_stack=tech_stack,
        has_tests=(path / "tests").exists() or (path / "test").exists(),
        test_framework=test_framework,
        formatter="ruff" if (path / "ruff.toml").exists() else None,
        linter="ruff" if "python" in tech_stack else None,
    )


def _detect_project_name(path: Path) -> str:
    """Detect project name from git or folder name."""
    # Try git remote
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,  # Explicit per CLAUDE.md security rules
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Extract repo name from URL
            name = url.rstrip("/").split("/")[-1]
            if name.endswith(".git"):
                name = name[:-4]
            return name
    except Exception:
        pass

    # Fall back to folder name
    return path.name


def _detect_tech_stack(path: Path) -> list[str]:
    """Detect tech stack from project files."""
    stack: list[str] = []

    # Python
    if (path / "pyproject.toml").exists() or (path / "setup.py").exists():
        stack.append("python")

    # Node.js
    if (path / "package.json").exists():
        stack.append("nodejs")

    # TypeScript
    if (path / "tsconfig.json").exists():
        stack.append("typescript")

    # Rust
    if (path / "Cargo.toml").exists():
        stack.append("rust")

    # Go
    if (path / "go.mod").exists():
        stack.append("go")

    return stack


def get_template_metadata(metadata_file: Path) -> dict[str, Any]:
    """Load template metadata from file."""
    try:
        result: dict[str, Any] = json.loads(metadata_file.read_text())
        return result
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_template_metadata(
    metadata_file: Path, files: dict[str, str], version: str | None = None
) -> None:
    """Save template metadata to file."""
    metadata = {
        "template_version": version or __version__,
        "files": files,
    }
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(json.dumps(metadata, indent=2))


def detect_conflicts(path: Path, mode: str) -> list[FileConflict]:
    """Detect files that would conflict during init."""
    conflicts: list[FileConflict] = []
    template_files = list_template_files(mode)

    for template_rel_path in template_files:
        target_path = path / template_rel_path
        if target_path.exists():
            conflicts.append(
                FileConflict(
                    template_path=template_rel_path,
                    target_path=target_path,
                    resolution=None,
                )
            )

    return conflicts


def preview_templates(path: Path, mode: str) -> list[tuple[str, bool]]:
    """Preview what files would be created.

    Returns list of (relative_path, would_overwrite) tuples.
    """
    template_files = list_template_files(mode)
    preview: list[tuple[str, bool]] = []

    for template_rel_path in template_files:
        target_path = path / template_rel_path
        preview.append((template_rel_path, target_path.exists()))

    return preview


def copy_templates(
    path: Path,
    mode: str,
    config: ProjectConfig,
    force: bool = False,
    conflict_resolutions: dict[str, ConflictResolution] | None = None,
) -> list[Path]:
    """Copy templates to target directory.

    Args:
        path: Target directory
        mode: "minimal" or "full"
        config: Project configuration for template rendering
        force: If True, overwrite all existing files
        conflict_resolutions: Dict mapping template paths to resolution strategy
    """
    created_files: list[Path] = []
    template_contents: dict[str, str] = {}
    conflict_resolutions = conflict_resolutions or {}

    # Get list of templates for mode
    template_files = list_template_files(mode)

    # Context for template rendering
    context = {
        "project_name": config.project_name,
        "tech_stack": config.tech_stack,
        "has_tests": config.has_tests,
        "test_framework": config.test_framework,
        "formatter": config.formatter,
        "linter": config.linter,
    }

    for template_rel_path in template_files:
        target_path = path / template_rel_path

        # Handle existing files
        if target_path.exists():
            if force:
                pass  # Will overwrite
            elif template_rel_path in conflict_resolutions:
                resolution = conflict_resolutions[template_rel_path]
                if resolution == ConflictResolution.SKIP:
                    continue
                elif resolution == ConflictResolution.RENAME:
                    # Rename existing file with .bak extension
                    backup_path = target_path.with_suffix(target_path.suffix + ".bak")
                    counter = 1
                    while backup_path.exists():
                        backup_path = target_path.with_suffix(
                            f"{target_path.suffix}.bak{counter}"
                        )
                        counter += 1
                    target_path.rename(backup_path)
                # OVERWRITE falls through to write the file
            else:
                continue  # Skip by default if no resolution specified

        # Get template content
        try:
            # Try .j2 template first
            content = render_template(f"{template_rel_path}.j2", context)
        except TemplateNotFound:
            # Fall back to raw file
            content = get_bundled_template(template_rel_path)

        if not content:
            continue

        # Create parent directories
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file with UTF-8 encoding for cross-platform compatibility
        target_path.write_text(content, encoding="utf-8")
        created_files.append(target_path)
        template_contents[template_rel_path] = content

    # Save metadata for future updates
    if created_files:
        metadata_file = path / ".claude" / ".echograph-meta.json"
        save_template_metadata(metadata_file, template_contents)

    return created_files
