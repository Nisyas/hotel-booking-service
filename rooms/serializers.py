from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть положительным числом"
            )
        
        if value > 999999.99:
            raise serializers.ValidationError(
                "Цена не может превышать 999,999.99 рублей"
            )
        
        return value
    
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Название номера не может быть пустым"
            )
        
        if len(value) < 3:
            raise serializers.ValidationError(
                "Название номера должно содержать минимум 3 символа"
            )
        
        return value.strip()


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'price', 'created_at']
