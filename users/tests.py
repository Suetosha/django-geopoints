from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class RegistrationTests(APITestCase):

    # Тест по успешной регистрации пользователя
    def test_register_user_success(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test_123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertNotIn('password', response.data)

    # Тест по регистрации с недостающими данными
    def test_register_user_missing_data(self):
        url = reverse('register')
        data = {'username': 'testuser'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    # Тест регистрации с существующим именем пользователя
    def test_register_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='password123')
        url = reverse('register')
        data = {
            'username': 'existinguser',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
