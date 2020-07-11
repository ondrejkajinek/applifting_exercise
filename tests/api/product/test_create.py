"""Test suite for POST /api/product endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error

# local
from api.product.models import Product


def test_product_create_invalid(test_data, api_client):
    """Test failing product creation."""
    api_response = api_client.post(
        reverse("product-list"), test_data["input"], format="json"
    )
    assert api_response.status_code == 400
    assert api_response.data == test_data["error"]


@pytest.mark.django_db
def test_product_create_valid(test_data, api_client):
    """Test successful product creation."""
    api_response = api_client.post(
        reverse("product-list"), test_data["input"], format="json"
    )
    assert api_response.status_code == 201
    product_id = api_response.data["id"]
    product = Product.objects.get(pk=product_id)
    assert product.name == test_data["output"]["name"]
    assert product.description == test_data["output"]["description"]
