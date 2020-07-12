"""Signals for Product api."""

# third-party
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from api.product.models import Product
from .client import OfferMicroserviceClient


@receiver(post_save, sender=Product)
def register_product(instance, created, **kwargs):
    """Register product to Offer microservice."""
    if not created:
        return

    client = OfferMicroserviceClient()
    client.register_product(instance)
