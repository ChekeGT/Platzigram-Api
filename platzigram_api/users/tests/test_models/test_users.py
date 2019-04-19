"""User model related tests."""

# Django
from django.test import TestCase
from django.contrib.auth import authenticate

# Models
from platzigram_api.users.models import (
    User,
    Profile
)


class UserModelTestCase(TestCase):
    """User Model Test Case defines all the tests related with the user model."""

    def setUp(self) -> None:
        """Sets up every thing we are going to use on the tests."""
        self.user = User.objects.create_user(
            username='cheke',
            password='idkskere',
            email='chekelosos@gmail.com',
            first_name='Francisco Ezequiel',
            last_name='Banos Ramirez',
            phone_number='+52 9581006329'
        )
        self.raw_password = 'idkskere'
        self.username = self.user.username

    def test_profile_is_created_when_user_is_created(self) -> 'None':
        """This test evaluates if a Profile proxy model is created when a user is created."""

        profile_queryset = Profile.objects.filter(
            user=self.user
        )
        self.assertTrue(
            profile_queryset.exists()
        )

    def test_password_is_encrypted_when_user_is_created(self) -> 'None':
        """This test evaluates if when we create an user the password is encrypted."""

        self.assertNotEqual(self.raw_password, self.user.password)

    def test_authentication_is_usable(self) -> 'None':
        """This test evaluates if the authentication is usable."""

        user = authenticate(
            username=self.username,
            password=self.raw_password,
        )

        self.assertIsNotNone(user)
