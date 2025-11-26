---
description: Re-ingest queued files into local-rag database
---

# Re-Ingest Queued Documentation Files

Re-ingests files that were modified and queued by the PostToolUse hook.

**Purpose**: Update the local-rag vector database with latest documentation changes.

---

## Process

1. **Read Queue File**: `.claude/rag-reingest-queue.txt`
2. **For Each File in Queue**:
   - Call `mcp__local-rag__ingest_file({ filePath: absolute_path })`
   - Report chunk count from result
   - Remove from queue on success
   - Keep in queue on failure (report error)
3. **Show Summary**: X files re-ingested, Y failed, Z remaining in queue

---

## Expected Output Format

```
🔄 Re-ingesting Queued Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Processing 2 files from queue...

✅ PRPs/ai_docs/library-guide.md (149 chunks)
✅ docs/design-system.md (39 chunks)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
  • 2 files re-ingested successfully
  • 0 failed
  • Queue is now empty
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## If Queue is Empty

Check if `.claude/rag-reingest-queue.txt` exists and has content.

If empty or doesn't exist, report:
```
No files pending re-ingestion. Queue is empty.
```

---

## Error Handling

If a file fails to re-ingest:
1. Report the error clearly
2. Keep the file in the queue for retry
3. Continue processing remaining files
4. Show failed files in summary

Example error output:
```
✅ PRPs/ai_docs/file1.md (39 chunks)
❌ PRPs/ai_docs/file2.md (ERROR: File not found)
✅ PRPs/ai_docs/file3.md (15 chunks)

Summary:
  • 2 files re-ingested successfully
  • 1 failed (kept in queue for retry)
  • 0 remaining
```

---

## Implementation Steps

1. Read `.claude/rag-reingest-queue.txt`
   - If file doesn't exist or is empty, report "Queue is empty" and exit

2. Parse file paths (one per line, skip empty lines)

3. For each file path:
   ```javascript
   try {
     const result = await mcp__local-rag__ingest_file({
       filePath: file_path
     });
     // result.chunkCount contains number of chunks
     console.log(`✅ ${file_path} (${result.chunkCount} chunks)`);
     successes++;
   } catch (error) {
     console.log(`❌ ${file_path} (ERROR: ${error.message})`);
     failed_files.push(file_path);
     failures++;
   }
   ```

4. Write failed files back to queue (overwrite with only failed entries)

5. Show summary with counts

---

## After Re-Ingestion

**CRITICAL**: After re-ingesting files, the local-rag database is updated. All future queries will use the new content:

- `/generate-prp` will use latest patterns and documentation
- `/execute-prp` will validate against current conventions
- Queries return up-to-date information

---

## Maintenance

**When to run:**
- After editing files in `PRPs/ai_docs/`
- When you see "📝 Queued for RAG re-ingestion" message
- Periodically to process accumulated changes
- Before starting new PRP generation (ensure latest context)

**How often:**
- Manual trigger (run when convenient)
- Batch multiple edits (no need to run after every single edit)
- Before starting new feature work

---

## Debugging

**Check queue contents:**
```bash
cat .claude/rag-reingest-queue.txt
```

**Manually add file to queue:**
```bash
echo "[[ABSOLUTE_PATH_TO_FILE]]" >> .claude/rag-reingest-queue.txt
```

**Clear queue:**
```bash
rm .claude/rag-reingest-queue.txt
```

**Verify re-ingestion worked:**
```javascript
mcp__local-rag__query_documents({
  query: "content that should be updated",
  limit: 3
})
```

---

## See Also

- `.claude/hooks/track-ai-docs.sh` - Hook that populates the queue (if configured)
- `.claude/settings.local.json` - Hook configuration (if using hooks)
- `/update-rag` - Full RAG database update command
- `@docs/mcp-servers.md` - MCP server documentation (if exists)
