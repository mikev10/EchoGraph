# PRP: Context Engineering CLI

**Parent Task**: [TASK-002] Context Engineering CLI (from `.claude/TASK.md`)
**Child Task**: [TASK-002.1] through [TASK-002.9] - Full CLI implementation

---

## 1. Goal

Build the foundational `echograph` CLI that scaffolds Context Engineering workflows into any project, providing templates, validation, and setup verification for Claude Code best practices.

## 2. Why (Business Value)

- **Immediate value**: Developers can adopt Context Engineering without waiting for full EchoGraph search stack
- **Reduced friction**: Single command (`echograph init`) sets up entire `.claude/` structure
- **Consistency**: Standard templates ensure teams follow best practices
- **Discoverability**: `echograph doctor` helps troubleshoot Claude Code setup issues
- **Update path**: `echograph update` allows template updates without losing customizations

## 3. What (Success Criteria)

- [ ] `pip install echograph` works from PyPI
- [ ] `echograph --version` shows correct version
- [ ] `echograph --help` shows all available commands with descriptions
- [ ] `echograph init` scaffolds `.claude/` directory in <5 seconds
- [ ] `echograph init --minimal` creates only CLAUDE.md, PLANNING.md, TASK.md
- [ ] `echograph init --full` creates complete structure with all commands
- [ ] `echograph init` detects existing `.claude/` and prompts for confirmation
- [ ] `echograph init` respects .gitignore patterns for project detection
- [ ] `echograph update` preserves user customizations via three-way merge
- [ ] `echograph update` reports conflicts clearly with resolution options
- [ ] `echograph validate` checks required fields in context files
- [ ] `echograph validate` validates `@` import references point to existing files
- [ ] `echograph validate` reports issues with file:line references
- [ ] `echograph doctor` checks Claude Code CLI availability
- [ ] `echograph doctor` verifies `.claude/` directory structure
- [ ] `echograph doctor` checks MCP configuration
- [ ] `echograph doctor` reports template version vs latest
- [ ] Placeholder commands show helpful "coming soon" messages
- [ ] Rich terminal output with colors, panels, and progress indicators
- [ ] All tests pass with 80%+ coverage

## 4. All Needed Context

### Package Structure

```
packages/
└── cli/
    ├── pyproject.toml
    ├── src/
    │   └── echograph_cli/
    │       ├── __init__.py
    │       ├── main.py              # Typer app entry point
    │       ├── commands/
    │       │   ├── __init__.py
    │       │   ├── init.py          # init command
    │       │   ├── update.py        # update command
    │       │   ├── validate.py      # validate command
    │       │   ├── doctor.py        # doctor command
    │       │   └── placeholders.py  # search, sync, decision
    │       ├── core/
    │       │   ├── __init__.py
    │       │   ├── templates.py     # Template loading/rendering
    │       │   ├── merge.py         # Three-way merge logic
    │       │   └── validation.py    # Validation rules
    │       └── templates/           # Bundled templates
    │           ├── .claude/
    │           │   ├── CLAUDE.md.j2
    │           │   ├── PLANNING.md.j2
    │           │   ├── TASK.md.j2
    │           │   ├── commands/
    │           │   │   └── ... (all command templates)
    │           │   ├── tasks/
    │           │   │   └── README.md
    │           │   └── templates/
    │           │       └── ... (template files)
    │           └── PRPs/
    │               └── .gitkeep
    └── tests/
        ├── __init__.py
        ├── test_init.py
        ├── test_update.py
        ├── test_validate.py
        ├── test_doctor.py
        ├── test_merge.py
        └── conftest.py              # pytest fixtures
```

### Data Models

```python
# packages/cli/src/echograph_cli/core/models.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

class SetupMode(Enum):
    """Init setup mode."""
    MINIMAL = "minimal"
    FULL = "full"
    INTERACTIVE = "interactive"

@dataclass
class ProjectConfig:
    """Project configuration for template rendering."""
    project_name: str
    tech_stack: list[str] = field(default_factory=list)
    has_tests: bool = True
    test_framework: str = "pytest"
    formatter: str = "ruff"
    linter: str = "ruff"

@dataclass
class ValidationResult:
    """Result of a validation check."""
    file_path: Path
    line_number: Optional[int]
    rule: str
    message: str
    severity: str  # "error", "warning", "info"

@dataclass
class DoctorCheck:
    """Result of a doctor check."""
    name: str
    passed: bool
    message: str
    fix_hint: Optional[str] = None

@dataclass
class MergeConflict:
    """A conflict detected during three-way merge."""
    file_path: Path
    line_number: int
    base_content: str
    user_content: str
    new_content: str

@dataclass
class MergeResult:
    """Result of template merge operation."""
    merged_content: str
    conflicts: list[MergeConflict]
    has_conflicts: bool = field(init=False)

    def __post_init__(self):
        self.has_conflicts = len(self.conflicts) > 0
```

### CLI Structure (Typer Pattern)

```python
# packages/cli/src/echograph_cli/main.py
import typer
from rich.console import Console
from typing_extensions import Annotated

from echograph_cli.commands import init, update, validate, doctor, placeholders

app = typer.Typer(
    name="echograph",
    help="EchoGraph - Context Engineering for Claude Code",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()

# Add command groups
app.add_typer(placeholders.app, name="search")
app.add_typer(placeholders.app, name="sync")
app.add_typer(placeholders.app, name="decision")

# Register commands
app.command()(init.init_command)
app.command(name="update")(update.update_command)
app.command()(validate.validate_command)
app.command()(doctor.doctor_command)

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show version and exit")
    ] = False,
):
    """EchoGraph - Context Engineering for Claude Code."""
    if version:
        from echograph_cli import __version__
        console.print(f"echograph {__version__}")
        raise typer.Exit()

if __name__ == "__main__":
    app()
```

### Template Loading Pattern

```python
# packages/cli/src/echograph_cli/core/templates.py
from importlib import resources
from pathlib import Path
from jinja2 import Environment, BaseLoader, TemplateNotFound

class PackageTemplateLoader(BaseLoader):
    """Load templates from package resources."""

    def __init__(self, package: str, template_dir: str = "templates"):
        self.package = package
        self.template_dir = template_dir

    def get_source(self, environment, template):
        template_path = f"{self.template_dir}/{template}"
        try:
            # Python 3.9+ pattern
            files = resources.files(self.package)
            content = (files / template_path).read_text()
            return content, template_path, lambda: True
        except FileNotFoundError:
            raise TemplateNotFound(template)

def create_template_env() -> Environment:
    """Create Jinja2 environment for template rendering."""
    loader = PackageTemplateLoader("echograph_cli")
    env = Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    return env

def render_template(template_name: str, context: dict) -> str:
    """Render a template with the given context."""
    env = create_template_env()
    template = env.get_template(template_name)
    return template.render(**context)

def list_templates(mode: str = "full") -> list[str]:
    """List all template files for the given mode."""
    files = resources.files("echograph_cli") / "templates"
    templates = []

    minimal_files = {"CLAUDE.md.j2", "PLANNING.md.j2", "TASK.md.j2"}

    for item in files.iterdir():
        if mode == "minimal" and item.name not in minimal_files:
            continue
        templates.append(item.name)

    return templates
```

### Three-Way Merge Pattern

```python
# packages/cli/src/echograph_cli/core/merge.py
import difflib
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MergeConflict:
    """A conflict detected during three-way merge."""
    line_number: int
    base_content: str
    user_content: str
    new_content: str

def three_way_merge(
    base: str,
    user: str,
    new: str,
) -> tuple[str, list[MergeConflict]]:
    """
    Perform three-way merge preserving user customizations.

    Args:
        base: Original template content (from previous version)
        user: User's modified version
        new: New template version

    Returns:
        Tuple of (merged_content, list_of_conflicts)
    """
    base_lines = base.splitlines(keepends=True)
    user_lines = user.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)

    conflicts: list[MergeConflict] = []
    merged_lines: list[str] = []

    # Use SequenceMatcher to find differences
    user_matcher = difflib.SequenceMatcher(None, base_lines, user_lines)
    new_matcher = difflib.SequenceMatcher(None, base_lines, new_lines)

    user_changes = {op[1]: op for op in user_matcher.get_opcodes() if op[0] != 'equal'}
    new_changes = {op[1]: op for op in new_matcher.get_opcodes() if op[0] != 'equal'}

    i = 0
    while i < len(base_lines):
        user_op = user_changes.get(i)
        new_op = new_changes.get(i)

        if user_op is None and new_op is None:
            # No changes at this position
            merged_lines.append(base_lines[i])
            i += 1
        elif user_op is None:
            # Only new template changed
            tag, i1, i2, j1, j2 = new_op
            merged_lines.extend(new_lines[j1:j2])
            i = i2
        elif new_op is None:
            # Only user changed - preserve their changes
            tag, i1, i2, j1, j2 = user_op
            merged_lines.extend(user_lines[j1:j2])
            i = i2
        else:
            # Both changed - check if same change or conflict
            _, u_i1, u_i2, u_j1, u_j2 = user_op
            _, n_i1, n_i2, n_j1, n_j2 = new_op

            user_content = ''.join(user_lines[u_j1:u_j2])
            new_content = ''.join(new_lines[n_j1:n_j2])

            if user_content == new_content:
                # Same change - use either
                merged_lines.extend(user_lines[u_j1:u_j2])
            else:
                # Conflict - add markers
                conflict = MergeConflict(
                    line_number=len(merged_lines) + 1,
                    base_content=''.join(base_lines[u_i1:u_i2]),
                    user_content=user_content,
                    new_content=new_content,
                )
                conflicts.append(conflict)

                # Add conflict markers
                merged_lines.append('<<<<<<< YOUR CHANGES\n')
                merged_lines.extend(user_lines[u_j1:u_j2])
                merged_lines.append('=======\n')
                merged_lines.extend(new_lines[n_j1:n_j2])
                merged_lines.append('>>>>>>> NEW TEMPLATE\n')

            i = max(u_i2, n_i2)

    return ''.join(merged_lines), conflicts
```

### Validation Rules

```python
# packages/cli/src/echograph_cli/core/validation.py
import re
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of a validation check."""
    file_path: Path
    line_number: int | None
    rule: str
    message: str
    severity: str  # "error", "warning", "info"

def validate_claude_md(content: str, file_path: Path) -> list[ValidationResult]:
    """Validate CLAUDE.md file."""
    results = []

    # Rule: Must have project context section
    if "## Project Context" not in content and "## project context" not in content.lower():
        results.append(ValidationResult(
            file_path=file_path,
            line_number=None,
            rule="claude-md-context",
            message="CLAUDE.md should have a '## Project Context' section",
            severity="warning",
        ))

    # Rule: Check @ imports reference existing files
    import_pattern = r'@([^\s]+\.md)'
    for i, line in enumerate(content.splitlines(), 1):
        for match in re.finditer(import_pattern, line):
            import_path = match.group(1)
            full_path = file_path.parent / import_path
            if not full_path.exists():
                results.append(ValidationResult(
                    file_path=file_path,
                    line_number=i,
                    rule="import-exists",
                    message=f"Import '@{import_path}' references non-existent file",
                    severity="error",
                ))

    return results

def validate_planning_md(content: str, file_path: Path) -> list[ValidationResult]:
    """Validate PLANNING.md file."""
    results = []

    # Rule: Should have goals section
    if "## " not in content:
        results.append(ValidationResult(
            file_path=file_path,
            line_number=None,
            rule="planning-structure",
            message="PLANNING.md should have at least one section (## heading)",
            severity="warning",
        ))

    return results

def validate_task_md(content: str, file_path: Path) -> list[ValidationResult]:
    """Validate TASK.md file."""
    results = []

    # Rule: Should have status sections
    required_sections = ["In Progress", "Pending", "Completed"]
    for section in required_sections:
        if f"## {section}" not in content:
            results.append(ValidationResult(
                file_path=file_path,
                line_number=None,
                rule="task-sections",
                message=f"TASK.md should have '## {section}' section",
                severity="warning",
            ))

    return results

def validate_directory(path: Path) -> list[ValidationResult]:
    """Validate entire .claude directory structure."""
    results = []
    claude_dir = path / ".claude"

    if not claude_dir.exists():
        results.append(ValidationResult(
            file_path=path,
            line_number=None,
            rule="claude-dir-exists",
            message=".claude directory does not exist",
            severity="error",
        ))
        return results

    # Check required files
    required_files = ["CLAUDE.md", "PLANNING.md", "TASK.md"]
    for filename in required_files:
        # Check both .claude/ and root
        claude_file = claude_dir / filename
        root_file = path / filename

        if not claude_file.exists() and not root_file.exists():
            results.append(ValidationResult(
                file_path=path,
                line_number=None,
                rule="required-file",
                message=f"Required file {filename} not found in .claude/ or project root",
                severity="error",
            ))
        else:
            # Validate the file that exists
            target = claude_file if claude_file.exists() else root_file
            content = target.read_text()

            if filename == "CLAUDE.md":
                results.extend(validate_claude_md(content, target))
            elif filename == "PLANNING.md":
                results.extend(validate_planning_md(content, target))
            elif filename == "TASK.md":
                results.extend(validate_task_md(content, target))

    return results
```

### Doctor Checks

```python
# packages/cli/src/echograph_cli/core/doctor.py
import shutil
import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DoctorCheck:
    """Result of a doctor check."""
    name: str
    passed: bool
    message: str
    fix_hint: str | None = None

def check_claude_cli() -> DoctorCheck:
    """Check if Claude Code CLI is available."""
    claude_path = shutil.which("claude")
    if claude_path:
        return DoctorCheck(
            name="Claude Code CLI",
            passed=True,
            message=f"Found at {claude_path}",
        )
    return DoctorCheck(
        name="Claude Code CLI",
        passed=False,
        message="'claude' command not found in PATH",
        fix_hint="Install Claude Code: https://docs.anthropic.com/claude-code/installation",
    )

def check_directory_structure(path: Path) -> DoctorCheck:
    """Check .claude directory structure."""
    claude_dir = path / ".claude"

    if not claude_dir.exists():
        return DoctorCheck(
            name="Directory Structure",
            passed=False,
            message=".claude directory not found",
            fix_hint="Run 'echograph init' to create the directory structure",
        )

    required = ["CLAUDE.md", "PLANNING.md", "TASK.md"]
    missing = [f for f in required if not (claude_dir / f).exists() and not (path / f).exists()]

    if missing:
        return DoctorCheck(
            name="Directory Structure",
            passed=False,
            message=f"Missing files: {', '.join(missing)}",
            fix_hint="Run 'echograph init' to create missing files",
        )

    return DoctorCheck(
        name="Directory Structure",
        passed=True,
        message="All required files present",
    )

def check_mcp_config(path: Path) -> DoctorCheck:
    """Check MCP configuration."""
    # Check project-level config first
    project_mcp = path / ".mcp.json"
    home_mcp = Path.home() / ".claude" / "mcp.json"

    if project_mcp.exists():
        try:
            json.loads(project_mcp.read_text())
            return DoctorCheck(
                name="MCP Configuration",
                passed=True,
                message=f"Project config found at {project_mcp}",
            )
        except json.JSONDecodeError:
            return DoctorCheck(
                name="MCP Configuration",
                passed=False,
                message=f"Invalid JSON in {project_mcp}",
                fix_hint="Fix JSON syntax errors in .mcp.json",
            )

    if home_mcp.exists():
        try:
            json.loads(home_mcp.read_text())
            return DoctorCheck(
                name="MCP Configuration",
                passed=True,
                message=f"Global config found at {home_mcp}",
            )
        except json.JSONDecodeError:
            return DoctorCheck(
                name="MCP Configuration",
                passed=False,
                message=f"Invalid JSON in {home_mcp}",
                fix_hint="Fix JSON syntax errors in ~/.claude/mcp.json",
            )

    return DoctorCheck(
        name="MCP Configuration",
        passed=True,
        message="No MCP config found (optional)",
    )

def check_git_repo(path: Path) -> DoctorCheck:
    """Check if project is a git repository."""
    git_dir = path / ".git"

    if git_dir.exists():
        return DoctorCheck(
            name="Git Repository",
            passed=True,
            message="Project is a git repository",
        )

    return DoctorCheck(
        name="Git Repository",
        passed=False,
        message="Project is not a git repository",
        fix_hint="Run 'git init' to initialize a repository (recommended)",
    )

def run_all_checks(path: Path) -> list[DoctorCheck]:
    """Run all doctor checks."""
    return [
        check_claude_cli(),
        check_directory_structure(path),
        check_mcp_config(path),
        check_git_repo(path),
    ]
```

### Rich Output Patterns

```python
# packages/cli/src/echograph_cli/output.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

console = Console()

def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green][bold]✓[/bold][/green] {message}")

def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red][bold]✗[/bold][/red] {message}")

def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow][bold]![/bold][/yellow] {message}")

def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue][bold]ℹ[/bold][/blue] {message}")

def print_doctor_results(checks: list) -> None:
    """Print doctor check results in a table."""
    table = Table(title="EchoGraph Doctor", show_header=True)
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    for check in checks:
        status = "[green]PASS[/green]" if check.passed else "[red]FAIL[/red]"
        details = check.message
        if check.fix_hint and not check.passed:
            details += f"\n[dim]{check.fix_hint}[/dim]"
        table.add_row(check.name, status, details)

    console.print(table)

def print_validation_results(results: list) -> None:
    """Print validation results."""
    if not results:
        print_success("All validation checks passed!")
        return

    errors = [r for r in results if r.severity == "error"]
    warnings = [r for r in results if r.severity == "warning"]

    if errors:
        console.print(Panel(
            "\n".join(f"[red]{r.file_path}:{r.line_number or 0}[/red] {r.message}"
                     for r in errors),
            title="[red]Errors[/red]",
            border_style="red",
        ))

    if warnings:
        console.print(Panel(
            "\n".join(f"[yellow]{r.file_path}:{r.line_number or 0}[/yellow] {r.message}"
                     for r in warnings),
            title="[yellow]Warnings[/yellow]",
            border_style="yellow",
        ))

def create_progress() -> Progress:
    """Create progress bar for file operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )
```

### pyproject.toml

```toml
# packages/cli/pyproject.toml
[project]
name = "echograph"
version = "0.1.0"
description = "Context Engineering CLI for Claude Code"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [
    {name = "EchoGraph Team"}
]
keywords = ["cli", "context-engineering", "claude", "ai", "developer-tools"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = [
    "typer>=0.12.0",
    "rich>=13.7.0",
    "jinja2>=3.1.0",
]

[project.scripts]
echograph = "echograph_cli.main:app"

[project.urls]
Homepage = "https://github.com/echograph/echograph"
Documentation = "https://echograph.dev/docs"
Repository = "https://github.com/echograph/echograph"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/echograph_cli"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]
target-version = "py311"

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=echograph_cli --cov-report=term-missing"
```

### Known Gotchas

1. **importlib.resources**: Use `resources.files()` pattern (Python 3.9+), not deprecated `resources.path()`
2. **Typer annotations**: Use `Annotated` from `typing_extensions` for compatibility
3. **Rich console**: Create single `Console()` instance and reuse; avoid creating in hot paths
4. **Jinja2 autoescape**: Disable for Markdown templates (not HTML)
5. **Path handling**: Use `pathlib.Path` throughout; Windows compatibility requires forward slashes in templates
6. **Template newlines**: Set `keep_trailing_newline=True` in Jinja2 to preserve file endings

### Related Files

**Will be created:**
- `packages/cli/pyproject.toml`
- `packages/cli/src/echograph_cli/__init__.py`
- `packages/cli/src/echograph_cli/main.py`
- `packages/cli/src/echograph_cli/commands/init.py`
- `packages/cli/src/echograph_cli/commands/update.py`
- `packages/cli/src/echograph_cli/commands/validate.py`
- `packages/cli/src/echograph_cli/commands/doctor.py`
- `packages/cli/src/echograph_cli/commands/placeholders.py`
- `packages/cli/src/echograph_cli/core/templates.py`
- `packages/cli/src/echograph_cli/core/merge.py`
- `packages/cli/src/echograph_cli/core/validation.py`
- `packages/cli/src/echograph_cli/core/doctor.py`
- `packages/cli/src/echograph_cli/output.py`
- `packages/cli/src/echograph_cli/templates/` (all bundled templates)
- `packages/cli/tests/` (all test files)

**Will be modified:**
- None (new package)

**Templates to bundle (from existing .claude/):**
- All files under `.claude/commands/`
- `.claude/tasks/README.md`
- `.claude/PLANNING.md` (as template base)
- `.claude/TASK.md` (as template base)
- `CLAUDE.md` (as template base)

## 5. Implementation Blueprint

### Step 1: Set Up Package Structure
- **What**: Create monorepo package structure for CLI
- **Files**:
  - `packages/cli/pyproject.toml` - Package configuration
  - `packages/cli/src/echograph_cli/__init__.py` - Package init with version
- **Validation**: `uv sync` succeeds

### Step 2: Implement Main CLI Entry Point
- **What**: Create Typer app with version flag and help
- **Files**:
  - `packages/cli/src/echograph_cli/main.py` - Main app
  - `packages/cli/src/echograph_cli/output.py` - Rich output helpers
- **Code Pattern**: See CLI Structure section above
- **Validation**: `uv run echograph --help` shows help

### Step 3: Bundle Templates
- **What**: Copy existing `.claude/` templates into package
- **Files**:
  - `packages/cli/src/echograph_cli/templates/.claude/` - All templates
  - `packages/cli/src/echograph_cli/core/templates.py` - Template loader
- **Code Pattern**: See Template Loading Pattern above
- **Validation**: `python -c "from echograph_cli.core.templates import list_templates; print(list_templates())"` lists files

### Step 4: Implement Init Command
- **What**: Scaffold `.claude/` directory with templates
- **Files**:
  - `packages/cli/src/echograph_cli/commands/init.py`
- **Logic**:
  1. Check if `.claude/` exists, prompt if so
  2. Detect project info (name from git/folder, tech stack)
  3. Render templates with Jinja2
  4. Write files with Rich progress display
- **Validation**: `uv run echograph init --minimal` creates 3 core files

### Step 5: Implement Update Command
- **What**: Update templates with three-way merge
- **Files**:
  - `packages/cli/src/echograph_cli/commands/update.py`
  - `packages/cli/src/echograph_cli/core/merge.py`
- **Logic**:
  1. Load original templates (from package metadata)
  2. Load user's current files
  3. Load new templates
  4. Three-way merge each file
  5. Report conflicts with resolution options
- **Validation**: `uv run echograph update` preserves user changes

### Step 6: Implement Validate Command
- **What**: Check context files for required fields
- **Files**:
  - `packages/cli/src/echograph_cli/commands/validate.py`
  - `packages/cli/src/echograph_cli/core/validation.py`
- **Logic**:
  1. Find all context files
  2. Apply validation rules
  3. Report errors and warnings with file:line references
- **Validation**: `uv run echograph validate` reports issues clearly

### Step 7: Implement Doctor Command
- **What**: Verify Claude Code setup
- **Files**:
  - `packages/cli/src/echograph_cli/commands/doctor.py`
  - `packages/cli/src/echograph_cli/core/doctor.py`
- **Logic**:
  1. Check Claude CLI availability
  2. Check directory structure
  3. Check MCP config
  4. Report results in table format
- **Validation**: `uv run echograph doctor` shows status table

### Step 8: Add Placeholder Commands
- **What**: Show "coming soon" for search/sync/decision
- **Files**:
  - `packages/cli/src/echograph_cli/commands/placeholders.py`
- **Validation**: `uv run echograph search` shows helpful message

### Step 9: Write Tests
- **What**: Unit and integration tests
- **Files**:
  - `packages/cli/tests/test_init.py`
  - `packages/cli/tests/test_update.py`
  - `packages/cli/tests/test_validate.py`
  - `packages/cli/tests/test_doctor.py`
  - `packages/cli/tests/test_merge.py`
  - `packages/cli/tests/conftest.py` - Fixtures
- **Validation**: `uv run pytest --cov` shows 80%+ coverage

## 6. Validation Loop

### Syntax/Style Check
```bash
uv run ruff check packages/cli/
uv run ruff format --check packages/cli/
uv run mypy packages/cli/src/
```

### Unit Tests
```bash
uv run pytest packages/cli/tests/ -v --cov=echograph_cli --cov-report=term-missing
```

### Integration Tests
```bash
# Test init in temp directory
cd $(mktemp -d) && echograph init --full && ls -la .claude/

# Test validate
cd /path/to/project && echograph validate

# Test doctor
echograph doctor
```

### Acceptance Testing
- [ ] User can install with `pip install echograph`
- [ ] `echograph init` creates complete `.claude/` structure
- [ ] `echograph init --minimal` creates only 3 core files
- [ ] `echograph update` merges without destroying customizations
- [ ] `echograph validate` catches missing required sections
- [ ] `echograph doctor` reports Claude CLI status correctly
- [ ] `echograph search` shows roadmap link
- [ ] Rich output is colorful and well-formatted

## 7. Confidence Score: 9/10

**High confidence because:**
- Clear requirements from feature request
- Standard library approach (Typer, Rich, Jinja2)
- Existing templates to bundle from `.claude/`
- Well-documented CLI patterns

**Minor uncertainties:**
- Three-way merge edge cases may need iteration
- Template variable detection for project config

---

**Generated**: 2025-11-27
**Feature Request**: `PRPs/feature-requests/context-engineering-cli.md`
