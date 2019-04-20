"""User model related Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from platzigram_api.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User Model Serializer"""

    class Meta:
        """Metadata class."""

        model = User

        fields = (
            'username', 'first_name', 'last_name',
            'email'
        )
        read_only_fields = (
            'email'
        )

