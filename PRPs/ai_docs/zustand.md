# Zustand Documentation

## Overview

Zustand is a lightweight (1KB), fast state management library for React with:
- Simple API
- No boilerplate
- TypeScript support
- Middleware for persistence, devtools, etc.

## Basic Usage

### Create a Store

```typescript
import { create } from 'zustand'

interface BearState {
  bears: number
  increase: () => void
  decrease: () => void
  reset: () => void
}

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  decrease: () => set((state) => ({ bears: state.bears - 1 })),
  reset: () => set({ bears: 0 }),
}))
```

### Use in Component

```typescript
function BearCounter() {
  const bears = useBearStore((state) => state.bears)
  return <Text>{bears} bears</Text>
}

function Controls() {
  const increase = useBearStore((state) => state.increase)
  const decrease = useBearStore((state) => state.decrease)

  return (
    <>
      <Button onPress={increase}>Add Bear</Button>
      <Button onPress={decrease}>Remove Bear</Button>
    </>
  )
}
```

## Selectors

### Primitive Selector
```typescript
const bears = useBearStore((state) => state.bears)
```

### Multiple Values
```typescript
const { bears, increase } = useBearStore((state) => ({
  bears: state.bears,
  increase: state.increase,
}))
```

### Computed Values
```typescript
const hasEnoughBears = useBearStore((state) => state.bears > 5)
```

## Updating State

### Shallow Merge
```typescript
set({ bears: 10 })
```

### Function Update
```typescript
set((state) => ({ bears: state.bears + 1 }))
```

### Replace State (no merge)
```typescript
set({ bears: 10 }, true)
```

## Middleware

### Persist Middleware

Save state to AsyncStorage:

```typescript
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'

const useStore = create<State>()(
  persist(
    (set, get) => ({
      bears: 0,
      increase: () => set((state) => ({ bears: state.bears + 1 })),
    }),
    {
      name: 'bear-storage', // Key in AsyncStorage
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
)
```

### Partial Persistence

Only persist certain fields:

```typescript
persist(
  (set) => ({
    bears: 0,
    tempValue: 'not persisted',
    increase: () => set((state) => ({ bears: state.bears + 1 })),
  }),
  {
    name: 'bear-storage',
    storage: createJSONStorage(() => AsyncStorage),
    partialize: (state) => ({ bears: state.bears }), // Only persist bears
  }
)
```

### Immer Middleware

Mutate state directly (uses Immer under the hood):

```typescript
import { immer } from 'zustand/middleware/immer'

const useStore = create<State>()(
  immer((set) => ({
    todos: [],
    addTodo: (todo) =>
      set((state) => {
        state.todos.push(todo) // Direct mutation
      }),
  }))
)
```

## Accessing Store Outside Components

```typescript
// Get current state
const state = useBearStore.getState()

// Subscribe to changes
const unsubscribe = useBearStore.subscribe((state) => {
  console.log('bears changed:', state.bears)
})

// Unsubscribe
unsubscribe()

// Update state
useBearStore.setState({ bears: 5 })
```

## Combining Stores

### Multiple Stores
```typescript
const useBearStore = create<BearState>(...)
const useFishStore = create<FishState>(...)

function Component() {
  const bears = useBearStore((state) => state.bears)
  const fish = useFishStore((state) => state.fish)

  return <Text>{bears} bears, {fish} fish</Text>
}
```

### Store Composition
```typescript
const useStore = create((set) => ({
  ...createBearSlice(set),
  ...createFishSlice(set),
}))
```

## TypeScript Best Practices

### Inline Types
```typescript
const useStore = create<{ bears: number; increase: () => void }>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
}))
```

### Separate Interface
```typescript
interface BearState {
  bears: number
  increase: () => void
  decrease: () => void
}

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  decrease: () => set((state) => ({ bears: state.bears - 1 })),
}))
```

## Best Practices

✅ **Use for client-side state only** - Not for server state (use React Query)
✅ **One store per feature** - Don't create one massive store
✅ **Use selectors** - `(state) => state.value` prevents unnecessary rerenders
✅ **No derived state in store** - Compute in components or use selectors
✅ **Use persist middleware** - For caching user preferences
✅ **Split actions** - Keep action creators separate from state

## Performance Optimization

### Prevent Unnecessary Rerenders

❌ Bad (rerenders on any state change):
```typescript
const state = useStore()
```

✅ Good (only rerenders when `bears` changes):
```typescript
const bears = useStore((state) => state.bears)
```

✅ Good (only rerenders when computed value changes):
```typescript
const hasEnoughBears = useStore((state) => state.bears > 5)
```

### Shallow Comparison

For multiple values:
```typescript
import shallow from 'zustand/shallow'

const { bears, fish } = useStore(
  (state) => ({ bears: state.bears, fish: state.fish }),
  shallow
)
```

## Gotchas

❌ **Don't use for server state** - Use React Query instead
❌ **Mutations outside `set()` don't trigger updates** - Always use `set()`
❌ **Subscribing in render causes infinite loops** - Use `useEffect` or selectors
❌ **Persist middleware is async** - State may not be available immediately

## Common Patterns

### Reset Store
```typescript
const initialState = {
  bears: 0,
  fish: 0,
}

const useStore = create<State>((set) => ({
  ...initialState,
  reset: () => set(initialState),
}))
```

### Async Actions
```typescript
const useStore = create<State>((set) => ({
  users: [],
  fetchUsers: async () => {
    const response = await fetch('/api/users')
    const users = await response.json()
    set({ users })
  },
}))
```

### Computed Values
```typescript
const useStore = create<State>((set, get) => ({
  bears: 0,
  fish: 0,
  getTotalAnimals: () => get().bears + get().fish, // Getter function
}))

// In component
const total = useStore((state) => state.bears + state.fish) // Computed in selector
```
