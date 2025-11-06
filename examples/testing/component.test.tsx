import { render, fireEvent, waitFor } from '@testing-library/react-native'
import { TamaguiProvider } from 'tamagui'
import { ReservationCard } from '@/components/ReservationCard'
import config from '@/tamagui.config'

describe('ReservationCard', () => {
  const mockReservation = {
    id: '123',
    title: 'Yoga Flow',
    instructor: 'Emily Ewing',
    venue: 'Studio A',
    startTime: '5:00 PM',
    endTime: '6:00 PM',
    spotsBooked: 8,
    spotsTotal: 12,
    type: 'session' as const,
  }

  const renderWithProvider = (component: React.ReactElement) => {
    return render(
      <TamaguiProvider config={config} defaultTheme="light">
        {component}
      </TamaguiProvider>
    )
  }

  describe('when rendering', () => {
    it('should display reservation details', () => {
      const { getByText } = renderWithProvider(
        <ReservationCard {...mockReservation} />
      )

      expect(getByText('Yoga Flow')).toBeTruthy()
      expect(getByText('Emily Ewing')).toBeTruthy()
      expect(getByText('Studio A')).toBeTruthy()
      expect(getByText('5:00 PM - 6:00 PM')).toBeTruthy()
    })

    it('should display correct capacity', () => {
      const { getByText } = renderWithProvider(
        <ReservationCard {...mockReservation} />
      )

      expect(getByText('8/12 spots booked')).toBeTruthy()
      expect(getByText('4 available')).toBeTruthy()
    })

    it('should show book button when spots available', () => {
      const mockOnBook = jest.fn()
      const { getByText } = renderWithProvider(
        <ReservationCard {...mockReservation} onBook={mockOnBook} />
      )

      const bookButton = getByText('Book')
      expect(bookButton).toBeTruthy()
    })

    it('should not show book button when no spots available', () => {
      const mockOnBook = jest.fn()
      const { queryByText } = renderWithProvider(
        <ReservationCard
          {...mockReservation}
          spotsBooked={12}
          onBook={mockOnBook}
        />
      )

      expect(queryByText('Book')).toBeNull()
    })
  })

  describe('when interacting', () => {
    it('should call onBook when book button pressed', async () => {
      const mockOnBook = jest.fn()
      const { getByText } = renderWithProvider(
        <ReservationCard {...mockReservation} onBook={mockOnBook} />
      )

      const bookButton = getByText('Book')
      fireEvent.press(bookButton)

      await waitFor(() => {
        expect(mockOnBook).toHaveBeenCalledTimes(1)
      })
    })
  })

  describe('when displaying type colors', () => {
    it('should use correct color for session type', () => {
      const { getByTestId } = renderWithProvider(
        <ReservationCard {...mockReservation} type="session" />
      )

      // Add testID to your component's border for this test
      // Or check computed styles if available
    })
  })
})
