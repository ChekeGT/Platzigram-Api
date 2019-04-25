"""Test related to login view."""

# Django
from django.shortcuts import reverse
from django.urls import (
    path,
    include
)

# Django REST Framework
from rest_framework.test import (
    APITestCase,
    URLPatternsTestCase
)

# Views
from .dummie_views import AuthenticationRequiredDummieView


class UserLoginTestCase(APITestCase, URLPatternsTestCase):
    """User Login functionality related tests."""

    urlpatterns = [
        path('', include('config.urls')),
        path('is_authenticated/', AuthenticationRequiredDummieView.as_view(), name='is_authenticated')
    ]

    def setUp(self) -> None:
        """Sets up all the data to login an user."""

        self.user_data = {
            'username': 'luis',
            'email': 'luis@gmail.com',
            'password': 'luis1234',
            'password_confirmation': 'luis1234',
            'first_name': 'Luis',
            'last_name': 'Perez',
            'phone_number': '+1 4687897977854'
        }

        self.username = self.user_data['username']
        self.password = self.user_data['password']

        self.client.post(
            reverse('users:users-signup'),
            data=self.user_data,
            format='json'
        )

        self.url = reverse('users:users-login')

        self.response = self.client.post(
            self.url,
            data={
                'username': self.username,
                'password': self.password
            },
            format='json'
        )
        self.token = self.response.json().get('access', False)

    def test_authentication_is_valid(self):
        """Test that checks if the authentication is succeed when trying to access protected views."""

        response = self.client.get(
            reverse('is_authenticated'),
            HTTP_AUTHORIZATION=f'JWT {self.token}'
        )
        self.assertEqual(response.status_code, 200)
