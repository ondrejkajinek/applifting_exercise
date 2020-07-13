"""Modul with Offer microservice exceptions."""


class BaseOMSException(BaseException):
    """Base class for exceptions."""


class BadRequest(BaseOMSException):
    """Raised when generic bad request is returned."""


class MissingApiKey(BaseOMSException):
    """Raised when API token cannot be obtained."""


class NotFound(BaseOMSException):
    """Raised when request object is not found."""


class ServerError(BaseOMSException):
    """Raised when server returns 5xx status."""


class UnauthorizedRequest(BaseOMSException):
    """Raised when bad or no API key is used for authorization."""


class UnrecognizedResponse(BaseOMSException):
    """Raised when server returned unrecongized response."""
