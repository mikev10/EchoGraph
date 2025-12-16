# PRP: Role-Based Workflow Adoption

**Generated**: 2025-12-15
**Status**: DRAFT
**Parent Task**: Documentation Enhancement
**Related Proposals**:
- `PRPs/feature-requests/product-workflow-redesign-PROPOSAL.md`
- `PRPs/feature-requests/product-workflow-quickref-PROPOSAL.md`

---

## Confidence Score

**8/10** - Clear scope, well-defined changes, addresses specific user feedback

Documentation-focused changes with clear source material from proposals and direct user feedback about workflow confusion.

---

## Problem Statement

### User Feedback Received

> "It is a great system but it's confusing to understand the order to execute commands and who is responsible for each step."

> "Do I create a plan first or feature request? I see there are also commands to create user stories, how is that different from feature requests?"

> "I think there should be a clear set of agents, commands, and skills organized as real team members in the product team (PM, BA, PO, etc) with clear guide how to use them and when to use them and what order."

> "PRPs are one of the most critical files to ensure proper execution of features but the order seems complicated to understand and might even skip a few steps."

### Core Issues to Address

| Issue | Root Cause | Solution |
|-------|------------|----------|
| Confusing command order | No clear hierarchy documentation | Artifact Hierarchy Guide |
| Unclear responsibilities | Commands not grouped by role | Role-based namespaces |
| Plan vs Feature vs Story confusion | Missing "when to use what" guide | Decision Tree + Definitions |
| PRP entry point unclear | Only one documented path | Dual paths: Feature→PRP AND Story→PRP |
| Missing step-by-step guide | No scannable quick reference | Comprehensive Quick Reference |

---

## Feature Overview

### What
Update EchoGraph documentation to provide:
1. **Clear artifact hierarchy** showing the relationship between Initiatives, Epics, Features, Stories, and PRPs
2. **Role-based command namespaces** (`/pm:`, `/ba:`, `/po:`, `/dev:`, `/qa:`)
3. **Dual PRP generation paths** supporting both Feature→PRP and Story→PRP workflows
4. **Decision tree** helping users know where to start
5. **Quick reference documentation** as a scannable user guide
6. **Optional BA role** for teams needing requirements analysis separation

### Why
- Teams are confused about artifact order and relationships
- Commands don't indicate who should use them
- PRPs can be generated from features OR stories (both are valid)
- Agile/Scrum teams need workflows that match their existing processes

### Success Criteria
- [ ] Clear hierarchy diagram showing Initiative → Epic → Feature → Story → PRP → Task
- [ ] Decision tree answers "where do I start?"
- [ ] Both PRP paths documented (Feature→PRP for small work, Story→PRP for scrum teams)
- [ ] All commands use role-based namespaces
- [ ] Quick reference is scannable in < 5 minutes
- [ ] BA role documented as optional for enterprise teams

---

## Artifact Hierarchy & Definitions

### The Complete Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                      ARTIFACT HIERARCHY                          │
│            (Top = Strategic, Bottom = Tactical)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INITIATIVE (Optional - Portfolio/Program level)                │
│  ├── Definition: Strategic business objective spanning quarters │
│  ├── Example: "Improve customer retention by 20%"               │
│  ├── Owner: Executive / Senior PM                               │
│  ├── Scope: Multiple epics, cross-team                          │
│  └── Command: /pm:initiative                                    │
│                                                                  │
│      │                                                           │
│      ▼                                                           │
│                                                                  │
│  EPIC (Groups related features toward a goal)                   │
│  ├── Definition: Large body of work delivering business value   │
│  ├── Example: "Self-service account management"                 │
│  ├── Owner: Product Manager                                     │
│  ├── Scope: Multiple features, 1-3 months                       │
│  └── Command: /pm:epic                                          │
│                                                                  │
│      │                                                           │
│      ▼                                                           │
│                                                                  │
│  FEATURE (Deliverable capability)                               │
│  ├── Definition: User-facing functionality that delivers value  │
│  ├── Example: "Password reset via email"                        │
│  ├── Owner: Product Manager / Product Owner                     │
│  ├── Scope: Multiple stories OR single PRP, 1-4 weeks           │
│  ├── Command: /pm:feature or /po:feature                        │
│  └── NOTE: Can generate PRP directly (Path A - small features)  │
│                                                                  │
│      │                                                           │
│      ▼                                                           │
│                                                                  │
│  USER STORY (Sprint-sized work item)                            │
│  ├── Definition: Smallest unit of value from user perspective   │
│  ├── Example: "As a user, I want to request a password reset"   │
│  ├── Owner: Product Owner (refined by BA if present)            │
│  ├── Scope: Fits in a sprint, 1-5 days of dev work              │
│  ├── Command: /po:story or /ba:story                            │
│  └── NOTE: Generates PRP when dev picks up (Path B - DEFAULT)   │
│                                                                  │
│      │                                                           │
│      ▼                                                           │
│                                                                  │
│  PRP - Product Requirements Prompt (Implementation plan)        │
│  ├── Definition: Technical implementation plan for AI execution │
│  ├── Example: "PRP-042: Password Reset Implementation"          │
│  ├── Owner: Developer                                           │
│  ├── Scope: Steps, files, validation criteria                   │
│  ├── Command: /dev:prp [story-id] or /dev:prp [feature-id]      │
│  └── NOTE: The bridge between "what" and "how"                  │
│                                                                  │
│      │                                                           │
│      ▼                                                           │
│                                                                  │
│  TASK (Atomic work unit within PRP)                             │
│  ├── Definition: Single step in PRP execution                   │
│  ├── Example: "Create database migration for reset_tokens"      │
│  ├── Owner: Developer                                           │
│  ├── Scope: Minutes to hours                                    │
│  └── Command: /dev:execute [prp-id] --step N                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Artifact Definitions Summary

| Artifact | What It Is | Who Owns It | Typical Size |
|----------|------------|-------------|--------------|
| **Initiative** | Strategic business goal | Executive/Sr. PM | Quarters |
| **Epic** | Large feature group | PM | 1-3 months |
| **Feature** | Deliverable capability | PM/PO | 1-4 weeks |
| **User Story** | Sprint-sized user value | PO (+ BA) | 1-5 days |
| **PRP** | Technical implementation plan | Developer | Per story/feature |
| **Task** | Atomic PRP step | Developer | Minutes-hours |

---

## Two PRP Generation Paths

### Why Two Paths?

Different situations call for different entry points:

| Scenario | Recommended Path | Why |
|----------|------------------|-----|
| Small feature, solo dev | Feature → PRP | Less overhead, faster |
| Scrum team with backlog | Story → PRP | Matches existing workflow |
| Bug fix | Story → PRP | Already sized for sprint |
| Spike/research | Feature → PRP | Exploratory, not story-sized |
| Large feature, team effort | Feature → Stories → PRPs | Divide and conquer |

### Path A: Feature → PRP (Direct Implementation)

```
┌──────────────────────────────────────────────────────────────┐
│                    PATH A: FEATURE → PRP                      │
│              (Small features, solo devs, spikes)              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. PM/PO creates feature                                    │
│     /pm:feature "Add password reset via email"               │
│         │                                                     │
│         ▼                                                     │
│  2. (Optional) BA enriches with requirements                 │
│     /ba:requirements [feature-id]                            │
│         │                                                     │
│         ▼                                                     │
│  3. Developer generates PRP from feature                     │
│     /dev:prp [feature-id]                                    │
│         │                                                     │
│         ▼                                                     │
│  4. Developer executes PRP                                   │
│     /dev:execute [prp-id]                                    │
│         │                                                     │
│         ▼                                                     │
│  5. QA generates test plan                                   │
│     /qa:test-plan [prp-id]                                   │
│                                                               │
└──────────────────────────────────────────────────────────────┘

Best for:
• Features < 1 week of work
• Solo developers
• Spikes and research tasks
• Hotfixes that need full context
```

### Path B: Feature → Stories → PRP (Scrum/Agile Default)

```
┌──────────────────────────────────────────────────────────────┐
│              PATH B: FEATURE → STORIES → PRP                  │
│           (Scrum teams, standard agile workflow)              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. PM creates feature                                       │
│     /pm:feature "Add password reset via email"               │
│         │                                                     │
│         ▼                                                     │
│  2. PO/BA breaks feature into stories                        │
│     /po:story "Request password reset" --feature [id]        │
│     /po:story "Receive reset email" --feature [id]           │
│     /po:story "Set new password" --feature [id]              │
│         │                                                     │
│         ▼                                                     │
│  3. (Optional) BA refines acceptance criteria                │
│     /ba:acceptance-criteria [story-id]                       │
│         │                                                     │
│         ▼                                                     │
│  4. Stories go to backlog, dev picks one                     │
│     [Standard sprint planning / backlog grooming]            │
│         │                                                     │
│         ▼                                                     │
│  5. Developer generates PRP from story ← KEY STEP            │
│     /dev:prp [story-id]                                      │
│         │                                                     │
│         ▼                                                     │
│  6. Developer executes PRP                                   │
│     /dev:execute [prp-id]                                    │
│         │                                                     │
│         ▼                                                     │
│  7. QA generates test plan                                   │
│     /qa:test-plan [story-id]                                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘

Best for:
• Features > 1 week of work
• Teams using Scrum/Kanban
• Multiple developers on same feature
• Standard sprint-based development
```

---

## Decision Tree: Where Do I Start?

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHERE DO I START?                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Q1: What do you have?                                          │
│      │                                                           │
│      ├── "A vague idea or business goal"                        │
│      │       → Start with /pm:initiative or /pm:epic            │
│      │                                                           │
│      ├── "A specific feature to build"                          │
│      │       → Start with /pm:feature                           │
│      │       │                                                   │
│      │       └── Q2: How big is it?                             │
│      │               │                                           │
│      │               ├── "< 1 week, solo dev"                   │
│      │               │       → Path A: /dev:prp [feature-id]    │
│      │               │                                           │
│      │               └── "> 1 week or team effort"              │
│      │                       → Path B: Break into stories first │
│      │                         /po:story --feature [id]         │
│      │                                                           │
│      ├── "A user story ready to implement"                      │
│      │       → /dev:prp [story-id]                              │
│      │                                                           │
│      ├── "A bug to fix"                                         │
│      │       → /po:story "Bug: [description]"                   │
│      │       → /dev:prp [story-id]                              │
│      │                                                           │
│      ├── "Customer feedback or support tickets"                 │
│      │       → /support:feedback-patterns                       │
│      │       → /pm:feature (from patterns)                      │
│      │                                                           │
│      └── "An existing PRP to execute"                           │
│              → /dev:execute [prp-id]                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Decision Matrix

| I have... | I should run... | Then... |
|-----------|-----------------|---------|
| Business goal | `/pm:initiative` | Break into epics |
| Large scope idea | `/pm:epic` | Break into features |
| Feature to build (small) | `/pm:feature` → `/dev:prp` | Execute PRP |
| Feature to build (large) | `/pm:feature` → `/po:story` | Stories → PRPs |
| Story ready for dev | `/dev:prp [story-id]` | Execute PRP |
| Bug report | `/po:story` → `/dev:prp` | Execute PRP |
| Customer feedback | `/support:feedback-patterns` | Create features |
| PRP ready | `/dev:execute [prp-id]` | Code! |

---

## Role Responsibility Matrix

### Who Does What?

| Role | Primary Responsibilities | Commands |
|------|-------------------------|----------|
| **PM** | Strategy, roadmap, features, priorities | `/pm:initiative`, `/pm:epic`, `/pm:feature` |
| **PO** | Backlog, stories, acceptance criteria, sprint scope | `/po:story`, `/po:prioritize`, `/po:publish` |
| **BA** (Optional) | Requirements analysis, acceptance criteria, gaps | `/ba:analyze`, `/ba:requirements`, `/ba:gaps` |
| **Dev** | PRPs, implementation, code execution | `/dev:prp`, `/dev:execute`, `/dev:impact` |
| **QA** | Test plans, edge cases, regression risks | `/qa:test-plan`, `/qa:edge-cases` |
| **Support** | Feedback patterns, ticket linking | `/support:feedback-patterns`, `/support:link-ticket` |

### Role Flow Through Artifacts

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROLE OWNERSHIP BY ARTIFACT                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Initiative ──────────────────────────────────────── PM         │
│       │                                                          │
│       ▼                                                          │
│  Epic ────────────────────────────────────────────── PM         │
│       │                                                          │
│       ▼                                                          │
│  Feature ─────────────────────────────────────────── PM/PO      │
│       │                                                          │
│       ▼                                                          │
│  User Story ──────────────────────────────────────── PO (+BA)   │
│       │                                                          │
│       │  ┌─────────────────────────────────────────────────┐    │
│       │  │ HANDOFF: PO → Dev (sprint planning/pickup)      │    │
│       │  └─────────────────────────────────────────────────┘    │
│       ▼                                                          │
│  PRP ─────────────────────────────────────────────── Dev        │
│       │                                                          │
│       ▼                                                          │
│  Code + Tests ────────────────────────────────────── Dev + QA   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Command Namespace Reference

### All Commands by Role

#### PM Commands (`/pm:`)
```
/pm:initiative "description"          # Create strategic initiative
/pm:epic "description"                # Create epic
/pm:feature "description"             # Create feature
/pm:roadmap                           # View/manage roadmap
/pm:prioritize [id]                   # Set priority
```

#### PO Commands (`/po:`)
```
/po:story "description"               # Create user story
/po:story --feature [id]              # Create story under feature
/po:backlog                           # View/manage backlog
/po:refine [story-id]                 # Refine story details
/po:publish [story-id]                # Sync to Jira/ADO
/po:accept [story-id]                 # Mark story accepted
```

#### BA Commands (`/ba:`) - Optional Role
```
/ba:analyze [feature-id]              # Deep requirements analysis
/ba:requirements [id]                 # Generate requirements doc
/ba:gaps [story-id]                   # Find requirement gaps
/ba:acceptance-criteria [id]          # Generate/refine AC
/ba:workshop-prep [feature]           # Prepare refinement session
```

#### Dev Commands (`/dev:`)
```
/dev:prp [story-id]                   # Generate PRP from story
/dev:prp [feature-id]                 # Generate PRP from feature
/dev:execute [prp-id]                 # Execute PRP step-by-step
/dev:execute [prp-id] --step N        # Execute specific step
/dev:impact [file-path]               # Impact analysis
/dev:patterns [topic]                 # Find code patterns
/dev:context [question]               # Query knowledge graph
```

#### QA Commands (`/qa:`)
```
/qa:test-plan [story-id]              # Generate test plan from story
/qa:test-plan [prp-id]                # Generate test plan from PRP
/qa:edge-cases [feature]              # Identify edge cases
/qa:regression-risks [component]      # Find regression risks
/qa:test-data [scenario]              # Generate test data
```

#### Support Commands (`/support:`)
```
/support:feedback-patterns [days]     # Analyze feedback patterns
/support:link-ticket [ticket] [id]    # Link ticket to feature/story
/support:draft-story [pattern]        # Draft story from feedback
```

---

## Implementation Steps

### Step 1: Create Comprehensive Quick Reference
**Goal**: Single document answering "where do I start?" and "what order?"

**Tasks**:
- [ ] Create `WORKFLOW-QUICKREF.md` in Obsidian vault
- [ ] Include artifact hierarchy diagram
- [ ] Include decision tree
- [ ] Include both PRP paths (A and B)
- [ ] Include role responsibility matrix
- [ ] Include all commands by role
- [ ] Make it scannable (tables, diagrams, minimal prose)

**Files to Create**:
- `C:\Users\Mike\Documents\Obsidian Vault\echograph\WORKFLOW-QUICKREF.md`

**Expected Outcome**: New user can understand the system in < 5 minutes

---

### Step 2: Update PHASE-2-TEAM-PLATFORM.md
**Goal**: Align with new hierarchy and dual PRP paths

**Tasks**:
- [ ] Update artifact hierarchy section (currently lines ~153-200)
- [ ] Add "Two PRP Generation Paths" section
- [ ] Update PM/PO Assistant commands to use namespaces (lines ~233-242)
- [ ] Update Developer Assistant commands (lines ~305-313)
- [ ] Update QA Assistant commands (lines ~374-379)
- [ ] Update Support Assistant commands (lines ~436-438)
- [ ] Add optional BA Assistant section
- [ ] Update workflow diagram to show both paths (lines ~452-512)
- [ ] Update MCP integration examples with new commands

**Files to Modify**:
- `C:\Users\Mike\Documents\Obsidian Vault\echograph\PHASE-2-TEAM-PLATFORM.md`

**Expected Outcome**: Document reflects dual paths and role-based commands

---

### Step 3: Update UNIFIED-VISION.md
**Goal**: Add artifact hierarchy and BA role to vision

**Tasks**:
- [ ] Add artifact hierarchy section with definitions
- [ ] Add BA role to Role Definitions as optional
- [ ] Add command namespace convention explanation
- [ ] Update any existing command examples

**Files to Modify**:
- `C:\Users\Mike\Documents\Obsidian Vault\echograph\UNIFIED-VISION.md`

**Expected Outcome**: Vision doc sets foundation for hierarchy and roles

---

### Step 4: Update IMPLEMENTATION-ROADMAP.md
**Goal**: Ensure roadmap aligns with artifact hierarchy

**Tasks**:
- [ ] Update Phase 2 CLI commands to use namespaces
- [ ] Add note about dual PRP paths
- [ ] Add BA Assistant as optional Phase 2 item
- [ ] Update any inline command examples

**Files to Modify**:
- `C:\Users\Mike\Documents\Obsidian Vault\echograph\IMPLEMENTATION-ROADMAP.md`

**Expected Outcome**: Roadmap consistent with new workflow

---

### Step 5: Update PHASE-3-LANGGRAPH-WORKFLOW.md
**Goal**: Ensure workflow supports both PRP entry points

**Tasks**:
- [ ] Update workflow states to support Feature→PRP path
- [ ] Update workflow states to support Story→PRP path
- [ ] Update command examples with namespaces
- [ ] Verify human gates match role responsibilities

**Files to Modify**:
- `C:\Users\Mike\Documents\Obsidian Vault\echograph\PHASE-3-LANGGRAPH-WORKFLOW.md`

**Expected Outcome**: LangGraph workflow supports dual paths

---

### Step 6: Update GitHub EchoGraph Documentation
**Goal**: Sync GitHub repo with Obsidian changes

**Tasks**:
- [ ] Update `.claude/PLANNING.md` with artifact hierarchy
- [ ] Update PRP templates with new command references
- [ ] Create GitHub version of quick reference if needed
- [ ] Update `.claude/commands/` to use new naming convention

**Files to Review/Modify**:
- `C:\Users\Mike\Documents\GitHub\EchoGraph\.claude\PLANNING.md`
- `C:\Users\Mike\Documents\GitHub\EchoGraph\.claude\commands\*.md`
- `C:\Users\Mike\Documents\GitHub\EchoGraph\PRPs\templates\*.md`

**Expected Outcome**: GitHub repo aligned with Obsidian vault

---

### Step 7: Cross-Reference Validation
**Goal**: Ensure consistency across all documents

**Tasks**:
- [ ] Search for old command patterns (`/story`, `/prp`, etc.)
- [ ] Verify all cross-document links work
- [ ] Ensure BA role consistently marked optional
- [ ] Verify both PRP paths documented consistently
- [ ] Update document changelogs

**Validation**:
```bash
# Search for old command patterns
grep -rn "^/story\|^/prp\|^/test-plan\|^/execute" "C:\Users\Mike\Documents\Obsidian Vault\echograph\"
# Should return no results after migration

# Search for new patterns to confirm
grep -rn "/pm:\|/dev:\|/po:\|/qa:" "C:\Users\Mike\Documents\Obsidian Vault\echograph\"
# Should return many results
```

**Expected Outcome**: Zero inconsistencies across all documentation

---

## Quick Reference Document Structure

The new `WORKFLOW-QUICKREF.md` should be structured for scannability:

```markdown
# EchoGraph Workflow Quick Reference

## TL;DR: Where Do I Start?
[Decision tree - 10 lines max]

## Artifact Hierarchy
[Visual diagram from this plan]

## Two Ways to Generate PRPs
[Path A and Path B side by side]

## Commands by Role
[Tables for PM, PO, BA, Dev, QA, Support]

## Role Handoffs
[Who hands off to whom at each stage]

## Common Workflows
### "I have a feature idea" → [steps]
### "I picked up a story from backlog" → [steps]
### "I need to fix a bug" → [steps]
### "I see customer feedback patterns" → [steps]
```

---

## BA Role Details

### When to Enable BA Role

| Team Size | Recommendation |
|-----------|----------------|
| 1-5 developers | Skip - PO handles requirements |
| 6-15 developers | Optional - if POs are overloaded |
| 15+ developers | Recommended - dedicated requirements |

### BA vs PO Responsibility Split

| Activity | Without BA | With BA |
|----------|------------|---------|
| Story creation | PO | PO |
| Acceptance criteria | PO | **BA** |
| Requirements analysis | PO | **BA** |
| Gap identification | PO + Dev | **BA** |
| Refinement facilitation | PO | **BA** |
| Backlog prioritization | PO | PO |
| Sprint planning | PO | PO |

---

## Addressing Original Feedback

| Original Feedback | How This Plan Addresses It |
|-------------------|----------------------------|
| "Confusing order to execute commands" | Decision tree + artifact hierarchy |
| "Who is responsible for each step" | Role-based namespaces + responsibility matrix |
| "Step-by-step guide for agile/scrum" | Quick reference + Path B (Story→PRP) |
| "Plan vs feature request vs user story confusion" | Clear definitions + hierarchy diagram |
| "Clear set of agents organized as team members" | Commands grouped by role (/pm:, /dev:, etc.) |
| "Research → plan → features → stories → PRPs order" | Artifact hierarchy with flow arrows |
| "PRPs skip steps" | Two paths documented - choose based on context |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Users still confused | Low | Medium | Decision tree + examples |
| Old command references missed | Medium | Low | Grep validation step |
| Path A vs B confusion | Medium | Low | Clear "best for" guidance |
| BA role overcomplicates | Low | Low | Clearly marked optional |

---

## Execution Checklist

### Pre-Execution
- [ ] Read all related proposals
- [ ] Have Obsidian vault and GitHub repo accessible
- [ ] Note current document versions

### Execution (in order)
- [ ] Step 1: Create WORKFLOW-QUICKREF.md (foundation)
- [ ] Step 2: Update PHASE-2-TEAM-PLATFORM.md (main content)
- [ ] Step 3: Update UNIFIED-VISION.md (vision alignment)
- [ ] Step 4: Update IMPLEMENTATION-ROADMAP.md (roadmap)
- [ ] Step 5: Update PHASE-3-LANGGRAPH-WORKFLOW.md (workflow)
- [ ] Step 6: Update GitHub EchoGraph docs (sync)
- [ ] Step 7: Cross-reference validation (quality)

### Post-Execution
- [ ] Archive proposal docs to `PRPs/completed/`
- [ ] Update TASK.md with completion
- [ ] Commit GitHub changes

---

## References

- **Source Proposals**:
  - `PRPs/feature-requests/product-workflow-redesign-PROPOSAL.md`
  - `PRPs/feature-requests/product-workflow-quickref-PROPOSAL.md`
- **Target Documents**:
  - Obsidian: `C:\Users\Mike\Documents\Obsidian Vault\echograph\`
  - GitHub: `C:\Users\Mike\Documents\GitHub\EchoGraph\`
- **User Feedback**: Original prompt requesting workflow improvements
