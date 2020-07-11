"""Views for Product api."""

# third-party
# from django.http import JsonResponse, Http404
from django.http import Http404
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
        # offer = self._get_offer(pk)
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
            # return JsonResponse(
                {
                    "time_from": "Timestamp expected",
                    "time_to": "Timestamp expected"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # offer = self._get_offer(pk)
        offer = self.get_object()
        prices = (
            offer.prices
            .filter(timestamp_to__gte=time_from)
            .filter(timestamp_from__lte=time_to)
        )
        base_price = prices[0].price
        for price in prices:
            price.price = price.price / base_price - 1

        serializer = self.get_serializer(prices, many=True)
        return Response(serializer.data)

    """
    def _get_offer(self, ident):
        try:
            return Offer.objects.prefetched().get(pk=ident)
        except Offer.DoesNotExist:
            raise Http404
    """
