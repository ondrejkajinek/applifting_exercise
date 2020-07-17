"""Test suite for GET /api/product endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_product_list(
        test_data, product_factory_no_register, fix_structure, api_client
):
    """List products."""
    def sort_products(products):
        for product in products:
            product["offers"].sort(key=lambda x: x["id"])

        return sorted(products, key=lambda x: x["id"])

    if test_data["input"]:
        for product in test_data["input"]:
            product_factory_no_register(product)

    api_response = api_client.get(reverse("product-list"))
    assert sort_products(fix_structure(api_response.data)) == \
        sort_products(test_data["output"])
