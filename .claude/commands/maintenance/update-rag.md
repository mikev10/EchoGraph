---
description: Update local-rag with completed PRPs and key documentation
---

# Update Local RAG Database

Updates the local-rag vector database with completed PRPs and essential project documentation.

**Purpose**: Ensure AI has latest implementation context from completed work.

---

## Process

1. **Show Current Status**: Display document/chunk counts before update
2. **Ingest Completed PRPs**: Process all files in `PRPs/completed/`
3. **Ingest Key Docs**: Update critical reference documents
4. **Show Final Status**: Display before/after comparison

---

## Files to Ingest

### Completed PRPs (Priority 1)
All markdown files in `PRPs/completed/*.md`:
- These contain actual implementation details
- Include patterns, code samples, and decisions made
- Critical for understanding what's been built

### Core Documentation (Priority 2)
Key reference files:
- `CLAUDE.md` - Project conventions and global rules
- `.claude/PLANNING.md` - Architecture overview
- `.claude/TASK.md` - Task hierarchy
- `[[PROJECT_SPECIFIC_DOCS]]` - Add your project-specific documentation here
- `PRPs/ai_docs/*.md` - Library-specific documentation
- `examples/README.md` - Code pattern index and guide

**CUSTOMIZE THIS LIST** for your project:
- Add paths to design system documentation
- Add paths to API specifications or summaries
- Add paths to migration plans or architecture documents
- Add paths to team conventions or style guides

---

## Expected Output Format

```
🔄 Updating Local RAG Database
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Current Status:
  • Documents: 6
  • Chunks: 485
  • Memory: 30.8 MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Ingesting Completed PRPs...

✅ PRPs/completed/feature-1.md (113 chunks)
✅ PRPs/completed/feature-2.md (87 chunks)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Updating Core Documentation...

✅ CLAUDE.md (45 chunks)
✅ .claude/PLANNING.md (25 chunks)
✅ .claude/TASK.md (15 chunks)
✅ PRPs/ai_docs/library-guide.md (52 chunks)
✅ examples/README.md (32 chunks)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Final Status:
  • Documents: 6 → 11 (+5 new)
  • Chunks: 485 → 887 (+402)
  • Memory: 30.8 MB → 42.5 MB

✨ RAG database updated successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Implementation Steps

### Step 1: Get Initial Status
```javascript
const statusBefore = await mcp__local-rag__status();
console.log(`📊 Current Status:`);
console.log(`  • Documents: ${statusBefore.documentCount}`);
console.log(`  • Chunks: ${statusBefore.chunkCount}`);
console.log(`  • Memory: ${statusBefore.memoryUsage.toFixed(1)} MB`);
```

### Step 2: Ingest Completed PRPs
```javascript
const completedPrpsPath = '[[ABSOLUTE_PATH_TO_PROJECT]]/PRPs/completed';

// Get all .md files in PRPs/completed/
const prpFiles = glob('*.md', { cwd: completedPrpsPath });

console.log(`\n📝 Ingesting Completed PRPs...\n`);

for (const file of prpFiles) {
  const filePath = path.join(completedPrpsPath, file);
  try {
    const result = await mcp__local-rag__ingest_file({ filePath });
    console.log(`✅ PRPs/completed/${file} (${result.chunkCount} chunks)`);
  } catch (error) {
    console.log(`❌ PRPs/completed/${file} (ERROR: ${error.message})`);
  }
}
```

### Step 3: Ingest Core Documentation
```javascript
const rootPath = '[[ABSOLUTE_PATH_TO_PROJECT]]';

const coreFiles = [
  // Project documentation
  'CLAUDE.md',
  '.claude/PLANNING.md',
  '.claude/TASK.md',

  // [[CUSTOMIZE THIS LIST FOR YOUR PROJECT]]
  // Examples:
  // 'docs/design-system.md',
  // 'docs/api-specification.md',
  // 'PRPs/ai_docs/database-schema.md',

  // Library guides
  'PRPs/ai_docs/*.md',  // All library documentation

  // Code patterns
  'examples/README.md'
];

console.log(`\n📚 Updating Core Documentation...\n`);

for (const file of coreFiles) {
  const filePath = path.join(rootPath, file);
  try {
    const result = await mcp__local-rag__ingest_file({ filePath });
    console.log(`✅ ${file} (${result.chunkCount} chunks)`);
  } catch (error) {
    // Check if it's a "file not found" error for optional files
    if (error.message.includes('not found')) {
      console.log(`⚠️  ${file} (not found - skipping)`);
    } else {
      console.log(`❌ ${file} (ERROR: ${error.message})`);
    }
  }
}
```

### Step 4: Show Final Status
```javascript
const statusAfter = await mcp__local-rag__status();

const docDiff = statusAfter.documentCount - statusBefore.documentCount;
const chunkDiff = statusAfter.chunkCount - statusBefore.chunkCount;

console.log(`\n📊 Final Status:`);
console.log(`  • Documents: ${statusBefore.documentCount} → ${statusAfter.documentCount} (${docDiff >= 0 ? '+' : ''}${docDiff})`);
console.log(`  • Chunks: ${statusBefore.chunkCount} → ${statusAfter.chunkCount} (${chunkDiff >= 0 ? '+' : ''}${chunkDiff})`);
console.log(`  • Memory: ${statusBefore.memoryUsage.toFixed(1)} MB → ${statusAfter.memoryUsage.toFixed(1)} MB`);

console.log(`\n✨ RAG database updated successfully!`);
```

---

## When to Run

**Run this command when:**
- ✅ After completing a PRP (move to `PRPs/completed/`)
- ✅ After major documentation updates (CLAUDE.md, PLANNING.md, examples/)
- ✅ Before starting a new feature (ensure latest context)
- ✅ When you need AI to be aware of recent implementation details
- ✅ After updating PLANNING.md files
- ✅ After adding new code patterns to `examples/` directory

**Don't need to run when:**
- ❌ Making minor code changes (implementation files)
- ❌ Updating comments only
- ❌ Changing configuration files
- ❌ Working on temporary/experimental code

---

## What Gets Updated

### Completed PRPs
PRPs contain the "source of truth" for implemented features:
- Actual code patterns used
- Implementation decisions made
- Gotchas encountered
- Validation results
- Architecture choices

### Core Documentation
Essential reference material:

**Project Structure & Conventions:**
- `CLAUDE.md` - Project conventions, task management, security rules
- `.claude/PLANNING.md` - Architecture and goals
- `.claude/TASK.md` - Current task hierarchy

**Design & Architecture:**
- Design system documentation (customize for your project)
- API specifications or summaries (customize for your project)
- Database schema references (customize for your project)

**Code Patterns:**
- `examples/README.md` - Code pattern index and examples

---

## Error Handling

If a file fails to ingest:
- ✅ Report the error clearly
- ✅ Continue processing remaining files
- ✅ Show which files succeeded/failed in summary
- ✅ Verify file path is correct (absolute path format)

Common errors:
- **File not found**: Check file path and spelling
- **Permission denied**: Ensure file is not locked/open
- **Invalid file format**: Only .md, .txt, .pdf, .docx supported

---

## Verification

After running, verify the update worked:

```javascript
// Query for recently added content
const results = await mcp__local-rag__query_documents({
  query: "[[specific topic from recently completed PRP]]",
  limit: 5
});

// Should return chunks from recently ingested files
```

---

## Performance Notes

- **Reingest is safe**: Re-ingesting existing files updates them
- **Chunk deduplication**: System handles duplicate content
- **Memory efficient**: Old chunks are replaced, not duplicated
- **Fast queries**: Vector search remains fast even with more documents

---

## Troubleshooting

**Problem**: Files not showing in queries after ingest

**Solution**:
1. Check ingestion success messages
2. Run `mcp__local-rag__list_files` to verify
3. Try querying with different keywords
4. Check file path format (absolute paths)

**Problem**: Memory usage growing too large

**Solution**:
1. Delete unused files: `mcp__local-rag__delete_file({ filePath })`
2. Only ingest essential documentation
3. Avoid ingesting large PDFs or redundant files

---

## See Also

- `/reingest-queue` - Process files queued by PostToolUse hook
- `mcp__local-rag__list_files` - View all ingested files
- `mcp__local-rag__query_documents` - Search ingested content
- `mcp__local-rag__delete_file` - Remove outdated files
