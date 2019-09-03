from django.urls import reverse
from rest_framework.test import APITestCase
from bookingApi.models import *
import json
from django.db.utils import IntegrityError


class BookingEfficiencyTestCase(APITestCase):
    """
    Test Module for checking efficiency
    """

    url = reverse("bookingApi:availablerooms")

    def setUp(self):
        # Create user for adding meeting rooms
        self.username = "testUsername"
        self.password = "testPassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create meeting rooms for booking
        self.room1 = Room.objects.create(user=self.user, room_id="room1", room_capacity=8)
        self.room2 = Room.objects.create(user=self.user, room_id="room2", room_capacity=3)
        self.room3 = Room.objects.create(user=self.user, room_id="room3", room_capacity=21)
        self.room4 = Room.objects.create(user=self.user, room_id="room4", room_capacity=30)

        # Create booking for check availability
        self.booking = Booking.objects.create(room_id=self.room1,
                                              number_of_people=3,
                                              date_start="2019-09-02T20:53:12Z",
                                              date_end="2019-09-02T21:00:00Z")

    def test_available_room_check_efficiency(self):
        request_data = {"number_of_people": 18,
                        "date_start": "2019-09-02T20:53:12Z",
                        "date_end": "2019-09-02T21:00:00Z"}
        response = self.client.post(self.url, request_data, format='json')

        # Checking response status code is 200
        self.assertEqual(200, response.status_code)
        # Checking response json must be "room3 for efficiency"
        self.assertEqual("room3", json.loads(response.content)["room_id"])


class AvailabilityTestCase(APITestCase):
    """
        Test method for checking "availableroom" cases
    """
    url = reverse("bookingApi:availablerooms")

    def setUp(self):
        # Create user for adding meeting rooms
        self.username = "test123"
        self.password = "test123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create meeting rooms for booking
        self.room1 = Room.objects.create(user=self.user, room_id="room1", room_capacity=8)

        # Create booking for check availability
        self.booking = Booking.objects.create(room_id=self.room1,
                                              number_of_people=3,
                                              date_start="2019-09-02T20:00:00Z",
                                              date_end="2019-09-02T21:00:00Z")

    def test_availability_not_available_exact_booking(self):
        request_data = {
            "number_of_people": 3,
            "date_start": "2019-09-02T20:00:00Z",
            "date_end": "2019-09-02T21:00:00Z"
        }
        response = self.client.post(self.url, request_data, format="json")
        self.assertEqual(400, response.status_code)

    def test_availability_not_available_between_start_and_end(self):
        request_data = {
            "number_of_people": 3,
            "date_start": "2019-09-02T20:10:00Z",
            "date_end": "2019-09-02T20:50:00Z"
        }
        response = self.client.post(self.url, request_data, format="json")
        self.assertEqual(400, response.status_code)

    def test_availability_not_available_gt_start_gt_end(self):
        request_data = {
            "number_of_people": 3,
            "date_start": "2019-09-02T20:10:00Z",
            "date_end": "2019-09-02T22:30:00Z"
        }
        response = self.client.post(self.url, request_data, format="json")
        self.assertEqual(400, response.status_code)

    def test_availability_not_available_lt_start_lt_end(self):
        request_data = {
            "number_of_people": 3,
            "date_start": "2019-09-02T19:10:00Z",
            "date_end": "2019-09-02T20:30:00Z"
        }
        response = self.client.post(self.url, request_data, format="json")
        self.assertEqual(400, response.status_code)

    def test_availability_available(self):
        request_data = {
            "number_of_people": 3,
            "date_start": "2019-09-02T15:10:00Z",
            "date_end": "2019-09-02T16:30:00Z"
        }
        response = self.client.post(self.url, request_data, format="json")
        self.assertEqual(200, response.status_code)


class BookingTestCase(APITestCase):
    """
        Test module for checking booking for available room
    """
    url = reverse("bookingApi:bookroom")

    def setUp(self):
        # Create user for adding meeting rooms
        self.username = "test123"
        self.password = "test123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create meeting rooms for booking
        self.room1 = Room.objects.create(user=self.user, room_id="room1", room_capacity=8)
        self.room2 = Room.objects.create(user=self.user, room_id="room2", room_capacity=3)

        self.booking = Booking.objects.create(room_id=self.room1,
                                              number_of_people=3,
                                              date_start="2019-09-02T20:00:00Z",
                                              date_end="2019-09-02T21:00:00Z")

    def test_booking_room_valid_date(self):
        request_data = {
            "room_id": "room1",
            "number_of_people": 3,
            "date_start": "2019-09-02T21:10:00Z",
            "date_end": "2019-09-02T23:00:00Z"
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(201, response.status_code)
    def test_booking_room_invalid_date(self):
        request_data = {
            "room_id": "room1",
            "number_of_people": 3,
            "date_start": "2019-09-02T20:20:00Z",
            "date_end": "2019-09-02T21:00:00Z"
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(406, response.status_code)

class RoomTestCase(APITestCase):
    """
        Test module for creating rooms and relationships
    """
    def setUp(self):
        # Create user for adding meeting rooms
        self.username = "test123"
        self.username2="test1234"
        self.password = "test123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password)

        # Create meeting rooms for booking

    def test_create_room_valid_user(self):
        self.room1 = Room.objects.create(user=self.user, room_id="room1", room_capacity=8)
        self.assertTrue((Room.objects.filter(room_id="room1")))
    def test_create_room_invalid_user(self):
        try:
            self.room1 = Room.objects.create(user="testUser", room_id="room1", room_capacity=8)
        except ValueError as Argument:
            self.assertTrue('"Room.user" must be a "User" instance' in str(Argument))
    def test_a_client_can_have_n_number_of_rooms(self):
        try:
            self.room1 = Room.objects.create(user=self.user, room_id="room1", room_capacity=8)
            self.room2 = Room.objects.create(user=self.user2, room_id="room1", room_capacity=3)
        except IntegrityError as Argument:
            self.assertTrue("UNIQUE constraint failed" in str(Argument))