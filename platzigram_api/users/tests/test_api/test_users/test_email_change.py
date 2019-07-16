"""Tests related to an endpoint to request an email change."""

# Django REST Framework
from rest_framework.test import APITestCase

# Django
from django.shortcuts import reverse
from django.core import mail
from django.conf import settings

# JWT
import jwt

# Models
from platzigram_api.users.models.users import User


class EmailChangeEndpointTestCase(APITestCase):
    """Test Class used to create tests to check the proper functioning of the endpoint to request the email change"""

    def setUp(self) -> None:
        """Set the data to use on all the tests of this class."""

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

        self.urls = {
            'request_email_change': reverse('users:users-request-email-change', args=[self.username]),
            'change_email': reverse('users:users-change-email', args=[self.username])
        }

        self.login_response = self.client.post(
            reverse('users:users-login'),
            data={
                'username': self.username,
                'password': self.password
            }
        ).json()

        self.token = self.login_response.get('access')

    def test_requesting_email_change(self):
        """Checks the requesting email endpoint works properly
        and the provided token works on the changing email endpoint.
        """

        url = self.urls['request_email_change']
        self.client.post(
            url,
            HTTP_AUTHORIZATION=f'JWT {self.token}',
            format='json'
        )
        self.assertEqual(len(mail.outbox), 1)

    def test_change_email(self):
        """Checks that changing email is made on a secure and safe way."""

        url = self.urls['change_email']
        new_email = 'idk@gmail.com'
        payload = {
            'user': self.username,
            'type': 'change_email'
        }

        # We are decoding a byte object not the Json Web token.
        token = jwt.encode(payload, settings.SECRET_KEY, args=['HS256']).decode()

        self.client.post(
            url,
            data={
                'token': token,
                'new_email': new_email
            },
            format='json',
            HTTP_AUTHORIZATION=f'JWT {self.token}'
        )

        user = User.objects.get(username=self.username)
        self.assertEqual(new_email, user.email)

        # The user will need to verify its new email.
        self.assertEqual(user.is_email_verified, False)
        self.assertEqual(len(mail.outbox), 1)
