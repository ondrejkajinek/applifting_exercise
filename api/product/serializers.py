"""API serializers for Product app."""

# third-party
from rest_framework import serializers

# local
from .models import Offer, Price, Product


# pylint: disable=too-few-public-methods
class PriceSerializer(serializers.ModelSerializer):
    # pylint: enable=too-few-public-methods
    """Serializer for Price entity."""

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Price
        fields = ["price", "timestamp_to", "timestamp_from"]


# pylint: disable=too-few-public-methods
class PriceChangeSerializer(serializers.ModelSerializer):
    # pylint: enable=too-few-public-methods
    """Serializer for Price change entity."""

    change = serializers.SerializerMethodField()

    # pylint: disable=too-few-public-methods
    class Meta(PriceSerializer.Meta):
        # pylint: enable=too-few-public-methods
        """Serializer configuration."""

        model = Price
        fields = ["change", "timestamp_to", "timestamp_from"]

    def get_change(self, price):    # pylint: disable=no-self-use
        """Get relative price change."""
        return (price.price - price.base_price) / price.base_price


# pylint: disable=too-few-public-methods
class OfferSerializer(serializers.ModelSerializer):
    # pylint: enable=too-few-public-methods
    """Serializer for Offer entity, selecting only active price."""

    price = serializers.SerializerMethodField()

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Offer
        fields = ["id", "price", "items_in_stock"]

    def get_price(self, offer):     # pylint: disable=no-self-use
        """Get current price for Offer."""
        return offer.prices.current().price


# pylint: disable=too-few-public-methods
class ProductDetailSerializer(serializers.ModelSerializer):
    # pylint: enable=too-few-public-methods
    """Detail serializer for Product entity."""

    offers = OfferSerializer(read_only=True, many=True)

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Product
        fields = ["id", "name", "description", "offers"]


# pylint: disable=too-few-public-methods
class ProductSerializer(serializers.ModelSerializer):
    # pylint: enable=too-few-public-methods
    """Serializer for Product entity."""

    class Meta:     # pylint: disable=too-few-public-methods
        """Serializer configuration."""

        model = Product
        fields = ["id", "name", "description"]
