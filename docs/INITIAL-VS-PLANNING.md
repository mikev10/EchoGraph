# Understanding INITIAL.md vs PLANNING.md

## Quick Answer

- **PLANNING.md** = Project-wide architecture blueprint (create **first**)
- **INITIAL.md** = Feature request template (use **repeatedly** for individual features)

---

## PLANNING.md - Project Architecture Blueprint

**Purpose:** Define the overall architecture and goals for your entire project.

**Scope:** Project-wide

**Created:** Once at project start (updated as architecture evolves)

**Contains:**
- Project goal and target users
- System architecture diagrams (Mermaid)
- Complete tech stack with rationale
- Data flow and state management strategy
- API integration patterns
- Security architecture
- Non-functional requirements
- Success criteria

**Think of it as:** The architectural blueprint for your entire house.

---

## INITIAL.md - Feature Request Template

**Purpose:** Template for requesting individual features within your project.

**Scope:** Single feature

**Created:** Each time you want to add a new feature (multiple times throughout project)

**Contains:**
- Specific functionality to implement
- Code examples showing expected structure
- Documentation links for libraries/APIs
- Feature-specific considerations and constraints

**Think of it as:** A work order template for adding a new room or feature to your house.

---

## The Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. CREATE PROJECT ARCHITECTURE                          │
│    .claude/PLANNING.md                                  │
│    (Define overall system design)                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. REQUEST FEATURE (repeat for each feature)            │
│    Copy .claude/INITIAL.md template                     │
│    Fill out all sections                                │
│    Save as: my-feature-request.md                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. GENERATE PRP (Project Requirement Plan)              │
│    /generate-prp my-feature-request.md                  │
│    → Creates: PRPs/my-feature.md                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 4. EXECUTE PRP                                          │
│    /execute-prp PRPs/my-feature.md                      │
│    → Implements the feature step-by-step                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 5. REPEAT STEPS 2-4 FOR NEXT FEATURE                    │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Example

### Step 1: Create Project Architecture (Once)

Fill out `.claude/PLANNING.md`:
```markdown
# My Todo App - Architecture & Goals

## Project Goal
Build a cross-platform task management app with offline-first
architecture and real-time sync.

## Tech Stack Rationale
| Technology | Why |
|------------|-----|
| React Native | Cross-platform with native performance |
| SQLite | Offline-first local storage |
| WebSocket | Real-time sync |
...
```

### Step 2: Request a Feature (Many Times)

Copy `.claude/INITIAL.md` → `user-auth-request.md`:
```markdown
# Feature Request Template

## FEATURE
User authentication with email/password and Google OAuth

## EXAMPLES
```javascript
function LoginScreen({ onLogin }) {
  return (
    <View>
      <TextInput placeholder="Email" />
      <TextInput placeholder="Password" secureTextEntry />
      <Button onPress={handleLogin}>Login</Button>
      <GoogleSignInButton onPress={handleGoogleLogin} />
    </View>
  )
}
```

## DOCUMENTATION
- Firebase Auth: https://firebase.google.com/docs/auth
- Google OAuth: PRPs/ai_docs/google-oauth-spec.md
...
```

### Step 3: Generate PRP
```bash
/generate-prp user-auth-request.md
# Creates: PRPs/user-authentication.md
```

### Step 4: Execute PRP
```bash
/execute-prp PRPs/user-authentication.md
# Claude implements the feature step-by-step
```

### Step 5: Next Feature
Repeat steps 2-4 for your next feature (e.g., task creation, categories, etc.)

---

## Key Differences Summary

| Aspect | PLANNING.md | INITIAL.md |
|--------|-------------|------------|
| **Scope** | Entire project | Single feature |
| **Frequency** | Once (updated occasionally) | Many times (per feature) |
| **Purpose** | Architecture blueprint | Feature request input |
| **Level** | Strategic/System-wide | Tactical/Specific |
| **Creates** | Project foundation | PRP for implementation |
| **Analogy** | House blueprint | Room addition work order |

---

## Common Mistakes

❌ **Skipping PLANNING.md** - Without it, Claude lacks architectural context
❌ **Using INITIAL.md for architecture** - It's only for feature requests
❌ **Treating INITIAL.md as one-time** - It's a template, use it repeatedly
❌ **Not filling out all sections** - Incomplete requests = incomplete PRPs

✅ **Best Practice:** Create PLANNING.md first, then use INITIAL.md template for each feature you want to add.

---

## Questions?

- See `.claude/INITIAL.md` for the actual template
- See `.claude/PLANNING.md` for the architecture template
- See `docs/CONTEXT_ENGINEERING_QUICKSTART.md` for full workflow guide
