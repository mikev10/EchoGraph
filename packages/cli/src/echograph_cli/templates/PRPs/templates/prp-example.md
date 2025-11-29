# PRP: User Profile Page with Avatar Upload

**Generated**: 2025-01-15
**Status**: DRAFT
**Parent Task**: [TASK-005] User Profile Management (from `.claude/TASK.md`)
**Child Task**: [TASK-005.4] Add profile image upload (from `.claude/tasks/TASK-005-user-profiles.md`)

**Note**: This PRP implements one subtask of the larger User Profile Management feature.

---

## Confidence Score

**8/10** - High confidence. Clear requirements, established patterns available in examples/, minor clarification needed on image storage strategy.

**Clarifications Needed:**
1. Should avatar images be stored in cloud storage (S3) or database (Base64)?
2. Max file size limit for avatars?

---

## Feature Overview

### What
Build a user profile page that displays user information (name, email, bio) and allows users to upload and update their profile avatar image. The page should support viewing mode and edit mode.

### Why
Users need the ability to personalize their profiles and update their information. Profile avatars improve user identification throughout the app.

### Success Criteria
- [ ] Profile page displays all user data correctly
- [ ] Users can upload avatar images (JPG, PNG)
- [ ] Avatar updates reflect immediately after upload
- [ ] Form validation prevents invalid data submission
- [ ] Works offline (shows cached data, queues updates)

---

## Technical Approach

### Architecture
Client-side profile page → API client → Backend `/api/users/:id` endpoint → Database + Cloud Storage

### Key Components
1. **ProfileScreen**: Main page component with view/edit modes
2. **AvatarUpload**: Reusable image upload component
3. **useUpdateProfile**: Mutation hook for profile updates
4. **profileStore**: Client state for edit mode

### Technology Stack
- **React Query**: Server state management, optimistic updates
- **FormData API**: File uploads
- **Zod**: Form validation

### Patterns to Use
- See `examples/hooks/use-create-item.ts` - Mutation pattern with optimistic updates
- See `examples/integrations/axios-client.ts` - API client with multipart/form-data
- See `examples/state/ui-store.ts` - UI state management (edit mode toggle)
- Reference `.claude/CLAUDE.md` section: Input Validation, Security Rules

---

## Implementation Steps

### Step 1: Create User Profile API Types
**Goal**: Define TypeScript types for user profile data

**Tasks**:
- [ ] Create `User` interface matching API response
- [ ] Create `UpdateProfileRequest` interface
- [ ] Export from types file

**Files to Create/Modify**:
- `src/types/user.ts` - User-related type definitions

**Validation**:
```bash
npm run type-check
```

**Expected Outcome**: Types compile without errors, match API specification

---

### Step 2: Create Profile Data Fetching Hook
**Goal**: Implement `useUserProfile` hook to fetch user data

**Tasks**:
- [ ] Create `useUserProfile(userId)` using React Query
- [ ] Set appropriate staleTime (30 min - user data changes infrequently)
- [ ] Handle loading and error states

**Files to Create/Modify**:
- `src/hooks/useUserProfile.ts` - Profile fetching hook

**Validation**:
```bash
npm run type-check
npm test src/hooks/useUserProfile.test.ts
```

**Expected Outcome**: Hook fetches user data, caches appropriately, types are correct

---

### Step 3: Create Profile Update Mutation Hook
**Goal**: Implement `useUpdateProfile` hook for updating profile

**Tasks**:
- [ ] Create mutation hook with optimistic updates
- [ ] Handle FormData for avatar upload
- [ ] Invalidate user query on success
- [ ] Add audit logging for profile updates

**Files to Create/Modify**:
- `src/hooks/useUpdateProfile.ts` - Profile update mutation

**Validation**:
```bash
npm run type-check
npm test src/hooks/useUpdateProfile.test.ts
```

**Expected Outcome**: Mutation updates profile, handles file uploads, optimistic UI works

---

### Step 4: Build Avatar Upload Component
**Goal**: Create reusable avatar image upload component

**Tasks**:
- [ ] Create AvatarUpload component with file picker
- [ ] Validate file type (JPG, PNG only) and size
- [ ] Show preview before upload
- [ ] Display loading state during upload

**Files to Create/Modify**:
- `src/components/AvatarUpload.tsx` - Avatar upload component
- `src/components/AvatarUpload.test.tsx` - Component tests

**Validation**:
```bash
npm run type-check
npm test src/components/AvatarUpload.test.tsx
npm run lint
```

**Expected Outcome**: Component allows image selection, validates files, shows preview

---

### Step 5: Build Profile Screen
**Goal**: Create main profile page with view/edit modes

**Tasks**:
- [ ] Create ProfileScreen component
- [ ] Implement view mode (display data)
- [ ] Implement edit mode (form with validation)
- [ ] Integrate avatar upload
- [ ] Add loading and error states

**Files to Create/Modify**:
- `src/screens/ProfileScreen.tsx` - Main profile page
- `src/screens/ProfileScreen.test.tsx` - Screen tests

**Validation**:
```bash
npm run type-check
npm test src/screens/ProfileScreen.test.tsx
npm run lint
npx expo export --platform ios # Build check
```

**Expected Outcome**: Profile page renders, edit mode works, form submits correctly

---

## Data Models

### User
```typescript
interface User {
  id: string
  email: string
  name: string
  bio?: string
  avatarUrl?: string
  createdAt: string
  updatedAt: string
}
```

### UpdateProfileRequest
```typescript
interface UpdateProfileRequest {
  name?: string
  bio?: string
  avatar?: File | Blob // For file uploads
}
```

---

## API Endpoints

### GET /api/users/:id
- **Method**: GET
- **Path**: `/api/users/:id`
- **Request Body**: None
- **Response**: `User`
- **Reference**: `docs/api/users-spec.md`

### PUT /api/users/:id
- **Method**: PUT
- **Path**: `/api/users/:id`
- **Request Body**: `multipart/form-data` with fields: name, bio, avatar (file)
- **Response**: `User`
- **Headers**: `Content-Type: multipart/form-data`

---

## Security Considerations

- [ ] Validate file types (whitelist JPG, PNG)
- [ ] Validate file size (max 5MB)
- [ ] Sanitize user inputs (name, bio) to prevent XSS
- [ ] Users can only update their own profile (auth check)
- [ ] Audit logging for profile updates
- [ ] Rate limit avatar uploads to prevent abuse

**Reference**: `.claude/CLAUDE.md` - Security Rules section

---

## Testing Strategy

### Unit Tests
- `AvatarUpload` - File validation, preview rendering, upload trigger
- `useUpdateProfile` - Mutation logic, optimistic updates, cache invalidation
- `useUserProfile` - Data fetching, caching, error handling

### Integration Tests
- Full profile update flow (edit → upload avatar → save → verify)
- Offline mode (cached data display, queued mutations)

### Manual Testing
- [ ] Upload various image formats (JPG, PNG, invalid formats)
- [ ] Upload oversized images (> 5MB)
- [ ] Edit and save profile multiple times
- [ ] Test on slow network (loading states)
- [ ] Test offline (cached data, mutation queue)

**Reference**: `examples/testing/` for test patterns

---

## Edge Cases & Gotchas

1. **Large Image Files**: Compress images client-side before upload to reduce bandwidth. Use library like `browser-image-compression` or `react-native-image-resizer`.

2. **Stale Avatar URLs**: Avatar URL may be cached by browser/CDN. Append query param `?t=timestamp` to force refresh.

3. **Concurrent Updates**: If user edits profile in multiple tabs/devices, last write wins. Consider adding optimistic lock (version field).

4. **File Upload Failures**: Handle partial uploads gracefully - don't update profile if avatar upload fails.

---

## Dependencies

### New Dependencies to Install
```bash
npm install react-hook-form zod @hookform/resolvers
```

### Existing Dependencies Used
- `@tanstack/react-query` - Data fetching and mutations
- `axios` - HTTP client with multipart/form-data support
- `examples/hooks/use-create-item.ts` - Mutation pattern

---

## Rollout Plan

1. **Development**: Implement all steps, test locally with dev API
2. **Staging/Testing**: Deploy to staging, run full test suite, manual QA
3. **Production**: Deploy with feature flag, monitor error rates, enable for all users

---

## Follow-up Tasks

- [ ] Add image cropping/resizing before upload
- [ ] Support additional profile fields (phone, location)
- [ ] Add profile privacy settings
- [ ] Performance: Lazy load avatar images in lists

---

## References

- **Feature Request**: `.claude/INITIAL.md`
- **Related PRPs**: None
- **External Docs**:
  - [React Query Mutations](https://tanstack.com/query/latest/docs/react/guides/mutations)
  - [FormData API](https://developer.mozilla.org/en-US/docs/Web/API/FormData)
- **Examples**:
  - `examples/hooks/use-create-item.ts`
  - `examples/integrations/axios-client.ts`
