---
description: Review staged git changes before commit
---

Reviews:
- Staged files for quality issues
- Adherence to CLAUDE.md conventions
- Test coverage for new code
- Security concerns

**Process**:
1. Get staged files: `git diff --cached --name-only`
2. Review each file against CLAUDE.md rules
3. Check if tests exist for new code
4. Verify no sensitive data (tokens, keys, passwords)
5. Ensure validation commands pass

**Checks**:
- [ ] No `any` types without justification
- [ ] No tokens in AsyncStorage
- [ ] All new functions have tests
- [ ] Follows naming conventions
- [ ] Proper import order
- [ ] Comments explain WHY, not WHAT

**Output**: Approval or list of issues to fix before committing
