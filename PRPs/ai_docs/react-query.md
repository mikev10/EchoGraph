# React Query (TanStack Query) Documentation

## Overview

React Query is a powerful data-fetching and state management library for React with:
- Automatic caching & background updates
- Optimistic updates
- Offline support
- Request deduplication

## Core Concepts

### Query Keys

Query keys uniquely identify queries and determine cache behavior:

```typescript
// Simple key
['todos']

// Key with ID
['todo', todoId]

// Key with filters
['schedule', locationId, startDate, endDate, filters]

// Hierarchical key
['users', userId, 'posts', postId]
```

**Rules:**
- Must be serializable (no functions)
- Order matters: `['a', 'b']` ≠ `['b', 'a']`
- Use consistent structure across app

### useQuery

Fetch and cache data:

```typescript
const { data, isLoading, isError, error, refetch } = useQuery({
  queryKey: ['todos'],
  queryFn: async () => {
    const response = await fetch('/api/todos')
    return response.json()
  },
  staleTime: 5 * 60 * 1000, // 5 minutes
  gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
})
```

**Options:**
- `staleTime` - How long data is fresh (won't refetch during this time)
- `gcTime` - How long unused data stays in cache
- `enabled` - Conditionally enable/disable query
- `retry` - Number of retry attempts
- `refetchOnMount`, `refetchOnWindowFocus`, `refetchOnReconnect`

### useMutation

Modify server data:

```typescript
const mutation = useMutation({
  mutationFn: async (newTodo) => {
    const response = await fetch('/api/todos', {
      method: 'POST',
      body: JSON.stringify(newTodo),
    })
    return response.json()
  },
  onSuccess: (data) => {
    // Invalidate queries to refetch
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
  onError: (error) => {
    console.error('Mutation failed:', error)
  },
})

// Use mutation
mutation.mutate({ title: 'New Todo' })
```

## Query Client

Setup and configuration:

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 30 * 60 * 1000,
      retry: 3,
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  )
}
```

## Cache Invalidation

```typescript
import { useQueryClient } from '@tanstack/react-query'

const queryClient = useQueryClient()

// Invalidate specific query
await queryClient.invalidateQueries({ queryKey: ['todos'] })

// Invalidate all queries with prefix
await queryClient.invalidateQueries({ queryKey: ['todos'] })

// Invalidate with predicate
await queryClient.invalidateQueries({
  predicate: (query) => query.queryKey[0] === 'todos'
})

// Refetch immediately
await queryClient.refetchQueries({ queryKey: ['todos'] })
```

## Optimistic Updates

Update UI immediately before server responds:

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos'] })

    // Snapshot previous value
    const previousTodos = queryClient.getQueryData(['todos'])

    // Optimistically update
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo])

    // Return context with snapshot
    return { previousTodos }
  },
  onError: (err, newTodo, context) => {
    // Rollback on error
    queryClient.setQueryData(['todos'], context.previousTodos)
  },
  onSettled: () => {
    // Always refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})
```

## Persistence (Offline Support)

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage'
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister'
import { persistQueryClient } from '@tanstack/react-query-persist-client'

const asyncStoragePersister = createAsyncStoragePersister({
  storage: AsyncStorage,
})

persistQueryClient({
  queryClient,
  persister: asyncStoragePersister,
  maxAge: 24 * 60 * 60 * 1000, // 24 hours
})
```

## Dependent Queries

```typescript
// userId must exist before fetching user
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  enabled: !!userId, // Only run if userId exists
})

// user must exist before fetching posts
const { data: posts } = useQuery({
  queryKey: ['posts', user?.id],
  queryFn: () => fetchPosts(user.id),
  enabled: !!user, // Only run if user exists
})
```

## Parallel Queries

```typescript
const results = useQueries({
  queries: [
    { queryKey: ['users'], queryFn: fetchUsers },
    { queryKey: ['posts'], queryFn: fetchPosts },
    { queryKey: ['comments'], queryFn: fetchComments },
  ],
})

const [usersQuery, postsQuery, commentsQuery] = results
```

## Gotchas

❌ **Cache keys must be serializable** - No functions in keys
❌ **Mutations don't auto-refetch** - Must call `invalidateQueries`
❌ **Background refetch happens even when inactive** - Configure with options
❌ **Query keys are compared by deep equality** - Order and structure matter
❌ **Don't use queries for mutations** - Use `useMutation` instead

## Best Practices

✅ Use consistent query key structure
✅ Set appropriate `staleTime` based on data freshness needs
✅ Implement optimistic updates for better UX
✅ Handle loading and error states
✅ Invalidate related queries after mutations
✅ Use `enabled` for dependent queries
✅ Configure retry logic appropriately
