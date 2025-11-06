# React Native Documentation

## Core Components

### View
- Basic building block for UI
- Similar to `<div>` in web
- Supports flexbox layout
- Use for containers and layout

```typescript
<View style={{ flex: 1, padding: 16 }}>
  {children}
</View>
```

### Text
- For displaying text
- **ALL text must be wrapped in `<Text>`**
- Supports nesting and styling
- Can handle press events

```typescript
<Text style={{ fontSize: 16, color: '#000' }}>
  Hello World
</Text>
```

### FlatList
- Efficient list rendering
- Only renders visible items
- Requires `data` and `renderItem` props
- Use `keyExtractor` for unique keys

```typescript
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ItemCard item={item} />}
/>
```

### ScrollView
- Scrollable container
- Renders all children at once (less performant for long lists)
- Use for small lists or heterogeneous content

### TouchableOpacity
- Pressable element with opacity feedback
- Use for buttons and clickable elements

```typescript
<TouchableOpacity onPress={handlePress}>
  <Text>Click Me</Text>
</TouchableOpacity>
```

## Hooks

### useState
```typescript
const [count, setCount] = useState(0)
```

### useEffect
```typescript
useEffect(() => {
  // Effect code
  return () => {
    // Cleanup
  }
}, [dependencies])
```

### useMemo
```typescript
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b)
}, [a, b])
```

### useCallback
```typescript
const handlePress = useCallback(() => {
  doSomething(value)
}, [value])
```

## Platform API

```typescript
import { Platform } from 'react-native'

const isIOS = Platform.OS === 'ios'
const isAndroid = Platform.OS === 'android'
```

## Common Gotchas

❌ **No `window` or `document`** - Use RN-specific APIs
❌ **No direct file paths for images** - Use `require()` or URIs
❌ **AsyncStorage is async** - Always `await` operations
❌ **Styles are objects, not CSS** - Use StyleSheet or inline objects
❌ **Text must be in `<Text>`** - Can't put text directly in `<View>`

## StyleSheet API

```typescript
import { StyleSheet } from 'react-native'

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
})
```

## Flexbox Defaults

- `flexDirection: 'column'` (opposite of web)
- `alignItems: 'stretch'`
- `flexShrink: 1`
