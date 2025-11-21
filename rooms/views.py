from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Room
from .serializers import RoomSerializer, RoomListSerializer


@api_view(['POST'])
def room_create(request):
    serializer = RoomSerializer(data=request.data)
    
    if serializer.is_valid():
        room = serializer.save()
        return Response(
            {"id": room.id},
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def room_delete(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    
    return Response(
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['GET'])
def room_list(request):
    sort_by = request.query_params.get('sort_by', 'created_at')
    order = request.query_params.get('order', 'desc')
    allowed_sort_fields = ['price', 'created_at']
    allowed_orders = ['asc', 'desc']
    if sort_by not in allowed_sort_fields:
        return Response(
            {
                "error": f"Недопустимое поле для сортировки: {sort_by}. "
                        f"Разрешённые значения: {', '.join(allowed_sort_fields)}"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if order not in allowed_orders:
        return Response(
            {
                "error": f"Недопустимый порядок сортировки: {order}. "
                        f"Разрешённые значения: {', '.join(allowed_orders)}"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order_prefix = '' if order == 'asc' else '-'
    order_by = f'{order_prefix}{sort_by}'
    rooms = Room.objects.all().order_by(order_by)
    serializer = RoomListSerializer(rooms, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
