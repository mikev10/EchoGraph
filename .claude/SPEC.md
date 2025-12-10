# Feature Request Template

Use this template when requesting new features. Fill out all sections.

## FEATURE

[Specific functionality to implement - be explicit]

**Example:**
```
[[EXAMPLE_FEATURE_DESCRIPTION_E_G_USER_AUTHENTICATION_WITH_EMAIL_PASSWORD_AND_SOCIAL_LOGINS]]
```

## EXAMPLES

[Provide code examples, screenshots, or links to similar implementations]

**Example:**
```[[LANGUAGE]]
// Expected component/function structure
function [[ComponentName]]({ [[props]] }) {
  return (
    <[[Element]] [[attributes]]>
      <[[ChildElement]]>[[content]]</[[ChildElement]]>
      <[[ActionElement]] [[event]]={[[handler]]}>[[label]]</[[ActionElement]]>
    </[[Element]]>
  )
}
```

## DOCUMENTATION

[Links to relevant documentation, APIs, libraries]

**Example:**
```
- [[YOUR_API]]: docs/api/[[spec-file]].md (or PRPs/ai_docs/[[api-name]]-spec-summary.md)
- [[LIBRARY_1]]: [[DOCS_URL_1]]
- [[LIBRARY_2]]: [[DOCS_URL_2]]
- Related patterns: examples/[[category]]/
```

## OTHER CONSIDERATIONS

[Gotchas, requirements, constraints]

**Example:**
```
- Must [[ARCHITECTURAL_REQUIREMENT_E_G_WORK_OFFLINE]]
- Must use [[SECURITY_REQUIREMENT_E_G_SECURE_STORAGE_FOR_TOKENS]]
- Must [[VALIDATION_REQUIREMENT_E_G_VALIDATE_INPUTS]]
- Must [[COMPLIANCE_REQUIREMENT_E_G_INCLUDE_AUDIT_LOGGING]]
- See CLAUDE.md for [[RELEVANT_SECTION_E_G_SECURITY_RULES]]
```

---

## HOW TO USE THIS TEMPLATE

1. Copy this template
2. Fill out all four sections with specific details
3. Replace [[PLACEHOLDERS]] with actual values
4. Save as feature-specific file (e.g., `user-auth-request.md`)
5. Run: `/generate-prp <your-file>.md`
6. Review generated PRP (check confidence score)
7. Run: `/execute-prp PRPs/<feature-name>.md`
