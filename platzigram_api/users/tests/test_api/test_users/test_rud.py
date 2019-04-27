"""Tests related to test the RUD of User Model"""

# Django
from django.shortcuts import reverse
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework.test import APITestCase

# Models
from platzigram_api.users.models import (
    Profile,
    User
)


class UserModelCRUDTestCase(APITestCase):
    """Tests related to the RUD of the user model."""

    def setUp(self) -> None:
        """Sets up everything related to this tests."""

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

        self.login_response = self.client.post(
            reverse('users:users-login'),
            data={
                'username': self.username,
                'password': self.password
            }
        )

        self.token = self.login_response.json().get('access')
        self.http_authorization = f'JWT {self.token}'

        self.url = reverse('users:users-detail', args=[self.username])

    def test_read_user(self):
        """Tests retrieve endpoint for the user model."""

        response = self.client.get(
            self.url,
            format='json',
            HTTP_AUTHORIZATION=self.http_authorization
        )
        json = response.json()

        self.assertEqual(
            json,
            {
                'username': self.username,
                'first_name': self.user_data['first_name'],
                'last_name': self.user_data['last_name'],
                'email': self.user_data['email'],
                'phone_number': self.user_data['phone_number'],
                'is_email_verified': False
            }
        )

    def test_update_user(self):
        """Tests full update endpoint of the user model."""

        new_user_data = {
            'username': 'pablo',
            'first_name': 'Pablo',
            'last_name': 'Trinidad xd',
            'phone_number': '+1 5464894984',
            'password': self.user_data['password'],
            'new_password': 'pablo123456',
            'new_password_confirmation': 'pablo123456',
        }
        response = self.client.put(
            self.url,
            data=new_user_data,
            format='json',
            HTTP_AUTHORIZATION=self.http_authorization
        )
        json = response.json()

        self.assertEqual(
            {
                'username': new_user_data['username'],
                'first_name': new_user_data['first_name'],
                'last_name': new_user_data['last_name'],
                'email': self.user_data['email'],
                'phone_number': new_user_data['phone_number'],
                'is_email_verified': False
            },
            json
        )

    def test_partial_update_user(self):
        """Tests partial update endpoint of the user model."""

        # Username is missing here so yes it is partial update
        new_user_data = {
            'first_name': 'Pablo',
            'last_name': 'Trinidad xd',
            'password': self.user_data['password'],
            'new_password': 'pablo123456',
            'new_password_confirmation': 'pablo123456',
            'phone_number': '+52 954164789',
        }
        response = self.client.patch(
            self.url,
            data=new_user_data,
            format='json',
            HTTP_AUTHORIZATION=self.http_authorization
        )
        json = response.json()

        self.assertEqual(
            {
                'username': self.username,
                'first_name': new_user_data['first_name'],
                'last_name': new_user_data['last_name'],
                'email': self.user_data['email'],
                'phone_number': new_user_data['phone_number'],
                'is_email_verified': False
            },
            json
        )

        self.assertIsNotNone(
            authenticate(
                username=self.username,
                password=new_user_data['new_password']
            )
        )

    def test_delete_user(self):
        """Tests delete endpoint of the user model."""

        user = User.objects.get(username=self.username)
        user_pk = user.pk
        profile_pk = user.profile.pk

        self.client.delete(
            self.url,
            format='json',
            HTTP_AUTHORIZATION=self.http_authorization
        )

        self.assertFalse(
            User.objects.filter(pk=user_pk).exists()
        )

        self.assertFalse(
            Profile.objects.filter(pk=profile_pk).exists()
        )
