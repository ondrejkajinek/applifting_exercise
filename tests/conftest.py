"""Utilities for pytesting."""

# std
import collections
import pathlib

# thid-party
from django.db.models.signals import post_save
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
import yaml     # pylint: disable=import-error
import pytest   # pylint: disable=import-error

# local
from api.product.models import Offer, Price, Product
from app.offer_microservice_integration.signals import register_product


class SignalMuter:
    """Context manager for temporary signal disconnection."""

    def __init__(self, signal, receiver, sender, dispatch_uid=None):
        """Signal muter initialization."""
        self.signal = signal
        self.receiver = receiver
        self.sender = sender
        self.dispatch_uid = dispatch_uid

    def __enter__(self):
        """Disconnect selected signal."""
        self.signal.disconnect(
            receiver=self.receiver,
            sender=self.sender,
            dispatch_uid=self.dispatch_uid,
        )

    def __exit__(self, exc_type, exc_value, traceback):
        """Re-connect signal upon context destruction."""
        self.signal.connect(
            receiver=self.receiver,
            sender=self.sender,
            dispatch_uid=self.dispatch_uid,
            weak=False
        )


@pytest.fixture
def api_client():
    """Create test API client."""
    return APIClient()


@pytest.fixture
def fix_structure():
    """Create method to fix data structure."""

    def fixer(data):
        if isinstance(data, collections.OrderedDict):
            return {
                key: fixer(value)
                for key, value
                in data.items()
            }

        if isinstance(data, list):
            return [fixer(value) for value in data]

        if isinstance(data, ErrorDetail):
            return str(data)

        return data

    return fixer


@pytest.fixture
def product_factory():
    """Create factory for Product with Offer and Price."""

    def factory(product_data):
        offer_data_set = product_data.pop("offers")
        product = Product.objects.create(**product_data)
        for offer_data in offer_data_set:
            price_data_set = offer_data.pop("prices")
            offer = Offer.objects.create(product=product, **offer_data)
            for price_data in price_data_set:
                Price.objects.create(offer=offer, **price_data)

        return product

    return factory


@pytest.fixture
# OndraK: use fixtures product_factory and no_product_register
# pylint: disable=redefined-outer-name
def product_factory_no_register(product_factory, no_product_register):
# pylint: enable=redefined-outer-name
    """Create factory for full Product with register_product signal muted."""

    def factory(product_data):
        with no_product_register():
            return product_factory(product_data)

    return factory


@pytest.fixture
def no_product_register():
    """Return factory for SignalMuter."""

    def factory():
        return SignalMuter(
            signal=post_save,
            receiver=register_product,
            sender=Product,
            dispatch_uid="app.offer_microservice_integration.register_product"
        )

    return factory


def pytest_generate_tests(metafunc):
    """Load test data from external file."""
    for fixture in metafunc.fixturenames:
        if fixture == "test_data":
            test_data = _load_function_test_data(metafunc)
            metafunc.parametrize(fixture, test_data)


def _load_function_test_data(metafunc):
    module_dirs = metafunc.function.__module__.split(".")[:-1]
    data_source_path = (
        pathlib.Path.cwd()
        .joinpath(*module_dirs)
        .joinpath("{}.yaml".format(metafunc.function.__name__))
    )
    with open(str(data_source_path)) as data_source:
        return yaml.safe_load(data_source.read())
