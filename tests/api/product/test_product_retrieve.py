"""Test suite for GET /api/product/{pk} endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_product_retrieve(
        test_data, product_factory_no_register, fix_structure, api_client
):
    """Retrieve existing product."""
    product = product_factory_no_register(test_data["input"])

    api_response = api_client.get(
        reverse("product-detail", kwargs={"pk": product.id})
    )
    assert api_response.status_code == 200
    assert fix_structure(api_response.data) == test_data["output"]


@pytest.mark.django_db
def test_product_retrieve_not_found(api_client):
    """Retrieve nonexisting product."""
    api_response = api_client.get(
        reverse("product-detail", kwargs={"pk": 1})
    )
    assert api_response.status_code == 404
