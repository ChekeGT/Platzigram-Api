"""User model related Serializers."""

# Django
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Django REST Framework
from rest_framework import serializers

# Models
from platzigram_api.users.models import User

# Validators
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

# Utilities
from django.utils import timezone
from datetime import timedelta

# JWT
import jwt


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
            'email',
        )


class UserSignupSerializer(serializers.Serializer):
    """User Signup Serializer.

    Handles all the log related to the creation of an user.
    """

    username = serializers.CharField(
        min_length=2,
        max_length=150,
        validators=[
            UniqueValidator(
                User.objects.all()
            )
        ]
    )

    email = serializers.EmailField(
        min_length=6,
        max_length=1000,
        validators=[
            UniqueValidator(
                User.objects.all(

                )
            )
        ]
    )

    password = serializers.CharField(
        min_length=8,
    )
    password_confirmation = serializers.CharField(
        min_length=8
    )

    PHONE_REGEX_VALIDATOR = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +99 999. Up to 20 digits allowed."
    )

    phone_number = serializers.CharField(
        validators=[
            PHONE_REGEX_VALIDATOR
        ]
    )

    first_name = serializers.CharField(
        max_length=100
    )

    last_name = serializers.CharField(
        max_length=100
    )

    def validate(self, data):
        """Validates password field with this verifications:

        Password and its confirmation are equal
        The password is valid according to the password validators of django
        """

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError('Password and password confirmation must be equal.')

        data.pop('password_confirmation')
        validate_password(password)

        return data

    def create(self, validated_data):
        """Handles the user creation."""

        user = User.objects.create_user(
            **validated_data
        )
        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        """Handles sending a confirmation email to the recently created user."""

        verification_token = self.generate_verification_token(user)
        subject = f'Welcome @{user.username}! Verify your account to start using Platzigram'
        from_email = 'Platzigram <noreply@platzigram.com>'
        content = render_to_string(
            template_name='emails/verify_account.html',
            context={
                'token': verification_token,
                'user': user,

                # Change this if the dns is another one.
                'dns': 'platzigram.com'
            }
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, 'text/html')
        msg.send()

    @staticmethod
    def generate_verification_token(user):
        """Handles generating a JWT for the user can verify its account"""

        expiration_date = timezone.now() + timedelta(days=3)

        payload = {
            'user': user.username,
            'exp': expiration_date,
            'type': 'email_confirmation'
        }

        # This could be a little bit confusing, why are we decoding this?
        # Well, the function jwt.encode returns a byte object so to parse
        # it to a string we need to use the method decode, but we are not
        # decoding the JWT, just passing the byte object to str.
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode()

        return token
