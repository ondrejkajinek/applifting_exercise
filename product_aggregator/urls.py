"""product_aggregator URL Configuration."""

# third-party
from django.urls import include, path

urlpatterns = [
    path("api/", include("api.product.urls"))
]
