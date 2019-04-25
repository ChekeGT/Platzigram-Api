"""Dummie views that will be used on tests."""

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated

# Status
from rest_framework.status import (
    HTTP_200_OK
)


class AuthenticationRequiredDummieView(APIView):
    """Dummie View for check authentication is valid."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Dummie method to return HTTP 200 if authentication succeeds."""

        return Response(data={}, status=HTTP_200_OK)
