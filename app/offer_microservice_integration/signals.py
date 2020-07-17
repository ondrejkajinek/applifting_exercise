"""Signals for Product api."""

# third-party
from django.db.models.signals import post_save

# local
from api.product.models import Product
from .client import OfferMicroserviceClient


# pylint: disable=unused-argument
def register_product(instance, created, **kwargs):
    """Register product to Offer microservice."""
    if not created:
        return

    client = OfferMicroserviceClient()
    client.register_product(instance)
# pylint: enable=unused-argument


post_save.connect(
    register_product,
    sender=Product,
    dispatch_uid="app.offer_microservice_integration.register_product"
)
