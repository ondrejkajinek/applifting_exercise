"""Views for Product api."""

# third-party
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

# local
from .models import Offer, Product
from .serializers import PriceChangeSerializer, PriceSerializer
from .serializers import ProductDetailSerializer, ProductSerializer


# pylint: disable=too-many-ancestors
class ProductViewSet(viewsets.ModelViewSet):
    """
    Product endpoints.

    Supports:
        list: GET /api/product/
        create: POST /api/product/
        detail: GET /api/product/{id}/
        update: PUT /api/product/{id}/
        delete: DELETE /api/product/{id}/
    """

    queryset = Product.objects
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Get non-prefetched queryset for update and destroy actions."""
        return (
            Product.objects.prefetched()
            if self.action == "retrieve"
            else super().get_queryset()
        )

    def get_serializer_class(self):
        """Get special serializer for retrieve action."""
        return (
            ProductDetailSerializer
            if self.action == "retrieve"
            else super().get_serializer_class()
        )

    def list(self, *args, **kwargs):    # pylint: disable=unused-argument
        """Handle for GET /api/product/."""
        queryset = (
            self.get_queryset()
            .annotate(prices_count=Count("offers__prices"))
            .filter(prices_count__gt=0)
        )
        return Response(queryset.values("id", "name", "description"))

    # pylint: disable=unused-argument
    def create(self, request, *args, **kwargs):
        # pylint: enable=unused-argument
        """Handle for POST /api/product/."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        product_data = dict(serializer.data)
        product_data["id"] = created.pk
        return Response(product_data, status=status.HTTP_201_CREATED)

    def update(self, *args, **kwargs):
        """Handle for PUT /api/product/{id}/."""
        kwargs["partial"] = True
        return super().update(*args, **kwargs)  # pylint: disable=no-member


class OfferViewSet(viewsets.GenericViewSet):
    """
    Price history endpoint.

    Supports:
        changes: GET /api/offer/{id}/changes/
    """

    queryset = Offer.objects.prefetched()
    serializer_class = PriceSerializer

    @decorators.action(detail=True, methods=["GET"])
    # pylint: disable=unused-argument
    def changes(self, request, *args, **kwargs):
        # pylint: enable=unused-argument
        """Handle for GET /api/price/changes/."""
        try:
            time_from = int(request.query_params.get("time_from") or 0)
            time_to = int(
                request.query_params.get("time_to") or
                timezone.now().timestamp()
            )
        except ValueError:
            return Response(
                {
                    "time_from": "Timestamp expected",
                    "time_to": "Timestamp expected"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        offer = self.get_object()
        prices = (
            offer.prices
            .filter(timestamp_from__lt=time_to)
            .filter(
                Q(timestamp_to__gte=time_from) |
                Q(timestamp_to__isnull=True)
            )
        )
        base_price = prices.first().price
        for price in prices:
            price.base_price = base_price

        serializer = PriceChangeSerializer(prices, many=True)
        return Response(serializer.data)
# pylint: enable=too-many-ancestors
