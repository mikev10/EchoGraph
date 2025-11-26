---
description: Validate all context files for completeness and correctness
---

Checks:

## 1. CLAUDE.md
- [ ] All sections present (Code Structure, Tech Stack, Testing, Security, etc.)
- [ ] Complete and up-to-date conventions
- [ ] No contradictions
- [ ] Validation commands are correct

## 2. examples/
- [ ] All code examples syntactically valid
- [ ] Examples use correct imports
- [ ] Examples follow CLAUDE.md conventions
- [ ] Examples are complete (not pseudocode)
- [ ] TypeScript types are correct

## 3. PRPs/
- [ ] Follow template structure
- [ ] All sections present (Goal, Why, What, Context, Blueprint, Validation, Confidence)
- [ ] Implementation steps are clear
- [ ] References to examples/ are valid
- [ ] Validation commands work

## 4. docs/
- [ ] No broken links
- [ ] Consistent formatting
- [ ] Up-to-date information
- [ ] API documentation matches actual API

## 5. ai_docs/
- [ ] Library versions match package.json
- [ ] Documentation is accurate
- [ ] Examples are correct
- [ ] Gotchas are documented

**Output**: Report of issues found with severity levels
