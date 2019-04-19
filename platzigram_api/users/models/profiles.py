"""Profile model."""

# Django
from django.db import models

# Models
from .users import User
from platzigram_api.utils.models import PlatzigramBaseAbstractModel


class Profile(PlatzigramBaseAbstractModel):
    """Profile model.

    Proxy model that contains public data of an user.
    the public data it contains is:
        Website
        Biography
        Phone Number
        Picture
        Followers
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    website = models.URLField(
        blank=True,
        max_length=300,
    )
    biography = models.TextField(
        blank=True
    )

    picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='users/pictures'
    )

    followers = models.ManyToManyField(
        'self',
        related_name='following',
        symmetrical=False
    )

    def __str__(self) -> 'str':
        """Returns the string representation of a profile."""

        return f"Profile of User {self.user.username}"

    def follow(self, profile) -> 'None':
        """Function that allows this profile to follow another one."""

        self.following.add(profile)
        profile.followers.add(self)

    def unfollow(self, profile) -> 'None':
        """Function that allows this profile to unfollow another one."""

        self.following.remove(profile)
        profile.followers.remove(profile)
