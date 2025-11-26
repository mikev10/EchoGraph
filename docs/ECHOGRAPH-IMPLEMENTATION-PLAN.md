# EchoGraph Implementation Plan

> Complete plan for setting up the EchoGraph repository and creating Phase 1 feature requests.

**Purpose:** This document contains everything needed to bootstrap the EchoGraph project, including repo structure and all Phase 1 feature requests. It can be executed in a new session without prior context.

---

## Part 1: Repository Structure

### Create New Directory

```
C:\Users\Mike\OneDrive - EZFacility, Inc\R&D\EZProjects\EchoGraph\
```

### Full Directory Tree

```
echograph/
├── .github/
│   └── workflows/
│       ├── ci-python.yml
│       ├── ci-typescript.yml
│       └── release.yml
├── packages/
│   ├── cli/                          # Python CLI (echograph command)
│   │   ├── src/
│   │   │   └── echograph_cli/
│   │   │       ├── __init__.py
│   │   │       ├── main.py
│   │   │       ├── commands/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── search.py
│   │   │       │   ├── decision.py
│   │   │       │   ├── sync.py
│   │   │       │   └── init.py
│   │   │       └── config/
│   │   │           ├── __init__.py
│   │   │           └── settings.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   ├── core/                         # Python core library (shared logic)
│   │   ├── src/
│   │   │   └── echograph_core/
│   │   │       ├── __init__.py
│   │   │       ├── ingestion/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── base.py
│   │   │       │   ├── github.py
│   │   │       │   ├── azure_devops.py
│   │   │       │   └── filesystem.py
│   │   │       ├── processing/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── chunker.py
│   │   │       │   └── embedder.py
│   │   │       ├── retrieval/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── vector_search.py
│   │   │       │   ├── keyword_search.py
│   │   │       │   └── hybrid.py
│   │   │       ├── storage/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── sqlite.py
│   │   │       │   ├── chroma.py
│   │   │       │   └── models.py
│   │   │       └── decisions/
│   │   │           ├── __init__.py
│   │   │           └── manager.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   ├── api/                          # FastAPI service (Docker mode)
│   │   ├── src/
│   │   │   └── echograph_api/
│   │   │       ├── __init__.py
│   │   │       ├── main.py
│   │   │       ├── routes/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── search.py
│   │   │       │   ├── decisions.py
│   │   │       │   └── sync.py
│   │   │       └── dependencies.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   └── vscode-extension/             # VS Code extension (Phase 1 stretch)
│       ├── src/
│       │   ├── extension.ts
│       │   └── ...
│       ├── package.json
│       └── README.md
│
├── templates/                        # What `echograph init` scaffolds
│   ├── .claude/
│   │   ├── CLAUDE.md
│   │   ├── PLANNING.md
│   │   ├── TASK.md
│   │   └── commands/
│   │       ├── generate-prp.md
│   │       ├── execute-prp.md
│   │       └── ...
│   ├── PRPs/
│   │   └── .gitkeep
│   └── echograph.yaml.template
│
├── docker/
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── .env.example
│
├── docs/
│   ├── UNIFIED-VISION.md             # Copy from ContextEngineering
│   ├── IMPLEMENTATION-PLAN.md        # This file
│   └── api/
│       └── openapi.yaml
│
├── PRPs/                             # Feature requests for EchoGraph itself
│   └── phase1/
│       ├── BACKLOG.md                # Master tracking file
│       ├── 001-monorepo-setup/
│       │   └── INITIAL.md
│       ├── 002-cli-scaffold/
│       │   └── INITIAL.md
│       └── ... (all 24 features)
│
├── .gitignore
├── .editorconfig
├── turbo.json
├── pyproject.toml                    # Root Python config
├── pnpm-workspace.yaml
├── package.json                      # Root package.json for pnpm
├── README.md
└── LICENSE                           # Apache 2.0
```

---

## Part 2: Phase 1 Feature Requests

### Master Backlog (PRPs/phase1/BACKLOG.md)

Track all features, their status, and dependencies.

### Feature List with INITIAL.md Content

---

#### Feature 001: Monorepo Setup

**Path:** `PRPs/phase1/001-monorepo-setup/INITIAL.md`

```markdown
# Feature Request: Monorepo Setup

## Overview
Set up the EchoGraph monorepo with Turborepo, Poetry for Python packages, and pnpm for any TypeScript packages. This is the foundation for all other work.

## User Story
As a developer, I want a well-organized monorepo structure so that I can develop Python and TypeScript packages together with shared tooling.

## Requirements
- Initialize Turborepo configuration
- Set up Poetry for Python package management (packages/cli, packages/core, packages/api)
- Set up pnpm workspace for TypeScript packages (packages/vscode-extension)
- Configure shared linting (ruff for Python, eslint for TypeScript)
- Configure shared formatting (black for Python, prettier for TypeScript)
- Create root pyproject.toml with shared dev dependencies
- Create .gitignore, .editorconfig
- Set up basic GitHub Actions CI workflow

## Acceptance Criteria
- [ ] `pnpm install` works from root
- [ ] `poetry install` works in each Python package
- [ ] `turbo run lint` runs linters across all packages
- [ ] `turbo run test` runs tests across all packages
- [ ] CI workflow passes on GitHub

## Technical Notes
- Use Python 3.11+
- Use Node.js 20 LTS
- Use Turborepo 2.x
- Use Poetry 1.7+
- Use pnpm 8.x

## Dependencies
None - this is the first feature.

## Estimated Size
1 day
```

---

#### Feature 002: CLI Scaffold

**Path:** `PRPs/phase1/002-cli-scaffold/INITIAL.md`

```markdown
# Feature Request: CLI Scaffold

## Overview
Create the basic CLI structure using Click/Typer with placeholder commands.

## User Story
As a user, I want to run `echograph` commands so that I can interact with the EchoGraph system.

## Requirements
- Create packages/cli with Click/Typer setup
- Implement main entry point (`echograph`)
- Add placeholder commands: `init`, `search`, `decision`, `sync`, `status`
- Add --version and --help flags
- Add --server flag for Docker mode (placeholder)
- Create console output utilities using Rich
- Make installable via `pip install -e packages/cli`

## Acceptance Criteria
- [ ] `echograph --version` shows version
- [ ] `echograph --help` shows available commands
- [ ] `echograph init` runs (can be placeholder)
- [ ] `echograph search "test"` runs (can be placeholder)
- [ ] Rich formatting works for output

## Technical Notes
- Use Typer (built on Click) for CLI framework
- Use Rich for terminal formatting
- Entry point in pyproject.toml

## Dependencies
- Feature 001 (Monorepo Setup)

## Estimated Size
1 day
```

---

#### Feature 003: Configuration System

**Path:** `PRPs/phase1/003-configuration-system/INITIAL.md`

```markdown
# Feature Request: Configuration System

## Overview
Implement the configuration system that reads from echograph.yaml and environment variables.

## User Story
As a user, I want to configure EchoGraph via a YAML file so that I can customize behavior per project.

## Requirements
- Create echograph.yaml schema (Pydantic model)
- Support configuration for:
  - Data sources (GitHub repos, Azure DevOps, local paths)
  - Storage locations (database path, vector store path)
  - Embedding model settings
  - Server mode settings (host, port)
- Load from echograph.yaml in current directory or specified path
- Support environment variable overrides (ECHOGRAPH_*)
- Create `echograph init` command that generates echograph.yaml
- Validate configuration on load

## Acceptance Criteria
- [ ] `echograph init` creates echograph.yaml template
- [ ] Configuration loads from YAML file
- [ ] Environment variables override YAML values
- [ ] Invalid config shows helpful error messages
- [ ] Config is accessible throughout the application

## Technical Notes
- Use Pydantic for config validation
- Use pydantic-settings for env var support
- Store config in XDG-compliant locations for global settings

## Dependencies
- Feature 002 (CLI Scaffold)

## Estimated Size
1 day
```

---

#### Feature 004: Embedded Storage Setup

**Path:** `PRPs/phase1/004-embedded-storage/INITIAL.md`

```markdown
# Feature Request: Embedded Storage Setup

## Overview
Set up SQLite for metadata and Chroma for vectors in embedded mode (no Docker required).

## User Story
As a user, I want EchoGraph to work immediately after `pip install` without needing Docker.

## Requirements
- Create SQLAlchemy models for:
  - Documents (source, content, metadata, embedding_id)
  - Decisions (title, context, decision, rationale, status, links)
  - Sources (type, config, last_synced)
  - SyncHistory (source, timestamp, stats)
- Initialize SQLite database on first run
- Initialize Chroma in embedded/persistent mode
- Create storage abstraction layer (for future Postgres/Qdrant migration)
- Store data in ~/.echograph/ or project-local .echograph/
- Implement basic CRUD operations

## Acceptance Criteria
- [ ] Database initializes on first `echograph` command
- [ ] Documents can be stored and retrieved
- [ ] Vectors can be stored and retrieved via Chroma
- [ ] Data persists between runs
- [ ] Storage location is configurable

## Technical Notes
- SQLite via aiosqlite for async support
- Chroma 0.5+ in persistent mode
- Use Alembic for migrations (future-proofing)
- Storage interface should be swappable

## Dependencies
- Feature 003 (Configuration System)

## Estimated Size
2 days
```

---

#### Feature 005: Local File Ingestion

**Path:** `PRPs/phase1/005-local-file-ingestion/INITIAL.md`

```markdown
# Feature Request: Local File Ingestion

## Overview
Implement ingestion of local files from the filesystem into the knowledge graph.

## User Story
As a user, I want to index my local codebase so that I can search across my files.

## Requirements
- Walk directory tree respecting .gitignore patterns
- Filter by file extensions (configurable)
- Extract file content with metadata (path, size, modified date)
- Support common file types: .py, .ts, .js, .md, .txt, .json, .yaml
- Handle binary files gracefully (skip or extract text)
- Create Document records in storage
- Track file hashes for incremental updates
- Implement `echograph sync local` command

## Acceptance Criteria
- [ ] `echograph sync local ./src` indexes files
- [ ] .gitignore patterns are respected
- [ ] File metadata is captured
- [ ] Re-running only processes changed files
- [ ] Progress is shown during indexing

## Technical Notes
- Use pathspec for .gitignore parsing
- Use hashlib for file hashing
- Batch processing for large directories

## Dependencies
- Feature 004 (Embedded Storage)

## Estimated Size
2 days
```

---

#### Feature 006: Code Parsing with Tree-sitter

**Path:** `PRPs/phase1/006-code-parsing/INITIAL.md`

```markdown
# Feature Request: Code Parsing with Tree-sitter

## Overview
Use tree-sitter for syntax-aware parsing of code files to extract structure.

## User Story
As a user, I want code to be parsed intelligently so that searches understand code structure.

## Requirements
- Integrate tree-sitter for Python, TypeScript, JavaScript, C#, Go
- Extract code structure:
  - Functions/methods with signatures
  - Classes with methods
  - Imports/dependencies
  - Comments and docstrings
- Create structured metadata for each code element
- Preserve location information (file, line, column)
- Handle parsing errors gracefully

## Acceptance Criteria
- [ ] Python files parsed into functions/classes
- [ ] TypeScript/JavaScript files parsed correctly
- [ ] C# files parsed correctly
- [ ] Docstrings/comments extracted
- [ ] Location info preserved for jump-to-source

## Technical Notes
- Use tree-sitter-languages or py-tree-sitter
- Support top 5 languages initially, extensible design
- Cache parsed ASTs for performance

## Dependencies
- Feature 005 (Local File Ingestion)

## Estimated Size
2 days
```

---

#### Feature 007: Semantic Chunking

**Path:** `PRPs/phase1/007-semantic-chunking/INITIAL.md`

```markdown
# Feature Request: Semantic Chunking

## Overview
Implement intelligent chunking that respects code and document structure.

## User Story
As a user, I want code to be chunked at natural boundaries so that search results are meaningful.

## Requirements
- Chunk code at function/class boundaries (using tree-sitter output)
- Chunk markdown at heading boundaries
- Chunk plain text with overlap for context
- Configurable chunk sizes (default 512 tokens)
- Configurable overlap (default 50-100 tokens)
- Preserve metadata about chunk origin
- Handle very long functions (split with overlap)

## Acceptance Criteria
- [ ] Functions stay together when possible
- [ ] Classes chunk into logical pieces
- [ ] Markdown respects heading structure
- [ ] Chunks have consistent size range
- [ ] Chunk metadata traces back to source

## Technical Notes
- Use tiktoken for token counting
- Recursive chunking for oversized elements
- LangChain text splitters as reference

## Dependencies
- Feature 006 (Code Parsing)

## Estimated Size
2 days
```

---

#### Feature 008: Embedding Generation

**Path:** `PRPs/phase1/008-embedding-generation/INITIAL.md`

```markdown
# Feature Request: Embedding Generation

## Overview
Generate embeddings for chunks using Nomic embedding models.

## User Story
As a user, I want my code indexed with semantic embeddings so that I can search by meaning.

## Requirements
- Integrate Nomic Embed Text v1.5 via sentence-transformers
- Batch embedding generation for efficiency
- Store embeddings in Chroma with metadata
- Cache embeddings to avoid regeneration
- Support GPU acceleration when available
- Progress reporting during embedding

## Acceptance Criteria
- [ ] Embeddings generated for all chunks
- [ ] Batch processing works efficiently
- [ ] Embeddings stored in Chroma
- [ ] Re-indexing skips unchanged content
- [ ] Works on CPU (GPU optional)

## Technical Notes
- nomic-ai/nomic-embed-text-v1.5 (768 dimensions)
- Batch size 32 for efficiency
- ~50ms per batch on CPU

## Dependencies
- Feature 007 (Semantic Chunking)

## Estimated Size
2 days
```

---

#### Feature 009: GitHub Ingestion

**Path:** `PRPs/phase1/009-github-ingestion/INITIAL.md`

```markdown
# Feature Request: GitHub Ingestion

## Overview
Ingest code, PRs, issues, and commits from GitHub repositories.

## User Story
As a user, I want to index my GitHub repos so that I can search across code and discussions.

## Requirements
- Authenticate via GitHub Personal Access Token
- Clone/pull repository code
- Fetch PR metadata, descriptions, and comments
- Fetch issue metadata, descriptions, and comments
- Fetch commit messages and metadata
- Link PRs/issues to code changes
- Implement `echograph sync github` command
- Support incremental sync (only new content)

## Acceptance Criteria
- [ ] `echograph sync github owner/repo` works
- [ ] Code files are indexed
- [ ] PRs with comments are indexed
- [ ] Issues with comments are indexed
- [ ] Commit messages are indexed
- [ ] Incremental sync only fetches new data

## Technical Notes
- Use PyGithub for API access
- Use GitPython for repo cloning
- Respect rate limits (5000 req/hour)
- Store sync cursor for incremental updates

## Dependencies
- Feature 008 (Embedding Generation)

## Estimated Size
3 days
```

---

#### Feature 010: Azure DevOps Ingestion

**Path:** `PRPs/phase1/010-azure-devops-ingestion/INITIAL.md`

```markdown
# Feature Request: Azure DevOps Ingestion

## Overview
Ingest repos, work items, wiki, and pipelines from Azure DevOps.

## User Story
As a user, I want to index my Azure DevOps project so that I can search across all artifacts.

## Requirements
- Authenticate via Azure DevOps PAT
- Fetch repository code (Azure Repos)
- Fetch work items (user stories, tasks, bugs)
- Fetch wiki pages
- Fetch pipeline definitions and run summaries (stretch)
- Implement `echograph sync azuredevops` command
- Support incremental sync

## Acceptance Criteria
- [ ] `echograph sync azuredevops org/project` works
- [ ] Azure Repos code is indexed
- [ ] Work items with comments are indexed
- [ ] Wiki pages are indexed
- [ ] Incremental sync only fetches new data

## Technical Notes
- Use azure-devops Python package or REST API directly
- Organization + Project structure
- Handle pagination for large datasets

## Dependencies
- Feature 008 (Embedding Generation)

## Estimated Size
3 days
```

---

#### Feature 011: Background Sync Scheduler

**Path:** `PRPs/phase1/011-background-sync/INITIAL.md`

```markdown
# Feature Request: Background Sync Scheduler

## Overview
Implement scheduled background sync to keep the index up to date.

## User Story
As a user, I want EchoGraph to automatically sync periodically so my index stays current.

## Requirements
- Schedule periodic sync (configurable interval, default 30 min)
- Run sync in background without blocking CLI
- Support running as a daemon/service
- Log sync activity and errors
- Implement `echograph sync --watch` for continuous mode
- Respect rate limits across sync jobs

## Acceptance Criteria
- [ ] `echograph sync --watch` runs continuously
- [ ] Sync runs at configured intervals
- [ ] Sync errors are logged, don't crash daemon
- [ ] Multiple sources sync in sequence
- [ ] Can run as background service

## Technical Notes
- Use APScheduler for scheduling
- Consider using systemd/launchd for daemon mode
- Store last sync time per source

## Dependencies
- Feature 009 (GitHub Ingestion)
- Feature 010 (Azure DevOps Ingestion)

## Estimated Size
2 days
```

---

#### Feature 012: Vector Similarity Search

**Path:** `PRPs/phase1/012-vector-search/INITIAL.md`

```markdown
# Feature Request: Vector Similarity Search

## Overview
Implement semantic search using vector similarity in Chroma.

## User Story
As a user, I want to search using natural language and find semantically relevant results.

## Requirements
- Generate query embedding from search text
- Search Chroma for similar vectors
- Return top-k results with scores
- Include metadata in results (file, line, source)
- Support filtering by source type, date, language
- Format results for CLI display

## Acceptance Criteria
- [ ] `echograph search "authentication logic"` returns relevant code
- [ ] Results include file paths and snippets
- [ ] Results are ranked by relevance
- [ ] Filters narrow results appropriately
- [ ] Search completes in <500ms for typical queries

## Technical Notes
- Cosine similarity for matching
- Return top 20 candidates initially
- Display top 10 to user

## Dependencies
- Feature 008 (Embedding Generation)

## Estimated Size
2 days
```

---

#### Feature 013: BM25 Keyword Search

**Path:** `PRPs/phase1/013-keyword-search/INITIAL.md`

```markdown
# Feature Request: BM25 Keyword Search

## Overview
Implement keyword-based search using BM25 algorithm.

## User Story
As a user, I want exact keyword matches to surface in search results.

## Requirements
- Implement BM25 ranking algorithm
- Build inverted index from document content
- Support phrase matching
- Support boolean operators (AND, OR, NOT)
- Return top-k results with scores
- Index should update incrementally

## Acceptance Criteria
- [ ] Exact keyword matches are found
- [ ] Phrase matching works ("user authentication")
- [ ] Boolean queries work
- [ ] Results ranked by BM25 score
- [ ] Index updates on new documents

## Technical Notes
- Use rank-bm25 library or implement custom
- Store inverted index in SQLite
- Tokenize with same tokenizer as chunks

## Dependencies
- Feature 005 (Local File Ingestion)

## Estimated Size
1 day
```

---

#### Feature 014: Hybrid Retrieval

**Path:** `PRPs/phase1/014-hybrid-retrieval/INITIAL.md`

```markdown
# Feature Request: Hybrid Retrieval (RRF)

## Overview
Combine vector and keyword search using Reciprocal Rank Fusion.

## User Story
As a user, I want search to combine semantic and keyword matching for best results.

## Requirements
- Run vector search and BM25 search in parallel
- Combine results using RRF algorithm
- Deduplicate results from both sources
- Return merged, re-ranked results
- Make fusion parameters configurable

## Acceptance Criteria
- [ ] Search uses both vector and keyword methods
- [ ] Results are deduplicated
- [ ] RRF ranking produces good ordering
- [ ] Performance is acceptable (<1s total)
- [ ] Can configure blend ratio

## Technical Notes
- RRF formula: score = sum(1 / (k + rank_i))
- k = 60 is typical
- Run searches in parallel with asyncio

## Dependencies
- Feature 012 (Vector Search)
- Feature 013 (Keyword Search)

## Estimated Size
1 day
```

---

#### Feature 015: Search CLI Commands

**Path:** `PRPs/phase1/015-search-cli/INITIAL.md`

```markdown
# Feature Request: Search CLI Commands

## Overview
Implement the full search experience in the CLI.

## User Story
As a user, I want to search from the command line and see well-formatted results.

## Requirements
- `echograph search "query"` performs hybrid search
- Display results with syntax highlighting
- Show file path, line number, snippet
- Support output formats: table, json, simple
- Support filters: --type, --language, --since
- Open result in editor (--open flag)
- Paginate large result sets

## Acceptance Criteria
- [ ] Search command produces formatted output
- [ ] Syntax highlighting works for code
- [ ] Filters narrow results
- [ ] JSON output works for scripting
- [ ] Can open result in $EDITOR

## Technical Notes
- Use Rich for formatting
- Use Pygments for syntax highlighting
- Respect terminal width

## Dependencies
- Feature 014 (Hybrid Retrieval)

## Estimated Size
1 day
```

---

#### Feature 016: Decision Record Model

**Path:** `PRPs/phase1/016-decision-model/INITIAL.md`

```markdown
# Feature Request: Decision Record Model

## Overview
Create the data model for architectural decision records.

## User Story
As a user, I want to track architectural decisions with full context.

## Requirements
- Decision fields: title, context, decision, alternatives, rationale, status
- Status values: proposed, decided, deprecated, superseded
- Tags for categorization
- Links to documents (code files, PRs, issues, commits)
- Created/updated timestamps
- Author tracking
- Search indexing for decisions

## Acceptance Criteria
- [ ] Decision model created in SQLAlchemy
- [ ] All fields properly typed
- [ ] Links to other entities work
- [ ] Decisions are searchable
- [ ] Migrations handle schema

## Technical Notes
- Use SQLAlchemy relationships for links
- Index decision content for search
- Consider ADR (Architecture Decision Record) format

## Dependencies
- Feature 004 (Embedded Storage)

## Estimated Size
1 day
```

---

#### Feature 017: Decision CLI Commands

**Path:** `PRPs/phase1/017-decision-cli/INITIAL.md`

```markdown
# Feature Request: Decision CLI Commands

## Overview
Implement CLI commands for managing decision records.

## User Story
As a user, I want to create and manage decisions from the command line.

## Requirements
- `echograph decision create` - interactive or with flags
- `echograph decision list` - list all decisions
- `echograph decision show <id>` - show decision details
- `echograph decision search "query"` - search decisions
- `echograph decision update <id>` - update a decision
- `echograph decision link <id> <target>` - link to code/PR
- Export to markdown format

## Acceptance Criteria
- [ ] Can create decision interactively
- [ ] Can create decision with flags
- [ ] List shows summary table
- [ ] Search finds relevant decisions
- [ ] Export produces clean markdown

## Technical Notes
- Use Rich prompts for interactive mode
- Support piping for scripting
- Format similar to GitHub CLI

## Dependencies
- Feature 016 (Decision Model)

## Estimated Size
2 days
```

---

#### Feature 018: Decision Linking

**Path:** `PRPs/phase1/018-decision-linking/INITIAL.md`

```markdown
# Feature Request: Decision Linking

## Overview
Link decisions to code, PRs, commits, and other artifacts.

## User Story
As a user, I want to link decisions to the code they affect.

## Requirements
- Link decisions to file paths
- Link decisions to commit hashes
- Link decisions to PR/issue URLs
- Show links when displaying decision
- Show decisions when viewing code (reverse lookup)
- Auto-suggest links based on content similarity

## Acceptance Criteria
- [ ] Can link decision to file
- [ ] Can link decision to commit
- [ ] Can link decision to PR URL
- [ ] Links displayed with decision
- [ ] Reverse lookup works in search results

## Technical Notes
- Store links in junction table
- Support multiple link types
- URL validation for external links

## Dependencies
- Feature 017 (Decision CLI)

## Estimated Size
1 day
```

---

#### Feature 019: FastAPI Service

**Path:** `PRPs/phase1/019-fastapi-service/INITIAL.md`

```markdown
# Feature Request: FastAPI Service

## Overview
Create the FastAPI service that wraps core functionality for Docker mode.

## User Story
As a team, we want a server mode so multiple developers can share one index.

## Requirements
- FastAPI application with routes for:
  - POST /search - perform search
  - GET /decisions - list decisions
  - POST /decisions - create decision
  - POST /sync - trigger sync
  - GET /status - system status
- Async endpoints for performance
- Request/response validation with Pydantic
- OpenAPI documentation
- Health check endpoint
- CORS configuration

## Acceptance Criteria
- [ ] API starts with uvicorn
- [ ] All endpoints functional
- [ ] OpenAPI docs at /docs
- [ ] Health check at /health
- [ ] CORS allows configured origins

## Technical Notes
- Use FastAPI 0.115+
- Use Pydantic v2 for models
- Async throughout

## Dependencies
- Feature 015 (Search CLI)
- Feature 017 (Decision CLI)

## Estimated Size
2 days
```

---

#### Feature 020: Docker Compose Setup

**Path:** `PRPs/phase1/020-docker-compose/INITIAL.md`

```markdown
# Feature Request: Docker Compose Setup

## Overview
Create Docker Compose configuration for running EchoGraph as a service.

## User Story
As a team, we want to run EchoGraph with `docker compose up`.

## Requirements
- Dockerfile for API service (multi-stage build)
- docker-compose.yml with:
  - API service
  - Volume mounts for data persistence
  - Environment variable configuration
- docker-compose.dev.yml for development
- .env.example with all variables
- Health checks for startup ordering
- Documentation for deployment

## Acceptance Criteria
- [ ] `docker compose up` starts the service
- [ ] Data persists in volumes
- [ ] Environment variables configure behavior
- [ ] Health checks work
- [ ] Dev compose has hot reload

## Technical Notes
- Use python:3.11-slim base image
- Multi-stage build for small image
- Non-root user for security

## Dependencies
- Feature 019 (FastAPI Service)

## Estimated Size
1 day
```

---

#### Feature 021: CLI Server Mode

**Path:** `PRPs/phase1/021-cli-server-mode/INITIAL.md`

```markdown
# Feature Request: CLI Server Mode

## Overview
Add --server flag to CLI to use remote API instead of embedded mode.

## User Story
As a user, I want the CLI to work with a remote server.

## Requirements
- Add --server flag to CLI commands
- Store server URL in config
- HTTP client for API communication
- Same command interface, different backend
- Handle connection errors gracefully
- Support authentication (basic for now)

## Acceptance Criteria
- [ ] `echograph --server http://localhost:8000 search "query"` works
- [ ] Server URL can be set in config
- [ ] Connection errors show helpful message
- [ ] All commands work in server mode
- [ ] Auth header sent when configured

## Technical Notes
- Use httpx for async HTTP client
- Abstract storage/search behind interface
- Detect server mode from config or flag

## Dependencies
- Feature 019 (FastAPI Service)
- Feature 020 (Docker Compose)

## Estimated Size
1 day
```

---

#### Feature 022: Claude Code Slash Commands

**Path:** `PRPs/phase1/022-slash-commands/INITIAL.md`

```markdown
# Feature Request: Claude Code Slash Commands

## Overview
Create slash commands for Claude Code that integrate with EchoGraph.

## User Story
As a Claude Code user, I want to search EchoGraph using slash commands.

## Requirements
- /search-context - search EchoGraph and inject results
- /show-decision - display a decision record
- /create-decision - create a decision from conversation
- Commands work with local or server mode
- Results formatted for Claude Code context
- Document the commands in templates/

## Acceptance Criteria
- [ ] /search-context finds and injects results
- [ ] /show-decision displays formatted decision
- [ ] /create-decision creates record
- [ ] Commands documented
- [ ] Works in Claude Code environment

## Technical Notes
- Slash commands are markdown files in .claude/commands/
- Commands should invoke echograph CLI
- Format output for LLM consumption

## Dependencies
- Feature 015 (Search CLI)
- Feature 017 (Decision CLI)

## Estimated Size
2 days
```

---

#### Feature 023: CLAUDE.md Template

**Path:** `PRPs/phase1/023-claude-template/INITIAL.md`

```markdown
# Feature Request: CLAUDE.md Template

## Overview
Create the CLAUDE.md template that `echograph init` scaffolds into projects.

## User Story
As a user, I want EchoGraph to set up Claude Code integration automatically.

## Requirements
- CLAUDE.md template with:
  - Project context section
  - EchoGraph integration instructions
  - Search patterns and examples
  - Decision tracking workflow
- Supporting files (PLANNING.md, TASK.md)
- Slash commands for EchoGraph
- Template variables for project customization
- `echograph init` copies and customizes templates

## Acceptance Criteria
- [ ] `echograph init` creates .claude/ folder
- [ ] CLAUDE.md has project-specific values
- [ ] Slash commands are installed
- [ ] Documentation is clear
- [ ] Works with existing Claude Code projects

## Technical Notes
- Use Jinja2 for templating
- Detect existing .claude/ and merge
- Preserve user customizations on update

## Dependencies
- Feature 022 (Slash Commands)

## Estimated Size
1 day
```

---

#### Feature 024: VS Code Extension (Basic)

**Path:** `PRPs/phase1/024-vscode-extension/INITIAL.md`

```markdown
# Feature Request: VS Code Extension (Basic)

## Overview
Create a basic VS Code extension for searching EchoGraph.

## User Story
As a VS Code user, I want to search EchoGraph without leaving my editor.

## Requirements
- Extension with sidebar panel
- Search input with results display
- Click result to open file at line
- Show decision records
- Support server mode (configured URL)
- Basic syntax highlighting in results

## Acceptance Criteria
- [ ] Extension installs in VS Code
- [ ] Search panel in sidebar
- [ ] Results show with snippets
- [ ] Click opens file
- [ ] Decisions viewable

## Technical Notes
- TypeScript extension
- Use VS Code WebView for results
- HTTP client for API calls
- Keybinding for quick search (Ctrl+Shift+E)

## Dependencies
- Feature 019 (FastAPI Service)

## Estimated Size
3 days
```

---

## Part 3: Dependency Graph

```
001 Monorepo Setup
 └─► 002 CLI Scaffold
      └─► 003 Configuration System
           └─► 004 Embedded Storage
                ├─► 005 Local File Ingestion
                │    └─► 006 Code Parsing
                │         └─► 007 Semantic Chunking
                │              └─► 008 Embedding Generation
                │                   ├─► 009 GitHub Ingestion ─────┐
                │                   ├─► 010 Azure DevOps Ingestion┤
                │                   │                              │
                │                   └─► 012 Vector Search          │
                │                                                  │
                └─► 013 BM25 Keyword Search                       │
                     │                                             │
                     └─► 014 Hybrid Retrieval ◄────────────────────┤
                          │                                        │
                          └─► 015 Search CLI ◄─────────────────────┤
                               │                                   │
                ├─► 016 Decision Model                             │
                │    └─► 017 Decision CLI                          │
                │         └─► 018 Decision Linking                 │
                │                                                  │
                └─────────────────┬─────────────────────────────────┘
                                  │
                                  ▼
                          011 Background Sync
                                  │
                          019 FastAPI Service
                           ├─► 020 Docker Compose
                           │    └─► 021 CLI Server Mode
                           │
                           └─► 024 VS Code Extension

                015 + 017 ─► 022 Slash Commands
                              └─► 023 CLAUDE.md Template
```

---

## Part 4: Execution Order

### Wave 1: Foundation (Week 1)
1. 001 - Monorepo Setup
2. 002 - CLI Scaffold
3. 003 - Configuration System
4. 004 - Embedded Storage

### Wave 2: Ingestion Pipeline (Week 2-3)
5. 005 - Local File Ingestion
6. 006 - Code Parsing
7. 007 - Semantic Chunking
8. 008 - Embedding Generation

### Wave 3: Data Sources (Week 3-4)
9. 009 - GitHub Ingestion
10. 010 - Azure DevOps Ingestion
11. 013 - BM25 Keyword Search (can parallel with 009/010)

### Wave 4: Search (Week 4-5)
12. 012 - Vector Search
13. 014 - Hybrid Retrieval
14. 015 - Search CLI

### Wave 5: Decisions (Week 5)
15. 016 - Decision Model
16. 017 - Decision CLI
17. 018 - Decision Linking

### Wave 6: Server Mode (Week 6)
18. 019 - FastAPI Service
19. 020 - Docker Compose
20. 021 - CLI Server Mode
21. 011 - Background Sync

### Wave 7: Integration (Week 7)
22. 022 - Slash Commands
23. 023 - CLAUDE.md Template
24. 024 - VS Code Extension

---

## Part 5: Next Steps

1. **Create the EchoGraph directory** at the specified path
2. **Create the directory structure** as outlined above
3. **Create each INITIAL.md file** from the content in this document
4. **Create BACKLOG.md** to track progress
5. **Copy UNIFIED-VISION.md** from ContextEngineering
6. **Initialize git** and create first commit
7. **Begin Feature 001** - Monorepo Setup

---

*This plan can be executed in a new Claude Code session without prior context.*
