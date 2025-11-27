# Feature Request - Context Engineering CLI

## FEATURE

Create the foundational CLI that scaffolds Context Engineering workflows into projects. This ships before any search/embedding infrastructure, providing immediate value to developers who want to set up Claude Code best practices in their projects.

### User Stories

- As a developer, I want to run `echograph init` to set up Context Engineering in my project without needing the full EchoGraph search stack
- As a developer, I want to choose between minimal and full setup options based on my project needs
- As a developer, I want to update my templates when new versions are released while preserving my customizations
- As a developer, I want to validate my context files to ensure they follow best practices
- As a developer, I want to verify my Claude Code setup is configured correctly

### Key Requirements

1. **CLI Framework**: Basic CLI with Typer + Rich for beautiful terminal output
2. **Init Command**: `echograph init` scaffolds `.claude/` directory with templates
3. **Init Options**: `--minimal` for basic setup, `--full` for complete setup with examples
4. **Update Command**: `echograph update` updates templates via three-way merge (preserving customizations)
5. **Validate Command**: `echograph validate` checks context files for required fields and structure
6. **Doctor Command**: `echograph doctor` verifies Claude Code CLI, `.claude/` structure, MCP config
7. **Bundled Templates**: All templates from ContextEngineering repo bundled in package
8. **Placeholder Commands**: search/sync/decision commands show "coming soon" with roadmap link

## EXAMPLES

### Example CLI Structure

```python
# packages/cli/src/echograph_cli/main.py
import typer
from rich.console import Console

app = typer.Typer(
    name="echograph",
    help="EchoGraph - Context Engineering for Claude Code",
    add_completion=False,
)
console = Console()

@app.command()
def init(
    path: Path = typer.Argument(Path("."), help="Project directory"),
    minimal: bool = typer.Option(False, "--minimal", "-m", help="Minimal setup"),
    full: bool = typer.Option(False, "--full", "-f", help="Full setup with examples"),
) -> None:
    """Initialize Context Engineering in your project."""
    pass

@app.command()
def update(
    path: Path = typer.Argument(Path("."), help="Project directory"),
) -> None:
    """Update templates while preserving customizations."""
    pass

@app.command()
def validate(
    path: Path = typer.Argument(Path("."), help="Project directory"),
) -> None:
    """Validate context files for completeness."""
    pass

@app.command()
def doctor() -> None:
    """Verify Claude Code setup and configuration."""
    pass
```

### Example Template Structure

```
templates/
├── .claude/
│   ├── CLAUDE.md
│   ├── PLANNING.md
│   ├── TASK.md
│   ├── commands/
│   │   ├── workflow/
│   │   │   ├── generate-prp.md
│   │   │   ├── execute-prp.md
│   │   │   ├── archive-prp.md
│   │   │   └── create-feature-request.md
│   │   ├── review/
│   │   │   ├── review-staged.md
│   │   │   ├── review-general.md
│   │   │   └── create-pr.md
│   │   ├── dev/
│   │   │   ├── debug.md
│   │   │   ├── planning-create.md
│   │   │   ├── onboarding.md
│   │   │   └── refactor-simple.md
│   │   ├── story/
│   │   │   ├── write-user-story.md
│   │   │   ├── refine-story.md
│   │   │   ├── convert-story.md
│   │   │   ├── enrich-story-tech.md
│   │   │   ├── enrich-story-qa.md
│   │   │   ├── validate-story-ready.md
│   │   │   └── three-amigos-prep.md
│   │   ├── validation/
│   │   │   ├── validate-context.md
│   │   │   └── validate-tasks.md
│   │   └── maintenance/
│   │       ├── update-rag.md
│   │       ├── research.md
│   │       └── prime-core.md
│   ├── tasks/
│   │   └── README.md
│   └── templates/
│       ├── prp-template.md
│       └── story-to-initial.md
└── PRPs/
    └── .gitkeep
```

### Example Jinja2 Template Variable Usage

```markdown
# {{ project_name }} - Context Engineering

## Project Context

@.claude/PLANNING.md
@.claude/TASK.md

## Tech Stack

{% if tech_stack %}
{% for tech in tech_stack %}
- {{ tech }}
{% endfor %}
{% else %}
- (Configure your tech stack here)
{% endif %}
```

### Example Three-Way Merge for Updates

```python
# packages/cli/src/echograph_cli/commands/update.py
from difflib import unified_diff
from pathlib import Path

def three_way_merge(
    original: str,  # Original template (from previous version)
    modified: str,  # User's modified version
    updated: str,   # New template version
) -> tuple[str, list[str]]:
    """
    Perform three-way merge preserving user customizations.

    Returns:
        Tuple of (merged_content, list_of_conflicts)
    """
    # Implementation using diff3-style merge
    pass
```

## DOCUMENTATION

### Relevant Libraries/Frameworks

- **Typer**: CLI framework built on Click with type hints
- **Rich**: Terminal formatting, tables, progress bars, syntax highlighting
- **Jinja2**: Template engine for variable substitution
- **importlib.resources**: Bundle templates with Python package

### CLI Commands

| Command | Description |
|---------|-------------|
| `echograph init` | Scaffold `.claude/` directory |
| `echograph init --minimal` | Basic setup (CLAUDE.md, PLANNING.md, TASK.md) |
| `echograph init --full` | Full setup with all commands and examples |
| `echograph update` | Update templates preserving customizations |
| `echograph validate` | Check context files for required fields |
| `echograph doctor` | Verify Claude Code CLI and MCP config |
| `echograph search` | (Placeholder) "Coming soon" message |
| `echograph sync` | (Placeholder) "Coming soon" message |
| `echograph decision` | (Placeholder) "Coming soon" message |

### References

- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Python Packaging Guide](https://packaging.python.org/)

## OTHER CONSIDERATIONS

### Security

- No sensitive data in templates (no tokens, secrets, or credentials)
- Validate file paths to prevent path traversal attacks
- Use `importlib.resources` for safe template access

### Performance

- Template scaffolding should complete in <5 seconds
- Use lazy loading for optional features
- First run may download model for validation (~500MB) - document this

### Testing

- Unit tests for template rendering with various configurations
- Integration tests for init/update/validate commands
- Test three-way merge with various conflict scenarios
- Test .gitignore detection and handling
- Minimum 80% code coverage

### Distribution

- Publish to PyPI as `echograph` package
- Support Python 3.11+
- Single package (no monorepo dependencies yet)
- Entry point: `echograph` command

### Validation Rules (for `echograph validate`)

1. **CLAUDE.md**: Must exist, must have project context section
2. **PLANNING.md**: Must exist, should have goals and architecture
3. **TASK.md**: Must exist, should have current priorities
4. **Commands**: Validate markdown syntax in slash commands
5. **Imports**: Check that `@` references point to existing files

### Doctor Checks (for `echograph doctor`)

1. **Claude Code CLI**: Check if `claude` command is available
2. **Directory Structure**: Verify `.claude/` exists and has required files
3. **MCP Config**: Check `~/.claude/mcp.json` or project-level MCP config
4. **Git Integration**: Verify project is a git repository (recommended)
5. **Template Version**: Report current template version vs latest

## DEPENDENCIES

None - this is the first feature. Ships standalone before monorepo setup.

## ACCEPTANCE CRITERIA

- [ ] `pip install echograph` works from PyPI (or test PyPI initially)
- [ ] `echograph --version` shows correct version
- [ ] `echograph --help` shows all available commands
- [ ] `echograph init` scaffolds `.claude/` in <5 seconds
- [ ] `echograph init --minimal` creates only core files (CLAUDE.md, PLANNING.md, TASK.md)
- [ ] `echograph init --full` creates complete directory structure with all commands
- [ ] `echograph update` preserves user customizations via three-way merge
- [ ] `echograph validate` checks file structure and required fields, reports issues clearly
- [ ] `echograph doctor` verifies Claude Code CLI, `.claude/` structure, MCP config
- [ ] Placeholder commands (search, sync, decision) show helpful "coming soon" messages with roadmap link
- [ ] Rich formatting produces beautiful terminal output
- [ ] All tests pass with 80%+ coverage
