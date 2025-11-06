---
description: Refactor code while maintaining functionality and tests
---

Process:
1. Analyze code structure
2. Identify improvement opportunities:
   - Extract repeated code into functions
   - Split large files (>300 lines)
   - Improve naming
   - Simplify complex logic
   - Remove dead code
3. Create refactoring plan
4. Execute with validation gates:
   - Tests must pass after each change
   - No behavior changes
   - Type-check must pass
5. Verify no regressions

**Rules**:
- ✅ Keep files under 300 lines
- ✅ Extract reusable logic to hooks
- ✅ Simplify nested conditions
- ✅ Use descriptive names
- ❌ Don't change behavior
- ❌ Don't skip tests
