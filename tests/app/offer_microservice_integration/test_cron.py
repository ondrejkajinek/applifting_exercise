"""Test suite for Offer microservice integration cron."""

# std
from unittest import mock

# third-party
from django.utils import timezone
import pytest   # pylint: disable=import-error

# local
from api.product.models import Offer, Product
from app.offer_microservice_integration.cron import _create_offer
from app.offer_microservice_integration.cron import _update_offer


def compare_prices(price_object, price_dict):
    """Comparison for two prices."""
    assert price_object.timestamp_from == price_dict["timestamp_from"]
    assert price_object.timestamp_to == price_dict["timestamp_to"]
    assert price_object.price == price_dict["price"]


@pytest.mark.django_db
def test_create_offer(test_data, no_product_register):
    """Test new offer creation."""
    offer_data = test_data["input"].pop("offer")
    with no_product_register():
        product = Product.objects.create(**test_data["input"])

    _create_offer(product, offer_data)
    offer = Offer.objects.get(external_id=test_data["output"]["id"])
    price = offer.prices.current()
    assert offer.items_in_stock == test_data["output"]["items_in_stock"]
    assert offer.product_id == product.id
    assert price.price == test_data["output"]["price"]
    assert price.timestamp_from == 0
    assert price.timestamp_to is None


@pytest.mark.django_db
def test_create_offer_atomic(test_data, no_product_register):
    """Test atomicity of _create_offer method."""
    offer_data = test_data.pop("offer")
    with no_product_register():
        product = Product.objects.create(**test_data)

    with pytest.raises(Exception):
        _create_offer(product, offer_data)

    assert Offer.objects.all().count() == 0


@pytest.mark.django_db
@mock.patch.object(timezone, "now")
def test_update_offer(mock_now, test_data, product_factory_no_register):
    """Test existing offer update."""
    mock_now.return_value = mock.Mock(**{
        "timestamp.return_value": test_data["timestamp"]
    })
    new_offer_data = test_data["input"].pop("new_offer")
    product = product_factory_no_register(test_data["input"])
    _update_offer(new_offer_data)

    original_offers = {
        offer["external_id"]: offer
        for offer
        in test_data["input"]["offers"]
    }
    for offer in product.offers.exclude(external_id=new_offer_data["id"]):
        offer_data = original_offers[offer.external_id]
        assert offer.items_in_stock == offer_data["items_in_stock"]
        offer_data["prices"].sort(key=lambda price: price["timestamp_from"])
        prices = list(offer.prices.all().order_by("timestamp_from"))
        assert len(prices) == len(offer_data["prices"])
        for price, price_data in zip(prices, offer_data["prices"]):
            compare_prices(price, price_data)

    offer = product.offers.get(external_id=new_offer_data["id"])
    prices = list(offer.prices.all().order_by("timestamp_from"))
    for price, price_data in zip(prices, test_data["output"]["new_prices"]):
        compare_prices(price, price_data)
