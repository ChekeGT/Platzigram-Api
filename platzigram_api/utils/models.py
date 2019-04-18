"""Utils models.

They are abstract models on which other models from this web
service will inherit.
"""

# Django
from django.db import models


class PlatzigramBaseAbstractModel(models.Model):
    """This is the model from which every model on the webservice Platzigram will inherit.

    provides this fields to the models that will inherit from this class:
        created --> The date in which the object was created
        updated --> The last date in which the object was modified.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadata class."""

        abstract = True
        ordering = ['-created', '-updated']
