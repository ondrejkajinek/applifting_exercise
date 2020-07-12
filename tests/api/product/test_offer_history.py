"""Test suite for PUT /api/offer/{pk}/history endpoint."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_offer_history_not_found(api_client):
    """Retrieve non-existing offer history."""
    api_response = api_client.get(
        reverse("offer-history", kwargs={"pk": 1}),
        {},
        format="json"
    )
    assert api_response.status_code == 404
