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

## Product Owner Integration

**User Story to Feature Request Workflow:**

Product Owners write user stories in Azure DevOps. Developers convert these to feature requests (INITIAL.md) for PRP generation.

**Key Principle:** 1 User Story (1-3 days) = 1 Feature Request = 1 PRP

### For Product Owners: Drafting User Stories (OPTIONAL)

**Before creating ADO work items, you can draft and refine stories using AI assistance:**

1. **Use the `/write-user-story` command:**
   - Run: `/write-user-story "Users need to reset their password..."`
   - AI asks clarifying questions about requirements
   - AI generates well-structured user story with Given/When/Then acceptance criteria
   - Story saved to `user-stories/drafts/` for review

2. **Review and refine:**
   - Check acceptance criteria are testable and comprehensive
   - Verify story size is appropriate (1-3 days, 3-8 story points)
   - Ensure all edge cases and error scenarios are covered
   - Add any business context or constraints

3. **Create ADO work item:**
   - Copy content from generated markdown file
   - Create new user story in Azure DevOps
   - Link designs, mockups, dependencies
   - Assign to developer

**This step is OPTIONAL but recommended for:**
- Complex features needing careful planning
- POs new to writing user stories
- Features with many edge cases or business rules
- Offline/async planning sessions
- Learning to write better user stories

**See also:** `docs/PRODUCT-OWNER-GUIDE.md` for complete guidance on writing effective user stories.

### Three Amigos Workflow (Recommended)

**Before stories enter team grooming**, use the Three Amigos workflow to ensure alignment:

**Participants:**
- **Product Owner** - Business perspective
- **Dev Lead** - Technical perspective
- **QA Lead** - Testing perspective

**Workflow Steps:**

```
Step 1: PO Creates Story → /write-user-story
Step 2: Dev Lead Enriches → /enrich-story-tech [story-path]
Step 3: QA Lead Enriches → /enrich-story-qa [story-path]
Step 4: Alignment Meeting → /three-amigos-prep [story-path]
Step 5: Validate Ready → /validate-story-ready [story-path]
```

**New Commands for Three Amigos:**

| Command | Owner | Purpose |
|---------|-------|---------|
| `/enrich-story-tech` | Dev Lead | Add technical context: APIs, data model, patterns, security |
| `/enrich-story-qa` | QA Lead | Add test scenarios, edge cases, test data requirements |
| `/three-amigos-prep` | Facilitator | Generate meeting agenda for 30-45 min alignment session |
| `/validate-story-ready` | Any | Check story against Definition of Ready criteria |

**Definition of Ready:**
Stories are READY when they pass all criteria in `docs/DEFINITION-OF-READY.md`:
- User story structure (specific user, clear value)
- Acceptance criteria (3+ scenarios, Given/When/Then)
- Technical context (feasibility, APIs, dependencies)
- QA context (test scenarios, test data)
- Three Amigos alignment (questions resolved, scope agreed)

**When to Use Three Amigos:**
- ✅ New features with user-facing changes
- ✅ Complex stories with unknown complexity
- ✅ Stories touching security or payments
- ❌ Bug fixes with clear reproduction steps
- ❌ Technical debt / developer-only work
- ❌ Trivial changes

**See also:** `.claude/docs/three-amigos-guide.md` for complete Three Amigos documentation.

### For Developers: Converting User Stories

**When you receive a user story from a Product Owner:**

1. **If story quality is poor, optionally refine it first:**
   - Run: `/refine-story [ADO-ID]`
   - AI analyzes story against INVEST criteria
   - Shows before/after comparison with identified issues
   - Decide whether to use improved version or request PO updates

2. **Use the `/convert-story` command:**
   - Command prompts you to paste ADO user story content
   - AI researches codebase for similar patterns, API endpoints, libraries
   - Asks clarifying questions about technical approach
   - Generates INITIAL.md with technical enrichment

3. **Review and adjust the generated INITIAL.md:**
   - Verify API endpoints match specification
   - Check libraries/versions are correct
   - Add any project-specific gotchas
   - Ensure security considerations are complete

4. **Proceed with standard workflow:**
   - `/generate-prp` → Creates comprehensive PRP
   - `/execute-prp` → Implements step-by-step
   - Update ADO story status when complete

**Alternative: Manual conversion**
- Reference template: `.claude/templates/story-to-initial.md`
- See examples and guidelines for proper conversion
- Ensure all acceptance criteria are captured

### Granularity Guidelines

**Three levels of work:**

| Level | ADO Item | Context Engineering | Size | Example |
|-------|----------|---------------------|------|---------|
| **Story** | User Story | 1 INITIAL.md → 1 PRP | 1-3 days | "User login with email/password" |
| **Feature** | Feature | Multiple PRPs (one per story) | 1-2 weeks | "User Authentication" (login, logout, reset, refresh) |
| **Epic** | Epic | Multiple Features → Multiple PRPs | Multiple weeks | "User Management" (auth, profiles, permissions, audit) |

**Story-level work (most common):**
- Product Owner writes small user story (1-3 days)
- Developer converts to INITIAL.md using `/convert-story`
- Single PRP generated and executed
- Can be deployed independently

**Feature-level work:**
- Product Owner writes multiple related user stories
- Developer creates feature task file (TASK-XXX)
- Each story becomes a subtask (TASK-XXX.Y) with its own PRP
- All PRPs contribute to one feature
- Feature ships when all stories complete

**Epic-level work:**
- Product Owner defines large initiative
- Break into features, then into stories
- Each story still follows 1:1 PRP mapping
- Ships across multiple sprints

### What Product Owners Need to Provide

**Required in every user story:**
- ✅ User story format: "As a [user], I want [capability], so that [benefit]"
- ✅ Minimum 2-3 acceptance criteria (ideally Given/When/Then format)
- ✅ Business value explanation
- ✅ Story size: 1-3 days (3-8 story points)

**Nice to have:**
- Mockups or wireframes
- Links to competitor examples
- Business constraints (deadlines, compliance)
- Platform requirements

**Product Owners should NOT provide:**
- ❌ Technical implementation details
- ❌ Code examples or API endpoint specifications
- ❌ Library/framework choices
- ❌ Database schemas

**Developers research technical context during conversion.**

### Resources for Product Owners

- **Complete guide:** `docs/PRODUCT-OWNER-GUIDE.md`
- **Three Amigos guide:** `.claude/docs/three-amigos-guide.md`
- **Definition of Ready:** `docs/DEFINITION-OF-READY.md`
- **Story workflow guide:** `.claude/docs/story-workflow-guide.md`
- **Conversion template:** `.claude/templates/story-to-initial.md`
- **Conversion command:** `/convert-story`

### When to Skip User Story Conversion

**Write INITIAL.md directly (without user story) for:**
- Technical work (refactoring, bug fixes, technical debt)
- Developer-initiated improvements
- Work with no Product Owner involvement
- Very technical features requiring significant research upfront

In these cases, use the standard INITIAL.md template and proceed directly to `/generate-prp`.

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
