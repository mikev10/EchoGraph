import AsyncStorage from '@react-native-async-storage/async-storage'
import NetInfo from '@react-native-community/netinfo'
import { apiClient } from '@/lib/api/client'

interface QueuedMutation {
  id: string
  type: string
  endpoint: string
  method: 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  data: any
  timestamp: number
  retryCount: number
}

const MUTATION_QUEUE_KEY = '@mutation_queue'
const MAX_RETRY_COUNT = 3

class MutationQueue {
  private processing = false

  /**
   * Queue a mutation when offline or API call fails
   */
  async queueMutation(mutation: Omit<QueuedMutation, 'id' | 'timestamp' | 'retryCount'>): Promise<void> {
    const queuedMutation: QueuedMutation = {
      ...mutation,
      id: this.generateId(),
      timestamp: Date.now(),
      retryCount: 0,
    }

    const queue = await this.getQueue()
    queue.push(queuedMutation)
    await AsyncStorage.setItem(MUTATION_QUEUE_KEY, JSON.stringify(queue))
  }

  /**
   * Process all queued mutations when online
   */
  async processQueue(): Promise<void> {
    if (this.processing) {
      console.log('Queue is already being processed')
      return
    }

    const netInfo = await NetInfo.fetch()
    if (!netInfo.isConnected) {
      console.log('No network connection, skipping queue processing')
      return
    }

    this.processing = true

    try {
      const queue = await this.getQueue()
      const results: { success: string[]; failed: QueuedMutation[] } = {
        success: [],
        failed: [],
      }

      for (const mutation of queue) {
        try {
          await this.executeMutation(mutation)
          results.success.push(mutation.id)
        } catch (error) {
          console.error('Failed to execute mutation:', error)

          // Increment retry count
          mutation.retryCount++

          if (mutation.retryCount < MAX_RETRY_COUNT) {
            results.failed.push(mutation)
          } else {
            console.warn('Max retries reached for mutation:', mutation.id)
            // Optionally notify user about failed mutation
          }
        }
      }

      // Update queue with only failed mutations that haven't exceeded retry limit
      await AsyncStorage.setItem(MUTATION_QUEUE_KEY, JSON.stringify(results.failed))

      if (results.success.length > 0) {
        console.log(`Successfully processed ${results.success.length} mutations`)
      }

      if (results.failed.length > 0) {
        console.warn(`${results.failed.length} mutations failed, will retry`)
      }
    } finally {
      this.processing = false
    }
  }

  /**
   * Execute a single mutation
   */
  private async executeMutation(mutation: QueuedMutation): Promise<void> {
    const response = await apiClient({
      method: mutation.method,
      url: mutation.endpoint,
      data: mutation.data,
    })

    if (response.status < 200 || response.status >= 300) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  }

  /**
   * Get current queue
   */
  async getQueue(): Promise<QueuedMutation[]> {
    try {
      const queueJson = await AsyncStorage.getItem(MUTATION_QUEUE_KEY)
      return queueJson ? JSON.parse(queueJson) : []
    } catch {
      return []
    }
  }

  /**
   * Get queue size
   */
  async getQueueSize(): Promise<number> {
    const queue = await this.getQueue()
    return queue.length
  }

  /**
   * Clear queue
   */
  async clearQueue(): Promise<void> {
    await AsyncStorage.removeItem(MUTATION_QUEUE_KEY)
  }

  /**
   * Generate unique ID
   */
  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }
}

export const mutationQueue = new MutationQueue()

// Auto-process queue when app comes online
NetInfo.addEventListener((state) => {
  if (state.isConnected) {
    mutationQueue.processQueue()
  }
})
