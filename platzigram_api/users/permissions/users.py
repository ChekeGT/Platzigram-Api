"""User model related permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Permission that allows
     a user to access a view only if the requesting
     user matches with the user object
    """

    message = 'You are not the account owner.'

    def has_object_permission(self, request, view, user):
        """Returns if the requesting user matches with  the user being used by the view."""

        return request.user == user
