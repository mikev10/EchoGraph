import { renderHook, waitFor } from '@testing-library/react-native'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useSchedule } from '@/hooks/use-schedule'
import { apiClient } from '@/lib/api/client'

// Mock the API client
jest.mock('@/lib/api/client')

describe('useSchedule', () => {
  let queryClient: QueryClient

  beforeEach(() => {
    // Create a new QueryClient for each test to ensure isolation
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false, // Disable retries in tests
        },
      },
    })
    jest.clearAllMocks()
  })

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )

  const mockParams = {
    locationId: 1,
    startDate: new Date('2025-01-01'),
    endDate: new Date('2025-01-07'),
  }

  const mockScheduleData = [
    {
      id: '1',
      title: 'Yoga Flow',
      type: 'session',
      startTime: '2025-01-01T17:00:00Z',
      endTime: '2025-01-01T18:00:00Z',
      instructor: { id: '1', name: 'Emily Ewing' },
      venue: { id: '1', name: 'Studio A' },
      spotsTotal: 12,
      spotsBooked: 8,
      status: 'active',
    },
  ]

  describe('when fetching schedule', () => {
    it('should return schedule data on success', async () => {
      // Arrange
      ;(apiClient.get as jest.Mock).mockResolvedValue({
        data: mockScheduleData,
      })

      // Act
      const { result } = renderHook(() => useSchedule(mockParams), { wrapper })

      // Assert
      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(result.current.data).toEqual(mockScheduleData)
      expect(apiClient.get).toHaveBeenCalledWith('/v2/schedule', {
        params: {
          location_id: 1,
          start_date: '2025-01-01',
          end_date: '2025-01-07',
          instructor_ids: undefined,
          venue_ids: undefined,
          types: undefined,
          statuses: undefined,
        },
      })
    })

    it('should handle API errors', async () => {
      // Arrange
      const mockError = new Error('Network error')
      ;(apiClient.get as jest.Mock).mockRejectedValue(mockError)

      // Act
      const { result } = renderHook(() => useSchedule(mockParams), { wrapper })

      // Assert
      await waitFor(() => {
        expect(result.current.isError).toBe(true)
      })

      expect(result.current.error).toEqual(mockError)
    })

    it('should show loading state initially', () => {
      // Arrange
      ;(apiClient.get as jest.Mock).mockImplementation(
        () => new Promise(() => {}) // Never resolves
      )

      // Act
      const { result } = renderHook(() => useSchedule(mockParams), { wrapper })

      // Assert
      expect(result.current.isLoading).toBe(true)
      expect(result.current.data).toBeUndefined()
    })

    it('should include filters in API call', async () => {
      // Arrange
      ;(apiClient.get as jest.Mock).mockResolvedValue({
        data: mockScheduleData,
      })

      const paramsWithFilters = {
        ...mockParams,
        instructorIds: ['1', '2'],
        venueIds: ['1'],
        types: ['session'],
        statuses: ['active'],
      }

      // Act
      const { result } = renderHook(() => useSchedule(paramsWithFilters), {
        wrapper,
      })

      // Assert
      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(apiClient.get).toHaveBeenCalledWith('/v2/schedule', {
        params: {
          location_id: 1,
          start_date: '2025-01-01',
          end_date: '2025-01-07',
          instructor_ids: '1,2',
          venue_ids: '1',
          types: 'session',
          statuses: 'active',
        },
      })
    })
  })

  describe('when using cache', () => {
    it('should use cached data on subsequent calls', async () => {
      // Arrange
      ;(apiClient.get as jest.Mock).mockResolvedValue({
        data: mockScheduleData,
      })

      // Act - First call
      const { result: result1 } = renderHook(() => useSchedule(mockParams), {
        wrapper,
      })

      await waitFor(() => {
        expect(result1.current.isSuccess).toBe(true)
      })

      // Act - Second call with same params
      const { result: result2 } = renderHook(() => useSchedule(mockParams), {
        wrapper,
      })

      // Assert
      // Should use cached data immediately
      expect(result2.current.data).toEqual(mockScheduleData)

      // API should only be called once due to caching
      expect(apiClient.get).toHaveBeenCalledTimes(1)
    })
  })
})
