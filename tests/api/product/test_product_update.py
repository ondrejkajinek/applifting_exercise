"""Test suite for PUT /api/product/{pk} endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error

# local
from api.product.models import Product


@pytest.mark.django_db
def test_product_update_not_found(api_client):
    """Update non-existing product."""
    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": 1}),
        {},
        format="json"
    )
    assert api_response.status_code == 404


@pytest.mark.django_db
def test_product_update_invalid(
        test_data, fix_structure, no_product_register, api_client
):
    """Update existing product with invalid data."""
    with no_product_register():
        product = Product.objects.create(**test_data["input"])

    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": product.id}),
        test_data["change"],
        format="json"
    )
    assert api_response.status_code == 400
    assert fix_structure(api_response.data) == test_data["error"]


@pytest.mark.django_db
def test_product_update_valid(test_data, no_product_register, api_client):
    """Update existing product with valid data."""
    with no_product_register():
        product = Product.objects.create(**test_data["input"])

    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": product.id}),
        test_data["change"],
        format="json"
    )
    assert api_response.status_code == 200
    product = Product.objects.get(pk=product.id)
    assert product.name == test_data["output"]["name"]
    assert product.description == test_data["output"]["description"]
