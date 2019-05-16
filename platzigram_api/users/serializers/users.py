"""User model related Serializers."""

# Django
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers

# Django REST Framework Simple JWT
from rest_framework_simplejwt.tokens import (
    UntypedToken,
    RefreshToken
)

# Models
from platzigram_api.users.models import User

# Validators
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

# Utilities
from django.utils import timezone
from datetime import timedelta
from platzigram_api.utils.jwt import blacklist_token

# JWT
import jwt

# Exceptions
from rest_framework_simplejwt.exceptions import TokenError


class UserModelSerializer(serializers.ModelSerializer):
    """User Model Serializer"""

    password = serializers.CharField(required=False)

    new_password = serializers.CharField(
        min_length=8,
        required=False
    )
    new_password_confirmation = serializers.CharField(
        min_length=8,
        required=False
    )

    refresh_token = serializers.CharField(
        required=False
    )

    class Meta:
        """Metadata class."""

        model = User

        fields = (
            # Serializer fields
            'username', 'first_name', 'last_name',
            'email', 'phone_number', 'is_email_verified',

            # Not Serialized fields
            'new_password', 'new_password_confirmation',
            'password', 'refresh_token'
        )

        read_only_fields = (
            'is_email_verified', 'email'
        )

    def validate_refresh_token(self, refresh_token):
        """Validates that refresh token:

        Is valid to the given user.
        """

        UntypedToken(refresh_token)

        try:
            RefreshToken(refresh_token)
        except TokenError as e:
            raise serializers.ValidationError(e)

        payload = jwt.decode(refresh_token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])

        request = self.context['request']

        if payload.get('user_id', False) != request.user.id:
            raise serializers.ValidationError('The given refresh token is not valid for this user.')

        return refresh_token

    def validate(self, data):
        """Validates password fields."""

        # If the requesting user is trying to change its password

        if 'password' in data or 'new_password' in data or 'new_password_confirmation' in data:

            # Checks if some data is missing

            password = data.get('password', False)
            if not password:
                raise serializers.ValidationError('You must provide your password')

            new_password = data.get('new_password', False)
            if not new_password:
                raise serializers.ValidationError('You must provide a new password')

            new_password_confirmation = data.get('new_password_confirmation', False)
            if not new_password_confirmation:
                raise serializers.ValidationError('You must provide the confirmation of your new password.')

            refresh_token = data.get('refresh_token', False)
            if not refresh_token:
                raise serializers.ValidationError('You must provide your refresh token.')

            # Checks if the password is valid.

            username = self.context['request'].user.username

            if not authenticate(username=username, password=password):
                raise serializers.ValidationError('Password you provide is wrong.')

            # Checks the new password

            if new_password != new_password_confirmation:
                raise serializers.ValidationError('New password and its confirmation must be equal.')

            validate_password(new_password)

            data.pop('password')
            data.pop('new_password_confirmation')

            self.context['is_user_changing_password'] = True

        return data

    def update(self, instance, validated_data):
        """Extends the normal functionality to:

        Change password of the user if is trying to change it.
        """

        if self.context.get('is_user_changing_password', False):

            new_password = validated_data['new_password']

            instance.set_password(new_password)
            instance.save()

            token = validated_data['refresh_token']

            if token:
                blacklist_token(token)

            validated_data.pop('new_password')

        return super(UserModelSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        """Returns the normal representation only excluding the password."""

        representation_data = super(UserModelSerializer, self).to_representation(instance)
        representation_data.pop('password')

        if 'refresh_token' in representation_data:
            representation_data.pop('refresh_token')

        return representation_data


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


class VerifyUserSerializer(serializers.Serializer):
    """Handles verification of an user.

    Manages validating the JWT and if it's valid
    will make the user verified :D.
    """

    token = serializers.CharField(max_length=10**10)

    def validate_token(self, token):
        """Handles validating the JWT and verifying that was signed by the api."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            payload_type = payload['type']

            if payload_type != 'email_confirmation':
                raise jwt.PyJWTError

        except (
            jwt.PyJWTError,
            jwt.DecodeError
        ):
            raise serializers.ValidationError('Token is not valid.')

        self.context['username'] = payload['user']

        return token

    def validate(self, data):
        """Handles validating the User is not verified yet."""

        username = self.context['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('You\'re trying to verify a user who no longer exists.')

        if user.is_email_verified:
            raise serializers.ValidationError('User is already verified.')

        self.context['user'] = user
        return data

    def save(self):
        """Handles making the user verified."""

        username = self.context['user']

        user = User.objects.get(username=username)

        user.is_email_verified = True
        user.save()

        return user
