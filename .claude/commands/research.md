---
description: Comprehensive multi-source research workflow
---

# Multi-Source Research Command

Conducts systematic research by combining project context, library documentation, and external best practices.

**Input**: A specific research question or topic

---

## Research Process

### Phase 1: Query Project Documentation

**Search for existing patterns and context within the project:**

**MCP Server Strategy (PREFERRED - Use First):**

1. **Use local-rag to query project documentation** (FASTEST):
   ```javascript
   // Search for similar implementations
   mcp__local-rag__query_documents({
     query: "[feature/topic] implementation patterns examples",
     limit: 5
   })

   // Query style guide and conventions
   mcp__local-rag__query_documents({
     query: "design patterns conventions for [topic]",
     limit: 3
   })

   // Query API endpoints (if applicable)
   mcp__local-rag__query_documents({
     query: "[feature] API endpoints request response schema",
     limit: 5
   })

   // Find library usage patterns
   mcp__local-rag__query_documents({
     query: "[library name] usage patterns configuration",
     limit: 3
   })
   ```

**Traditional Search (if local-rag doesn't have indexed docs):**
- Use Grep tool to search for relevant code patterns
- Use Glob tool to find similar files
- Read example implementations in `examples/`
- Check `PRPs/ai_docs/` for library-specific guidance
- Review `.claude/PLANNING.md` for architecture context

**Example queries:**
- "How is data persistence implemented?"
- "What UI components are used for forms?"
- "API endpoints and their request/response formats"

---

### Phase 2: Fetch Library Documentation

**Get up-to-date documentation for relevant libraries:**

**MCP Server Strategy (PREFERRED - Most Accurate):**

1. **Use context7 for library documentation** (RECOMMENDED):
   ```javascript
   // Step 1: Resolve library name to Context7 ID
   mcp__context7__resolve-library-id({
     libraryName: "[library name]"  // e.g., "next.js", "react-query"
   })
   // Returns: Context7-compatible library ID (e.g., "/vercel/next.js")

   // Step 2: Fetch focused documentation
   mcp__context7__get-library-docs({
     context7CompatibleLibraryID: "/org/project",
     topic: "[specific topic]",  // e.g., "server actions", "middleware"
     tokens: 5000-7000
   })
   // Returns: Accurate, up-to-date API signatures and examples
   ```

**Alternative Sources (if context7 unavailable):**
- Use WebFetch for official documentation pages
- Check `PRPs/ai_docs/` for curated library guides
- Access GitHub repositories (README, docs folder)
- Review npm package documentation

**When to use context7:**
- Verifying current API signatures (prevents hallucinations!)
- Understanding best practices for a library
- Checking for breaking changes or deprecations
- Getting official, tested examples
- Understanding advanced features and patterns

**Example topics:**
- "server actions and data mutations"
- "app router and navigation patterns"
- "state management and persistence"
- "authentication and authorization"

---

### Phase 3: External Research

**Research beyond project and library documentation:**

**MCP Server Strategy (PREFERRED - Most Comprehensive):**

1. **Use perplexity for quick research** (RECOMMENDED):
   ```javascript
   // For straightforward questions
   mcp__perplexity__search({
     query: "How to implement [feature] in [tech stack]?
            Include: [specific requirements]
            Environment: [versions, dependencies]"
   })
   ```

2. **Use perplexity reasoning for complex analysis**:
   ```javascript
   mcp__perplexity__reason({
     query: "How to implement [feature] in [tech stack]?
            Consider: [requirements, constraints]
            Environment: [framework versions, dependencies]
            Include: Architecture patterns, tradeoffs, code examples
            Compare: [different approaches]"
   })
   ```

3. **Use deep research for comprehensive investigation**:
   ```javascript
   mcp__perplexity__deep_research({
     query: "[feature] implementation strategies",
     focus_areas: ["performance", "security", "scalability", "best practices"]
   })
   ```

**Alternative Sources (WebSearch/WebFetch):**
- Community best practices and patterns
- Real-world implementation examples
- Performance benchmarks and comparisons
- Security considerations
- Troubleshooting and debugging guides

**CRITICAL: Include full context in searches!**

❌ Bad: "How to implement authentication?"
✅ Good: "How to implement JWT authentication with refresh tokens in Next.js 15 app router? Stack: Next.js 15, TypeScript, PostgreSQL. Consider: secure token storage, middleware protection, session management, CSRF protection. Need: Implementation examples, security best practices."

---

### Phase 4: Synthesize Results

**Combine information from all sources:**

1. **Project Patterns** (from local-rag + traditional search)
   - How does the project currently handle similar features?
   - What conventions are established?
   - What gotchas have been documented?
   - Are there existing implementations to reference?

2. **Library Best Practices** (from context7 + official docs)
   - What does the official documentation recommend?
   - Are there current API patterns we should follow?
   - Any breaking changes or deprecations?
   - What are the recommended approaches?

3. **Industry Standards** (from perplexity + external research)
   - What are the best practices in the wider community?
   - What are the tradeoffs of different approaches?
   - Are there security or performance considerations?
   - What are proven production patterns?

4. **Actionable Recommendations**
   - Specific approach to take (based on all sources)
   - Code examples combining project patterns + library APIs + best practices
   - Step-by-step implementation guide
   - Potential issues to watch for
   - Validation strategy

---

## Example Research Workflows

### Example 1: "How should I implement calendar filtering?"

**Step 1: Search project**
- Use Grep to search for existing filter patterns: `pattern: "filter.*component"`
- Check `examples/` for filter implementations
- Review `CLAUDE.md` for UI component guidelines

**Step 2: Fetch library docs**
- WebFetch React Query documentation on query filters
- WebFetch Tamagui documentation for filter UI components
- Check `PRPs/ai_docs/react-query.md` for curated patterns

**Step 3: External research**
- WebSearch: "React Native calendar filtering best practices 2025"
- WebSearch: "React Query parameterized queries patterns"
- WebFetch relevant blog posts and tutorials

**Step 4: Synthesize**
- Use project's established filter component patterns
- Implement parameterized queries per React Query docs
- Apply best practices for multi-criteria filtering
- Ensure style guide compliance

---

### Example 2: "Should I use Zustand or Jotai for this feature?"

**Step 1: Search project**
- Grep for existing state management: `pattern: "zustand|jotai"`
- Check `CLAUDE.md` for state management conventions
- Review existing implementations

**Step 2: Fetch both libraries' docs**
- WebFetch Zustand documentation
- WebFetch Jotai documentation
- Compare API patterns and features
- Check `PRPs/ai_docs/zustand.md` if available

**Step 3: External research**
- WebSearch: "Zustand vs Jotai React Native 2025"
- Look for bundle size comparisons
- Check for TypeScript support differences
- Research persistence patterns

**Step 4: Synthesize**
- Stick with existing choice if project already uses one (consistency)
- Apply official best practices
- Document decision in `CLAUDE.md`
- Note tradeoffs and gotchas

---

### Example 3: "How to debug this error?"

**Step 1: Search project**
- Grep for error message or keywords
- Check if error was encountered before
- Review similar code sections
- Check `CLAUDE.md` for known gotchas

**Step 2: Search library docs**
- WebFetch relevant library documentation
- Look for troubleshooting sections
- Check migration guides
- Review breaking changes

**Step 3: External research**
- WebSearch exact error message
- Include full stack trace in search
- Look for GitHub issues with same error
- Check Stack Overflow solutions
- Include environment details (OS, versions)

**Step 4: Synthesize**
- Apply fix from research
- Verify solution matches project patterns
- Document gotcha if project-specific
- Update `CLAUDE.md` if it's a common issue

---

## Research Quality Checklist

Before considering research complete, ensure:

- [ ] Searched project for similar patterns and implementations
- [ ] Checked project conventions in `CLAUDE.md`
- [ ] Reviewed `examples/` folder for relevant code
- [ ] Fetched relevant library documentation
- [ ] Conducted external research with full context
- [ ] Synthesized findings from all sources
- [ ] Identified actionable recommendations
- [ ] Considered project conventions and constraints
- [ ] Noted any tradeoffs or gotchas
- [ ] Provided code examples where applicable

---

## When to Use This Command

**Use /research when:**
- Planning a new feature (before generating PRP)
- Debugging complex issues
- Evaluating architectural decisions
- Comparing library options
- Understanding best practices
- Investigating performance issues
- Resolving ambiguous requirements

**DON'T use /research when:**
- Simple factual question (use single search)
- Information already in context
- Urgent bug fix (search error directly)
- Answer is in `CLAUDE.md` or `PLANNING.md`

---

## Tips for Effective Research

### Be Specific in Searches
❌ "How to use React Query?"
✅ "How to implement offline-first React Query with AsyncStorage persistence, optimistic updates, and background sync for React Native Expo app?"

### Include Full Context
Always mention:
- Exact versions (React Native, Expo, libraries)
- Platform (iOS, Android, both, web)
- Stack (TypeScript, UI library, state management)
- Constraints (offline-first, performance, security)
- What you've tried (for debugging)

### Search Strategically
1. Start local (project patterns)
2. Go official (library docs)
3. Expand external (community practices)
4. Synthesize findings

### Document Findings
- Add new patterns to `examples/`
- Update `CLAUDE.md` with gotchas
- Update `PRPs/ai_docs/` with curated guidance
- Document architectural decisions

---

## Output Format

Present research findings as:

```markdown
# Research: [Topic]

## Question
[Original research question]

## Sources Searched
- Project: [What was searched - files, patterns, examples]
- Official docs: [Which libraries, what sections]
- External: [Search queries, articles, discussions]

## Findings

### Project Context
[Key findings from project documentation and code]

### Library Documentation
[Official recommendations and patterns]

### Industry Best Practices
[Community standards and approaches]

## Recommendations

### Approach
[Specific approach to take]

### Implementation
[Step-by-step guide or code example]

### Gotchas
[Potential issues to watch for]

### Related Documentation
[Links to relevant project docs or examples]
```

---

## See Also

- `@CLAUDE.md` - Project conventions and guidelines
- `@.claude/PLANNING.md` - Architecture overview
- `@examples/` - Working code patterns
- `@PRPs/ai_docs/` - Library-specific guidance
