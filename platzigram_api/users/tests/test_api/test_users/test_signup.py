"""Signup View Related tests."""

# Django REST Framework
from rest_framework.test import (
    APITestCase
)

# Django
from django.shortcuts import reverse
from django.contrib.auth import authenticate

# Models
from platzigram_api.users.models import User


class SignupUserTest(APITestCase):
    """User Model Viewset related tests."""

    def setUp(self) -> None:
        """Sets up all the data to create an user."""

        self.user_data = {
            'username': 'luis',
            'email': 'luis@gmail.com',
            'password': 'luis1234',
            'password_confirmation': 'luis1234',
            'first_name': 'Luis',
            'last_name': 'Perez',
            'phone_number': '+1 4687897977854'
        }

        self.url = reverse('users:users-signup')

        self.response = self.client.post(
            self.url,
            data=self.user_data,
            format='json'
        )

        self.username = self.user_data['username']
        self.password = self.user_data['password']

    def test_status_code_when_user_is_created(self):
        """Test that when a user is created the status code equals 201."""

        self.assertEqual(self.response.status_code, 201)

    def test_user_creation(self):
        """Tests that the user is created when we call the api."""

        self.assertTrue(
            User.objects.filter(username=self.user_data['username']).exists()
        )

    def test_password_is_encrypted(self):
        """Test that when an user is created the password is encrypted."""

        user = User.objects.get(
            username=self.user_data['username']
        )

        self.assertNotEqual(self.user_data['password'], user.password)

    def test_user_can_authenticate(self):
        """Test the user created can authenticate to the api."""

        username = self.user_data['username']
        password = self.user_data['password']

        user = authenticate(username=username, password=password)

        self.assertIsNotNone(user)
        self.assertEqual(
            User.objects.get(username=username),
            user
        )
