from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer


@api_view(['POST'])
def booking_create(request):
    serializer = BookingCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        booking = serializer.save()
        return Response(
            {"id": booking.id},
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    
    return Response(
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['GET'])
def booking_list(request):
    room_id = request.query_params.get('room_id')
    
    if not room_id:
        return Response(
            {"error": "Параметр room_id обязателен"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    from rooms.models import Room
    room = get_object_or_404(Room, id=room_id)
    
    bookings = Booking.objects.filter(room=room)
    
    serializer = BookingSerializer(bookings, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

