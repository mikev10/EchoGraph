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

**What to search for:**
- Existing implementations and patterns (search `examples/` folder)
- Style guide rules and design patterns (check `CLAUDE.md`)
- API endpoints and schemas (check `docs/api/` if applicable)
- Library usage patterns (review existing code)
- Past decisions and gotchas (check documentation)

**Search strategies:**
- Use Grep tool to search for relevant code patterns
- Use Glob tool to find similar files
- Read example implementations in `examples/`
- Check `PRPs/ai_docs/` for library-specific guidance
- Review `.claude/PLANNING.md` for architecture context

**Example searches:**
- "How is offline persistence implemented?"
- "What UI components are used for forms?"
- "Calendar API endpoints and their request/response formats"

---

### Phase 2: Fetch Library Documentation

**Get up-to-date documentation for relevant libraries:**

**Sources:**
- Official library documentation websites
- `PRPs/ai_docs/` for curated library guides
- GitHub repositories (README, docs folder)
- npm package documentation
- Library-specific tutorials and guides

**Use WebFetch tool to access:**
- Official documentation pages
- API reference guides
- Migration guides and changelogs
- Best practices and patterns
- Code examples and recipes

**When to use:**
- Verifying current API signatures
- Understanding best practices for a library
- Checking for breaking changes
- Getting official examples
- Understanding advanced features

**Example topics:**
- "offline support and persistence"
- "optimistic updates and mutations"
- "file-based routing and navigation"
- "state persistence and hydration"

---

### Phase 3: External Research

**Research beyond project and library documentation:**

**Use WebSearch and WebFetch for:**
- Community best practices and patterns
- Real-world implementation examples
- Performance benchmarks and comparisons
- Security considerations
- Architecture patterns
- Troubleshooting and debugging guides

**Research strategies:**
1. Search for specific patterns or problems
2. Look for recent articles (prefer last 1-2 years)
3. Check official blogs and release notes
4. Review Stack Overflow for common issues
5. Look for production-tested approaches

**CRITICAL: Include full context in searches!**

❌ Bad: "How to implement offline support?"
✅ Good: "How to implement offline-first calendar with React Query including optimistic updates, AsyncStorage persistence, and background sync for React Native Expo app? Stack: Expo SDK 50, React Query v5, TypeScript. Consider: cache invalidation, conflict resolution, UI feedback."

---

### Phase 4: Synthesize Results

**Combine information from all sources:**

1. **Project Patterns** (from local search)
   - How does the project currently handle similar features?
   - What conventions are established?
   - What gotchas have been documented?

2. **Library Best Practices** (from official docs)
   - What does the official documentation recommend?
   - Are there current API patterns we should follow?
   - Any breaking changes or deprecations?

3. **Industry Standards** (from external research)
   - What are the best practices in the wider community?
   - What are the tradeoffs of different approaches?
   - Are there security or performance considerations?

4. **Actionable Recommendations**
   - Specific approach to take
   - Code examples combining all sources
   - Step-by-step implementation guide
   - Potential issues to watch for

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
