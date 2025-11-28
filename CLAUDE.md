# EchoGraph - Global Conventions

## Project Context (Auto-Loaded)

@.claude/PLANNING.md
@.claude/TASK.md

## Response Optimization (MANDATORY)

**Context is precious. Every token matters.**

- **Never repeat content back** - Don't paste code/content after editing. Say what changed, not the full result.
- **No code unless asked** - Reference `file:line` instead. User can read files if needed.
- **Concise by default** - "Done. Fixed X." not "I have successfully completed the task..."
- **Don't narrate** - Don't explain what you're about to do. Just do it.
- **No preamble** - Skip "Great question!" or restating the question.
- **Verbose only when**: User asks for explanation, complex tradeoffs exist, or debugging needs evidence.
- **Edit responses**: "Fixed `file.py:23` - added null check" (1 line, no code paste)
- **Multi-step tasks**: Use TodoWrite for tracking. Final summary: bullet points only.

## Mandatory MCP Server Rules

**When working with libraries or documentation:**

1. **context7 MCP server** - ALWAYS use for library documentation lookups
   - First call `mcp__context7__resolve-library-id` to get the library ID
   - Then call `mcp__context7__get-library-docs` with topic for specific docs
   - Never guess library APIs - always verify with context7

2. **local-rag MCP server** - Use for project-specific documentation
   - Query `mcp__local-rag__query_documents` for project patterns
   - Ingest important docs with `mcp__local-rag__ingest_file`

3. **perplexity MCP server** - Use for current/recent information
   - `mcp__perplexity__search` for quick lookups
   - `mcp__perplexity__reason` for complex technical questions

**Planning Rule**: When planning features involving libraries:
- Use context7 to verify current API patterns
- Check local-rag for existing project patterns
- Never assume library behavior - verify first

**Implementation Rule**: When implementing with external libraries:
- First call context7 to see correct usage patterns
- Reference verified patterns, not memory
- Update PRPs/ai_docs/ with key findings for future reference

## Project Awareness

**Before starting ANY work:**
- Review `examples/` folder for established patterns (when available)
- Consult `PRPs/ai_docs/` for library-specific documentation
- Reference `docs/ECHOGRAPH-IMPLEMENTATION-PLAN.md` or  `D:\Obsidian\Knowledge Base\echograph\TECHNOLOGY-INVENTORY.md` for validated tool choices
- Reference `D:\Obsidian\Knowledge Base\echograph\ECHOGRAPH-IMPLEMENTATION-PLAN.md` for feature details

**Note:** Architecture (PLANNING.md) and current priorities (TASK.md) are auto-loaded via imports above.

## Code Structure

**File Organization:**
- Keep files under 300 lines; split when exceeded
- Monorepo structure: `packages/{cli,core,api,vscode-extension}/`
- Each package contains: `src/`, `tests/`, `pyproject.toml`
- Separate concerns: CLI commands, core logic, storage, retrieval

**Naming Conventions:**
- Files: `snake_case.py` (e.g., `vector_search.py`, `github_ingestion.py`)
- Classes: `PascalCase` (e.g., `EmbeddingService`, `VectorStore`)
- Functions/variables: `snake_case` (e.g., `generate_embeddings`, `search_results`)
- Constants: `SCREAMING_SNAKE_CASE` (e.g., `DEFAULT_CHUNK_SIZE`, `API_BASE_URL`)
- Types: `PascalCase` (e.g., `SearchResult`, `DecisionRecord`)

**Import Order:**
1. Standard library (os, pathlib, typing)
2. Third-party dependencies (fastapi, pydantic, lancedb)
3. Internal absolute imports (echograph_core, echograph_cli)
4. Relative imports (./models, ../utils)
5. Type imports (from typing import TYPE_CHECKING)

## Tech Stack Patterns

**uv (Package Manager):**
- Use `uv sync` to install dependencies
- Use `uv run pytest` to run tests
- Use `uv add <package>` to add dependencies
- Lock file: `uv.lock` (committed to git)

**Typer (CLI Framework):**
- Use type hints for all arguments/options
- Use Rich for formatted output
- Use `typer.Typer()` with `add_completion=False`
- Commands in separate files under `commands/`

**FastAPI (API Service):**
- Async endpoints throughout
- Pydantic v2 models for request/response
- Use lifespan context manager for startup/shutdown
- OpenAPI docs at `/docs`

**LanceDB (Vector Store):**
- Connect with `lancedb.connect(path)`
- Create tables with schema from dataclass or dict
- Use `.search(vector).limit(k).to_pandas()` for queries
- Store metadata columns for filtering

**SQLAlchemy 2.0 (Metadata Store):**
- Use async sessions with aiosqlite
- Define models with `DeclarativeBase`
- Use Alembic for migrations

## Testing Requirements

**Test Coverage:**
- Minimum 80% coverage for core library
- Test files: `test_{filename}.py`
- Test location: `packages/{package}/tests/`

**Test Structure:**

```python
class TestEmbeddingService:
    """Tests for EmbeddingService class."""

    def test_encode_single_text(self):
        """Should generate embedding for single text."""
        # Arrange
        service = EmbeddingService()
        text = "test input"

        # Act
        result = service.encode_single(text)

        # Assert
        assert result.shape == (768,)

    def test_encode_empty_list(self):
        """Should return empty array for empty input."""
        # Arrange / Act / Assert pattern
```

**Test Patterns:**
- Unit tests: pytest with pytest-asyncio for async
- Integration tests: pytest with fixtures for database/vector store
- Use `pytest-cov` for coverage reporting

## Security Rules (CRITICAL)

**Token Storage:**
- Store PATs in system keyring or environment variables
- NEVER commit tokens to git
- NEVER log token values
- Use `ECHOGRAPH_GITHUB_TOKEN` env var pattern

**API Calls:**
- Use httpx for async HTTP client
- Always set timeouts on requests
- Handle rate limits gracefully (GitHub: 5000 req/hour)
- Validate URLs before making requests

**Input Validation:**
- Validate all user input with Pydantic
- Sanitize file paths (no path traversal)
- Validate on CLI entry and API boundary

## Style & Formatting

**Code Style:**
- Formatter: Ruff format (line-length 88)
- Linter: Ruff (select = ["E", "F", "I", "N", "W", "UP"])
- Type checker: mypy (strict mode)
- Max line length: 88 characters

**Comments:**
- Comment WHY, not WHAT
- Use docstrings for public functions (Google style)
- Use inline comments for non-obvious logic

**Docstring Format:**
```python
def search(query: str, top_k: int = 10) -> list[SearchResult]:
    """Search for documents matching the query.

    Args:
        query: Natural language search query
        top_k: Maximum number of results to return

    Returns:
        List of search results ranked by relevance

    Raises:
        ValueError: If query is empty
    """
```

## Documentation Requirements

**When to Update Docs:**
- New command added: Update README and CLI help
- New pattern established: Add to `examples/`
- Architecture change: Update `.claude/PLANNING.md`
- New dependency: Document in `PRPs/ai_docs/`

## Task Management

**Three-Level Task System:**

**Level 1: Master TASK.md** - Epic/feature tracking
**Level 2: Feature Task Files** - `.claude/tasks/TASK-XXX-*.md`
**Level 3: TodoWrite** - Session-level granular tasks

See `.claude/tasks/README.md` for full documentation.

## Validation Commands (Must Pass Before Committing)

```bash
# Lint all Python code (must pass with no errors)
uv run ruff check .

# Format check (must have no changes needed)
uv run ruff format --check .

# Type check (must pass)
uv run mypy packages/

# Run tests (must pass)
uv run pytest
```

## Critical Gotchas

**uv:**
- Always use `uv run` to execute commands in the virtual environment
- `uv.lock` must be committed - it's the lockfile
- Use `uv sync --frozen` in CI to ensure reproducible builds

**LanceDB:**
- Tables are created lazily - first insert creates the table
- Vector column must be named `vector` by convention
- Use `.where()` for SQL-like metadata filtering

**tree-sitter:**
- Parser objects are not thread-safe
- Create parser per-thread or use locks
- Language bindings must match tree-sitter version

**Embeddings:**
- First call loads model (~500MB download)
- Batch processing (32 items) is much faster than single
- Nomic requires `trust_remote_code=True`

## Skills

**context-optimizer** (Auto-triggered for complex tasks):
- Enforces Response Optimization rules above
- Uses subagents for parallelizable work (context isolation)
- Summary-first reporting - bullet points, not prose
- Progressive file reading: Grep → Read relevant sections → Delegate if large
- See `.claude/skills/context-optimizer/SKILL.md` for full details

## What NOT to Do

- Use `any` type without strong justification
- Store tokens in config files
- Skip tests for "simple" features
- Use `print()` instead of logging/Rich console
- Commit without running validation commands
- Delete code without explicit instruction
- Assume library availability without checking
- Use `os.system()` or `subprocess.call()` without shell=False
- Ignore rate limits on external APIs
- Paste code back after editing (use file:line references)
- Narrate what you're about to do (just do it)
- Write verbose success messages ("I have successfully...")

## What to ALWAYS Do

- Run validation commands before committing
- Write tests for new features
- Validate inputs at boundaries
- Handle errors gracefully with user-friendly messages
- Update TASK.md with progress
- Reference PLANNING.md for architectural decisions
- Ask for clarification if requirements unclear
- Use Rich console for CLI output
- Use async/await for I/O operations
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Use MCP servers (context7, local-rag) before implementing with libraries
- Keep responses concise - context is precious
