from rest_framework import serializers
from django.contrib.gis.geos import Point as GeosPoint
from .models import Point, Message


class PointSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Point
        fields = ['id', 'user', 'name', 'coordinates', 'latitude', 'longitude', 'created_at']
        read_only_fields = ['user', 'coordinates', 'created_at']

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')

        # Преобразование lat и lon в coordinates перед сохранением в бд
        validated_data['coordinates'] = GeosPoint(lon, lat, srid=4326)

        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'text', 'point', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
