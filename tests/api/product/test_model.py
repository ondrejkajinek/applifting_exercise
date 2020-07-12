"""Test suite for Product models."""

# third-party
import pytest   # pylint: disable=import-error


@pytest.mark.django_db
def test_product_str(test_data, product_factory):
    """Test Product.__str__."""
    product = product_factory(test_data["input"])
    assert str(product) == test_data["output"]["product"]["str"]
    offers = product.offers.all()
    for offer, expected_offer in zip(offers, test_data["output"]["offers"]):
        assert str(offer) == expected_offer["str"]
        prices = offer.prices.all()
        for price, expected_price in zip(prices, expected_offer["prices"]):
            assert str(price) == expected_price["str"]
