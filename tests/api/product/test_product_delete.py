"""Test suite for DELETE /api/product/{pk} endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error

# local
from api.product.models import Product


@pytest.mark.django_db
def test_product_delete_not_found(api_client):
    """Delete non-existing product."""
    api_response = api_client.delete(
        reverse("product-detail", kwargs={"pk": 1})
    )
    assert api_response.status_code == 404


@pytest.mark.django_db
def test_product_delete_valid(test_data, api_client):
    """Delete existing product."""
    product = Product.objects.create(**test_data["input"])
    api_response = api_client.delete(
        reverse("product-detail", kwargs={"pk": product.id})
    )
    assert api_response.status_code == 204
    with pytest.raises(Product.DoesNotExist):
        product = Product.objects.get(pk=product.id)
