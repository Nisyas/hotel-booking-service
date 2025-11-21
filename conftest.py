import pytest
from rest_framework.test import APIClient
from rooms.models import Room
from bookings.models import Booking
from datetime import date, timedelta


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_room():
    return Room.objects.create(
        name="Тестовый номер",
        description="Номер для тестирования",
        price=5000.00
    )


@pytest.fixture
def sample_rooms():
    rooms = [
        Room.objects.create(
            name="Эконом",
            description="Бюджетный номер",
            price=2000.00
        ),
        Room.objects.create(
            name="Стандарт",
            description="Стандартный номер",
            price=4000.00
        ),
        Room.objects.create(
            name="Люкс",
            description="Люксовый номер",
            price=8000.00
        ),
    ]
    return rooms


@pytest.fixture
def sample_booking(sample_room):
    today = date.today()
    return Booking.objects.create(
        room=sample_room,
        date_start=today + timedelta(days=1),
        date_end=today + timedelta(days=5)
    )


@pytest.fixture
def future_dates():
    today = date.today()
    return {
        'today': today,
        'tomorrow': today + timedelta(days=1),
        'in_3_days': today + timedelta(days=3),
        'in_5_days': today + timedelta(days=5),
        'in_10_days': today + timedelta(days=10),
    }
