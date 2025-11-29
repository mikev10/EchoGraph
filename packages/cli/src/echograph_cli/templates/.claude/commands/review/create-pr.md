---
description: Create pull request with summary, test plan, and screenshots
---

Generates:
- PR title (conventional commits format: `feat:`, `fix:`, `refactor:`, etc.)
- Description with changes summary
- Test plan checklist
- Files changed list
- Breaking changes (if any)

**Process**:
1. Analyze git diff
2. Identify main changes
3. Generate PR description
4. Create test plan
5. Note any breaking changes

**Output Format**:
```markdown
## Summary
[Brief description of changes]

## Changes
- Added feature X
- Fixed bug Y
- Refactored Z

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested on iOS/Android

## Files Changed
- src/components/ReservationCard.tsx
- src/hooks/use-schedule.ts

## Breaking Changes
[None or list of breaking changes]
```
