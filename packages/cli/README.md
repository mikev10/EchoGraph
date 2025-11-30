# EchoGraph CLI

Context Engineering CLI for Claude Code - scaffold, validate, and maintain your AI-assisted development workflow.

## Installation

```bash
pip install echograph
```

## Quick Start

```bash
# Navigate to your project
cd /path/to/your-project

# Initialize Context Engineering
echograph init

# Check your setup
echograph doctor

# Validate context files
echograph validate
```

## Commands

### `echograph init`

Scaffold Context Engineering templates for your project.

```bash
# Interactive mode (asks questions)
echograph init

# Minimal setup (core files only)
echograph init --minimal

# Full setup (all templates and commands)
echograph init --full

# Merge missing sections into existing CLAUDE.md
echograph init --merge

# Overwrite existing files
echograph init --force

# Preview without creating files
echograph init --dry-run

# Initialize a specific directory
echograph init /path/to/project
```

**Created files (minimal):**
- `CLAUDE.md` - Project conventions (at project root)
- `.claude/PLANNING.md` - Architecture and goals
- `.claude/TASK.md` - Task tracking

**Additional files (full):**
- `.claude/commands/` - Slash commands
- `.claude/skills/` - Custom skills
- `.claude/tasks/` - Feature task templates
- `PRPs/` - Product Requirement Prompts structure

**Using `--merge` with existing projects:**

If your project already has a `CLAUDE.md`, use `--merge` to add missing sections from the template without overwriting your existing content:

```bash
echograph init --merge
```

This will:
- Keep all your existing sections intact
- Add any sections from the template that you're missing (e.g., Response Optimization, Security Rules)
- Match sections case-insensitively (ignoring emojis)

### `echograph update`

Update templates while preserving your customizations using three-way merge.

```bash
# Update templates
echograph update

# Preview changes without modifying files
echograph update --dry-run
```

**How it works:**
1. Compares your current files with the original template version
2. Merges in new template changes
3. Preserves your customizations
4. Marks conflicts for manual resolution (if any)

### `echograph validate`

Check context files for completeness and valid references.

```bash
# Validate current directory
echograph validate

# Validate specific directory
echograph validate /path/to/project

# Treat warnings as errors
echograph validate --strict
```

**Checks performed:**
- Required files exist (CLAUDE.md at root, PLANNING.md and TASK.md in .claude/)
- `@` imports reference existing files
- CLAUDE.md has Project Context section
- TASK.md has required sections (In Progress, Pending, Completed)

### `echograph doctor`

Diagnose your Claude Code setup.

```bash
echograph doctor
```

**Checks performed:**
- Claude Code CLI is installed (`claude` command available)
- `.claude/` directory structure is correct
- MCP configuration is valid (if present)
- Project is a git repository
- Template version is current

## Configuration

The CLI auto-detects project configuration:

- **Project name**: From git remote or folder name
- **Tech stack**: From pyproject.toml, package.json, Cargo.toml, etc.
- **Test framework**: From pytest.ini, jest.config.js, etc.

Templates are customized based on detected configuration.

## Coming Soon

These commands show a "coming soon" message:

- `echograph search` - Semantic code search
- `echograph sync` - Sync external sources (GitHub, Azure DevOps)
- `echograph decision` - Track architectural decisions

## Development

```bash
# Clone the repository
git clone https://github.com/echograph/echograph
cd echograph

# Install dependencies
uv sync --all-packages

# Run tests
uv run pytest --cov

# Run linters
uv run ruff check packages/cli/
uv run mypy packages/cli/src/
```

## License

MIT
