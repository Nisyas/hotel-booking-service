from datetime import date

from rest_framework import serializers

from rooms.models import Room

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source="room.name", read_only=True)
    duration_days = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "room",
            "room_name",
            "date_start",
            "date_end",
            "duration_days",
            "total_price",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_room(self, value):
        if not isinstance(value, Room):
            try:
                value = Room.objects.get(id=value)
            except Room.DoesNotExist:
                raise serializers.ValidationError(f"Номер с ID {value} не существует")
        return value

    def validate_date_start(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                f"Нельзя забронировать номер на прошедшую дату. "
                f"Минимальная дата: {date.today().isoformat()}"
            )
        return value

    def validate(self, data):
        date_start = data.get("date_start")
        date_end = data.get("date_end")
        room = data.get("room")

        if date_end <= date_start:
            raise serializers.ValidationError(
                {"date_end": "Дата окончания должна быть позже даты начала"}
            )

        if date_start < date.today():
            raise serializers.ValidationError(
                {
                    "date_start": f"Нельзя бронировать на прошедшую дату. "
                    f"Минимальная дата: {date.today().isoformat()}"
                }
            )

        room_id = room.id if isinstance(room, Room) else room

        overlapping_bookings = Booking.objects.filter(
            room_id=room_id, date_start__lt=date_end, date_end__gt=date_start
        )

        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

        if overlapping_bookings.exists():
            conflict = overlapping_bookings.first()
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        f"Номер '{room.name if isinstance(room, Room) else room_id}' "
                        f"уже забронирован на период с {date_start} по {date_end}. "
                        f"Конфликтующая бронь: {conflict.date_start} - {conflict.date_end}. "
                        f"Выберите другие даты или другой номер."
                    ]
                }
            )

        return data


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)
    date_start = serializers.DateField(input_formats=["%Y-%m-%d"])
    date_end = serializers.DateField(input_formats=["%Y-%m-%d"])

    def validate_date_start(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                f"Нельзя забронировать номер на прошедшую дату. "
                f"Минимальная дата: {date.today().isoformat()}"
            )
        return value

    def validate(self, data):
        date_start = data["date_start"]
        date_end = data["date_end"]
        room_id = data["room_id"]

        if date_end <= date_start:
            raise serializers.ValidationError(
                {"date_end": "Дата окончания должна быть позже даты начала"}
            )

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise serializers.ValidationError({"room_id": f"Номер с ID {room_id} не существует"})

        overlapping = Booking.objects.filter(
            room_id=room_id, date_start__lt=date_end, date_end__gt=date_start
        )

        if overlapping.exists():
            conflict = overlapping.first()
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        f"Номер уже забронирован на указанные даты. "
                        f"Конфликтующая бронь: {conflict.date_start} - {conflict.date_end}"
                    ]
                }
            )

        data["room"] = room
        return data

    def create(self, validated_data):
        return Booking.objects.create(
            room=validated_data["room"],
            date_start=validated_data["date_start"],
            date_end=validated_data["date_end"],
        )
