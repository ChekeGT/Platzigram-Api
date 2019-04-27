"""User model related views."""

# Django REST Framework
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)

# Serializers
from platzigram_api.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer,
    VerifyUserSerializer
)

# Mixins
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

# Models
from platzigram_api.users.models import User

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from platzigram_api.users.permissions import IsAccountOwner


class UserModelViewset(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """User Model Viewset

    Manages all tasks related to the user model.
    """

    queryset = User.objects.all()
    lookup_field = 'username'

    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        """Signup endpoint manages the creation of an user

        It also manages sending a confirmation email when the user is created
        and generate a verification token to the verification can be performed.
        """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            data = UserModelSerializer(user).data

            return Response(data=data, status=HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request, *args, **kwargs):
        """Verification endpoint manages the verification of an user.

        Requires a JWT signed by the api, and if it is valid this
        endpoint will make verified to the user contained in the
        JWT.
        """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            data = UserModelSerializer(user).data

            return Response(data=data, status=HTTP_200_OK)

    def get_serializer_class(self):
        """Returns serializers based on action"""

        if self.action == 'signup':
            return UserSignupSerializer

        if self.action == 'verify':
            return VerifyUserSerializer

        else:
            return UserModelSerializer

    def get_permissions(self):
        """Returns permissions based on action."""

        if self.action in ['verify', 'login', 'signup']:
            return [AllowAny()]

        if self.action in ['destroy', 'retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsAccountOwner()]

        return super(UserModelViewset, self).get_permissions()
