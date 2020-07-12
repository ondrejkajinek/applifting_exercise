"""Test suite for GET /api/product endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_product_list(
        test_data, product_factory, fix_structure, no_product_register,
        api_client
):
    """List products."""
    if test_data["input"]:
        with no_product_register():
            for product in test_data["input"]:
                product_factory(product)

    api_response = api_client.get(reverse("product-list"))
    assert fix_structure(api_response.data) == test_data["output"]
