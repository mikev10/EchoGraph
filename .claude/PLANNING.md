# [[PROJECT_NAME]] - Architecture & Goals

## Project Goal

[[ONE_SENTENCE_DESCRIPTION_OF_WHAT_YOU_ARE_BUILDING_AND_WHY]]

## Target Users

- [[USER_PERSONA_1_WITH_BRIEF_DESCRIPTION]]
- [[USER_PERSONA_2]]
- [[USER_PERSONA_3]]

## Feature Hierarchy (Priority Order)

1. **PRIMARY**: [[FEATURE_1]] ([[PERCENTAGE]]% of effort)
   - [[SUB_FEATURE_A]]
   - [[SUB_FEATURE_B]]
   - [[SUB_FEATURE_C]]

2. **SECONDARY**: [[FEATURE_2]] ([[PERCENTAGE]]% of effort)
   - [[SUB_FEATURE_A]]
   - [[SUB_FEATURE_B]]

3. **TERTIARY**: [[FEATURE_3]] ([[PERCENTAGE]]% of effort - OPTIONAL)
   - [[SUB_FEATURE_A]]

## System Architecture

```mermaid
graph TD
    A[[[COMPONENT_1]]] --> B[[[COMPONENT_2]]]
    A --> C[[[COMPONENT_3]]]
    B --> D[[[COMPONENT_4]]]
    C --> D
    D --> E[[[COMPONENT_5]]]
```

## Data Flow

1. **[[STEP_1]]** → [[STEP_2]]
2. **[[STEP_2]]** → [[STEP_3]]
3. **[[STEP_3]]** → [[STEP_4]]
4. **[[STEP_4]]** → [[STEP_5]]

## State Management Strategy

**[[STATE_SOLUTION_1]] ([[USE_CASE]]):**
- [[WHAT_DATA_GOES_HERE]]
- [[WHY_THIS_SOLUTION]]

**[[STATE_SOLUTION_2]] ([[USE_CASE]]):**
- [[WHAT_DATA_GOES_HERE]]
- [[WHY_THIS_SOLUTION]]

**[[PERSISTENCE]] (if applicable):**
- [[WHAT_GETS_PERSISTED]]
- [[WHERE_AND_HOW]]

## API Integration

**API Specification Reference** (if applicable):
- **Full spec:** `docs/api/[[YOUR_API_NAME]]-spec.json`
- **AI summary:** `PRPs/ai_docs/[[your_api]]-spec-summary.md`
- **Live endpoints:** [[API_BASE_URLS]]

**Authentication Flow:**
```
[[DESCRIBE_AUTH_FLOW_OR_ADD_MERMAID_DIAGRAM]]
```

**Data Fetching Strategy:**
- [[STRATEGY_ELEMENT_1]]
- [[STRATEGY_ELEMENT_2]]
- [[STRATEGY_ELEMENT_3]]

## [[OPTIONAL_ARCHITECTURE_SECTION]]

**[[ASPECT_1]]:**
- [[IMPLEMENTATION_DETAIL_1]]
- [[IMPLEMENTATION_DETAIL_2]]

**[[ASPECT_2]]:**
- [[IMPLEMENTATION_DETAIL_1]]
- [[IMPLEMENTATION_DETAIL_2]]

## Security Architecture

**[[SECURITY_CONCERN_1]]:**
- [[IMPLEMENTATION_APPROACH]]

**[[SECURITY_CONCERN_2]]:**
- [[IMPLEMENTATION_APPROACH]]

**[[SECURITY_CONCERN_3]]:**
- [[IMPLEMENTATION_APPROACH]]

## Tech Stack Rationale

| Technology | Why |
|------------|-----|
| [[TECH_1]] | [[JUSTIFICATION]] |
| [[TECH_2]] | [[JUSTIFICATION]] |
| [[TECH_3]] | [[JUSTIFICATION]] |
| [[TECH_4]] | [[JUSTIFICATION]] |
| [[TECH_5]] | [[JUSTIFICATION]] |

## Non-Functional Requirements

**Performance Targets:**
- [[METRIC_1]]: [[TARGET]]
- [[METRIC_2]]: [[TARGET]]
- [[METRIC_3]]: [[TARGET]]

**[[OTHER_NFR_CATEGORY]]:**
- [[REQUIREMENT_1]]
- [[REQUIREMENT_2]]

**[[ANOTHER_NFR_CATEGORY]]:**
- [[REQUIREMENT_1]]
- [[REQUIREMENT_2]]

## Success Criteria [[FOR_PROJECT_OR_MILESTONE_OR_DEMO]]

- [ ] [[SPECIFIC_MEASURABLE_CRITERION_1]]
- [ ] [[SPECIFIC_MEASURABLE_CRITERION_2]]
- [ ] [[SPECIFIC_MEASURABLE_CRITERION_3]]
- [ ] [[SPECIFIC_MEASURABLE_CRITERION_4]]
- [ ] [[SPECIFIC_MEASURABLE_CRITERION_5]]
