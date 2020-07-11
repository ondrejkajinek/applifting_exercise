"""Test suite for POST /api/product endpoint."""

# std
import pathlib

# third-party
from django.urls import reverse
import yaml
import pytest

# local
from api.product.models import Product


data_path = pathlib.Path(__file__).parent / "test_product_create_invalid.yaml"
with open(str(data_path)) as data_source:
    PRODUCT_DATA_INVALID = yaml.safe_load(data_source.read())


data_path = pathlib.Path(__file__).parent / "test_product_create_valid.yaml"
with open(str(data_path)) as data_source:
    PRODUCT_DATA_VALID = yaml.safe_load(data_source.read())


@pytest.mark.parametrize("product_data", PRODUCT_DATA_INVALID)
def test_product_create_invalid(product_data, api_client):
    """Test failing product creation."""
    api_response = api_client.post(
        reverse("product-list"), product_data["input"], format="json"
    )
    assert api_response.status_code == 400
    assert api_response.data == product_data["error"]


@pytest.mark.django_db
@pytest.mark.parametrize("product_data", PRODUCT_DATA_VALID)
def test_product_create_valid(product_data, api_client):
    """Test successful product creation."""
    api_response = api_client.post(
        reverse("product-list"), product_data["input"], format="json"
    )
    assert api_response.status_code == 201
    product_id = api_response.data["id"]
    product = Product.objects.get(pk=product_id)
    assert product.name == product_data["output"]["name"]
    assert product.description == product_data["output"]["description"]
