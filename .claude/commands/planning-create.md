---
description: Create planning documents with architecture diagrams and task breakdowns
---

Generate comprehensive planning document for a feature or project phase.

**Input**: Feature name or phase description

**Output**:
- Architecture diagram (Mermaid syntax)
- Component hierarchy
- Data flow diagrams
- State management strategy
- API integration points
- Task breakdown with time estimates
- Dependencies and risks

**Process**:

1. **Understand Scope**:
   - What is being built?
   - What are the dependencies?
   - What is the complexity level?

2. **Create Architecture Diagram**:
   ```mermaid
   graph TD
       A[Component] --> B[Service]
       B --> C[API]
   ```

3. **Define Data Flow**:
   - User interactions
   - State updates
   - API calls
   - Cache invalidation

4. **Identify Components**:
   - List all components needed
   - Define props and state
   - Map to existing patterns from examples/

5. **Break Down Tasks**:
   - Create detailed task list
   - Estimate time for each task
   - Identify blockers

6. **Save Output**:
   - Location: `PRPs/planning/[feature-name]-plan.md`

**Example Output Structure**:

```markdown
# Feature Name - Planning Document

## Overview
[Brief description]

## Architecture
[Mermaid diagram]

## Components
- Component A: [description]
- Component B: [description]

## State Management
- Server State: React Query
- Client State: Zustand

## API Integration
- Endpoint 1: [details]
- Endpoint 2: [details]

## Task Breakdown
1. [x] Task 1 (2h)
2. [ ] Task 2 (4h)
3. [ ] Task 3 (3h)

## Dependencies
- Library A
- Library B

## Risks
- Risk 1: [mitigation]
- Risk 2: [mitigation]
```
