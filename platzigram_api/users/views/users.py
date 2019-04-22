"""User model related views."""

# Django REST Framework
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Status
from rest_framework.status import (
    HTTP_201_CREATED
)

# Serializers
from platzigram_api.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer
)


class UserModelViewset(GenericViewSet):
    """User Model Viewset

    Manages all tasks related to the user model.
    """

    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        """"""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            data = UserModelSerializer(user).data

            return Response(data=data, status=HTTP_201_CREATED)

    def get_serializer_class(self):
        """Returns serializers based on action"""

        if self.action == 'signup':
            return UserSignupSerializer

        else:
            return super(UserModelViewset, self).get_serializer_class()
