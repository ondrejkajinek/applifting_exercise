"""Modul with Offer microservice exceptions."""


class BaseOMIException(BaseException):
    """Base class for exceptions."""


class MissingAPIToken(BaseOMIException):
    """Raised when API token cannot be obtained."""
