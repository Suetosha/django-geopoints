from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point as GeosPoint
from django.contrib.gis.measure import D
from .models import Point, Message
from .serializers import PointSerializer, MessageSerializer


class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Создание сообщения
    @action(detail=False, methods=['post'])
    def messages(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Поиск точек по радиусу
    @action(detail=False, methods=['get'])
    def search(self, request):
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        radius = request.query_params.get('radius')

        if not all([lat, lon, radius]):
            return Response({"error": "Укажите latitude, longitude и radius"}, status=400)

        user_location = GeosPoint(float(lon), float(lat), srid=4326)

        # Ищем точки, которые находятся в радиусе
        points = Point.objects.filter(
            coordinates__distance_lte=(user_location, D(km=radius))
        ).annotate(distance=Distance('coordinates', user_location)).order_by('distance')

        serializer = self.get_serializer(points, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Поиск сообщений по радиусу
    @action(detail=False, methods=['get'])
    def search(self, request):
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        radius = request.query_params.get('radius')

        if not all([lat, lon, radius]):
            return Response({"error": "Укажите latitude, longitude и radius"}, status=400)

        user_location = GeosPoint(float(lon), float(lat), srid=4326)

        # Ищем сообщения, точки которых находятся в радиусе
        messages = Message.objects.filter(
            point__coordinates__distance_lte=(user_location, D(km=radius))
        )

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
