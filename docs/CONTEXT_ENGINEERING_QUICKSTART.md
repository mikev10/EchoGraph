# Context Engineering Quick Start

**Get context engineering running in your project in 4 hours.**

---

## What Is This?

Context Engineering = Giving AI everything it needs upfront (conventions, examples, validation) so it can build features with 70%+ first-pass success rate.

**Result:** 50-70% faster development, fewer bugs, consistent quality.

**Investment:** 4-20 hours (this guide focuses on minimum viable setup in 4 hours)

---

## Prerequisites

- Existing project or new project scaffold
- Package manager (npm, yarn, pnpm, uv, pip, etc.)
- Git repository
- Claude Code or Claude Desktop

---

## 30-Minute Quick Setup

### Step 1: Create Directory Structure (5 min)

```bash
# From project root
mkdir -p .claude/commands
mkdir -p PRPs/ai_docs PRPs/templates PRPs/completed
mkdir -p examples/integrations examples/components
mkdir -p examples/hooks examples/state examples/testing
```

### Step 2: Copy Universal Files (10 min)

**From EZMobile project, copy these 12 files to your project:**

`.claude/commands/` directory:
1. ✅ `generate-prp.md`
2. ✅ `execute-prp.md`
3. ✅ `prime-core.md`
4. ✅ `validate-context.md`
5. ✅ `review-general.md`
6. ✅ `review-staged.md`
7. ✅ `refactor-simple.md`
8. ✅ `create-pr.md`
9. ✅ `onboarding.md`
10. ✅ `debug.md`
11. ✅ `planning-create.md`
12. ✅ `archive-prp.md`

**Also copy:**
- ✅ `.claude/INITIAL.md` (feature request template)
- ✅ `.claude/settings.local.json` (permissions config)

**Quick fix paths in commands:**
- Open each command file
- Find/replace `.claude/CLAUDE.md` → your path (if different)
- Find/replace `examples/` → your path (if different)
- Find/replace validation commands (e.g., `npm run type-check` → your command)

### Step 3: Create TASK.md (2 min)

**File:** `.claude/TASK.md`

```markdown
# Current Tasks

## In Progress
- [ ] Setup context engineering foundation

## Pending
- [ ] Create first example patterns
- [ ] Generate first PRP
- [ ] Execute first PRP

## Completed
_Tasks move here as completed_

---

**Last Updated**: [Today's date]
```

### Step 4: Create Minimal CLAUDE.md (10 min)

**File:** `.claude/CLAUDE.md`

```markdown
# [Your Project Name] - Global Conventions

## Project Context (Auto-Loaded)
@.claude/PLANNING.md
@.claude/TASK.md

## Project Awareness
**Before starting ANY work:**
- Review `examples/` folder for established patterns
- Consult `PRPs/ai_docs/` for library-specific documentation

## Code Structure
**File Organization:**
- [Your file organization pattern]
- Keep files under 300 lines

**Naming Conventions:**
- Files: [your convention]
- Components: [your convention]
- Functions: [your convention]

## Tech Stack Patterns
**[Primary Framework]:**
- [Key pattern 1]
- [Key pattern 2]

**[Key Library 1]:**
- [Key pattern]

**[Key Library 2]:**
- [Key pattern]

## Testing Requirements
**Test Coverage:** [Your target]
**Test Files:** [Location and naming]

## Validation Commands (Must Pass Before Committing)
```bash
# Type check
[your type check command]

# Lint
[your lint command]

# Tests
[your test command]
```

## Critical Gotchas
**[Technology 1]:**
- [Gotcha 1]

## Never Do This
❌ [Anti-pattern 1]
❌ [Anti-pattern 2]

## Always Do This
✅ [Best practice 1]
✅ [Best practice 2]
✅ Run validation commands before committing
✅ Reference examples/ for patterns
```

**Note:** You'll expand this significantly, but this minimal version is enough to start.

### Step 5: Create Minimal PLANNING.md (3 min)

**File:** `.claude/PLANNING.md`

```markdown
# [Your Project Name] - Architecture & Goals

## Project Goal
[One sentence: What are we building?]

## Target Users
- [User type 1]
- [User type 2]

## Feature Hierarchy
1. **PRIMARY**: [Main feature] (80% effort)
2. **SECONDARY**: [Secondary feature] (15% effort)
3. **TERTIARY**: [Nice-to-have] (5% effort - OPTIONAL)

## System Architecture
[Brief description or simple diagram]

## Tech Stack Rationale
| Technology | Why |
|------------|-----|
| [Tech 1] | [Reason] |
| [Tech 2] | [Reason] |

## Validation Commands
```bash
[List your validation commands]
```
```

---

## 2-Hour Core Setup

### Step 6: Create 3 Essential Examples (1 hour)

**You need at minimum:**

#### Example 1: API Client / Data Fetching
**File:** `examples/integrations/api-client.ts` (or .py, .go, etc.)

```typescript
// Complete working example of how to call your API
// Include: auth, error handling, interceptors/middleware

// [Your complete implementation with inline comments]
```

**Why:** This is the #1 most-used pattern. Get it right once, AI reuses forever.

---

#### Example 2: Component Pattern
**File:** `examples/components/card-component.tsx` (or your UI framework)

```typescript
// Complete component following your UI library patterns
// Include: props, styling, event handlers, error states

// [Your complete implementation with inline comments]
```

**Why:** Shows AI your component structure, styling approach, prop patterns.

---

#### Example 3: Test Pattern
**File:** `examples/testing/component.test.tsx`

```typescript
// Complete test following your testing patterns
// Include: setup, assertions, mocks

// [Your complete implementation with inline comments]
```

**Why:** AI will write tests matching your structure.

---

### Step 7: Create 2 Library Docs (1 hour)

**Document your 2 most-used libraries:**

#### Doc 1: Primary Framework
**File:** `PRPs/ai_docs/[framework-name].md`

```markdown
# [Framework Name]

## Overview
[What it is, why you use it]

## Key Concepts
### [Concept 1]
[Explanation + code example]

### [Concept 2]
[Explanation + code example]

## Common Patterns
### [Pattern 1]
```[language]
// Example
```

## Gotchas
❌ **DON'T**: [Anti-pattern]
✅ **DO**: [Best practice]
```

---

#### Doc 2: Key Library
**File:** `PRPs/ai_docs/[library-name].md`

Use same structure as above.

**Prioritize:**
- Data fetching library (React Query, SWR, etc.)
- State management (Redux, Zustand, etc.)
- UI library (if using one)
- ORM/database library (if backend)

---

## First Feature Test (1 hour)

### Step 8: Load Context

```bash
# In Claude Code or Desktop
/prime-core
```

**This loads all your context into AI's memory.**

### Step 9: Create Feature Request

**Edit `.claude/INITIAL.md`:**

```markdown
## FEATURE
Create a simple [component/endpoint/function] that [does what]

## EXAMPLES
[Link to similar implementation or screenshot]

## DOCUMENTATION
- [Framework]: PRPs/ai_docs/[framework].md
- [Library]: PRPs/ai_docs/[library].md
- Pattern example: examples/[category]/[file]

## OTHER CONSIDERATIONS
- Must follow patterns in examples/
- Must pass validation commands
- [Any other constraints]
```

**Pick something simple for first test** (e.g., card component, API endpoint, utility function)

### Step 10: Generate PRP

```bash
/generate-prp .claude/INITIAL.md
```

**AI will:**
1. Research your examples/
2. Review your CLAUDE.md
3. Generate a PRP in PRPs/ directory

**Check the confidence score** (should be in the PRP). If < 7, you need more context.

### Step 11: Execute PRP

```bash
/execute-prp PRPs/[generated-filename].md
```

**AI will:**
1. Plan with TodoWrite (ULTRATHINK phase)
2. Implement step-by-step
3. Run validation after each step
4. Fix errors and retry
5. Report results

**Watch for:**
- ✅ Does it follow your patterns?
- ✅ Do validation commands pass?
- ✅ Does it ask reasonable questions (<2)?
- ❌ If AI struggles, you need more context

### Step 12: Iterate

**If execution was successful:**
- ✅ You're ready for real features!
- ✅ Add more examples as patterns emerge
- ✅ Expand CLAUDE.md with gotchas

**If execution struggled:**
- ❌ Add missing examples to examples/
- ❌ Expand CLAUDE.md with missing patterns
- ❌ Add more library docs
- ❌ Make validation commands clearer
- ❌ Retry with updated context

---

## File Copy Checklist

### ✅ Must Copy (Universal)
- [ ] All 12 slash commands from `.claude/commands/`
- [ ] `.claude/INITIAL.md` (feature request template)
- [ ] `.claude/settings.local.json` (update project paths)

### ✅ Must Create (Project-Specific)
- [ ] `.claude/CLAUDE.md` (global conventions)
- [ ] `.claude/PLANNING.md` (architecture)
- [ ] `.claude/TASK.md` (task tracking)
- [ ] 3+ examples in `examples/` (API, component, test minimum)
- [ ] 2+ library docs in `PRPs/ai_docs/`

### 📁 Directory Structure
```
✅ .claude/
✅ .claude/commands/
✅ PRPs/ai_docs/
✅ PRPs/templates/
✅ PRPs/completed/
✅ examples/integrations/
✅ examples/components/
✅ examples/testing/
```

---

## Must-Customize Checklist

### In Slash Commands
- [ ] Update file paths (`.claude/CLAUDE.md`, `examples/`, etc.)
- [ ] Update validation commands (`npm run type-check` → your commands)
- [ ] Update test commands (`npm test` → your test runner)

### In CLAUDE.md
- [ ] Replace tech stack sections with YOUR stack
- [ ] Add YOUR naming conventions
- [ ] Add YOUR file organization rules
- [ ] Add YOUR validation commands
- [ ] Add YOUR critical gotchas
- [ ] Add YOUR security rules (if sensitive data)

### In PLANNING.md
- [ ] Replace project goal with YOUR goal
- [ ] Replace target users with YOUR users
- [ ] Replace features with YOUR features
- [ ] Replace architecture with YOUR architecture
- [ ] Replace tech stack with YOUR tech stack

### In examples/
- [ ] Create examples using YOUR libraries
- [ ] Use YOUR project patterns (not generic)
- [ ] Add inline comments explaining YOUR gotchas
- [ ] Use YOUR actual types/interfaces

### In PRPs/ai_docs/
- [ ] Document YOUR key libraries (not EZMobile's)
- [ ] Include YOUR common patterns
- [ ] Add YOUR gotchas
- [ ] Use YOUR project examples

---

## Validation Checklist

### ✅ Structure Validation
- [ ] All directories created
- [ ] All slash commands copied
- [ ] CLAUDE.md exists and has key sections
- [ ] PLANNING.md exists
- [ ] TASK.md exists
- [ ] At least 3 examples exist
- [ ] At least 2 library docs exist

### ✅ Content Validation
- [ ] CLAUDE.md has validation commands section
- [ ] CLAUDE.md references examples/ folder
- [ ] Slash commands reference correct paths
- [ ] Examples/ files have inline comments
- [ ] Library docs have code examples
- [ ] All file paths use YOUR project structure

### ✅ Workflow Validation
- [ ] `/prime-core` loads without errors
- [ ] Can create feature request in INITIAL.md
- [ ] `/generate-prp` produces PRP with confidence 5+
- [ ] Generated PRP references your examples/
- [ ] Generated PRP includes validation commands
- [ ] `/execute-prp` starts execution (even if not perfect)

---

## Quick Win: First Feature

**Goal:** Generate and execute first PRP successfully

**Choose a simple feature:**
- ✅ Single component (button, card, badge)
- ✅ Single API endpoint (GET /users)
- ✅ Single utility function (date formatter)
- ✅ Single test (component or function)

**Don't start with:**
- ❌ Multi-component features
- ❌ Complex state management
- ❌ Multi-step workflows
- ❌ Features requiring new libraries

**Success Criteria:**
1. ✅ PRP generates with confidence 7+
2. ✅ PRP executes without blocking errors
3. ✅ Generated code follows your patterns
4. ✅ Validation commands pass
5. ✅ AI asks <3 clarifying questions

**If you hit this, you're ready to scale up!**

---

## Troubleshooting

### Issue: Low Confidence Score (<7)
**Problem:** PRP doesn't have enough context

**Solutions:**
- Add more examples to examples/
- Expand CLAUDE.md with patterns
- Add library doc to PRPs/ai_docs/
- Reference more existing code
- Break feature into smaller pieces

---

### Issue: AI Doesn't Follow Patterns
**Problem:** AI doesn't know your patterns exist

**Solutions:**
- Make examples/ more prominent in CLAUDE.md
- Add "Before starting ANY work: Review examples/" to CLAUDE.md
- Reference specific example files in PRP
- Add more inline comments to examples explaining WHY

---

### Issue: Validation Fails
**Problem:** Validation commands in slash commands are wrong

**Solutions:**
- Update validation commands in `/execute-prp`
- Add correct commands to CLAUDE.md
- Ensure commands actually work in your project
- Test commands manually first

---

### Issue: AI Asks Many Questions
**Problem:** Missing critical context

**Solutions:**
- Add missing info to CLAUDE.md (conventions, gotchas)
- Add example demonstrating the pattern
- Add library doc for the library in question
- Be more explicit in PRP about requirements

---

### Issue: Generated Code Has Bugs
**Problem:** Examples have bugs or bad patterns

**Solutions:**
- Review and fix examples/ (make sure they work)
- Add test examples showing correct testing
- Expand library docs with gotchas
- Add validation gates catching these bugs

---

## Expanding Beyond Minimum

**After first successful PRP, add:**

### More Examples (Priority Order)
1. State management pattern (`examples/state/`)
2. Form handling pattern (`examples/components/form-*.tsx`)
3. Error handling pattern (`examples/integrations/error-handler.ts`)
4. Auth pattern (`examples/security/auth-*.ts`)
5. Hook patterns (`examples/hooks/use-*.ts`)

### More Library Docs (Priority Order)
1. Testing library (Jest, Vitest, Pytest, etc.)
2. Form library (if using one)
3. Routing library
4. Database/ORM (if backend)
5. UI library components

### More CLAUDE.md Sections (Priority Order)
1. Security Rules (if handling sensitive data)
2. Offline-First Architecture (if applicable)
3. API Integration patterns (with spec if you have one)
4. Error Handling conventions
5. Logging conventions

---

## Time Investment Summary

### Minimum Viable Setup (4 hours)
- ✅ 30 min: Copy files, create structure
- ✅ 10 min: Minimal CLAUDE.md
- ✅ 3 min: Minimal PLANNING.md
- ✅ 1 hour: 3 essential examples
- ✅ 1 hour: 2 library docs
- ✅ 1 hour: First feature test
- ✅ 30 min: Iterate based on results

**Result:** Can generate and execute simple PRPs with confidence 6-7

---

### Recommended Setup (8 hours)
- ✅ Everything above (4 hours)
- ✅ 2 hours: Expand CLAUDE.md (more patterns, gotchas)
- ✅ 1 hour: 5 more examples (state, hooks, errors, auth, forms)
- ✅ 1 hour: 3 more library docs

**Result:** Can generate and execute complex PRPs with confidence 8+

---

### Complete Setup (20 hours)
- ✅ Everything above (8 hours)
- ✅ 4 hours: Comprehensive CLAUDE.md (all patterns documented)
- ✅ 4 hours: 10+ examples covering all patterns
- ✅ 2 hours: 5-7 library docs (all key libraries)
- ✅ 2 hours: API spec integration (if applicable)

**Result:** Can generate and execute any PRP with confidence 9-10

---

## Next Steps

1. **Block 4 hours** on your calendar
2. **Follow 30-minute quick setup** (Steps 1-5)
3. **Follow 2-hour core setup** (Steps 6-7)
4. **Test with first feature** (Steps 8-12)
5. **Iterate based on results**
6. **Gradually expand** as you discover patterns

**Remember:** This is a living system. You'll add examples, update docs, and refine conventions as you build. Don't aim for perfection on day 1—aim for "good enough to start."

---

## Success Indicators

**You'll know it's working when:**
- ✅ PRPs generate with confidence 7+
- ✅ AI asks <2 clarifying questions per feature
- ✅ Generated code follows your patterns
- ✅ Validation passes on first try (80%+ of the time)
- ✅ Features ship 50%+ faster than before
- ✅ Fewer bugs in QA/production
- ✅ New developers onboard faster

**If you're not seeing these results:**
- Add more examples
- Expand CLAUDE.md
- Make patterns more explicit
- Ensure examples are high-quality and working

---

## Resources

**EZMobile Project** (reference implementation):
- `.claude/CLAUDE.md` - Comprehensive conventions example
- `.claude/commands/` - All 12 slash commands
- `examples/` - 15 working code patterns
- `PRPs/ai_docs/` - 6 library documentation files

**Comprehensive Guide:**
- See `docs/CONTEXT_ENGINEERING_REUSABILITY_GUIDE.md` for detailed explanations

**External Resources:**
- Cole Medin's Context Engineering: https://github.com/coleam00/context-engineering-intro
- Wirasm PRPs: https://github.com/Wirasm/PRPs-agentic-eng

---

## Questions?

**Most common questions:**

**Q: Do I need all 20 hours of setup?**
A: No! Start with 4-hour minimum viable setup, expand as needed.

**Q: What if my tech stack is different?**
A: The structure is universal, just replace content (examples, patterns, libraries).

**Q: Can I skip examples/?**
A: No—examples are critical. AI learns from working code, not descriptions.

**Q: How many examples do I need?**
A: Minimum 3 (API, component, test). Recommended 10+. More = better results.

**Q: What if I don't have an API spec?**
A: Skip Phase 5. API spec is optional but highly recommended if you have one.

**Q: Can I use this for backend projects?**
A: Yes! Same structure, just adapt examples (endpoints, ORM, etc.).

**Q: Can I use this for non-TypeScript projects?**
A: Yes! Python, Go, Rust, etc. all work. Just adapt examples and patterns.

---

## Final Tips

1. **Start small** - Get first PRP working, then expand
2. **Copy patterns** - Don't reinvent, adapt EZMobile's structure
3. **Prioritize examples** - They're the most critical component
4. **Iterate quickly** - Run first test in 4 hours, not 20
5. **Document gotchas** - Add them to CLAUDE.md as you discover them
6. **Trust the process** - It feels like a lot upfront, but it pays off fast

**Now go build something! 🚀**
