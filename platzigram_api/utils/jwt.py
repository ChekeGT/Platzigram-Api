"""Utilities related to the jwt technologies"""

# Django REST Framework Simple JWT
from rest_framework_simplejwt.tokens import RefreshToken


def blacklist_token(token):
    """Handles blacklisting a token so that it can not be used again"""

    refresh_token = RefreshToken(token)
    refresh_token.blacklist()
