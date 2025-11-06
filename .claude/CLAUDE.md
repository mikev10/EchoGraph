# [[PROJECT_NAME]] - Global Conventions

## Project Context (Auto-Loaded)

@.claude/PLANNING.md
@.claude/TASK.md

## Project Awareness

**Before starting ANY work:**
- Review `examples/` folder for established patterns
- Consult `PRPs/ai_docs/` for library-specific documentation
- **Verify API endpoints in `docs/api/[[YOUR_API_SPEC]].json`** (if applicable)
- [[ADD_PROJECT_SPECIFIC_REQUIREMENTS]]

**Note:** Architecture (PLANNING.md) and current priorities (TASK.md) are auto-loaded via imports above.

## Code Structure

**File Organization:**
- Keep files under [[MAX_LINES_PER_FILE]] lines; split when exceeded
- [[ORGANIZATIONAL_PATTERN]] structure: `src/[[FEATURE_PATTERN]]/`
- Each feature contains: [[FEATURE_SUBDIRECTORIES]]
- Separate concerns: UI, logic, state, types

**Naming Conventions:**
- Files: [[FILE_NAMING_CONVENTION]] (e.g., `user-profile.tsx`)
- Components/Classes: [[COMPONENT_NAMING]] (e.g., `UserProfile`)
- Functions/variables: [[FUNCTION_NAMING]] (e.g., `getUserData`, `selectedUser`)
- Constants: [[CONSTANT_NAMING]] (e.g., `API_BASE_URL`)
- Types/Interfaces: [[TYPE_NAMING]] (e.g., `User`, `ApiResponse`)

**Import Order:**
1. External dependencies (react, etc.)
2. Internal absolute imports (@/lib/, @/components/)
3. Relative imports (./types, ../utils)
4. Type imports (import type { ... })

## Tech Stack Patterns

**[[PRIMARY_FRAMEWORK]]:**
- [[PATTERN_1_WITH_EXAMPLE]]
- [[PATTERN_2_WITH_EXAMPLE]]
- See `PRPs/ai_docs/[[framework]].md` for detailed patterns

**[[DATA_FETCHING_LIBRARY]]:**
- Cache strategy: [[CACHE_STRATEGY]]
- Error handling: [[ERROR_HANDLING_PATTERN]]
- See `examples/integrations/` for implementation patterns

**[[STATE_MANAGEMENT]]:**
- Use for [[WHAT_STATE_GOES_HERE]]
- Store structure: [[STORE_PATTERN]]
- Selectors: [[SELECTOR_PATTERN]]
- See `examples/state/` for implementation patterns

**[[OTHER_KEY_LIBRARIES]]:**
- [[LIBRARY_NAME]]: [[USAGE_PATTERN]]

## Testing Requirements

**Test Coverage:**
- Minimum [[COVERAGE_PERCENTAGE]]% coverage for [[COVERAGE_SCOPE]]
- Test files: `{filename}.test.[[EXTENSION]]`
- Test location: [[TEST_LOCATION_PATTERN]]

**Test Structure:**
```[[LANGUAGE]]
describe('[[ComponentName]]', () => {
  describe('when [[condition]]', () => {
    it('should [[expected_behavior]]', () => {
      // Arrange
      // Act
      // Assert
    })
  })
})
```

**Test Patterns:**
- [[TEST_TYPE_1]]: [[TESTING_TOOL_1]]
- [[TEST_TYPE_2]]: [[TESTING_TOOL_2]]
- See `examples/testing/` for implementation patterns

## Security Rules (CRITICAL)

**Authentication & Token Storage:**
- ✅ ALWAYS [[SECURE_STORAGE_METHOD]]
- ❌ NEVER [[INSECURE_STORAGE_METHOD]]
- ✅ ALWAYS check token expiry before API calls
- ✅ ALWAYS implement automatic token refresh

**API Calls:**
- ✅ ALWAYS use centralized API client (`lib/api/client.[[EXT]]`)
- ✅ ALWAYS include auth interceptor
- ✅ ALWAYS handle 401 (redirect to login)
- ✅ ALWAYS use HTTPS (no HTTP)

**API Implementation:**
- ✅ ALWAYS verify endpoints against API specification
- ✅ ALWAYS match request/response types from spec
- ✅ ALWAYS use correct HTTP methods (GET/POST/PUT/DELETE)
- 📄 Full spec: `docs/api/[[YOUR_API_SPEC]].json` (if applicable)
- 📄 AI summary: `PRPs/ai_docs/[[your_api]]-spec-summary.md` (if applicable)

**Input Validation:**
- ✅ ALWAYS validate [[VALIDATION_APPROACH]]
- ✅ ALWAYS sanitize user inputs
- ✅ ALWAYS validate on both client and server

**Audit Logging:**
- ✅ ALWAYS log [[SECURITY_EVENT_TYPES]]
- ✅ ALWAYS include user ID, timestamp, action type
- See `examples/security/audit-logger.ts` for implementation

## [[OPTIONAL_ARCHITECTURE_SECTION]] Architecture

**[[ARCHITECTURE_ASPECT_1]]:**
- [[IMPLEMENTATION_DETAIL_1]]
- [[IMPLEMENTATION_DETAIL_2]]

**[[ARCHITECTURE_ASPECT_2]]:**
- [[IMPLEMENTATION_DETAIL_1]]
- [[IMPLEMENTATION_DETAIL_2]]

## Style & Formatting

**Code Style:**
- Formatter: [[FORMATTER_NAME]] - [[FORMATTER_CONFIG]]
- Linter: [[LINTER_NAME]] - [[LINTER_CONFIG]]
- Max line length: [[MAX_LINE_LENGTH]] characters

**Comments:**
- Comment WHY, not WHAT
- Use [[DOC_COMMENT_STYLE]] for exported functions
- Use inline comments for non-obvious logic
- [[OTHER_COMMENT_GUIDELINES]]

## Documentation Requirements

**When to Update Docs:**
- New API endpoint used → [[UPDATE_ACTION_1]]
- New pattern established → add to `examples/`
- New component created → [[UPDATE_ACTION_2]]
- Architecture change → update `.claude/PLANNING.md`

## Task Management

**Three-Level Task System:**

**Level 1: Master TASK.md (Epic/Feature Level - Persistent):**
- High-level features and milestones tracked in `.claude/TASK.md`
- Each task has unique ID (TASK-001, TASK-002, etc.)
- References detailed feature task files in `.claude/tasks/`
- Progress auto-calculated from subtasks (e.g., "3/5 complete")
- Claude updates during work: marks complete, updates progress
- Updates happen: after PRP completion, at session end, after major milestones
- Human can manually edit/override anytime
- Tracked in git, survives sessions
- Format: `- [ ] [TASK-001] Feature name (3/5) → @.claude/tasks/TASK-001-feature.md`

**Level 2: Feature Task Files (Subtask Level - Persistent):**
- Concrete implementation steps (3-10 subtasks per feature)
- Located in `.claude/tasks/TASK-XXX-feature-name.md`
- Contains: context, subtasks, notes, testing requirements, acceptance criteria
- Each subtask has ID: TASK-001.1, TASK-001.2, etc.
- Persists across sessions, tracked in git
- Human and Claude can both update
- When all subtasks complete, parent task auto-completes
- See `.claude/tasks/README.md` for full documentation

**Level 3: TodoWrite (Session-Level - Temporary):**
- Granular step-by-step tasks for current work
- Claude manages automatically during PRP execution
- One task `in_progress` at a time
- Mark `completed` immediately when done
- Does not persist between sessions

**Task Workflow:**
1. Add high-level task to master TASK.md with unique ID
2. Create feature task file (`.claude/tasks/TASK-XXX-feature.md`)
3. Break down into 3-10 concrete subtasks
4. During work, use TodoWrite for granular execution steps
5. Mark subtasks complete as you finish them
6. Run `/validate-tasks` to update progress and auto-complete parent

**Validation:**
Run `/validate-tasks` to:
- Validate task ID format and uniqueness
- Check file references exist
- Update progress counts automatically
- Auto-complete parent tasks when all subtasks done
- Detect orphaned task files

## Validation Commands (Must Pass Before Committing)

```bash
# [[VALIDATION_COMMAND_1]] (must [[EXPECTED_RESULT]])
[[COMMAND_1]]

# [[VALIDATION_COMMAND_2]] (must [[EXPECTED_RESULT]])
[[COMMAND_2]]

# [[VALIDATION_COMMAND_3]] (must [[EXPECTED_RESULT]])
[[COMMAND_3]]
```

## Critical Gotchas

**[[TECHNOLOGY_1]]:**
- [[GOTCHA_1]]
- [[GOTCHA_2]]
- [[GOTCHA_3]]

**[[TECHNOLOGY_2]]:**
- [[GOTCHA_1]]
- [[GOTCHA_2]]

**[[TECHNOLOGY_3]]:**
- [[GOTCHA_1]]

## Never Do This

❌ [[ANTI_PATTERN_1]]
❌ [[ANTI_PATTERN_2]]
❌ [[ANTI_PATTERN_3]]
❌ Use `any` type without strong justification
❌ Store auth tokens in insecure storage
❌ Make API calls without auth interceptor
❌ Commit without running validation commands
❌ Delete code without explicit instruction
❌ Assume library availability without checking
❌ Skip tests for "simple" features

## Always Do This

✅ [[BEST_PRACTICE_1]]
✅ [[BEST_PRACTICE_2]]
✅ [[BEST_PRACTICE_3]]
✅ Run validation commands before committing
✅ Write tests for new features
✅ Validate inputs
✅ Handle loading and error states
✅ Update TASK.md with progress
✅ Reference examples/ for patterns
✅ Ask for clarification if requirements unclear
