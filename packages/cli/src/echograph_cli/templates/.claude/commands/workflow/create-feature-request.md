---
description: Create feature request following INITIAL.md format
---

# Create Feature Request

You are creating a new feature request for this project.

## Process

### 1. Gather Requirements

**Ask the user:**
- Feature name (e.g., "User Authentication", "Dashboard Analytics")
- Brief description of what needs to be implemented
- Key functionality or pages/endpoints to include

### 2. Research Context (MCP Servers - RECOMMENDED)

**Query project patterns:**
```javascript
// Find similar features
mcp__local-rag__query_documents({
  query: "similar features implementations patterns examples",
  limit: 5
})

// Review project architecture
mcp__local-rag__query_documents({
  query: "architecture patterns conventions project structure",
  limit: 3
})
```

**Traditional research:**
- Read `.claude/PLANNING.md` for architectural patterns
- Check `examples/` folder for implementation patterns
- Review `CLAUDE.md` for conventions and requirements

### 3. Generate Feature Request File

**Structure (INITIAL.md format):**

```markdown
# Feature Request - [Feature Name]

## FEATURE

[Detailed description of what needs to be built]

### User Stories
- As a [user type], I want to [action] so that [benefit]
- [Additional user stories]

### Key Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## EXAMPLES

[Detailed code examples showing expected patterns]

### Example Component/Module Structure
```[language]
// Code example following project conventions
```

### Example Data Model
```[language]
// Type definitions or data structures
```

## DOCUMENTATION

### Relevant Libraries/Frameworks
- [Library 1]: [Purpose/Usage]
- [Library 2]: [Purpose/Usage]

### API Endpoints (if applicable)
- `[METHOD] /api/[endpoint]` - [Description]

### References
- [Official docs URL]
- [Related project documentation]

## OTHER CONSIDERATIONS

### Security
- [Security requirement 1]
- [Security requirement 2]

### Performance
- [Performance consideration 1]
- [Performance consideration 2]

### Testing
- [Test requirement 1]
- [Test requirement 2]

### Accessibility (if UI)
- [A11y requirement 1]
- [A11y requirement 2]
```

### 4. Save the File

**Location**: `PRPs/feature-requests/[feature-name].md`
- Use kebab-case for filename (e.g., `user-authentication.md`, `dashboard-analytics.md`)

### 5. Provide Next Steps

Tell the user:
```
Feature request created: PRPs/feature-requests/[feature-name].md

Next steps:
1. Review the feature request and make any adjustments
2. Run: /workflow:generate-prp PRPs/feature-requests/[feature-name].md
3. Review the generated PRP
4. Run: /workflow:execute-prp PRPs/active/[feature-name].md
```

## Important Guidelines

- **Be specific**: Include exact component names, endpoints, data structures
- **Reference patterns**: Always cite PLANNING.md for architectural decisions
- **Include examples**: Provide detailed code examples matching project patterns
- **List dependencies**: Mention libraries, APIs, or external services needed
- **Security first**: Include validation and security requirements
- **Follow conventions**: Use project-specific naming from CLAUDE.md
- **Use MCP servers**: Query local-rag for existing patterns before writing

## Create Directory

Before generating, ensure the directory exists:
```bash
mkdir -p PRPs/feature-requests
```

---

**Now ask the user what feature they want to create.**
