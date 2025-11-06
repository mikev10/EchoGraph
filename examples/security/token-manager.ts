// examples/security/token-manager.ts
// Generic token management pattern for authentication
// Demonstrates: secure token storage, expiry tracking, automatic refresh, logout

import [[SECURE_STORAGE_IMPORT]] from '[[SECURE_STORAGE_LIBRARY]]' // e.g., expo-secure-store, react-native-keychain

// Why: Type-safe auth response
interface AuthResult {
  access_token: string
  refresh_token?: string // Optional: if API supports refresh tokens
  expires_in: number // Seconds until expiry
}

// Token Manager class - handles all token operations
// Why: Centralized auth logic, single source of truth
class TokenManager {
  // API configuration
  // Why: Externalize config for different environments
  private authEndpoint = '[[AUTH_ENDPOINT_URL]]' // e.g., '/api/auth/login'
  private refreshEndpoint = '[[REFRESH_ENDPOINT_URL]]' // e.g., '/api/auth/refresh'

  /**
   * Initial authentication - exchange credentials for tokens
   * @param username - User's username or email
   * @param password - User's password
   * @returns Auth result with access token and expiry
   */
  async login(username: string, password: string): Promise<AuthResult> {
    const response = await fetch(this.authEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any required headers (e.g., API key)
        // '[[API_KEY_HEADER]]': '[[API_KEY_VALUE]]'
      },
      body: JSON.stringify({ username, password }),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.message || 'Authentication failed')
    }

    const { access_token, refresh_token, expires_in } = await response.json()

    // Store tokens in secure storage (Keychain/Keystore on device)
    // Why: CRITICAL - Never use AsyncStorage/localStorage for tokens
    await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]]('auth_token', access_token)

    if (refresh_token) {
      await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]]('refresh_token', refresh_token)
    }

    // Store expiry timestamp for proactive refresh
    // Why: Avoid making API calls with expired tokens
    await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]](
      'token_expires_at',
      String(Date.now() + expires_in * 1000)
    )

    // Optional: Store username for re-auth scenarios
    await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]]('username', username)

    return { access_token, refresh_token, expires_in }
  }

  /**
   * Get valid token - auto-refresh if needed
   * @returns Valid access token
   * @throws NOT_AUTHENTICATED if no token exists
   * @throws SESSION_EXPIRED if refresh fails
   */
  async getValidToken(): Promise<string> {
    const token = await [[SECURE_STORAGE_IMPORT]].[[GET_METHOD]]('auth_token')
    const expiresAt = await [[SECURE_STORAGE_IMPORT]].[[GET_METHOD]]('token_expires_at')

    if (!token || !expiresAt) {
      throw new Error('NOT_AUTHENTICATED')
    }

    // Proactive refresh: refresh 5 minutes before expiry
    // Why: Prevents "token expired" errors during user session
    const refreshThreshold = 5 * 60 * 1000 // 5 minutes
    const shouldRefresh = Date.now() + refreshThreshold >= Number(expiresAt)

    if (shouldRefresh) {
      return await this.refreshToken()
    }

    return token
  }

  /**
   * Refresh token - get new access token without re-authentication
   * @returns New access token
   * @throws SESSION_EXPIRED if refresh fails
   */
  private async refreshToken(): Promise<string> {
    try {
      const refreshToken = await [[SECURE_STORAGE_IMPORT]].[[GET_METHOD]]('refresh_token')

      if (!refreshToken) {
        throw new Error('NO_REFRESH_TOKEN')
      }

      const response = await fetch(this.refreshEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })

      if (response.ok) {
        const { access_token, refresh_token: new_refresh_token, expires_in } = await response.json()

        // Update stored tokens
        await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]]('auth_token', access_token)

        if (new_refresh_token) {
          await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]]('refresh_token', new_refresh_token)
        }

        await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]](
          'token_expires_at',
          String(Date.now() + expires_in * 1000)
        )

        return access_token
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
    }

    // Refresh failed - user must re-authenticate
    // Why: Refresh token expired or invalid
    throw new Error('SESSION_EXPIRED')
  }

  /**
   * Logout - clear all stored authentication data
   */
  async logout(): Promise<void> {
    await [[SECURE_STORAGE_IMPORT]].[[DELETE_METHOD]]('auth_token')
    await [[SECURE_STORAGE_IMPORT]].[[DELETE_METHOD]]('refresh_token')
    await [[SECURE_STORAGE_IMPORT]].[[DELETE_METHOD]]('token_expires_at')
    await [[SECURE_STORAGE_IMPORT]].[[DELETE_METHOD]]('username')

    // Optional: Call logout API endpoint
    // Why: Invalidate tokens on server, revoke access
    // await fetch('[[LOGOUT_ENDPOINT]]', { method: 'POST', ... })
  }

  /**
   * Check if user is currently authenticated
   * @returns true if valid token exists and not expired
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      const token = await [[SECURE_STORAGE_IMPORT]].[[GET_METHOD]]('auth_token')
      const expiresAt = await [[SECURE_STORAGE_IMPORT]].[[GET_METHOD]]('token_expires_at')

      return !!token && Date.now() < Number(expiresAt)
    } catch {
      return false
    }
  }
}

// Export singleton instance
// Why: Single token manager across entire app
export const tokenManager = new TokenManager()

// Gotcha: Always use secure storage (SecureStore, Keychain), NEVER AsyncStorage/localStorage
// Why: Tokens in plain storage are accessible to attackers, XSS, etc.

// Gotcha: Don't refresh tokens too early or too late
// Why: Too early = unnecessary API calls, too late = expired token errors

// Gotcha: Handle refresh failures gracefully
// Why: User needs clear "please log in again" message, not cryptic errors

// Usage example:
/*
// Login
try {
  await tokenManager.login('user@example.com', 'password')
  // Navigate to home screen
} catch (error) {
  // Show error message
}

// Get token for API calls (auto-refreshes if needed)
const token = await tokenManager.getValidToken()

// Check auth status
const isLoggedIn = await tokenManager.isAuthenticated()

// Logout
await tokenManager.logout()
*/
