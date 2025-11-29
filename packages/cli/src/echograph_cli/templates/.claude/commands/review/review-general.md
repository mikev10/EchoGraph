---
description: Perform comprehensive code review with security, performance, and style checks
---

Reviews code for:

## 1. Security Vulnerabilities
- ❌ Tokens in AsyncStorage (must use SecureStore)
- ❌ Hardcoded credentials
- ❌ SQL injection risks
- ❌ XSS vulnerabilities
- ❌ Missing input validation
- ❌ Insecure API calls (HTTP instead of HTTPS)

## 2. Performance Issues
- ❌ Unnecessary re-renders
- ❌ Memory leaks (unsubscribed effects)
- ❌ Large bundle sizes
- ❌ Unoptimized images
- ❌ Inefficient queries (missing cache keys)
- ❌ Blocking operations on main thread

## 3. Style Violations
- Check against CLAUDE.md conventions
- ESLint rules compliance
- Prettier formatting
- Naming conventions (camelCase, PascalCase, etc.)
- Import order
- File organization

## 4. Test Coverage Gaps
- Missing tests for business logic
- Insufficient edge case coverage
- Missing error handling tests
- No integration tests

## 5. Documentation Completeness
- Missing JSDoc for exported functions
- Unclear variable names
- Complex logic without comments
- Missing README updates

**Process**:
1. Analyze all specified files or directories
2. Generate report with severity levels (CRITICAL, WARNING, INFO)
3. Provide specific recommendations with code examples
4. Link to relevant CLAUDE.md sections or examples/

**Output Format**:
```
Code Review Report
──────────────────

CRITICAL Issues: 2
⚠️  Warning Issues: 5
ℹ️  Info Issues: 3

[Detailed findings...]
```
