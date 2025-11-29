---
description: Add technical context to user story (Dev Lead workflow)
argument-hint: <story-path>
model: claude-sonnet-4-5-20250929
---

# Enrich Story with Technical Context

You are helping a **Dev Lead** add technical context to a user story that was drafted by a Product Owner. This is a critical step in the Three Amigos workflow that ensures stories have sufficient technical detail for accurate estimation and successful AI implementation.

**Purpose:** Research the codebase and add technical specifications, API references, security considerations, and implementation patterns to a user story.

**Input:** Path to user story markdown file: `$ARGUMENTS`

---

## Phase 1: Load and Validate Story

**Read the story file:**
```
$ARGUMENTS
```

If no path provided or file not found:
```
Please provide the path to a user story file.

Usage: /enrich-story-tech PRPs/user-stories/drafts/20251124-feature-name.md

Or paste the story content directly and I'll help you enrich it.
```

**Validate the story has required sections:**
- [ ] User Story (As a... I want... So that...)
- [ ] Acceptance Criteria (at least partial)

If missing, note what's needed but proceed with available content.

---

## Phase 2: Research Codebase for Technical Context

Use the Task tool with `subagent_type=Explore` to research:

### 2.1 Similar Implementations
Search for:
- Features with similar functionality
- Components that solve related problems
- Patterns that could be reused

**Questions to answer:**
- "Have we built something similar before?"
- "What patterns exist that we should follow?"
- "Are there components we can reuse?"

### 2.2 API Endpoints
Search for:
- Existing API specification files (`docs/api/*.json`, `swagger.json`, `openapi.yaml`)
- Related endpoints that this feature might interact with
- Authentication and authorization patterns

**Questions to answer:**
- "What API endpoints will this feature need?"
- "Do these endpoints already exist or need to be created?"
- "What's the request/response format?"

### 2.3 Data Model
Search for:
- Database schemas, migrations
- TypeScript interfaces and types
- Entity definitions

**Questions to answer:**
- "What data does this feature need to access?"
- "What tables/collections are involved?"
- "Are there data migrations needed?"

### 2.4 Libraries and Dependencies
Check:
- `package.json` or equivalent for available libraries
- Existing usage of relevant libraries
- Version constraints

**Questions to answer:**
- "What libraries are available for this?"
- "What's already in use for similar features?"
- "Are there version considerations?"

### 2.5 Security Patterns
Search for:
- Authentication mechanisms
- Authorization checks
- Input validation patterns
- Data encryption usage

**Questions to answer:**
- "What security requirements apply?"
- "How do similar features handle auth?"
- "What validation is needed?"

---

## Phase 3: Gather Dev Lead Input

Present research findings and ask clarifying questions:

```
## Technical Research Summary

I've researched the codebase for context relevant to this story. Here's what I found:

### Similar Implementations
[List findings or "No similar implementations found"]

### Relevant API Endpoints
[List findings or "No existing endpoints found - new endpoints needed"]

### Data Model
[List relevant tables/entities or "Need to define new data structures"]

### Available Libraries
[List relevant libraries with versions]

### Security Patterns
[List relevant patterns found]

---

## Questions for Dev Lead

Please answer these to complete the technical context:

1. **Architecture Approach:**
   [Specific question based on findings, e.g., "Should we extend the existing UserService or create a new service?"]

2. **API Design:**
   [Specific question, e.g., "Should this be a new endpoint or extend an existing one?"]

3. **Data Storage:**
   [Specific question, e.g., "Should we add a new table or extend the existing users table?"]

4. **Performance Considerations:**
   [Specific question, e.g., "Do we need caching for this feature?"]

5. **Security Requirements:**
   [Specific question, e.g., "Should this require admin role or regular user access?"]

6. **Dependencies:**
   [Specific question, e.g., "Does this depend on any other stories being completed first?"]

7. **Technical Risks:**
   [Ask about any concerns identified during research]
```

Wait for Dev Lead responses before proceeding.

---

## Phase 4: Generate Technical Context Section

Based on research and Dev Lead input, generate the technical context:

```markdown
## Technical Context

**Added by:** Dev Lead
**Date:** [current date]
**Status:** Technical review complete

### Architecture

**Approach:**
[Description of architectural approach based on Dev Lead input]

**Components Involved:**
- `[file/component path]` - [What it does, how it relates]
- `[file/component path]` - [What it does, how it relates]

**New Components Needed:**
- `[proposed path]` - [Description of new component]

### API Specifications

**Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| [GET/POST/etc] | `/api/v1/[path]` | [Description] |

**Request Format:**
```json
{
  "[field]": "[type] - [description]",
  "[field]": "[type] - [description]"
}
```

**Response Format:**
```json
{
  "[field]": "[type] - [description]",
  "[field]": "[type] - [description]"
}
```

**Error Responses:**
| Status | Code | Message |
|--------|------|---------|
| 400 | [code] | [message] |
| 401 | [code] | [message] |
| 404 | [code] | [message] |

### Data Model

**Tables/Collections:**
- `[table_name]` - [Description]
  - `[column]` ([type]) - [Description]
  - `[column]` ([type]) - [Description]

**Migrations Required:**
- [ ] [Description of migration]

### Libraries & Dependencies

**Existing Libraries to Use:**
- `[library]` (v[version]) - [How it will be used]

**New Dependencies Required:**
- [ ] None / [List any new dependencies]

### Security Considerations

**Authentication:**
- [Auth requirements - e.g., "Requires valid JWT token"]

**Authorization:**
- [Role requirements - e.g., "User must have 'admin' role"]

**Input Validation:**
- [Validation rules - e.g., "Email must be valid RFC 5322 format"]

**Data Protection:**
- [Protection requirements - e.g., "Password must be hashed with bcrypt"]

### Dependencies & Prerequisites

**Blocking Dependencies:**
- [ ] [Story/feature that must complete first] - [Why]

**Non-Blocking Dependencies:**
- [ ] [Related work that's nice to have but not required]

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | Low/Med/High | Low/Med/High | [How to mitigate] |

### Implementation Notes

**Patterns to Follow:**
- Reference: `[file path]` for [pattern description]

**Gotchas/Warnings:**
- [Any known issues or things to watch out for]

**Performance Considerations:**
- [Caching strategy, query optimization, etc.]

### Estimated Complexity

**Initial Assessment:** [Simple / Medium / Complex]
**Confidence:** [High / Medium / Low]
**Notes:** [Why this assessment]
```

---

## Phase 5: Update Story File

Append the Technical Context section to the existing story file:

1. Read the current story content
2. Find the appropriate insertion point (after Acceptance Criteria, before Additional Notes if exists)
3. Insert the generated Technical Context section
4. Update the file metadata if present

**File update approach:**
- Use Edit tool to append Technical Context section
- Preserve all existing content
- Add clear section separator

---

## Phase 6: Summary and Next Steps

After updating the file:

```
## Technical Enrichment Complete

**Story:** [story title]
**File:** [full path]

### What Was Added:
- Architecture approach and component mapping
- API specifications (endpoints, request/response formats)
- Data model and migration requirements
- Library dependencies
- Security considerations
- Technical risks assessment
- Implementation notes and patterns

### Definition of Ready Checklist (Technical):
- [x] Technical feasibility confirmed
- [x] API endpoints identified
- [x] Data model understood
- [x] Dependencies identified
- [x] Security considerations noted
- [x] Similar patterns referenced

### Next Steps:
1. **QA Lead enrichment:** Run `/enrich-story-qa [story-path]` to add test scenarios
2. **Three Amigos session:** Run `/three-amigos-prep [story-path]` to prepare alignment meeting
3. **Validation:** Run `/validate-story-ready [story-path]` to check all DoR criteria

### Ready for QA Review
The story now has technical context. QA Lead should review and add test scenarios.
```

---

## Error Handling

**If story file is malformed:**
```
The story file appears to be missing required sections.

Found:
- [x] or [ ] Title
- [x] or [ ] User Story
- [x] or [ ] Acceptance Criteria

Please ensure the story has at least a User Story section before technical enrichment.
Consider running /refine-story first to improve story structure.
```

**If codebase research finds nothing:**
```
No similar patterns found in the codebase for this feature.

This appears to be a new capability. Technical context will need to be defined from scratch.

Dev Lead, please provide:
1. Preferred architectural approach
2. Proposed API design
3. Data model requirements
4. Security requirements

I'll help structure this information into the Technical Context section.
```

**If Dev Lead skips questions:**
```
Some technical details are incomplete. This may affect:
- Estimation accuracy
- Implementation approach
- AI code generation quality

Would you like to:
A) Continue with partial technical context (note gaps)
B) Return to answer remaining questions
C) Mark as needs follow-up and proceed

Please respond with A, B, or C.
```

---

## Quality Checklist

Before finalizing, verify:

- [ ] Architecture approach is documented
- [ ] API endpoints are specified (or noted as TBD)
- [ ] Data model is understood
- [ ] Dependencies are identified
- [ ] Security requirements are explicit
- [ ] Technical risks are assessed
- [ ] Implementation patterns are referenced
- [ ] Complexity estimate is provided

---

## Examples

### Example 1: CRUD Feature

**Input Story:** "As a user, I want to save favorite products so I can find them easily later"

**Research Findings:**
- Found existing `FavoritesService` in `src/services/`
- Found `user_favorites` table in database
- Found similar feature for "saved searches"

**Technical Context Added:**
- Extend existing FavoritesService
- Use existing table structure
- Follow saved searches pattern for UI

### Example 2: New Integration

**Input Story:** "As a user, I want to pay with Apple Pay so I can checkout faster"

**Research Findings:**
- No existing Apple Pay integration
- Found Stripe integration for credit cards
- Found payment service abstraction layer

**Technical Context Added:**
- Create new ApplePayProvider implementing PaymentProvider interface
- Integrate with Stripe Apple Pay SDK
- Follow existing payment patterns
- Note: Requires Apple Developer account setup (dependency)

---

## Integration with Three Amigos Workflow

This command is Step 2 in the Three Amigos workflow:

```
Step 1: /write-user-story  → PO creates draft         ✓
Step 2: /enrich-story-tech → Dev Lead adds technical  ← YOU ARE HERE
Step 3: /enrich-story-qa   → QA Lead adds test scenarios
Step 4: /three-amigos-prep → Prepare alignment session
Step 5: /validate-story-ready → Check all DoR criteria
```

---

**Output:** Updated story file with comprehensive Technical Context section.
