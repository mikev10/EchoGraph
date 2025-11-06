// examples/security/audit-logger.ts
// Generic audit logging pattern for compliance and security tracking
// Demonstrates: event logging, local persistence, async server sync, offline support

import [[SECURE_STORAGE_IMPORT]] from '[[SECURE_STORAGE_LIBRARY]]' // e.g., expo-secure-store
import { [[BACKEND_CLIENT]] } from '@/lib/[[BACKEND_LIBRARY]]' // e.g., supabase, axios

// Why: Standardized audit event structure
interface AuditEvent {
  id: string
  timestamp: string
  userId: string
  action: string // e.g., 'USER_LOGGED_IN', 'PAYMENT_PROCESSED', 'DATA_EXPORTED'
  resource: string // e.g., 'user:123', 'order:456'
  details: Record<string, any> // Additional context
  ipAddress?: string
  deviceInfo?: {
    platform: string
    version: string
    [[OTHER_DEVICE_FIELDS]]?: string
  }
}

// Audit Logger class - centralized event logging
// Why: Single point for all compliance/security logging
class AuditLogger {
  /**
   * Log an audit event
   * Stores locally (encrypted) and sends to server asynchronously
   * @param event - Partial event (id, timestamp, deviceInfo auto-generated)
   */
  async log(event: Omit<AuditEvent, 'id' | 'timestamp' | 'deviceInfo'>): Promise<void> {
    const auditEvent: AuditEvent = {
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      ...event,
      deviceInfo: this.getDeviceInfo(),
    }

    // Store locally (encrypted) - critical for offline mode
    // Why: Ensures audit trail even when offline
    await this.storeLocal(auditEvent)

    // Send to server (async, non-blocking)
    // Why: Don't block user flow waiting for audit log
    this.sendToServer(auditEvent).catch((error) => {
      console.error('Failed to send audit log to server:', error)
      // Kept in local storage for retry later
    })
  }

  /**
   * Store audit event locally in encrypted storage
   * Why: Backup for offline mode, compliance requirement
   */
  private async storeLocal(event: AuditEvent): Promise<void> {
    try {
      const logs = await this.getLocalLogs()
      logs.push(event)

      // Keep only last N logs locally to prevent unbounded growth
      // Why: Balance between audit trail and storage limits
      const maxLocalLogs = 100
      const trimmedLogs = logs.slice(-maxLocalLogs)

      await [[SECURE_STORAGE_IMPORT]].[[SET_METHOD]]('audit_logs', JSON.stringify(trimmedLogs))
    } catch (error) {
      console.error('Failed to store audit log locally:', error)
      // Critical: Don't throw - logging failure shouldn't break app
    }
  }

  /**
   * Get local audit logs
   * @returns Array of audit events
   */
  private async getLocalLogs(): Promise<AuditEvent[]> {
    try {
      const logsJson = await [[SECURE_STORAGE_IMPORT]].[[GET_METHOD]]('audit_logs')
      return logsJson ? JSON.parse(logsJson) : []
    } catch {
      return []
    }
  }

  /**
   * Send audit event to backend server
   * @param event - Audit event to send
   */
  private async sendToServer(event: AuditEvent): Promise<void> {
    // Example: Using REST API
    await [[BACKEND_CLIENT]].post('[[AUDIT_LOG_ENDPOINT]]', {
      id: event.id,
      user_id: event.userId,
      action: event.action,
      resource: event.resource,
      details: event.details,
      device_info: event.deviceInfo,
      ip_address: event.ipAddress,
      timestamp: event.timestamp,
    })

    // Example: Using Supabase
    // const { error } = await [[BACKEND_CLIENT]].from('audit_logs').insert({
    //   id: event.id,
    //   user_id: event.userId,
    //   ...
    // })
    // if (error) throw error
  }

  /**
   * Sync local logs to server
   * Call when network restored or app becomes active
   */
  async syncPendingLogs(): Promise<void> {
    const localLogs = await this.getLocalLogs()

    for (const log of localLogs) {
      try {
        await this.sendToServer(log)
      } catch (error) {
        console.error('Failed to sync audit log:', error)
        // Keep in local storage for next sync attempt
      }
    }
  }

  /**
   * Get device information
   * Platform-specific implementation
   */
  private getDeviceInfo(): AuditEvent['deviceInfo'] {
    // Mobile (React Native/Expo):
    // return {
    //   platform: Platform.OS,
    //   version: String(Platform.Version),
    //   model: Device.modelName || 'unknown',
    // }

    // Web:
    // return {
    //   platform: 'web',
    //   version: navigator.userAgent,
    //   model: navigator.platform,
    // }

    // Generic/placeholder:
    return {
      platform: '[[PLATFORM]]',
      version: '[[VERSION]]',
    }
  }

  /**
   * Generate unique ID for audit event
   * Why: Ensures no duplicate events, enables idempotent operations
   */
  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    // Alternative: Use UUID library for better uniqueness guarantees
    // import { v4 as uuidv4 } from 'uuid'
    // return uuidv4()
  }
}

// Export singleton instance
// Why: Single audit logger across entire app
export const auditLogger = new AuditLogger()

// Gotcha: Don't log sensitive data (passwords, tokens, PII)
// Why: Audit logs may be stored long-term, accessible to admins

// Gotcha: Don't block user flow waiting for audit log
// Why: Logging is important but shouldn't impact UX

// Gotcha: Don't forget to sync pending logs on reconnect
// Why: Offline events need to reach server for compliance

// Usage examples:
/*
// User authentication
await auditLogger.log({
  userId: user.id,
  action: 'USER_LOGGED_IN',
  resource: `user:${user.id}`,
  details: { method: 'password' }
})

// Data export (GDPR, compliance)
await auditLogger.log({
  userId: admin.id,
  action: 'DATA_EXPORTED',
  resource: `user:${targetUserId}`,
  details: { exportType: 'full', reason: 'GDPR request' }
})

// Payment processing
await auditLogger.log({
  userId: user.id,
  action: 'PAYMENT_PROCESSED',
  resource: `order:${orderId}`,
  details: { amount: 99.99, currency: 'USD' }
})

// Sync pending logs on app resume
await auditLogger.syncPendingLogs()
*/
