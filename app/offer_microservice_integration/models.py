"""Database models for Offer microservice integration app."""

# third-party
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Configuration(models.Model):
    """Dynamic configuration."""

    key = models.CharField(
        verbose_name=_("Key"),
        max_length=255,
        unique=True
    )
    value = models.CharField(
        verbose_name=_("Value"),
        max_length=255
    )

    def __str__(self):
        """Create printable representation of Configuration."""
        return "{}: {}".format(self.key, self.value)
