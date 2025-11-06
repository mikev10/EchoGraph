# Expo Documentation

## Overview

Expo is a framework for React Native that provides:
- Managed workflow (no native code needed)
- Easy preview with Expo Go app
- Cross-platform development (iOS, Android, Web)
- Built-in APIs for device features

## Key Packages

### expo-router
File-based routing for React Native

```typescript
// app/(tabs)/index.tsx
export default function HomeScreen() {
  return <View>...</View>
}

// Navigate programmatically
import { router } from 'expo-router'
router.push('/details')
router.replace('/login')
router.back()
```

**Route Patterns:**
- `app/index.tsx` → `/`
- `app/about.tsx` → `/about`
- `app/users/[id].tsx` → `/users/:id`
- `app/(tabs)/profile.tsx` → `/profile` (group without path)

### expo-secure-store
Encrypted storage for sensitive data (iOS Keychain / Android Keystore)

```typescript
import * as SecureStore from 'expo-secure-store'

// Save
await SecureStore.setItemAsync('key', 'value')

// Read
const value = await SecureStore.getItemAsync('key')

// Delete
await SecureStore.deleteItemAsync('key')
```

⚠️ **Does NOT work in web** - device/simulator only

### expo-constants
Access environment variables and app configuration

```typescript
import Constants from 'expo-constants'

const apiUrl = Constants.expoConfig?.extra?.apiUrl
const isDev = __DEV__
```

**app.config.js:**
```javascript
export default {
  extra: {
    apiUrl: process.env.API_URL,
    supabaseUrl: process.env.SUPABASE_URL,
  }
}
```

### expo-font
Load custom fonts

```typescript
import { useFonts } from 'expo-font'

export default function App() {
  const [fontsLoaded] = useFonts({
    'FiraSans-Regular': require('./assets/fonts/FiraSans-Regular.ttf'),
    'FiraSans-Bold': require('./assets/fonts/FiraSans-Bold.ttf'),
  })

  if (!fontsLoaded) {
    return null // or <AppLoading />
  }

  return <AppContent />
}
```

### expo-linking
Deep linking and URL handling

```typescript
import * as Linking from 'expo-linking'

const url = Linking.createURL('/path')
await Linking.openURL('https://example.com')
```

## Environment Configuration

**Development:**
```bash
EXPO_PUBLIC_API_URL=https://api.sandbox.example.com
```

**Production:**
```bash
EXPO_PUBLIC_API_URL=https://api.example.com
```

Access in code:
```typescript
const apiUrl = process.env.EXPO_PUBLIC_API_URL
```

## Common Commands

```bash
# Start dev server
npx expo start

# Run on iOS
npx expo start --ios

# Run on Android
npx expo start --android

# Build
npx expo export --platform ios

# EAS Build (requires EAS CLI)
eas build --platform ios --profile production
```

## Gotchas

❌ **expo-secure-store doesn't work in web** - Use device/simulator
❌ **Environment variables must start with `EXPO_PUBLIC_`** for client-side access
❌ **EAS Build required for native builds** - Can't use `expo build` anymore
❌ **Expo Go has limitations** - Some packages require development builds

## Development Builds

For packages not supported by Expo Go:
```bash
npx expo install expo-dev-client
eas build --profile development
```
