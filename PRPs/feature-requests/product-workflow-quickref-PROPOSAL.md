# Product Workflow Quick Reference (Proposed)

**One-page guide for cross-functional product teams**

---

## The Flow at a Glance

```
STRATEGIC PLANNING                    BACKLOG REFINEMENT                    EXECUTION
(Quarterly)                           (Weekly/Sprint)                       (Daily)
─────────────────────────────────────────────────────────────────────────────────────────

    PM                                  BA/PO                                 DEV LEAD
     │                                    │                                      │
     ▼                                    ▼                                      ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│INITIATIVE│───▶│   EPIC   │───▶│ FEATURE  │───▶│  STORY   │───▶│   PRP    │───▶│   CODE   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
 "Mobile App"   "Auth System"   "Password      "Email          "Step-by-step    Implemented
  Launch"                        Reset"         validation"     impl guide"      & tested
     │                │               │              │               │
     │                │               │              │               │
  2-4 epics        3-10           2-8 stories    1 PRP per       5-15 tasks
  per initiative   features       per feature    story           per PRP
                   per epic
```

---

## Who Does What?

| Role | Creates | Main Commands | Frequency |
|------|---------|---------------|-----------|
| **Product Manager** | Initiatives, Epics | `/pm:create-initiative`, `/pm:create-epic`, `/pm:view-roadmap` | Quarterly |
| **Business Analyst** | Features, Story drafts | `/ba:create-feature`, `/ba:analyze-feature`, `/ba:decompose-feature` | Monthly |
| **Product Owner** | Stories, Sprint plans | `/po:create-story`, `/po:view-backlog`, `/po:plan-sprint`, `/po:accept-story` | Weekly |
| **Dev Lead** | PRPs, Technical specs | `/dev:enrich-story`, `/dev:generate-prp`, `/dev:execute-prp` | Per sprint |
| **QA Lead** | Test scenarios | `/qa:enrich-story`, `/qa:validate-ready` | Per story |

---

## The Happy Path (5 Steps)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: PM creates feature context                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
   /pm:create-initiative            │   (Skip if initiative exists)
   /pm:create-epic                  │   (Skip if epic exists)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: BA/PO defines feature and stories                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
   /ba:create-feature EPIC-001      │   Creates: features/FEAT-001-*.md
   /ba:decompose-feature FEAT-001   │   Creates: user-stories/US-001-*.md
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: Three Amigos refines story                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
   /dev:enrich-story US-001         │   Dev Lead adds technical context
   /qa:enrich-story US-001          │   QA Lead adds test scenarios
   /po:validate-ready US-001        │   Checks Definition of Ready
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: Sprint planning and PRP generation                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
   /po:plan-sprint US-001 US-002    │   PO selects stories for sprint
   /dev:generate-prp US-001         │   Creates: active/PRP-001-*.md
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: Implementation and completion                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
   /dev:execute-prp PRP-001         │   Implements step-by-step
   /review:create-pr                │   Creates pull request
   /po:accept-story US-001          │   PO accepts completed work
   /dev:archive-prp PRP-001         │   Archives to completed/
```

---

## Entry Points (Where Do I Start?)

```
"I have a new business initiative"
└── START: /pm:create-initiative
    └── Then: /pm:create-epic → /ba:create-feature → ...

"I have a feature to build"  (Most common)
└── START: /ba:create-feature
    └── Then: /ba:decompose-feature → Three Amigos → ...

"I have a bug or tech debt"
└── START: /po:create-story (category: technical)
    └── Then: /dev:enrich-story → /dev:generate-prp → ...

"I have a story ready to implement"
└── START: /dev:generate-prp
    └── Then: /dev:execute-prp → /review:create-pr → ...

"I need to check what's next"
└── START: /workflow:status
    └── Shows: Current state of all work items
```

---

## Document Hierarchy

```
PRPs/
├── initiatives/          ← PM creates (quarterly)
│   └── 2025-Q1-*.md
│
├── epics/                ← PM creates (monthly)
│   └── EPIC-001-*.md
│
├── features/             ← BA/PO creates (per epic)
│   └── FEAT-001-*.md
│
├── user-stories/         ← PO creates (per feature)
│   ├── drafts/           Stories being refined
│   ├── ready/            Stories ready for sprint
│   └── in-sprint/        Stories being implemented
│
├── active/               ← Dev creates PRPs
│   └── PRP-001-*.md
│
└── completed/            ← Archived PRPs
    └── PRP-000-*.md
```

---

## Sizing Guidelines

| Level | Typical Duration | # of Children | Example |
|-------|------------------|---------------|---------|
| **Initiative** | 2-4 quarters | 2-5 epics | "Mobile App Launch" |
| **Epic** | 1-3 months | 3-10 features | "User Authentication" |
| **Feature** | 1-3 sprints | 2-8 stories | "Password Reset" |
| **User Story** | 1-3 days | 1 PRP | "Email validation" |
| **PRP** | Hours-days | 5-15 tasks | "Implementation guide" |

---

## Three Amigos Checklist

Before marking story as READY:

**PO confirms:**
- [ ] Clear user type (not just "user")
- [ ] Business value stated
- [ ] Acceptance criteria testable

**Dev Lead confirms:**
- [ ] Technical approach documented
- [ ] API/data changes identified
- [ ] Security considered
- [ ] Effort estimated

**QA Lead confirms:**
- [ ] Test scenarios cover happy path
- [ ] Error cases documented
- [ ] Edge cases identified

---

## Key Differences from Current System

| Before | After |
|--------|-------|
| User Story → Feature Request | Feature → User Stories |
| No PM commands | `/pm:*` commands for strategy |
| No backlog view | `/po:view-backlog` |
| Mixed command naming | Role-based: `/pm:`, `/ba:`, `/po:`, `/dev:`, `/qa:` |
| Start with story | Start with initiative/feature |
| 3-level hierarchy | 6-level hierarchy |

---

## Quick Command Lookup

```
PM wants to...
  create initiative    → /pm:create-initiative
  create epic          → /pm:create-epic
  view roadmap         → /pm:view-roadmap

BA wants to...
  create feature       → /ba:create-feature
  analyze requirements → /ba:analyze-feature
  break into stories   → /ba:decompose-feature

PO wants to...
  create story         → /po:create-story
  view backlog         → /po:view-backlog
  plan sprint          → /po:plan-sprint
  accept work          → /po:accept-story
  check readiness      → /po:validate-ready

Dev Lead wants to...
  add tech context     → /dev:enrich-story
  prepare meeting      → /dev:three-amigos-prep
  create PRP           → /dev:generate-prp
  implement            → /dev:execute-prp
  archive              → /dev:archive-prp

QA Lead wants to...
  add test scenarios   → /qa:enrich-story
  check readiness      → /qa:validate-ready

Anyone wants to...
  see workflow state   → /workflow:status
  know next step       → /workflow:next-step
```

---

**See full proposal:** `PRPs/feature-requests/product-workflow-redesign-PROPOSAL.md`
