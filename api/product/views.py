"""Views for Product api."""

# third-party
# from django.http import JsonResponse, Http404
from django.http import Http404
from django.db.models import Q
from django.utils import timezone
from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

# local
from api.product.models import Offer, Product
from api.product.serializers import PriceSerializer, ProductSerializer


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

    queryset = Product.objects.prefetched()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Get non-prefetched queryset for update and destroy actions."""
        return (
            Product.objects
            if self.action in ("update", "destroy")
            else super().get_queryset()
        )

    def create(self, request):
        """Handle for POST /api/product/."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        product_data = dict(serializer.data)
        product_data["id"] = created.pk
        return Response(product_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle for PUT /api/product/{id}/."""
        return super().update(request, pk, partial=True)


class OfferViewSet(viewsets.GenericViewSet):
    """
    Price history endpoint.

    Supports:
        history: GET /api/price/history/
        changes: GET /api/price/changes/
    """

    queryset = Offer.objects.prefetched()
    serializer_class = PriceSerializer

    @decorators.action(detail=True, methods=["GET"])
    def history(self, request, pk=None):
        """Handle for GET /api/price/history/."""
        offer = self.get_object()
        prices = offer.prices.all()
        serializer = self.get_serializer(prices, many=True)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=["GET"])
    def changes(self, request, pk=None):
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
            .filter(timestamp_from__lte=time_to)
            .filter(
                Q(timestamp_to__gte=time_from) |
                Q(timestamp_to__isnull=True)
            )
        )
        base_price = prices.last().price
        for price in prices:
            price.price = (price.price - base_price) / base_price

        serializer = self.get_serializer(prices, many=True)
        return Response(serializer.data)
