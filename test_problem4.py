"""
Unit tests for Problem 4: MeetingRoom

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the MeetingRoom object
(e.g., bookings list, total_hours_booked, free slots, utilization rate)
to verify room state and conflict management.

Running tests:
    python -m unittest test_problem4.py -v
"""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        """
        Verify initial state of an empty meeting room.
        """
        self.assertEqual(self.room.room_id, "Conference-A")
        self.assertEqual(self.room.capacity, 10)
        self.assertEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)
        self.assertFalse(self.room.is_maintenance)

        self.assertEqual(self.room.get_free_slots(), [(8, 18)])
        self.assertEqual(self.room.get_utilization_rate(), 0.0)

    def test_single_booking_multi_attributes(self):
        """
        Test making a single valid booking.
        Verify bookings list, total_hours_booked, utilization rate, and free slots.
        """
        # TODO: Book meeting 'B01' from 10 to 12 with 5 attendees
        result = self.room.book(
            booking_id="B01",
            title="Team Meeting",
            start_time=10,
            end_time=12,
            attendees=5
        )

        self.assertTrue(result)
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertFalse(self.room.is_maintenance)

        booking = self.room.bookings[0]
        self.assertEqual(booking["booking_id"], "B01")
        self.assertEqual(booking["title"], "Team Meeting")
        self.assertEqual(booking["start_time"], 10)
        self.assertEqual(booking["end_time"], 12)
        self.assertEqual(booking["attendees"], 5)

        self.assertEqual(self.room.get_utilization_rate(), 0.2)
        self.assertEqual(
            self.room.get_free_slots(),
            [(8, 10), (12, 18)]
        )

    def test_back_to_back_meetings_allowed(self):
        """
        Test that valid consecutive / back-to-back meetings (e.g. 9-10 and 10-12)
        are permitted without raising conflict errors.
        Verify multi-attribute state after both bookings succeed.
        """
        # TODO: Book 'B01' from 9 to 10
        self.assertTrue(
            self.room.book("B01", "Morning Meeting", 9, 10, 5)
        )
        self.assertTrue(
            self.room.book("B02", "Late Morning Meeting", 10, 12, 6)
        )

        self.assertEqual(len(self.room.bookings), 2)
        self.assertEqual(
            [booking["booking_id"] for booking in self.room.bookings],
            ["B01", "B02"]
        )
        self.assertEqual(self.room.total_hours_booked, 3)
        self.assertEqual(self.room.get_utilization_rate(), 0.3)

        self.assertEqual(
            self.room.get_free_slots(),
            [(8, 9), (12, 18)]
        )

        self.assertEqual(
            self.room.bookings[0]["end_time"],
            self.room.bookings[1]["start_time"]
        )

    def test_overlapping_booking_rejected(self):
        """
        Test that overlapping bookings (e.g. 9-11 and 10-12, or completely inside 9-12 and 10-11)
        raise ValueError and leave room state unchanged.
        """
        # TODO: Implement test with self.assertRaises(ValueError)
        self.room.book("B01", "First Meeting", 9, 11, 4)

        bookings_before = [booking.copy() for booking in self.room.bookings]
        hours_before = self.room.total_hours_booked

        with self.assertRaises(ValueError):
            self.room.book("B02", "Overlapping Meeting", 10, 12, 3)

        self.assertEqual(self.room.bookings, bookings_before)
        self.assertEqual(self.room.total_hours_booked, hours_before)
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B01")
        self.assertEqual(self.room.get_utilization_rate(), 0.2)

    def test_cancel_booking_updates_all_attributes(self):
        """
        Test that cancelling a booking correctly removes it from bookings,
        decrements total_hours_booked, and restores free slots.
        """
        # TODO: Book two meetings, cancel one, verify all attributes
        self.room.book("B01", "Morning Meeting", 9, 10, 4)
        self.room.book("B02", "Afternoon Meeting", 13, 15, 6)

        self.assertEqual(len(self.room.bookings), 2)
        self.assertEqual(self.room.total_hours_booked, 3)
        self.assertEqual(self.room.get_utilization_rate(), 0.3)

        result = self.room.cancel("B01")

        self.assertTrue(result)
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B02")
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.get_utilization_rate(), 0.2)

        self.assertEqual(
            self.room.get_free_slots(),
            [(8, 13), (15, 18)]
        )

    def test_capacity_and_validation_exceptions(self):
        """
        Test edge cases and exceptions:
        - Attendees exceeding capacity (ValueError)
        - Start time >= End time (ValueError)
        - Duplicate booking ID (ValueError)
        - Booking when room is under maintenance (RuntimeError)
        - Cancelling non-existent booking (KeyError)
        """
        # TODO: Implement exception tests using self.assertRaises()
        # Attendees exceeding capacity
        with self.assertRaises(ValueError):
            self.room.book("B01", "Too Large", 9, 10, 11)

        self.assertEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)

        # Invalid time: end time is not greater than start time
        with self.assertRaises(ValueError):
            self.room.book("B02", "Invalid Time", 10, 10, 5)

        with self.assertRaises(ValueError):
            self.room.book("B03", "Invalid Time", 12, 11, 5)

        self.assertEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)

        # Valid booking
        self.room.book("B04", "Valid Meeting", 10, 12, 5)

        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)

        # Duplicate booking ID
        with self.assertRaises(ValueError):
            self.room.book("B04", "Duplicate Meeting", 13, 14, 3)

        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B04")
        self.assertEqual(self.room.total_hours_booked, 2)

        # Booking while under maintenance
        maintenance_room = MeetingRoom("Maintenance-Room", capacity=10)
        maintenance_room.is_maintenance = True

        with self.assertRaises(RuntimeError):
            maintenance_room.book("B05", "Maintenance Test", 9, 10, 2)

        self.assertTrue(maintenance_room.is_maintenance)
        self.assertEqual(maintenance_room.bookings, [])
        self.assertEqual(maintenance_room.total_hours_booked, 0)

        # Cancelling a non-existent booking
        with self.assertRaises(KeyError):
            self.room.cancel("UNKNOWN")

        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)


if __name__ == "__main__":
    unittest.main()
