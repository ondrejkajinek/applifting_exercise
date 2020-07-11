"""Utilities for pytesting."""

# std
import collections

# thid-party
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
import pytest


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
def api_client():
    """Create test API client."""
    return APIClient()
