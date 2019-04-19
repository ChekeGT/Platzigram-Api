"""Profile Model related tests."""

# Django
from django.test import TestCase

# Models
from platzigram_api.users.models import (
    User
)


class ProfileModelTestCase(TestCase):
    """Profile Model Test case is a class that manages every test related to Profile model."""

    def setUp(self) -> None:
        """Sets the general bars to be used on tests."""

        self.user = User.objects.create_user(
            username='cheke',
            password='idkskere',
            email='chekelosos@gmail.com',
            first_name='Francisco Ezequiel',
            last_name='Banos Ramirez',
            phone_number='+52 9581006329'
        )
        self.profile = self.user.profile

        self.user2 = User.objects.create_user(
            username='hermabody',
            password='idkskere',
            email='eli@fake.com',
            first_name='Eli',
            last_name='Estrada'
        )
        self.profile2 = self.user2.profile

    def test_following_other_user(self):
        """Test the functionality to follow another user."""

        self.profile.follow(
            self.profile2
        )

        self.assertIn(
            self.profile2,
            self.profile.following.all(
            )
        )
        self.assertIn(
            self.profile,
            self.profile2.followers.all(

            )
        )

    def test_unfollowing_other_user(self):
        """Test the functionality to unfollow another user."""

        self.profile.follow(
            self.profile2
        )

        # Following
        self.assertIn(
            self.profile2,
            self.profile.following.all(
            )
        )
        self.assertIn(
            self.profile,
            self.profile2.followers.all(

            )
        )

        self.profile.unfollow(
            self.profile2
        )

        # Unfollowing
        self.assertNotIn(
            self.profile2,
            self.profile.following.all(
            )
        )
        self.assertNotIn(
            self.profile,
            self.profile2.followers.all(

            )
        )
