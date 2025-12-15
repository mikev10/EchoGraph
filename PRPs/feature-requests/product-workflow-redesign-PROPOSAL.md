# Product Workflow Redesign Proposal

**Status**: DRAFT
**Created**: 2024-12-14
**Author**: Claude (based on product team feedback analysis)

---

## Executive Summary

This proposal redesigns the EchoGraph product workflow to align with industry-standard agile practices. The key changes:

1. **Invert the hierarchy** - Features become parents of user stories (not derived from them)
2. **Add strategic layers** - Introduce Initiatives and Epics for PM-level planning
3. **Role-based organization** - Clear command ownership by PM, BA, PO, Dev Lead, QA Lead
4. **Single workflow guide** - One document explaining the complete flow

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Proposed Hierarchy](#proposed-hierarchy)
3. [Role Definitions](#role-definitions)
4. [Document Types](#document-types)
5. [Command Structure](#command-structure)
6. [Workflow Stages](#workflow-stages)
7. [Directory Structure](#directory-structure)
8. [Migration Plan](#migration-plan)
9. [Implementation Phases](#implementation-phases)

---

## Problem Statement

### User Feedback Themes

1. "Confusing to understand the order to execute commands and who is responsible"
2. "Need a clear step-by-step guide for agile/scrum teams"
3. "Do I create a plan first or feature request? How are user stories different?"
4. "Should organize as real team members (PM, BA, PO) with clear guides"
5. "PRPs are critical but the order is complicated and might skip steps"

### Root Cause

The current workflow inverts the standard agile hierarchy:

```
CURRENT (Inverted):
User Story → Feature Request (SPEC.md) → PRP → Tasks
     ↑
   START

INDUSTRY STANDARD:
Initiative → Epic → Feature → User Stories → Tasks/PRPs
                       ↑
                     START (for most teams)
```

---

## Proposed Hierarchy

### Visual Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ECHOGRAPH WORK HIERARCHY                             │
└─────────────────────────────────────────────────────────────────────────────┘

STRATEGIC LAYER (Roadmap)
══════════════════════════════════════════════════════════════════════════════
│
├── INITIATIVE                                          Owner: Product Manager
│   "Q1 2025 - Mobile App Launch"
│   ├── Business case, ROI, success metrics
│   ├── Timeline: Multi-quarter
│   └── Contains: 1-N Epics
│
├── EPIC                                                Owner: Product Manager
│   "User Authentication System"
│   ├── High-level scope, dependencies
│   ├── Timeline: 1-3 months
│   └── Contains: 1-N Features
│
TACTICAL LAYER (Backlog)
══════════════════════════════════════════════════════════════════════════════
│
├── FEATURE                                             Owner: PO / BA
│   "Password Reset via Email"
│   ├── Business requirements, acceptance criteria
│   ├── Timeline: 1-3 sprints
│   └── Contains: 1-N User Stories
│
├── USER STORY                                          Owner: PO / Dev
│   "Email validation during reset"
│   ├── As a / I want / So that
│   ├── Timeline: 1 sprint (1-3 days work)
│   └── Contains: 1 PRP (when ready for implementation)
│
EXECUTION LAYER (Implementation)
══════════════════════════════════════════════════════════════════════════════
│
├── PRP (Product Requirements Plan)                     Owner: Dev Lead
│   "Password Reset Implementation Guide"
│   ├── Step-by-step implementation
│   ├── Timeline: Hours to days
│   └── Contains: N Tasks (auto-generated)
│
└── TASK                                                Owner: Developer
    "Add email validation regex"
    ├── Granular code changes
    └── Timeline: Minutes to hours
```

### Hierarchy Rules

| Level | Parent | Children | Typical Count | Sprint Fit |
|-------|--------|----------|---------------|------------|
| Initiative | (Roadmap) | Epics | 2-5 per quarter | Multi-quarter |
| Epic | Initiative | Features | 3-10 per epic | 1-3 months |
| Feature | Epic | User Stories | 2-8 per feature | 1-3 sprints |
| User Story | Feature | PRP/Tasks | 1 PRP per story | 1 sprint |
| PRP | User Story | Tasks | 5-15 tasks per PRP | Days |
| Task | PRP | — | — | Hours |

---

## Role Definitions

### Product Manager (PM)

**Focus**: Strategy, vision, market fit, ROI

**Responsibilities**:
- Define initiatives based on business goals
- Break initiatives into epics
- Prioritize epics on roadmap
- Track initiative success metrics
- Stakeholder communication

**Artifacts Created**:
- Initiatives (business case, ROI)
- Epics (scope, dependencies)
- Roadmap views

**Does NOT do**:
- Write detailed user stories
- Technical specifications
- Sprint-level planning

---

### Business Analyst (BA)

**Focus**: Requirements elicitation, process analysis, documentation

**Responsibilities**:
- Analyze features to understand requirements
- Decompose features into user stories
- Document business rules and edge cases
- Bridge between business and technical teams
- Validate requirements completeness

**Artifacts Created**:
- Feature specifications (detailed requirements)
- User story drafts
- Process flows and business rules
- Requirements traceability

**Does NOT do**:
- Strategic prioritization (PM role)
- Sprint planning (PO role)
- Technical architecture (Dev Lead role)

---

### Product Owner (PO)

**Focus**: Backlog management, sprint priorities, value maximization

**Responsibilities**:
- Prioritize features in backlog
- Refine user stories with team
- Accept/reject completed work
- Sprint planning participation
- Represent customer voice

**Artifacts Created**:
- Prioritized backlog
- User stories (final approval)
- Acceptance decisions

**Does NOT do**:
- Create initiatives/epics (PM role)
- Detailed requirements analysis (BA role)
- Technical implementation (Dev role)

---

### Dev Lead

**Focus**: Technical leadership, architecture, implementation guidance

**Responsibilities**:
- Add technical context to stories
- Create PRPs for implementation
- Architecture decisions
- Code review oversight
- Technical risk identification

**Artifacts Created**:
- Technical specifications
- PRPs (implementation guides)
- Architecture decisions
- Code review feedback

---

### QA Lead

**Focus**: Quality assurance, test strategy, acceptance criteria

**Responsibilities**:
- Add test scenarios to stories
- Validate Definition of Ready
- Create test plans
- Acceptance testing

**Artifacts Created**:
- Test scenarios
- Test plans
- QA context in stories
- Bug reports

---

## Document Types

### 1. Initiative Document

**Purpose**: Define strategic business objective
**Created by**: Product Manager
**Location**: `PRPs/initiatives/`
**Filename**: `YYYY-QN-initiative-name.md`

```markdown
# Initiative: [Name]

**ID**: INI-YYYY-QN-NNN
**Status**: Draft | Active | Completed | Cancelled
**Owner**: [PM Name]
**Timeline**: Q1 2025 - Q2 2025

## Business Case

### Problem Statement
[What business problem does this solve?]

### Opportunity
[What is the market/business opportunity?]

### Success Metrics
- [ ] Metric 1: [Target]
- [ ] Metric 2: [Target]

### ROI Estimate
[Expected return on investment]

## Scope

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Item 1]

## Epics

| Epic ID | Name | Status | Target |
|---------|------|--------|--------|
| EPIC-001 | [Name] | Draft | Q1 2025 |

## Stakeholders
- Executive Sponsor: [Name]
- Product Manager: [Name]
- Engineering Lead: [Name]

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [Plan] |

## Timeline
[High-level milestones]
```

---

### 2. Epic Document

**Purpose**: Define major deliverable within initiative
**Created by**: Product Manager
**Location**: `PRPs/epics/`
**Filename**: `EPIC-NNN-epic-name.md`

```markdown
# Epic: [Name]

**ID**: EPIC-NNN
**Parent Initiative**: INI-YYYY-QN-NNN
**Status**: Draft | Ready | In Progress | Done
**Owner**: [PM/PO Name]
**Target Release**: [Version or Date]

## Overview

### Description
[What is this epic about?]

### Business Value
[Why is this epic valuable?]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Features

| Feature ID | Name | Priority | Status | Stories |
|------------|------|----------|--------|---------|
| FEAT-001 | [Name] | P1 | Draft | 0/3 |

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Assumptions
- [Assumption 1]

## Constraints
- [Constraint 1]

## Notes
[Additional context]
```

---

### 3. Feature Document

**Purpose**: Define specific functionality to be built
**Created by**: PO or BA
**Location**: `PRPs/features/`
**Filename**: `FEAT-NNN-feature-name.md`

```markdown
# Feature: [Name]

**ID**: FEAT-NNN
**Parent Epic**: EPIC-NNN
**Status**: Draft | Ready | In Progress | Done
**Owner**: [PO/BA Name]
**Estimated Size**: S / M / L / XL

## Overview

### Description
[What does this feature do?]

### User Problem
[What user problem does this solve?]

### Business Value
[Why is this valuable to the business?]

## Acceptance Criteria (Feature Level)

- [ ] AC1: [Criterion]
- [ ] AC2: [Criterion]
- [ ] AC3: [Criterion]

## User Stories

| Story ID | Title | Status | Points |
|----------|-------|--------|--------|
| US-001 | [Title] | Draft | — |
| US-002 | [Title] | Draft | — |

## Requirements

### Functional Requirements
1. [FR1]
2. [FR2]

### Non-Functional Requirements
1. [NFR1 - Performance]
2. [NFR2 - Security]

## UI/UX Considerations
[Wireframes, mockups, or descriptions]

## Technical Considerations
[High-level technical notes - detailed specs in PRP]

## Out of Scope
- [Item explicitly excluded]

## Open Questions
- [ ] Question 1?
- [ ] Question 2?

## Notes
[Additional context]
```

---

### 4. User Story Document

**Purpose**: Define specific user need within a feature
**Created by**: PO, BA, or Dev
**Location**: `PRPs/user-stories/`
**Filename**: `US-NNN-story-name.md`

```markdown
# User Story: [Title]

**ID**: US-NNN
**Parent Feature**: FEAT-NNN
**Status**: Draft | Enriched | Ready | In Sprint | Done
**Owner**: [PO Name]
**Story Points**: [1-13]

## User Story

As a [specific user type]
I want [goal/desire]
So that [benefit/value]

## Acceptance Criteria

### Scenario 1: [Happy Path]
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

### Scenario 2: [Alternate Path]
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

### Scenario 3: [Error Case]
- **Given** [precondition]
- **When** [action]
- **Then** [expected error handling]

## Technical Context
<!-- Added by Dev Lead via /story:enrich-tech -->

### Architecture Approach
[How this fits into system architecture]

### API Changes
[New or modified endpoints]

### Data Model Changes
[Database/schema changes]

### Security Considerations
[Auth, validation, etc.]

## QA Context
<!-- Added by QA Lead via /story:enrich-qa -->

### Test Scenarios
[Comprehensive test cases]

### Edge Cases
[Boundary conditions]

### Test Data Requirements
[Data needed for testing]

## Definition of Ready Checklist
- [ ] User story follows format
- [ ] Acceptance criteria are testable
- [ ] Technical context added
- [ ] QA context added
- [ ] Story is sized
- [ ] Dependencies identified
- [ ] No blocking questions

## Notes
[Additional context]
```

---

### 5. PRP (Product Requirements Plan)

**Purpose**: Detailed implementation guide for a user story or small feature
**Created by**: Dev Lead
**Location**: `PRPs/active/` → `PRPs/completed/`
**Filename**: `PRP-NNN-implementation-name.md`

*(Structure remains similar to current PRP template with added parent linkage)*

```markdown
# PRP: [Implementation Name]

**ID**: PRP-NNN
**Parent Story**: US-NNN (or FEAT-NNN for small features)
**Status**: Draft | In Progress | Completed
**Owner**: [Dev Lead Name]
**Task File**: .claude/tasks/TASK-NNN-name.md

## Overview
[What this PRP implements]

## Implementation Steps
[Detailed steps - existing format]

## Completion Summary
<!-- Added after execution -->
[What was actually implemented]
```

---

## Command Structure

### Command Naming Convention

```
/[role]:[action]-[artifact]
```

Examples:
- `/pm:create-initiative`
- `/ba:analyze-feature`
- `/po:prioritize-backlog`
- `/dev:generate-prp`
- `/qa:add-test-scenarios`

---

### Product Manager Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/pm:create-initiative` | Create new strategic initiative | Business need | `initiatives/INI-*.md` |
| `/pm:create-epic` | Create epic within initiative | Initiative ID + scope | `epics/EPIC-*.md` |
| `/pm:view-roadmap` | Display initiative/epic timeline | — | Roadmap view |
| `/pm:prioritize-epics` | Reorder epic priorities | Epic IDs | Updated priorities |
| `/pm:initiative-status` | Check initiative progress | Initiative ID | Status report |

---

### Business Analyst Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/ba:create-feature` | Create feature from epic | Epic ID + description | `features/FEAT-*.md` |
| `/ba:analyze-feature` | Research and document requirements | Feature ID | Updated feature doc |
| `/ba:decompose-feature` | Break feature into user stories | Feature ID | Multiple `US-*.md` |
| `/ba:document-rules` | Add business rules to feature | Feature ID + rules | Updated feature |

---

### Product Owner Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/po:create-story` | Create user story in feature | Feature ID + need | `user-stories/US-*.md` |
| `/po:view-backlog` | Display prioritized backlog | — | Backlog view |
| `/po:prioritize-backlog` | Reorder story priorities | Story IDs | Updated priorities |
| `/po:validate-ready` | Check Definition of Ready | Story ID | Readiness report |
| `/po:accept-story` | Mark story as accepted | Story ID | Updated status |
| `/po:plan-sprint` | Select stories for sprint | Story IDs | Sprint backlog |

---

### Dev Lead Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/dev:enrich-story` | Add technical context | Story path | Updated story |
| `/dev:generate-prp` | Create implementation plan | Story/Feature ID | `active/PRP-*.md` |
| `/dev:execute-prp` | Implement PRP step-by-step | PRP path | Code changes |
| `/dev:archive-prp` | Move completed PRP | PRP path | `completed/PRP-*.md` |
| `/dev:three-amigos-prep` | Prepare alignment meeting | Story path | Meeting agenda |

---

### QA Lead Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/qa:enrich-story` | Add test scenarios | Story path | Updated story |
| `/qa:create-test-plan` | Create feature test plan | Feature ID | Test plan doc |
| `/qa:validate-ready` | Check story readiness | Story path | QA readiness report |

---

### Utility Commands (Any Role)

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/workflow:status` | Show current workflow state | — | Status dashboard |
| `/workflow:next-step` | Suggest next action for artifact | File path | Recommended command |
| `/workflow:trace` | Show artifact lineage | Any ID | Hierarchy view |

---

## Workflow Stages

### Stage 1: Strategic Planning (PM)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: STRATEGIC PLANNING                                      │
│ Owner: Product Manager                                           │
│ Frequency: Quarterly                                             │
└─────────────────────────────────────────────────────────────────┘

START: Business need or opportunity identified
  │
  ▼
/pm:create-initiative "Q1 2025 Mobile App Launch"
  │ Creates: PRPs/initiatives/2025-Q1-mobile-app-launch.md
  │
  ▼
/pm:create-epic "User Authentication"
  │ Creates: PRPs/epics/EPIC-001-user-authentication.md
  │
  ▼
/pm:view-roadmap
  │ Displays: Timeline of all initiatives and epics
  │
  ▼
GATE: Initiative approved by stakeholders?
  │
  ├── NO → Revise initiative
  │
  └── YES → Proceed to Stage 2
```

---

### Stage 2: Feature Definition (PM/BA/PO)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: FEATURE DEFINITION                                      │
│ Owners: PM (prioritize), BA (analyze), PO (refine)              │
│ Frequency: Monthly / Per Epic                                    │
└─────────────────────────────────────────────────────────────────┘

START: Epic approved and prioritized
  │
  ▼
/ba:create-feature "Password Reset via Email"
  │ Creates: PRPs/features/FEAT-001-password-reset.md
  │ Links to: EPIC-001
  │
  ▼
/ba:analyze-feature FEAT-001
  │ AI researches codebase, asks clarifying questions
  │ Updates: Feature requirements, technical notes
  │
  ▼
/ba:decompose-feature FEAT-001
  │ Creates: Multiple US-*.md files linked to FEAT-001
  │   - US-001-email-input-validation.md
  │   - US-002-reset-token-generation.md
  │   - US-003-password-update-flow.md
  │
  ▼
GATE: Features sized and prioritized?
  │
  └── YES → Proceed to Stage 3
```

---

### Stage 3: Story Refinement (Three Amigos)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: STORY REFINEMENT (Three Amigos)                        │
│ Owners: PO + Dev Lead + QA Lead                                 │
│ Frequency: Weekly / Per Sprint                                   │
└─────────────────────────────────────────────────────────────────┘

START: User stories drafted by BA/PO
  │
  ▼
/dev:enrich-story PRPs/user-stories/US-001-email-validation.md
  │ Dev Lead adds: Architecture, APIs, data model, security
  │
  ▼
/qa:enrich-story PRPs/user-stories/US-001-email-validation.md
  │ QA Lead adds: Test scenarios, edge cases, test data
  │
  ▼
/dev:three-amigos-prep PRPs/user-stories/US-001-email-validation.md
  │ Generates: Meeting agenda for 30-45 min alignment
  │
  ▼
[MEETING] Three Amigos Session
  │ PO + Dev Lead + QA Lead align on story
  │
  ▼
/po:validate-ready PRPs/user-stories/US-001-email-validation.md
  │ Checks: Definition of Ready criteria
  │
  ├── NOT READY → Address gaps, repeat refinement
  │
  └── READY → Proceed to Stage 4
```

---

### Stage 4: Sprint Planning (PO/Team)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: SPRINT PLANNING                                         │
│ Owners: PO (prioritize), Team (commit)                          │
│ Frequency: Per Sprint                                            │
└─────────────────────────────────────────────────────────────────┘

START: Stories marked as READY
  │
  ▼
/po:view-backlog
  │ Displays: All READY stories, prioritized
  │
  ▼
/po:plan-sprint US-001 US-002 US-003
  │ Creates: Sprint backlog with selected stories
  │ Updates: Story status to "In Sprint"
  │
  ▼
GATE: Team commits to sprint scope?
  │
  └── YES → Proceed to Stage 5
```

---

### Stage 5: Implementation (Dev Lead/Dev)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: IMPLEMENTATION                                          │
│ Owners: Dev Lead (PRP), Developers (execution)                  │
│ Frequency: Per Story                                             │
└─────────────────────────────────────────────────────────────────┘

START: Story in sprint, ready for implementation
  │
  ▼
/dev:generate-prp US-001
  │ Creates: PRPs/active/PRP-001-email-validation.md
  │ Creates: .claude/tasks/TASK-001-email-validation.md
  │ Links: PRP ↔ Story ↔ Task
  │
  ▼
/dev:execute-prp PRPs/active/PRP-001-email-validation.md
  │ Phase 0: Load context, create branch
  │ Phase 1: Validate with MCP servers
  │ Phase 2: Plan with ULTRATHINK
  │ Phase 3: Implement step-by-step
  │ Phase 4: Add completion summary
  │ Phase 5: Update task hierarchy
  │
  ▼
/review:create-pr
  │ Creates: Pull request for review
  │
  ▼
/review:review-pr
  │ AI reviews, posts feedback to GitHub
  │
  ▼
GATE: PR approved?
  │
  ├── NO → Address feedback, re-review
  │
  └── YES → Proceed to Stage 6
```

---

### Stage 6: Completion (PO/Team)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: COMPLETION                                              │
│ Owners: PO (accept), Dev Lead (archive)                         │
│ Frequency: Per Story                                             │
└─────────────────────────────────────────────────────────────────┘

START: PR merged, code deployed to test
  │
  ▼
[QA TESTING] Story tested against acceptance criteria
  │
  ▼
/po:accept-story US-001
  │ Updates: Story status to "Done"
  │ Updates: Feature progress (1/3 stories complete)
  │
  ▼
/dev:archive-prp PRPs/active/PRP-001-email-validation.md
  │ Moves: PRP to completed/
  │ Updates: Task file status
  │ Ingests: To local-rag for future reference
  │
  ▼
GATE: All stories in feature complete?
  │
  ├── NO → Continue with next story
  │
  └── YES → Feature complete!
              Update Epic progress
              (All epics done? Initiative complete!)
```

---

## Directory Structure

### Proposed Structure

```
PRPs/
├── README.md                    # This workflow guide
│
├── roadmap/
│   └── ROADMAP.md              # Visual timeline of initiatives
│
├── initiatives/                 # Strategic layer (PM)
│   ├── 2025-Q1-mobile-app.md
│   └── 2025-Q2-analytics.md
│
├── epics/                       # Major deliverables (PM)
│   ├── EPIC-001-authentication.md
│   └── EPIC-002-dashboard.md
│
├── features/                    # Specific functionality (BA/PO)
│   ├── FEAT-001-password-reset.md
│   └── FEAT-002-social-login.md
│
├── user-stories/                # Sprint-level work (PO/Dev)
│   ├── drafts/                  # Not yet ready
│   ├── ready/                   # Ready for sprint
│   └── in-sprint/               # Currently being worked
│
├── active/                      # PRPs in progress (Dev)
│   └── PRP-001-email-validation.md
│
├── completed/                   # Archived PRPs
│   └── PRP-000-example.md
│
├── templates/                   # Document templates
│   ├── INITIATIVE-TEMPLATE.md
│   ├── EPIC-TEMPLATE.md
│   ├── FEATURE-TEMPLATE.md
│   ├── USER-STORY-TEMPLATE.md
│   └── PRP-TEMPLATE.md
│
├── ai_docs/                     # Library documentation
│   └── README.md
│
└── scripts/                     # Utility scripts
    └── parse-tasks.js
```

---

## Migration Plan

### Phase 1: Documentation (Week 1)

1. Create this proposal document
2. Create new templates for Initiative, Epic, Feature
3. Update USER-STORY-TEMPLATE with new fields
4. Create single "Getting Started" guide

### Phase 2: Command Refactoring (Week 2-3)

1. Rename existing commands to new convention:
   - `/story:write-user-story` → `/po:create-story`
   - `/story:enrich-story-tech` → `/dev:enrich-story`
   - `/story:enrich-story-qa` → `/qa:enrich-story`
   - `/workflow:create-feature-request` → `/ba:create-feature`
   - `/workflow:generate-prp` → `/dev:generate-prp`
   - `/workflow:execute-prp` → `/dev:execute-prp`

2. Create new commands:
   - `/pm:create-initiative`
   - `/pm:create-epic`
   - `/pm:view-roadmap`
   - `/ba:analyze-feature`
   - `/ba:decompose-feature`
   - `/po:view-backlog`
   - `/po:plan-sprint`

3. Create utility commands:
   - `/workflow:status`
   - `/workflow:next-step`
   - `/workflow:trace`

### Phase 3: Directory Migration (Week 3)

1. Create new directories: `initiatives/`, `epics/`, `features/`
2. Rename `feature-requests/` to `features/`
3. Migrate existing SPEC.md files to Feature format
4. Update all internal links

### Phase 4: Testing & Validation (Week 4)

1. Test complete workflow end-to-end
2. Validate all commands work correctly
3. Update CLAUDE.md with new workflow
4. Create training examples

---

## Implementation Phases

### MVP (Minimum Viable Product)

Focus on most common workflow: Feature → Story → PRP

**Commands to implement first:**
1. `/ba:create-feature` (replaces `/workflow:create-feature-request`)
2. `/po:create-story` (replaces `/story:write-user-story`)
3. `/dev:enrich-story` (replaces `/story:enrich-story-tech`)
4. `/qa:enrich-story` (replaces `/story:enrich-story-qa`)
5. `/dev:generate-prp` (existing, update to link to Feature)
6. `/workflow:status` (new)

**Documents to create:**
1. Feature template
2. Updated user story template
3. Getting Started guide

### Phase 2: Strategic Layer

Add Initiative and Epic support:

**Commands:**
1. `/pm:create-initiative`
2. `/pm:create-epic`
3. `/pm:view-roadmap`

**Documents:**
1. Initiative template
2. Epic template
3. Roadmap view

### Phase 3: Sprint Planning

Add backlog and sprint management:

**Commands:**
1. `/po:view-backlog`
2. `/po:prioritize-backlog`
3. `/po:plan-sprint`
4. `/po:accept-story`

### Phase 4: Advanced Features

Polish and optimization:

**Commands:**
1. `/workflow:next-step`
2. `/workflow:trace`
3. Integration with Azure DevOps sync

---

## Quick Reference Card

### "What Command Do I Use?"

```
I am a PRODUCT MANAGER and I need to...
├── Start a new business initiative    → /pm:create-initiative
├── Break initiative into epics        → /pm:create-epic
├── See the roadmap                    → /pm:view-roadmap
└── Check initiative progress          → /pm:initiative-status

I am a BUSINESS ANALYST and I need to...
├── Create a new feature               → /ba:create-feature
├── Research feature requirements      → /ba:analyze-feature
├── Break feature into stories         → /ba:decompose-feature
└── Document business rules            → /ba:document-rules

I am a PRODUCT OWNER and I need to...
├── Write a user story                 → /po:create-story
├── See the backlog                    → /po:view-backlog
├── Prioritize work                    → /po:prioritize-backlog
├── Check if story is ready            → /po:validate-ready
├── Plan a sprint                      → /po:plan-sprint
└── Accept completed work              → /po:accept-story

I am a DEV LEAD and I need to...
├── Add technical context to story     → /dev:enrich-story
├── Prepare Three Amigos meeting       → /dev:three-amigos-prep
├── Create implementation plan         → /dev:generate-prp
├── Implement a PRP                    → /dev:execute-prp
└── Archive completed work             → /dev:archive-prp

I am a QA LEAD and I need to...
├── Add test scenarios to story        → /qa:enrich-story
├── Check story readiness              → /qa:validate-ready
└── Create feature test plan           → /qa:create-test-plan

I need to know...
├── Current workflow state             → /workflow:status
├── What to do next with a file        → /workflow:next-step
└── Where an artifact came from        → /workflow:trace
```

---

## Appendix: Comparison with Current System

| Aspect | Current | Proposed |
|--------|---------|----------|
| **Entry point** | User Story | Initiative, Epic, or Feature |
| **Feature Request** | Derived from story | Parent of stories |
| **PRP scope** | 1 story = 1 PRP | Same (but better linked) |
| **PM commands** | None | 5 commands |
| **BA commands** | None explicit | 4 commands |
| **PO commands** | 3 (write, refine, validate) | 6 commands |
| **Dev Lead commands** | 6 | 5 commands (consolidated) |
| **QA commands** | 2 | 3 commands |
| **Hierarchy levels** | 3 | 6 |
| **Roadmap support** | None | First-class |
| **Backlog view** | None | First-class |
| **Command naming** | Mixed (`story:`, `workflow:`) | Role-based (`pm:`, `ba:`, etc.) |

---

## Open Questions

1. **Azure DevOps Integration**: Should we auto-sync with ADO or keep local-first?
2. **ID Generation**: Auto-increment vs. user-provided IDs?
3. **Backwards Compatibility**: Keep old command names as aliases?
4. **Permissions**: Should commands validate role? (e.g., only PM can create initiatives)
5. **Notifications**: Alert team when artifacts are ready for their role?

---

## Next Steps

1. [ ] Review this proposal with stakeholders
2. [ ] Decide on MVP scope
3. [ ] Create implementation PRP for the redesign
4. [ ] Prioritize command development
5. [ ] Create migration script for existing files

---

**Feedback welcome!** This is a draft proposal for discussion.
