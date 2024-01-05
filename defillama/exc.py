"""Custom exceptions."""


class InvalidResponseDataException(Exception):
    """Raised when the response data is invalid."""


class InvalidResponseStatusCodeException(Exception):
    """Raised when the response status code is invalid."""
