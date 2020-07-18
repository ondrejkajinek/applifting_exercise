"""Test suite for PUT /api/offer/{pk}/history endpoint."""

# std
import urllib

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_offer_changes(
        test_data, product_factory_no_register, fix_structure, api_client
):
    """Retrieve existing offer changes."""
    product = product_factory_no_register(test_data["input"])
    offer = product.offers.first()
    url = reverse("offer-changes", kwargs={"pk": offer.id})
    if test_data.get("query_params"):
        url += "?" + urllib.parse.urlencode(test_data["query_params"])

    api_response = api_client.get(url)
    assert api_response.status_code == 200
    assert fix_structure(api_response.data) == test_data["output"]


@pytest.mark.django_db
def test_offer_changes_invalid(
        test_data, product_factory_no_register, api_client
):
    """Retrieve existing offer changes with invalid params."""
    product = product_factory_no_register(test_data["input"])
    offer = product.offers.first()
    url = reverse("offer-changes", kwargs={"pk": offer.id})
    url += "?" + urllib.parse.urlencode(test_data["query_params"])
    api_response = api_client.get(url)
    assert api_response.status_code == 400


@pytest.mark.django_db
def test_offer_changes_not_found(api_client):
    """Retrieve non-existing offer changes."""
    api_response = api_client.get(
        reverse("offer-changes", kwargs={"pk": 1})
    )
    assert api_response.status_code == 404
