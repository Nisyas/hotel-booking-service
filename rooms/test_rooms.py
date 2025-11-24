import pytest
from rest_framework import status

from rooms.models import Room


@pytest.mark.django_db
class TestRoomCreate:
    def test_create_room_valid_data(self, api_client):
        data = {
            "name": "Президентский сюит",
            "description": "Роскошный номер с видом на море",
            "price": "15000.00",
        }

        response = api_client.post("/rooms/create", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

        room = Room.objects.get(id=response.data["id"])
        assert room.name == "Президентский сюит"
        assert str(room.price) == "15000.00"

    def test_create_room_missing_name(self, api_client):
        data = {"description": "Описание", "price": "5000.00"}

        response = api_client.post("/rooms/create", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_create_room_negative_price(self, api_client):
        data = {"name": "Тест", "description": "Описание", "price": "-1000.00"}

        response = api_client.post("/rooms/create", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "price" in response.data

    def test_create_room_short_name(self, api_client):
        data = {"name": "AB", "description": "Описание", "price": "5000.00"}

        response = api_client.post("/rooms/create", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data


@pytest.mark.django_db
class TestRoomDelete:
    def test_delete_existing_room(self, api_client, sample_room):
        room_id = sample_room.id
        response = api_client.delete(f"/rooms/delete/{room_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Room.objects.filter(id=room_id).exists()

    def test_delete_nonexistent_room(self, api_client):
        response = api_client.delete("/rooms/delete/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_room_cascades_bookings(self, api_client, sample_booking):
        from bookings.models import Booking

        room_id = sample_booking.room.id
        booking_id = sample_booking.id

        assert Booking.objects.filter(id=booking_id).exists()

        response = api_client.delete(f"/rooms/delete/{room_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Room.objects.filter(id=room_id).exists()
        assert not Booking.objects.filter(id=booking_id).exists()


@pytest.mark.django_db
class TestRoomList:
    def test_list_all_rooms(self, api_client, sample_rooms):
        response = api_client.get("/rooms/list")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_rooms_sort_by_price_asc(self, api_client, sample_rooms):
        response = api_client.get("/rooms/list?sort_by=price&order=asc")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        prices = [float(room["price"]) for room in response.data]
        assert prices == sorted(prices)
        assert prices[0] == 2000.00
        assert prices[-1] == 8000.00

    def test_list_rooms_sort_by_price_desc(self, api_client, sample_rooms):
        response = api_client.get("/rooms/list?sort_by=price&order=desc")

        assert response.status_code == status.HTTP_200_OK

        prices = [float(room["price"]) for room in response.data]
        assert prices == sorted(prices, reverse=True)
        assert prices[0] == 8000.00
        assert prices[-1] == 2000.00

    def test_list_rooms_invalid_sort_field(self, api_client):
        response = api_client.get("/rooms/list?sort_by=invalid_field")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_list_rooms_invalid_order(self, api_client):
        response = api_client.get("/rooms/list?sort_by=price&order=invalid")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
