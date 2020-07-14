"""Test suite for OfferMicroserviceClient."""

# std
from unittest import mock

# third-party
from django.conf import settings
import pytest   # pylint: disable=import-error

# local
from api.product.models import Product
from app.offer_microservice_integration import client, exceptions


@pytest.mark.django_db
@mock.patch.object(client.OfferMicroserviceClient, "_request_auth_token")
def test_auth_token_once(mock_request_token, fake_token, oms_client):
    """Test if auth token is requested only once."""
    mock_request_token.return_value = fake_token
    for _ in range(10):
        assert oms_client.api_key == fake_token

    try:
        mock_request_token.assert_called_once()
    except AttributeError:
        assert mock_request_token.call_count == 1


@pytest.mark.django_db
@mock.patch.object(client.requests, "post")
def test_request_token(mock_request_post, oms_client, fake_token):
    """Test successful auth token request."""
    mock_request_post.return_value = mock.Mock(**{
        "json.return_value": {"access_token": fake_token}
    })
    assert oms_client.api_key == fake_token


@pytest.mark.django_db
def test_request_token_failed(oms_client):
    """Test various fails during auth token request."""
    with mock.patch.object(client.requests, "post") as mock_request_post:
        mock_request_post.return_value = mock.Mock(**{
            "raise_for_status.side_effect":
                client.requests.exceptions.HTTPError
        })
        with pytest.raises(exceptions.MissingApiKey):
            print(oms_client.api_key)

    with mock.patch.object(client.requests, "post") as mock_request_post:
        mock_request_post.return_value = mock.Mock(**{
            "text": "This is mocked error",
            "json.side_effect": ValueError
        })
        with pytest.raises(exceptions.UnrecognizedResponse):
            print(oms_client.api_key)

    with mock.patch.object(client.requests, "post") as mock_request_post:
        mock_request_post.return_value = mock.Mock(**{
            "text": "This is mocked error",
            "json.side_effect": KeyError
        })
        with pytest.raises(exceptions.UnrecognizedResponse):
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


@mock.patch.object(client.requests, "get")
def test_product_offers(
        mock_request_get, test_data, oms_client_with_fake_api_key
):
    """Test client response for product_offers."""
    mock_request_get.return_value = mock.Mock(**{
        "status_code": 200,
        "text": "",
        "json.return_value": test_data
    })
    offers = oms_client_with_fake_api_key.product_offers(1)
    assert offers == test_data
    mock_request_get.assert_called_with(
        url=settings.OFFER_MICROSERVICE_URL + "/products/{}/offers".format(1),
        headers={
            "Bearer": oms_client_with_fake_api_key.api_key
        }
    )
    try:
        mock_request_get.assert_called_once()
    except AttributeError:
        assert mock_request_get.call_count == 1


def test_product_offers_failed(oms_client_with_fake_api_key):
    """Test client response for product_offers error."""
    with mock.patch.object(client.requests, "get") as mock_request_get:
        mock_request_get.return_value = mock.Mock(**{
            "status_code": 200,
            "text": "This is mocked error",
            "json.side_effect": ValueError
        })
        with pytest.raises(exceptions.UnrecognizedResponse):
            oms_client_with_fake_api_key.product_offers(1)

    with mock.patch.object(client.requests, "get") as mock_request_get:
        mock_request_get.return_value = mock.Mock(**{
            "status_code": 499,
            "text": "This is mocked error",
            "json.return_value": {"msg": "This is mocked error"}
        })
        with pytest.raises(exceptions.UnrecognizedResponse):
            oms_client_with_fake_api_key.product_offers(1)

    with mock.patch.object(client.requests, "get") as mock_request_get:
        mock_request_get.return_value = mock.Mock(**{
            "status_code": 401,
            "text": "This is mocked error",
            "json.return_value": {"msg": "This is mocked error"}
        })
        with pytest.raises(exceptions.UnauthorizedRequest):
            oms_client_with_fake_api_key.product_offers(1)

    with mock.patch.object(client.requests, "get") as mock_request_get:
        mock_request_get.return_value = mock.Mock(**{
            "status_code": 404,
            "text": "This is mocked error",
            "json.return_value": {"msg": "This is mocked error"}
        })
        with pytest.raises(exceptions.NotFound):
            oms_client_with_fake_api_key.product_offers(1)

    with mock.patch.object(client.requests, "get") as mock_request_get:
        mock_request_get.return_value = mock.Mock(**{
            "status_code": 500,
            "text": "This is mocked error",
            "json.return_value": {"msg": "This is mocked error"}
        })
        with pytest.raises(exceptions.ServerError):
            oms_client_with_fake_api_key.product_offers(1)


@mock.patch.object(client.requests, "post")
def test_register_product(
        mock_request_post, test_data, oms_client_with_fake_api_key
):
    """Test client response for register_product."""
    expected_result = {
        "id": test_data["id"]
    }
    mock_request_post.return_value = mock.Mock(**{
        "status_code": 201,
        "text": "",
        "json.return_value": expected_result
    })
    product = Product(**test_data)
    response = oms_client_with_fake_api_key.register_product(product)
    assert response == expected_result
    mock_request_post.assert_called_with(
        url=settings.OFFER_MICROSERVICE_URL + "/products/register",
        headers={
            "Bearer": oms_client_with_fake_api_key.api_key
        },
        json=test_data
    )
    try:
        mock_request_post.assert_called_once()
    except AttributeError:
        assert mock_request_post.call_count == 1
