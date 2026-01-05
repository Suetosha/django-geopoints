from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point as GeosPoint
from .models import Point, Message


class GeoPointsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создание тестовой точки
        self.point = Point.objects.create(
            user=self.user,
            name="Тестовая точка",
            coordinates=GeosPoint(20.46, 44.81, srid=4326)
        )
        # Создание сообщения для этой точки
        self.message = Message.objects.create(
            user=self.user,
            point=self.point,
            text="Тестовое сообщение"
        )

    # Тест по поиску точек в радиусе
    def test_search_points_success(self):
        url = reverse('point-search')

        response = self.client.get(url, {
            'latitude': 44.81,
            'longitude': 20.46,
            'radius': 10
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Тестовая точка")

    # Тест по поиску сообщений в радиусе
    def test_search_messages_success(self):
        url = reverse('message-search')

        response = self.client.get(url, {
            'latitude': 44.81,
            'longitude': 20.46,
            'radius': 5
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], "Тестовое сообщение")

    # Тест по обработке некорректных параметров
    def test_search_invalid_params(self):
        url = reverse('point-search')

        response = self.client.get(url, {
            'latitude': 'abc',
            'longitude': 38.97,
            'radius': 5
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Координаты и радиус должны быть числами")

    # Тест по созданию сообщения
    def test_create_message_via_action(self):
        url = reverse('point-messages')

        data = {
            'point': self.point.id,
            'text': "Новое сообщение"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)
