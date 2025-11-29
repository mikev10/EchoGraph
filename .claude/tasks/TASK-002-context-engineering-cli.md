# [TASK-002] Context Engineering CLI

**Status**: Complete
**PRP**: @PRPs/active/context-engineering-cli.md
**Parent Task**: References `.claude/TASK.md` entry for TASK-002
**Started**: 2025-11-27
**Phase 1 Completed**: 2025-01-28 (PyPI published)
**Phase 2 Completed**: 2025-11-28 (Commands/Skills bundled)

## Context

Build the foundational CLI that scaffolds Context Engineering workflows into projects. This is the first feature of EchoGraph, shipping before any search/embedding infrastructure. Provides immediate value to developers who want to set up Claude Code best practices.

**User Story**: As a developer, I want to run `echograph init` to set up Context Engineering in my project so that I have all the templates and commands needed for effective AI-assisted development.

## Subtasks

- [x] [TASK-002.1] Set up CLI package structure with Typer + Rich
- [x] [TASK-002.2] Implement `echograph init` command with --minimal and --full options
- [x] [TASK-002.3] Bundle templates with package using importlib.resources
- [x] [TASK-002.4] Implement `echograph update` with three-way merge
- [x] [TASK-002.5] Implement `echograph validate` command
- [x] [TASK-002.6] Implement `echograph doctor` command
- [x] [TASK-002.7] Add placeholder commands (search, sync, decision)
- [x] [TASK-002.8] Write unit and integration tests (80%+ coverage)
- [x] [TASK-002.9] Package and publish to PyPI

### Phase 2: Bundle Commands & Skills
- [x] [TASK-002.10] Bundle all slash commands from `.claude/commands/` into CLI package
- [x] [TASK-002.11] Bundle skills from `.claude/skills/` into CLI package
- [x] [TASK-002.12] Bundle `PRPs/` folder structure (templates, ai_docs)
- [x] [TASK-002.13] Add conflict detection before file creation
- [x] [TASK-002.14] Implement interactive conflict resolution (skip/overwrite/rename)
- [x] [TASK-002.15] Add `--dry-run` flag to preview what would be created
- [x] [TASK-002.16] Update tests for new bundled content
- [x] [TASK-002.17] Publish updated package to PyPI (v0.2.0)

## Progress

**Completion**: 17/17 subtasks complete (100%)

## Notes

### Design Decisions
- Using Typer + Rich for CLI (FastAPI-style type hints, beautiful output)
- Templates bundled via importlib.resources (safe, standard library)
- Three-way merge using difflib (standard library, no external deps)
- Jinja2 for template variable substitution

### Implementation Notes
- [2025-11-27] COMPLETED tasks 002.1-002.8: Full CLI implementation
- Package structure: `packages/cli/` with hatch build system
- Template files use .j2 extension for Jinja2 rendering
- Metadata stored in `.echograph-meta.json` for update tracking
- See completion summary in PRP: PRPs/active/context-engineering-cli.md
- [2025-11-28] COMPLETED tasks 002.10-002.16: Phase 2 bundling
  - Bundled 24 slash commands (6 categories: dev, maintenance, review, story, validation, workflow)
  - Bundled 3 skills (context-optimizer, research-gate, validation-enforcer)
  - Bundled PRPs structure with templates, examples, scripts
  - Added --dry-run flag for preview mode
  - Added interactive conflict resolution (skip/overwrite/rename)
  - Fixed UTF-8 encoding for Windows compatibility
  - All 55 tests passing with 84% coverage

### Dependencies
- **Requires**: None (first feature, ships standalone)
- **Blocks**: Search infrastructure features

### Related Resources
- Feature request: `PRPs/feature-requests/context-engineering-cli.md`
- Template source: Existing `.claude/` directory structure
- PLANNING.md architecture section for CLI positioning

## Testing Requirements

- [x] Unit tests for template rendering
- [x] Unit tests for three-way merge with conflict scenarios
- [x] Integration tests for init/update/validate/doctor commands
- [x] Test .gitignore detection and handling
- [x] Minimum 80% code coverage (84% achieved 2025-11-28)

## Documentation Updates

- [x] README.md with installation and usage
- [x] CLI help text for all commands
- [ ] Configuration options documentation

## Acceptance Criteria

1. `pip install echograph` works - ✅ Published 2025-01-28
2. `echograph --version` shows correct version - ✅
3. `echograph --help` shows all available commands - ✅
4. `echograph init` scaffolds `.claude/` in <5 seconds - ✅
5. `echograph init --minimal` creates only core files - ✅
6. `echograph init --full` creates complete directory structure - ✅ (2025-11-28)
7. `echograph update` preserves user customizations - ✅
8. `echograph validate` checks files and reports issues clearly - ✅
9. `echograph doctor` verifies Claude Code CLI, structure, MCP config - ✅
10. All tests pass with 80%+ coverage - ✅ (84% achieved 2025-11-28)

---

**Last Updated**: 2025-11-28
