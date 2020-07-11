"""Test suite for GET /api/product endpoint."""

# std
import pathlib

# third-party
from django.urls import reverse
import yaml
import pytest

# local
from api.product.models import Offer, Price, Product


data_path = pathlib.Path(__file__).parent / "test_product_list.yaml"
with open(str(data_path)) as data_source:
    PRODUCT_LIST_DATA = yaml.safe_load(data_source.read())


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_data",
    PRODUCT_LIST_DATA
)
def test_product_list(product_data, fix_structure, api_client):
    """Test products listing."""
    if product_data["input"]:
        for product in product_data["input"]:
            _prepare_product(product)

    api_response = api_client.get(reverse("product-list"))
    assert fix_structure(api_response.data) == product_data["output"]


def _prepare_product(product_data):
    offer_data_set = product_data.pop("offers")
    product = Product.objects.create(**product_data)
    for offer_data in offer_data_set:
        price_data_set = offer_data.pop("prices")
        offer = Offer.objects.create(product=product, **offer_data)
        for price_data in price_data_set:
            Price.objects.create(offer=offer, **price_data)
