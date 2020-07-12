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


class PriceChangeSerializer(serializers.ModelSerializer):
    """Serializer for Price change entity."""

    change = serializers.SerializerMethodField()

    class Meta(PriceSerializer.Meta):
        """Serializer configuration."""

        model = Price
        fields = ["change", "timestamp_from", "timestamp_to"]

    def get_change(self, price):
        """Get relative price change."""
        return (price.price - price.base_price) / price.base_price


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
        return offer.prices.current().price


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product entity."""

    offers = OfferSerializer(read_only=True, many=True)

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Product
        fields = ["name", "description", "offers"]
