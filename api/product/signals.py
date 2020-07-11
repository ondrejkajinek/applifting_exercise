"""Signals for Product api."""

# third-party
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from .models import Product


# @receiver(post_save, sender=Product)
def register_product(instance, created, **kwargs):
    """Register product to Offer microservice."""
    # TODO: move to integration
    if created:
        data = {
            "name": instance.name,
            "description": instance.description
        }
        print("I would report product %r" % data)
        # TODO: register
