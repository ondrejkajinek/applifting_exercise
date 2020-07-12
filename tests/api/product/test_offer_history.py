"""Test suite for PUT /api/offer/{pk}/history endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_offer_changes(test_data, product_factory, fix_structure, api_client):
    """Retrieve existing offer changes."""
    product = product_factory(test_data["input"])
    offer = product.offers.first()
    api_response = api_client.get(
        reverse("offer-changes", kwargs={"pk": offer.id})
    )
    assert api_response.status_code == 200
    print(api_response.data)
    print(test_data["output"])
    assert fix_structure(api_response.data) == test_data["output"]


@pytest.mark.django_db
def test_offer_changes_not_found(api_client):
    """Retrieve non-existing offer changes."""
    api_response = api_client.get(
        reverse("offer-changes", kwargs={"pk": 1})
    )
    assert api_response.status_code == 404


@pytest.mark.django_db
def test_offer_history(test_data, product_factory, fix_structure, api_client):
    """Retrieve existing offer history."""
    product = product_factory(test_data["input"])
    offer = product.offers.first()
    api_response = api_client.get(
        reverse("offer-history", kwargs={"pk": offer.id})
    )
    assert api_response.status_code == 200
    assert fix_structure(api_response.data) == test_data["output"]


@pytest.mark.django_db
def test_offer_history_not_found(api_client):
    """Retrieve non-existing offer history."""
    api_response = api_client.get(
        reverse("offer-history", kwargs={"pk": 1})
    )
    assert api_response.status_code == 404
