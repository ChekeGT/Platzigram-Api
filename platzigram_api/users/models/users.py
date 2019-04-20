"""Users model."""

# Django
from django.db import models
from django.core.validators import RegexValidator

# Models
from platzigram_api.utils.models import PlatzigramBaseAbstractModel
from django.contrib.auth.models import AbstractUser

# Signals
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(PlatzigramBaseAbstractModel, AbstractUser):
    """User model that inherits from the Abstract user class.

    Extends the fields with:
        Phone Number
    """

    PHONE_REGEX_VALIDATOR = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +99 999. Up to 20 digits allowed."
    )

    phone_number = models.CharField(
        blank=True,
        validators=[
            PHONE_REGEX_VALIDATOR,
        ],
        max_length=20
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with this email already exists.'
        }
    )

    is_email_verified = models.BooleanField(
        default=False,
        help_text='Set to true when a user has verified its email.'
    )

    REQUIRED_FIELDS = ['email', 'phone_number', 'first_name', 'last_name']


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """When a user is created, creates a profile related to that user."""

    # I import profile here cause i can't import it right in the top.
    from .profiles import Profile

    user = kwargs['instance']

    Profile.objects.get_or_create(user=user)
