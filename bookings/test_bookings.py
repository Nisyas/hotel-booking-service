from datetime import date, timedelta

import pytest
from rest_framework import status

from bookings.models import Booking


@pytest.mark.django_db
class TestBookingCreate:
    def test_create_booking_valid_data(self, api_client, sample_room, future_dates):
        data = {
            "room_id": sample_room.id,
            "date_start": future_dates["tomorrow"].isoformat(),
            "date_end": future_dates["in_5_days"].isoformat(),
        }

        response = api_client.post("/bookings/create", data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

        booking = Booking.objects.get(id=response.data["id"])
        assert booking.room == sample_room
        assert booking.date_start == future_dates["tomorrow"]

    def test_create_booking_nonexistent_room(self, api_client, future_dates):
        data = {
            "room_id": 99999,
            "date_start": future_dates["tomorrow"].isoformat(),
            "date_end": future_dates["in_5_days"].isoformat(),
        }

        response = api_client.post("/bookings/create", data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "room_id" in response.data

    def test_create_booking_past_date(self, api_client, sample_room):
        yesterday = date.today() - timedelta(days=1)
        future = date.today() + timedelta(days=3)

        data = {
            "room_id": sample_room.id,
            "date_start": yesterday.isoformat(),
            "date_end": future.isoformat(),
        }

        response = api_client.post("/bookings/create", data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "date_start" in response.data

    def test_create_booking_end_before_start(self, api_client, sample_room, future_dates):
        data = {
            "room_id": sample_room.id,
            "date_start": future_dates["in_5_days"].isoformat(),
            "date_end": future_dates["tomorrow"].isoformat(),
        }

        response = api_client.post("/bookings/create", data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "date_end" in response.data or "non_field_errors" in response.data

    def test_create_booking_overlapping_dates(self, api_client, sample_room, future_dates):
        Booking.objects.create(
            room=sample_room,
            date_start=future_dates["tomorrow"],
            date_end=future_dates["in_5_days"],
        )

        data = {
            "room_id": sample_room.id,
            "date_start": future_dates["in_3_days"].isoformat(),
            "date_end": future_dates["in_10_days"].isoformat(),
        }

        response = api_client.post("/bookings/create", data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data


@pytest.mark.django_db
class TestBookingDelete:
    def test_delete_existing_booking(self, api_client, sample_booking):
        booking_id = sample_booking.id

        response = api_client.delete(f"/bookings/delete/{booking_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Booking.objects.filter(id=booking_id).exists()

    def test_delete_nonexistent_booking(self, api_client):
        response = api_client.delete("/bookings/delete/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookingList:
    def test_list_bookings_for_room(self, api_client, sample_room, future_dates):
        Booking.objects.create(
            room=sample_room,
            date_start=future_dates["tomorrow"],
            date_end=future_dates["in_3_days"],
        )
        Booking.objects.create(
            room=sample_room,
            date_start=future_dates["in_5_days"],
            date_end=future_dates["in_10_days"],
        )

        response = api_client.get(f"/bookings/list?room_id={sample_room.id}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        dates = [booking["date_start"] for booking in response.data]
        assert dates == sorted(dates)

    def test_list_bookings_missing_room_id(self, api_client):
        response = api_client.get("/bookings/list")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_list_bookings_nonexistent_room(self, api_client):
        response = api_client.get("/bookings/list?room_id=99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
