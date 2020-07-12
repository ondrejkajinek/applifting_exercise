"""API serializers for Product app."""

# third-party
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

# local
from .models import Offer, Price, Product


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for Price entity."""

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Price
        fields = ["price", "timestamp_from", "timestamp_to"]


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer entity, selecting only active price."""

    price = serializers.SerializerMethodField()

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Offer
        fields = ["price", "items_in_stock"]

    def get_price(self, offer):
        """Get current price for Offer."""
        current_timestamp = timezone.now().timestamp()
        return offer.prices.get(
            (
                Q(timestamp_to__isnull=True) |
                Q(timestamp_to__gte=current_timestamp)
            ),
            timestamp_from__lte=current_timestamp
        ).price


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product entity."""

    offers = OfferSerializer(read_only=True, many=True)

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Product
        fields = ["name", "description", "offers"]
