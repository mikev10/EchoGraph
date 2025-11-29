# AI Documentation

This directory stores library-specific documentation that provides AI context during implementation.

## Purpose

When implementing features with external libraries, Claude needs accurate, up-to-date information about APIs and patterns. This directory serves as a local cache of verified documentation.

## Workflow

### Adding Documentation

1. **During Research**: When using `/maintenance:research`, findings are documented here
2. **During Implementation**: Key patterns discovered are captured for future reference
3. **Manual Addition**: Developers can add important library docs

### Using Documentation

1. Claude checks this directory before implementing with libraries
2. `local-rag` MCP server indexes these files for semantic search
3. Patterns here take precedence over Claude's training data

## File Naming Convention

```
{library-name}.md
{library-name}-{topic}.md
```

Examples:
- `lancedb.md` - General LanceDB documentation
- `lancedb-vector-search.md` - Specific topic
- `typer-commands.md` - Typer CLI patterns
- `sentence-transformers.md` - Embedding library

## Document Structure

```markdown
# {Library Name}

**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Source**: [Official Docs](https://...)

## Overview
[Brief description of what this library does]

## Installation
[How to install/configure]

## Common Patterns

### Pattern 1: [Name]
[Code example with explanation]

### Pattern 2: [Name]
[Code example with explanation]

## Project-Specific Usage
[How we use this library in EchoGraph]

## Gotchas
[Known issues, quirks, or things to watch out for]

## References
- [Link to official docs]
- [Link to relevant examples]
```

## Integration with MCP Servers

### local-rag
Files in this directory are indexed by `local-rag` MCP server. Use:
```
mcp__local-rag__query_documents("lancedb vector search")
```

### context7
For latest library documentation not cached here, use context7:
```
mcp__context7__resolve-library-id("lancedb")
mcp__context7__get-library-docs({libraryId}, {topic: "vector search"})
```

## Knowledge Priority

When implementing with libraries, Claude follows this priority:

1. **local-rag** - Project-specific patterns from this directory
2. **PRPs/ai_docs/** - Library documentation (this folder)
3. **context7** - Official library documentation
4. **perplexity** - Current/recent information (gated)

## Maintenance

### Adding New Docs
```bash
# After researching a library
/maintenance:research {library-name}

# Or manually create
echo "# Library Name" > PRPs/ai_docs/{library}.md
```

### Updating Existing Docs
When library versions change or new patterns are discovered, update the relevant file and change the "Last Updated" date.

### Ingesting to local-rag
```bash
/maintenance:reingest-queue
# Or use mcp__local-rag__ingest_file directly
```

## See Also

- `/maintenance:research` - Research workflow command
- `/maintenance:update-rag` - Update local-rag with new docs
- `CLAUDE.md` - MCP server usage rules
