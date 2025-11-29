# User Story Conversion Example

This document demonstrates the complete flow from Product Owner user story (in Azure DevOps) to Context Engineering feature request (INITIAL.md).

**Key Principle:** 1 User Story (1-3 days) = 1 Feature Request = 1 PRP

---

## Step 1: Product Owner Writes User Story in ADO

**Azure DevOps Work Item: US-4523**

```
Title: User login with email and password

Work Item Type: User Story
Story Points: 5
Sprint: Sprint 12
Assigned To: [Developer Name]

User Story:
As a mobile app user
I want to login with my email and password
So that I can securely access my account and personal data

Acceptance Criteria:
- Given I have a registered account, when I enter correct email and password and tap "Login", then I am logged in and see my dashboard
- Given I enter an incorrect password, when I tap "Login", then I see an error message "Invalid email or password"
- Given I am logged in, when I close and reopen the app, then I remain logged in automatically
- Given I tap the password field, when I tap the "eye" icon, then I can toggle password visibility
- Given I enter an invalid email format, when I tap "Login", then I see an error "Please enter a valid email address"

Description:
This is the primary authentication method for the mobile app. Users should be able to login quickly and securely. Session should persist across app restarts to avoid requiring login every time.

Design mockup: https://figma.com/design/login-screen-v2
API Spec: See authentication endpoints in backend API documentation

Constraints:
- Must work on both iOS and Android
- Session must persist securely
- Must comply with security best practices
```

---

## Step 2: Developer Runs `/convert-story` Command

**Developer Action:**
```
Developer: /convert-story

Claude: Please provide the following from the Azure DevOps user story:
1. ADO Work Item ID:
2. Story Title:
3. User Story (As a... I want... So that...):
4. Acceptance Criteria:
5. Description/Additional Context:
6. Story Points (optional):
7. Sprint (optional):
```

**Developer Response:**
```
1. ADO Work Item ID: US-4523
2. Story Title: User login with email and password
3. User Story: As a mobile app user, I want to login with my email and password, so that I can securely access my account and personal data
4. Acceptance Criteria:
   - Given I have a registered account, when I enter correct email and password and tap "Login", then I am logged in and see my dashboard
   - Given I enter an incorrect password, when I tap "Login", then I see an error message "Invalid email or password"
   - Given I am logged in, when I close and reopen the app, then I remain logged in automatically
   - Given I tap the password field, when I tap the "eye" icon, then I can toggle password visibility
   - Given I enter an invalid email format, when I tap "Login", then I see an error "Please enter a valid email address"
5. Description: This is the primary authentication method for the mobile app. Session should persist across app restarts.
6. Story Points: 5
7. Sprint: Sprint 12
8. Design mockup: https://figma.com/design/login-screen-v2
```

---

## Step 3: AI Researches Codebase

**AI performs automatic research:**

```
Searching codebase for:
- Similar authentication patterns
- API endpoints in docs/api/
- Form components and validation
- Secure storage implementations
- Error handling patterns

Found:
- API endpoint: POST /api/v1/auth/login (docs/api/auth-spec.json)
- Form component: src/components/FormInput.tsx
- Validation utility: src/utils/validation.ts (email validation)
- Secure storage: src/utils/secureStorage.ts (uses expo-secure-store)
- Auth state: src/context/AuthContext.tsx
- Error handling: src/utils/errorHandler.ts
```

---

## Step 4: AI Asks Clarifying Questions

```
Claude: Based on my research, I have a few clarifying questions:

1. API Endpoint: I found POST /api/v1/auth/login in docs/api/auth-spec.json. Is this the correct endpoint?

2. Form Components: I found FormInput component in src/components/FormInput.tsx. Should we use this for email and password inputs?

3. Token Storage: I see expo-secure-store is already used in src/utils/secureStorage.ts. Continue with this approach?

4. Password Visibility Toggle: No existing pattern found. Should we add this as a new reusable component or make it specific to login?

5. Navigation: After successful login, where should users be redirected? I see DashboardScreen and HomeScreen in the navigation stack.
```

**Developer Responses:**
```
Developer:
1. Yes, POST /api/v1/auth/login is correct
2. Yes, reuse FormInput component
3. Yes, continue with expo-secure-store
4. Add password toggle to FormInput as a generic feature (prop: showPasswordToggle)
5. Redirect to DashboardScreen after login
```

---

## Step 5: AI Generates INITIAL.md

**File Created:** `PRPs/feature-requests/US-4523-user-login-INITIAL.md`

```markdown
<!-- SOURCE: ADO US-4523 -->
<!-- SPRINT: Sprint 12 -->
<!-- STORY POINTS: 5 -->
<!-- CONVERTED: 2025-11-19 -->

## FEATURE

Implement email and password login for mobile app users with session persistence and secure token storage.

**User Story:**
As a mobile app user, I want to login with my email and password, so that I can securely access my account and personal data.

**Acceptance Criteria:**
- [ ] Given I have a registered account, when I enter correct email and password and tap "Login", then I am logged in and see my dashboard
- [ ] Given I enter an incorrect password, when I tap "Login", then I see an error message "Invalid email or password"
- [ ] Given I am logged in, when I close and reopen the app, then I remain logged in automatically
- [ ] Given I tap the password field, when I tap the "eye" icon, then I can toggle password visibility
- [ ] Given I enter an invalid email format, when I tap "Login", then I see an error "Please enter a valid email address"

**Functional Requirements:**
- Login screen with email and password input fields
- Email validation (format check)
- Password field with visibility toggle (eye icon)
- "Login" button with loading state
- Form validation before submission
- Error message display for invalid credentials
- Error message display for invalid email format
- Secure token storage after successful login
- Session persistence across app restarts
- Automatic navigation to dashboard on successful login
- Loading state during authentication API call
- Network error handling

## EXAMPLES

**Similar Implementations:**
- Form pattern: `src/components/FormInput.tsx` - Reusable form input component
- Email validation: `src/utils/validation.ts` - `validateEmail()` function
- Error handling: `src/utils/errorHandler.ts` - Standard error display pattern
- Auth state management: `src/context/AuthContext.tsx` - Existing auth context

**UI Pattern to Follow:**
```tsx
// From src/components/FormInput.tsx
<FormInput
  label="Email"
  value={email}
  onChangeText={setEmail}
  keyboardType="email-address"
  autoCapitalize="none"
  error={emailError}
/>
```

**Design Reference:**
- Figma mockup: https://figma.com/design/login-screen-v2

## DOCUMENTATION

**API Endpoint:**
- `POST /api/v1/auth/login`
  - Request body: `{ email: string, password: string }`
  - Response: `{ token: string, user: { id: string, email: string, name: string } }`
  - Error responses: 400 (validation), 401 (invalid credentials), 500 (server error)
  - Full spec: `docs/api/auth-spec.json` (section: "Authentication")

**Libraries:**
- `expo-secure-store` (v13.0.2) - Secure token storage
- `react-native` - Core UI components
- `@react-navigation/native` - Navigation (redirect after login)

**Related Files:**
- `src/screens/LoginScreen.tsx` - Create new file (login UI)
- `src/context/AuthContext.tsx` - Extend with login function
- `src/api/auth.ts` - Add login API call
- `src/utils/secureStorage.ts` - Use existing secure storage for token
- `src/utils/validation.ts` - Use existing email validation
- `src/components/FormInput.tsx` - Extend with password toggle feature
- `src/navigation/AuthNavigator.tsx` - Navigation flow after login

**External Documentation:**
- Expo Secure Store: https://docs.expo.dev/versions/latest/sdk/securestore/
- React Navigation Authentication Flow: https://reactnavigation.org/docs/auth-flow/

## OTHER CONSIDERATIONS

**Security:**
- ✅ CRITICAL: Store auth token in expo-secure-store (never AsyncStorage or plain text)
- ✅ CRITICAL: Validate credentials server-side (client validation is only UX)
- ✅ CRITICAL: Use HTTPS for all API calls (enforce in API client)
- ✅ Handle token expiration gracefully (401 response → redirect to login)
- ✅ Clear token on logout
- ✅ Do not log sensitive data (passwords, tokens)
- ✅ Implement rate limiting awareness (display message if server rate-limits)

**User Experience:**
- Show loading indicator during API call (disable form while loading)
- Clear, actionable error messages:
  - "Invalid email or password" (don't reveal which is wrong for security)
  - "Please enter a valid email address" (for format errors)
  - "Unable to connect. Please check your internet connection." (network errors)
- Keyboard handling:
  - Email field → email keyboard type
  - Password field → secure text entry
  - Return key on email field → focus password field
  - Return key on password field → submit form
- Password visibility toggle accessible and clearly labeled
- Focus email field on screen mount
- Auto-dismiss keyboard on submit

**Testing:**
- Unit tests:
  - Email validation function
  - Form submission logic
  - Token storage/retrieval
- Integration tests:
  - Login API call with valid credentials
  - Login API call with invalid credentials
  - Token persistence across app restart
- E2E tests:
  - Complete login flow (valid credentials → dashboard)
  - Invalid credentials flow (error message displayed)
  - Invalid email format (validation error)
  - Password visibility toggle

**Platform Considerations:**
- iOS and Android both supported by expo-secure-store
- Test on both platforms (iOS keychain vs Android Keystore)
- Ensure keyboard behavior works correctly on both platforms

**Performance:**
- Login API call typically 200-500ms
- Show loading state for calls > 200ms
- Cache nothing (security-sensitive)

**Dependencies:**
- Backend API `/api/v1/auth/login` must be ready
- AuthContext must be set up in app
- Navigation stack must include DashboardScreen
- expo-secure-store must be installed and configured

**Gotchas:**
- expo-secure-store doesn't work in Expo Go on Android (requires development build)
- Password field must use `secureTextEntry={!showPassword}` prop
- Token must be retrieved on app startup to maintain logged-in state
- Handle edge case: token stored but user deleted on server (401 on first API call)

**Design Notes from Mockup:**
- Email field label: "Email Address"
- Password field label: "Password"
- Login button text: "Log In"
- Error text color: red
- Password toggle: eye icon (closed eye when hidden, open eye when visible)
- Forgot password link below login button (future feature, not in this story)
```

---

## Step 6: Developer Reviews Generated INITIAL.md

**Developer checks:**
- ✅ All acceptance criteria captured
- ✅ API endpoint correct (POST /api/v1/auth/login)
- ✅ Libraries and versions correct
- ✅ Security considerations comprehensive
- ✅ Design mockup linked
- ✅ All functional requirements derived properly

**Developer makes minor adjustments:**
- Adds note about keyboard return key behavior
- Adds specific error message text from design
- Confirms all looks good

---

## Step 7: Developer Proceeds to PRP Generation

**Command:**
```bash
/generate-prp PRPs/feature-requests/US-4523-user-login-INITIAL.md
```

**Result:**
- AI generates comprehensive PRP with 10-12 implementation steps
- Each step includes:
  - What to implement
  - Files to create/modify
  - Code patterns to reference
  - Validation commands
- PRP saved to: `PRPs/active/US-4523-user-login-PRP.md`
- Estimated execution time: 3-4 hours

---

## Step 8: Developer Executes PRP

**Command:**
```bash
/execute-prp PRPs/active/US-4523-user-login-PRP.md
```

**AI implements step-by-step:**
1. Create LoginScreen component
2. Extend FormInput with password toggle
3. Add email validation
4. Create login API call
5. Integrate with AuthContext
6. Add secure token storage
7. Implement navigation after login
8. Add error handling
9. Add loading states
10. Write tests
11. Validation: Run tests, check functionality

**Each step includes validation gate** - must pass before proceeding to next step.

---

## Step 9: Developer Updates ADO

**After PRP completes:**
- Developer marks US-4523 as "Done" in Azure DevOps
- Links completed PRP: `PRPs/completed/US-4523-user-login-PRP.md`
- Adds note: "Implemented with Context Engineering - see linked PRP for details"

---

## Complete Flow Summary

```
Product Owner (ADO)                     Developer                    Context Engineering AI
─────────────────                       ─────────                    ────────────────────

1. Write user story in ADO
   - User story format
   - Acceptance criteria
   - Story points
   - Design links
                                    2. Copy story from ADO
                                       Run: /convert-story
                                                                    3. Research codebase
                                                                       - Find similar patterns
                                                                       - Locate API endpoints
                                                                       - Identify libraries

                                                                    4. Ask clarifying questions
                                                                       - Confirm API endpoint
                                                                       - Verify components to use
                                                                       - Check navigation flow

                                                                    5. Generate INITIAL.md
                                                                       - FEATURE section
                                                                       - EXAMPLES section
                                                                       - DOCUMENTATION section
                                                                       - OTHER CONSIDERATIONS

                                    6. Review INITIAL.md
                                       Make adjustments if needed

                                    7. Run: /generate-prp
                                                                    8. Generate comprehensive PRP
                                                                       - 10-12 implementation steps
                                                                       - Full context at each step
                                                                       - Validation gates

                                    9. Run: /execute-prp
                                                                    10. Implement step-by-step
                                                                        - Write code
                                                                        - Run tests
                                                                        - Validate each step

                                    11. Review final implementation
                                        Test against acceptance criteria

                                    12. Mark story Done in ADO
                                        Link to completed PRP

13. Review completed work
    Verify acceptance criteria met
    Accept or request changes
```

---

## Key Takeaways

### For Product Owners

✅ **You don't change anything** - continue writing user stories in ADO exactly as you do today

✅ **Write clear acceptance criteria** - Given/When/Then format helps AI generate better technical specs

✅ **Keep stories small** - 1-3 days (3-8 story points) maps perfectly to 1 PRP

✅ **Provide context** - mockups, constraints, and business value help developers create better feature requests

### For Developers

✅ **Use `/convert-story` for consistency** - AI does the codebase research and technical enrichment

✅ **Always review generated INITIAL.md** - verify API endpoints, libraries, and security considerations

✅ **Ask clarifying questions early** - during conversion, not during implementation

✅ **1 user story = 1 PRP** - this is the optimal granularity for Context Engineering

### Why This Works

**Separation of concerns:**
- Product Owners focus on business value and user needs
- Developers focus on technical implementation
- AI bridges the gap with research and context

**Consistency:**
- Every user story goes through the same conversion process
- Standard format ensures nothing is missed
- Quality is maintained across all features

**Speed:**
- Conversion takes 5-10 minutes (vs hours of manual research)
- PRP generation includes comprehensive context automatically
- Implementation is faster with AI step-by-step guidance

**Traceability:**
- Clear link from ADO story → INITIAL.md → PRP → implementation
- Source metadata preserved
- Easy to trace decisions back to business requirements
