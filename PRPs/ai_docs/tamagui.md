# Tamagui Documentation

## Overview

Tamagui is a universal React Native + Web UI kit with:
- Type-safe design system with theme tokens
- Static extraction for optimal performance (3x faster)
- Built-in dark mode support
- Native platform adaptations

## Core Components

### YStack (Vertical Stack)
```typescript
<YStack gap="$4" padding="$4" bg="$background">
  <Text>Item 1</Text>
  <Text>Item 2</Text>
</YStack>
```

### XStack (Horizontal Stack)
```typescript
<XStack gap="$2" alignItems="center">
  <Icon name="user" />
  <Text>Username</Text>
</XStack>
```

### Text
```typescript
<Text
  color="$textPrimary"
  fontSize="$5"
  fontWeight="600"
  fontFamily="FiraSans"
>
  Hello World
</Text>
```

### Button
```typescript
<Button
  bg="$primary"
  color="$textInverse"
  pressStyle={{ opacity: 0.8 }}
  borderRadius="$2"
  onPress={handlePress}
>
  Click Me
</Button>
```

### Input
```typescript
<Input
  placeholder="Enter text"
  value={value}
  onChangeText={setValue}
  bg="$background"
  borderColor="$border"
  borderWidth={1}
  borderRadius="$2"
  padding="$3"
/>
```

## Theme Tokens

Tokens are accessed with `$` prefix:

**Colors:**
- `$primary` - Primary brand color
- `$success`, `$warning`, `$error`, `$info`
- `$background`, `$backgroundSecondary`, `$backgroundTertiary`
- `$textPrimary`, `$textSecondary`, `$textTertiary`, `$textInverse`
- `$border`, `$borderFocus`, `$borderError`

**Spacing:**
- `$1` (4px), `$2` (8px), `$3` (12px), `$4` (16px)
- `$6` (24px), `$8` (32px), `$12` (48px)

**Border Radius:**
- `$1` (4px), `$2` (8px), `$3` (12px), `$4` (16px)
- `$round` (999px - fully rounded)

**Font Sizes:**
- `$1` through `$10` (increasing sizes)

## Theme Configuration

```typescript
import { createTamagui, createTokens } from '@tamagui/core'
import { colors, darkColors } from './lib/theme/colors'

const tokens = createTokens({
  color: {
    primary: colors.primary,
    success: colors.success,
    // ... more colors
  },
  space: {
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    // ... more spaces
  },
})

const config = createTamagui({
  themes: {
    light: lightTheme,
    dark: darkTheme,
  },
  tokens,
})

export default config
```

## Using Themes

```typescript
import { TamaguiProvider, useTheme } from 'tamagui'
import config from './tamagui.config'

function App() {
  return (
    <TamaguiProvider config={config} defaultTheme="light">
      <YourApp />
    </TamaguiProvider>
  )
}

function Component() {
  const theme = useTheme()

  return (
    <View>
      {/* Access theme values */}
      <Icon color={theme.primary.val} />
    </View>
  )
}
```

## Dark Mode

```typescript
import { useColorScheme } from 'react-native'

function App() {
  const colorScheme = useColorScheme() // 'light' | 'dark'

  return (
    <TamaguiProvider config={config} defaultTheme={colorScheme}>
      <YourApp />
    </TamaguiProvider>
  )
}
```

## Static Extraction

For optimal performance, Tamagui extracts styles at build time:

```typescript
// This gets compiled to optimized native styles
<YStack bg="$background" padding="$4" gap="$2" />
```

## Common Props

Most components support:
- `bg` - background color
- `padding`, `paddingHorizontal`, `paddingVertical`
- `margin`, `marginHorizontal`, `marginVertical`
- `gap` - space between children
- `borderRadius`, `borderWidth`, `borderColor`
- `alignItems`, `justifyContent`
- `flex`, `width`, `height`

## Gotchas

❌ **Theme tokens don't work in StyleSheet** - Use Tamagui components
❌ **Must wrap app in `TamaguiProvider`** - Required for themes
❌ **Static extraction requires babel config** - Check tamagui.config.ts
❌ **Can't use dynamic styles** with static extraction - Use variants or style prop

## Press Styles

```typescript
<Button
  bg="$primary"
  pressStyle={{ bg: '$primaryHover', scale: 0.95 }}
  onPress={handlePress}
>
  Press Me
</Button>
```

## Responsive Design

```typescript
<YStack
  padding="$4"
  $sm={{ padding: '$2' }}  // Small screens
  $md={{ padding: '$6' }}  // Medium screens
  $lg={{ padding: '$8' }}  // Large screens
>
  Responsive Content
</YStack>
```
