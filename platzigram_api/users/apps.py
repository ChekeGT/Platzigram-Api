"""Users app configuration."""

# Django
from django.apps import AppConfig


class UserAppConfig(AppConfig):
    """User app class configuration.

    Contains all the necessary fields to the user app
    could be used as one.
    """

    name = 'platzigram_api.users'
    verbose_name = 'Users'
