"""Modul with Offer microservice exceptions."""


class BaseOMSException(BaseException):
    """Base class for exceptions."""


class MissingApiKey(BaseOMSException):
    """Raised when API token cannot be obtained."""
