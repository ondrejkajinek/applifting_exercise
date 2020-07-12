"""Test suite for GET /api/product endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_product_list(
        test_data, product_factory_no_register, fix_structure, api_client
):
    """List products."""
    if test_data["input"]:
        for product in test_data["input"]:
            product_factory_no_register(product)

    api_response = api_client.get(reverse("product-list"))
    assert fix_structure(api_response.data) == test_data["output"]
