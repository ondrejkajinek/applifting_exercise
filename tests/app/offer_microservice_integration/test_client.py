"""Test suite for OfferMicroserviceClient."""

# std
from unittest import mock

# third-party
import pytest   # pylint: disable=import-error

# local
from app.offer_microservice_integration import client
from app.offer_microservice_integration.exceptions import MissingAPIToken


@pytest.mark.django_db
@mock.patch.object(client.OfferMicroserviceClient, "_request_auth_token")
def test_auth_token(mock_request_token, fake_token, oms_client):
    """Test if auth token is requested only once."""
    mock_request_token.return_value = fake_token
    for _ in range(10):
        assert oms_client.api_key == fake_token

    try:
        mock_request_token.assert_called_once()
    except AttributeError:
        assert mock_request_token.call_count == 1


@pytest.mark.django_db
def test_request_token_failed(oms_client):
    """Test various fails during auth token request."""
    with mock.patch.object(client.requests, "get") as mock_request_get:
        mock_request_get.return_value = mock.Mock(
            status_code=500
        )
        with pytest.raises(MissingAPIToken):
            print(oms_client.api_key)

    with mock.patch.object(client.requests, "get") as mock_request_get:
        message = "I wanna break it"
        mock_request_get.return_value = mock.Mock(**{
            "status_code": 200,
            "text": message,
            "json.return_value": message
        })
        with pytest.raises(MissingAPIToken):
            print(oms_client.api_key)


@mock.patch.object(
    client.OfferMicroserviceClient, "api_key", new_callable=mock.PropertyMock
)
@mock.patch.object(client.requests, "get")
def test_api_key_accessed_once(
        mock_request_get, mock_api_key, fake_token, oms_client
):
    """Test if access token is accessed only once per request."""
    mock_request_get.return_value = mock.Mock(**{
        "status_code": 200,
        "text": "[]",
        "json.return_code": []
    })
    mock_api_key.return_value = fake_token
    oms_client.product_offers(1)
    try:
        mock_api_key.assert_called_once()
    except AttributeError:
        assert mock_api_key.call_count == 1


@mock.patch.object(
    client.OfferMicroserviceClient, "api_key", new_callable=mock.PropertyMock
)
@mock.patch.object(client.requests, "get")
def test_product_offers(
        mock_request_get, mock_api_key, test_data, fake_token, oms_client
):
    """Test client response for product_offers."""
    mock_request_get.return_value = mock.Mock(**{
        "status_code": 200,
        "text": "",
        "json.return_value": test_data
    })
    mock_api_key.return_value = fake_token
    offers = oms_client.product_offers(1)
    assert offers == test_data
