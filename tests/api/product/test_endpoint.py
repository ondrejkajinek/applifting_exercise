"""Test suite for API product enpoints."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_request_unauthorized(test_data, api_client):
    """Make unauthorized request to product enpoint."""
    url = reverse(test_data["route"], kwargs=test_data["route_args"])
    response = getattr(api_client, test_data["method"])(url)
    assert response.status_code != 403
