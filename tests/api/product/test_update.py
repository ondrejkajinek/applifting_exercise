"""Test suite for PUT /api/product/{pk} endpoint."""
import sys
print(sys.path)

# std
import pathlib

# third-party
from django.urls import reverse
import yaml
import pytest

# local
from api.product.models import Product


data_path = pathlib.Path(__file__).parent / "test_product_update_invalid.yaml"
with open(str(data_path)) as data_source:
    PRODUCT_DATA_INVALID = yaml.safe_load(data_source.read())


data_path = pathlib.Path(__file__).parent / "test_product_update_valid.yaml"
with open(str(data_path)) as data_source:
    PRODUCT_DATA_VALID = yaml.safe_load(data_source.read())


@pytest.mark.django_db
def test_product_update_not_found(api_client):
    """Test updating non-existing product."""
    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": 1}),
        {},
        format="json"
    )
    assert api_response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("product_data", PRODUCT_DATA_INVALID)
def test_product_update_invalid(product_data, fix_structure, api_client):
    """Test failing product update."""
    product = Product.objects.create(**product_data["input"])
    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": product.id}),
        product_data["change"],
        format="json"
    )
    assert api_response.status_code == 400
    assert fix_structure(api_response.data) == product_data["error"]


@pytest.mark.django_db
@pytest.mark.parametrize("product_data", PRODUCT_DATA_VALID)
def test_product_update_valid(product_data, api_client):
    """Test successful product update."""
    product = Product.objects.create(**product_data["input"])
    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": product.id}),
        product_data["change"],
        format="json"
    )
    assert api_response.status_code == 200
    product = Product.objects.get(pk=product.id)
    assert product.name == product_data["output"]["name"]
    assert product.description == product_data["output"]["description"]
