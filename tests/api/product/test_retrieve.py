"""Test suite for GET /api/product/{pk} endpoint."""

# std
import pathlib

# third-party
from django.urls import reverse
import yaml
import pytest

# local
from api.product.models import Offer, Price, Product


data_path = pathlib.Path(__file__).parent / "test_product_retrieve.yaml"
with open(str(data_path)) as data_source:
    PRODUCT_DATA = yaml.safe_load(data_source.read())


@pytest.mark.django_db
@pytest.mark.parametrize("product_data", PRODUCT_DATA)
def test_product_retrieve(product_data, fix_structure, api_client):
    """Test retrieving existing products."""
    product = _prepare_product(product_data["input"])
    api_response = api_client.get(
        reverse("product-detail", kwargs={"pk": product.id})
    )
    assert api_response.status_code == 200
    assert fix_structure(api_response.data) == product_data["output"]


@pytest.mark.django_db
def test_product_retrieve_not_found(api_client):
    """Test retrieving nonexisting products."""
    api_response = api_client.get(
        reverse("product-detail", kwargs={"pk": 1})
    )
    assert api_response.status_code == 404


def _prepare_product(product_data):
    offer_data_set = product_data.pop("offers")
    product = Product.objects.create(**product_data)
    for offer_data in offer_data_set:
        price_data_set = offer_data.pop("prices")
        offer = Offer.objects.create(product=product, **offer_data)
        for price_data in price_data_set:
            Price.objects.create(offer=offer, **price_data)

    return product
