"""Test suite for API product enpoints."""

# third-party
from django.urls import reverse
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "product-list"
    ]
)
def test_unauthorized_request(url, api_client):
    """Test unauthorized access to enpoints."""
    response = api_client.get(reverse(url))
    assert response.status_code == 200
