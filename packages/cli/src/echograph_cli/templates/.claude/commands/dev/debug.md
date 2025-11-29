---
description: Systematic debugging workflow with logs, tests, and root cause analysis
---

Process:
1. **Reproduce Issue**
   - Get exact steps to reproduce
   - Determine frequency (always, sometimes, rarely)
   - Check environment (dev, staging, prod)

2. **Gather Information**
   - Console logs
   - Error messages
   - Stack traces
   - Network requests (if API related)
   - Device info (iOS/Android, version)

3. **Analyze Root Cause**
   - Check recent changes (git log)
   - Review related code
   - Check for similar issues in history
   - Verify assumptions

4. **Implement Fix**
   - Follow CLAUDE.md patterns
   - Reference examples/ if available
   - Add error handling
   - Consider edge cases

5. **Add Regression Test**
   - Write test that would have caught the bug
   - Ensure test fails before fix
   - Ensure test passes after fix

6. **Verify Fix**
   - Test original reproduction steps
   - Run full test suite
   - Check for side effects
   - Test on multiple devices/platforms

7. **Document**
   - Update comments if code was unclear
   - Add gotcha to CLAUDE.md if common issue
   - Update docs/ if needed
