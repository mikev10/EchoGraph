# [TASK-002] Context Engineering CLI

**Status**: Pending
**PRP**: @PRPs/active/context-engineering-cli.md
**Parent Task**: References `.claude/TASK.md` entry for TASK-002
**Started**: Not started
**Completed**: Not yet

## Context

Build the foundational CLI that scaffolds Context Engineering workflows into projects. This is the first feature of EchoGraph, shipping before any search/embedding infrastructure. Provides immediate value to developers who want to set up Claude Code best practices.

**User Story**: As a developer, I want to run `echograph init` to set up Context Engineering in my project so that I have all the templates and commands needed for effective AI-assisted development.

## Subtasks

- [ ] [TASK-002.1] Set up CLI package structure with Typer + Rich
- [ ] [TASK-002.2] Implement `echograph init` command with --minimal and --full options
- [ ] [TASK-002.3] Bundle templates with package using importlib.resources
- [ ] [TASK-002.4] Implement `echograph update` with three-way merge
- [ ] [TASK-002.5] Implement `echograph validate` command
- [ ] [TASK-002.6] Implement `echograph doctor` command
- [ ] [TASK-002.7] Add placeholder commands (search, sync, decision)
- [ ] [TASK-002.8] Write unit and integration tests (80%+ coverage)
- [ ] [TASK-002.9] Package and publish to PyPI

## Progress

**Completion**: 0/9 subtasks complete (0%)

## Notes

### Design Decisions
- Using Typer + Rich for CLI (FastAPI-style type hints, beautiful output)
- Templates bundled via importlib.resources (safe, standard library)
- Three-way merge using difflib (standard library, no external deps)
- Jinja2 for template variable substitution

### Dependencies
- **Requires**: None (first feature, ships standalone)
- **Blocks**: Search infrastructure features

### Related Resources
- Feature request: `PRPs/feature-requests/context-engineering-cli.md`
- Template source: Existing `.claude/` directory structure
- PLANNING.md architecture section for CLI positioning

## Testing Requirements

- [ ] Unit tests for template rendering
- [ ] Unit tests for three-way merge with conflict scenarios
- [ ] Integration tests for init/update/validate/doctor commands
- [ ] Test .gitignore detection and handling
- [ ] Minimum 80% code coverage

## Documentation Updates

- [ ] README.md with installation and usage
- [ ] CLI help text for all commands
- [ ] Configuration options documentation

## Acceptance Criteria

1. `pip install echograph` works
2. `echograph --version` shows correct version
3. `echograph --help` shows all available commands
4. `echograph init` scaffolds `.claude/` in <5 seconds
5. `echograph init --minimal` creates only core files
6. `echograph init --full` creates complete directory structure
7. `echograph update` preserves user customizations
8. `echograph validate` checks files and reports issues clearly
9. `echograph doctor` verifies Claude Code CLI, structure, MCP config
10. All tests pass with 80%+ coverage

---

**Last Updated**: 2025-11-27
