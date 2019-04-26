"""Api tests related to the verification functionality on API."""

# Django
from django.shortcuts import reverse

# Django REST Framework
from rest_framework.test import APITestCase

# Models
from platzigram_api.users.models import User

# Serializers
from platzigram_api.users.serializers import UserSignupSerializer


class UserVerificationTest(APITestCase):
    """Tests related to the user verification functionality."""

    def setUp(self) -> None:
        """Sets up everything related to this test case class."""

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

        self.client.post(
            reverse('users:users-signup'),
            data=self.user_data,
            format='json'
        )

        self.user = User.objects.get(username=self.username)

    def test_user_verification(self):
        """Check that when we make a request to the verify url with a valid token the user becomes verified."""

        url = reverse('users:users-verify')
        verification_token = UserSignupSerializer.generate_verification_token(self.user)

        self.client.post(
            url,
            data={
                'token': verification_token
            },
            format='json'
        )

        user = User.objects.get(username=self.username)

        self.assertTrue(user.is_email_verified)
