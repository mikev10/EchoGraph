# PRP: [[FEATURE_NAME]]

**Generated**: [[DATE]]
**Status**: [[DRAFT/IN_PROGRESS/COMPLETED]]
**Parent Task**: [TASK-XXX] [[Parent feature name]] (from `.claude/TASK.md`)
**Child Task**: [TASK-XXX.Y] [[Specific subtask this PRP addresses]] (from `.claude/tasks/TASK-XXX-*.md`)

**Note**: These task IDs link this PRP to the hierarchical task system for progress tracking.

---

## Confidence Score

**[[SCORE]]/10** - [[EXPLANATION_OF_SCORE]]

**Rubric:**
- 9-10: Zero clarifications needed, can implement immediately
- 7-8: 1-2 clarifications on edge cases
- 5-6: Several clarifications, missing some context
- 3-4: Significant context gaps, likely failures
- 1-2: Too vague to implement

---

## Feature Overview

### What
[[ONE_PARAGRAPH_DESCRIPTION_OF_WHAT_NEEDS_TO_BE_BUILT]]

### Why
[[WHY_THIS_FEATURE_IS_NEEDED_VALUE_PROPOSITION]]

### Success Criteria
- [ ] [[CRITERION_1]]
- [ ] [[CRITERION_2]]
- [ ] [[CRITERION_3]]

---

## Technical Approach

### Architecture
[[HIGH_LEVEL_ARCHITECTURE_DESCRIPTION]]

```mermaid
[[OPTIONAL_ARCHITECTURE_DIAGRAM]]
```

### Key Components
1. **[[COMPONENT_1]]**: [[DESCRIPTION]]
2. **[[COMPONENT_2]]**: [[DESCRIPTION]]
3. **[[COMPONENT_3]]**: [[DESCRIPTION]]

### Technology Stack
- **[[TECH_1]]**: [[WHY]]
- **[[TECH_2]]**: [[WHY]]

### Patterns to Use
- See `examples/[[CATEGORY_1]]/[[FILE_1]]` - [[PATTERN_NAME]]
- See `examples/[[CATEGORY_2]]/[[FILE_2]]` - [[PATTERN_NAME]]
- Reference `.claude/CLAUDE.md` section: [[SECTION_NAME]]

---

## Implementation Steps

### Step 1: [[STEP_NAME]]
**Goal**: [[WHAT_THIS_STEP_ACCOMPLISHES]]

**Tasks**:
- [ ] [[TASK_1]]
- [ ] [[TASK_2]]
- [ ] [[TASK_3]]

**Files to Create/Modify**:
- `[[FILE_PATH_1]]` - [[PURPOSE]]
- `[[FILE_PATH_2]]` - [[PURPOSE]]

**Validation**:
```bash
[[VALIDATION_COMMANDS]]
```

**Expected Outcome**: [[WHAT_SHOULD_BE_TRUE_AFTER_THIS_STEP]]

---

### Step 2: [[STEP_NAME]]
**Goal**: [[WHAT_THIS_STEP_ACCOMPLISHES]]

**Tasks**:
- [ ] [[TASK_1]]
- [ ] [[TASK_2]]

**Files to Create/Modify**:
- `[[FILE_PATH]]` - [[PURPOSE]]

**Validation**:
```bash
[[VALIDATION_COMMANDS]]
```

**Expected Outcome**: [[WHAT_SHOULD_BE_TRUE_AFTER_THIS_STEP]]

---

### Step N: [[FINAL_STEP_NAME]]
**Goal**: [[WHAT_THIS_STEP_ACCOMPLISHES]]

**Tasks**:
- [ ] [[TASK_1]]
- [ ] [[TASK_2]]

**Files to Create/Modify**:
- `[[FILE_PATH]]` - [[PURPOSE]]

**Validation**:
```bash
[[VALIDATION_COMMANDS]]
```

**Expected Outcome**: [[WHAT_SHOULD_BE_TRUE_AFTER_THIS_STEP]]

---

## Data Models

### [[ENTITY_NAME_1]]
```typescript
interface [[EntityName]] {
  [[FIELD_1]]: [[TYPE]]
  [[FIELD_2]]: [[TYPE]]
  [[FIELD_3]]?: [[OPTIONAL_TYPE]]
}
```

### [[ENTITY_NAME_2]]
```typescript
interface [[EntityName]] {
  [[FIELD_1]]: [[TYPE]]
  [[FIELD_2]]: [[TYPE]]
}
```

---

## API Endpoints

### [[ENDPOINT_1]]
- **Method**: [[GET/POST/PUT/DELETE]]
- **Path**: `[[API_PATH]]`
- **Request Body**: [[SCHEMA_OR_NONE]]
- **Response**: [[SCHEMA]]
- **Reference**: `docs/api/[[API_SPEC]]` (if applicable)

### [[ENDPOINT_2]]
- **Method**: [[GET/POST/PUT/DELETE]]
- **Path**: `[[API_PATH]]`
- **Request Body**: [[SCHEMA_OR_NONE]]
- **Response**: [[SCHEMA]]

---

## Security Considerations

- [ ] [[SECURITY_REQUIREMENT_1]]
- [ ] [[SECURITY_REQUIREMENT_2]]
- [ ] [[SECURITY_REQUIREMENT_3]]
- [ ] Audit logging for [[SENSITIVE_OPERATIONS]]
- [ ] Input validation using [[VALIDATION_LIBRARY]]

**Reference**: `.claude/CLAUDE.md` - Security Rules section

---

## Testing Strategy

### Unit Tests
- [ ] [[COMPONENT_OR_FUNCTION_1]] - [[TEST_SCENARIOS]]
- [ ] [[COMPONENT_OR_FUNCTION_2]] - [[TEST_SCENARIOS]]

### Integration Tests
- [ ] [[INTEGRATION_SCENARIO_1]]
- [ ] [[INTEGRATION_SCENARIO_2]]

### Manual Testing
- [ ] [[MANUAL_TEST_SCENARIO_1]]
- [ ] [[MANUAL_TEST_SCENARIO_2]]

**Reference**: `examples/testing/` for test patterns

---

## Edge Cases & Gotchas

1. **[[EDGE_CASE_1]]**: [[DESCRIPTION_AND_HANDLING]]
2. **[[EDGE_CASE_2]]**: [[DESCRIPTION_AND_HANDLING]]
3. **[[GOTCHA_1]]**: [[WHY_THIS_IS_TRICKY_AND_HOW_TO_HANDLE]]

---

## Dependencies

### New Dependencies to Install
```bash
[[PACKAGE_MANAGER]] install [[PACKAGE_1]] [[PACKAGE_2]]
```

### Existing Dependencies Used
- `[[PACKAGE_1]]` - [[PURPOSE]]
- `[[PACKAGE_2]]` - [[PURPOSE]]

---

## Rollout Plan

1. **Development**: [[STEPS_FOR_DEV_ENVIRONMENT]]
2. **Staging/Testing**: [[STEPS_FOR_STAGING]]
3. **Production**: [[STEPS_FOR_PRODUCTION]]

---

## Follow-up Tasks

- [ ] [[TASK_AFTER_INITIAL_IMPLEMENTATION]]
- [ ] [[DOCUMENTATION_UPDATE]]
- [ ] [[PERFORMANCE_OPTIMIZATION]]
- [ ] [[FEATURE_ENHANCEMENT]]

---

## References

- **Feature Request**: `.claude/SPEC.md` or [[LINK_TO_REQUEST]]
- **Related PRPs**: [[LINK_TO_RELATED_PRPS]]
- **External Docs**: [[LINKS_TO_LIBRARY_DOCS]]
- **Examples**: `examples/[[CATEGORY]]/[[FILES]]`
