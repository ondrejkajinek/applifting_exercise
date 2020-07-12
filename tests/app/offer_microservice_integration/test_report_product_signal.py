"""Test suite for calling report_product when Product is created."""

# std
from unittest import mock

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error

# local
from api.product.models import Product


@pytest.mark.django_db
@mock.patch(
    "app.offer_microservice_integration.client"
    ".OfferMicroserviceClient.register_product"
)
def test_product_create_reported(mock_register, test_data, api_client):
    """Test if register_product is called after create."""
    mock_register.return_value = test_data["output"]
    api_response = api_client.post(
        reverse("product-list"), test_data["input"], format="json"
    )
    assert api_response.status_code == 201
    product_id = api_response.data["id"]
    product = Product.objects.get(pk=product_id)
    try:
        mock_register.assert_called_once()
    except AttributeError:
        assert mock_register.call_count == 1

    mock_register.assert_called_with(product)


@pytest.mark.django_db
@mock.patch(
    "app.offer_microservice_integration.client"
    ".OfferMicroserviceClient.register_product"
)
def test_product_update_unreported(
        mock_register, test_data, no_product_register, api_client
):
    """Test if register_product is not called after update."""
    with no_product_register():
        product = Product.objects.create(**test_data["input"])

    api_response = api_client.put(
        reverse("product-detail", kwargs={"pk": product.id}),
        test_data["change"],
        format="json"
    )
    assert api_response.status_code == 200
    assert mock_register.call_count == 0
