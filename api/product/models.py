"""Database models for Product api."""

# third-party
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductManager(models.Manager):
    """Manager for prefetched Products."""

    def prefetched(self):
        """Prepare queryset with prefetched related objects."""
        return (
            self.get_queryset()
            .annotate(prices_count=models.Count("offers__prices"))
            .filter(prices_count__gt=0)
            .prefetch_related("offers")
            .prefetch_related("offers__prices")
        )


class OfferManager(models.Manager):
    """Manager for prefetched Offers."""

    def prefetched(self):
        """Prepare queryset with prefetched related objects."""
        return (
            self.get_queryset()
            .prefetch_related("prices")
        )


class Product(models.Model):
    """Real world products you can buy."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255
    )
    description = models.TextField(
        verbose_name=_("Description")
    )

    objects = ProductManager()

    def __str__(self):
        """Create printable representation of Product."""
        return str(self.name)


class Offer(models.Model):
    """Offer representing a product being offered for some price somewhere."""

    external_id = models.IntegerField(
        verbose_name=_("Offer microservice ID"),
        unique=True
    )
    items_in_stock = models.PositiveIntegerField(
        verbose_name=_("Item in stock")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="offers"
    )

    objects = OfferManager()

    def __str__(self):
        """Create printable representation of Offer."""
        return "{} offer: {!d} items in stock".format(
            self.product, self.items_in_stock
        )


class Price(models.Model):
    """Price for offer that is valid in some time period."""

    timestamp_from = models.PositiveIntegerField(
        verbose_name=_("Timestamp from")
    )
    timestamp_to = models.PositiveIntegerField(
        verbose_name=_("Timestamp to, exclusive"),
        null=True
    )
    price = models.FloatField(
        verbose_name=_("Price")
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="prices"
    )

    class Meta:     # pylint: disable=too-few-public-methods
        """Model configuration."""

        ordering = ["-timestamp_from"]

    def __str__(self):
        """Create printable representation of Price."""
        return "{} price: {:0.2f}".format(self.offer, self.price)
