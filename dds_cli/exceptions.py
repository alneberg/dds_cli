"""Custom Exception classes."""

# Standard library
import logging
import requests

# Installed
import click

# Own modules

# Logger
LOG = logging.getLogger(__name__)


class InvalidMethodError(Exception):
    """Valid methods are only ls, put, get, rm. Anything else should raise errors."""

    def __init__(self, attempted_method, message="Attempting an invalid method in the DDS"):
        """Init invalid method error."""
        self.method = attempted_method
        self.message = message
        super().__init__(message)

    def __str__(self):
        """Print message and attempted method."""
        return f"{self.message}: {self.method}"


class DDSCLIException(click.ClickException):
    """Base exception for click in DDS."""


class AuthenticationError(click.ClickException):
    """Errors due to user authentication."""

    def __init__(self, message, sign=":no_entry_sign:"):
        """Update error message."""
        self.message = message
        self.sign = sign
        super().__init__(message)

    def __str__(self):
        """Return the message with Rich no-entry-sign emoji either side."""
        return f"{self.sign} {self.message} {self.sign}"


class TokenNotFoundError(AuthenticationError):
    """No token retrieved from REST API or from File."""

    def __init__(self, message, sign=":warning-emoji:"):
        """Reformat error message."""
        super().__init__(message=message, sign=sign)


class ApiRequestError(requests.exceptions.RequestException):
    """Request to REST API failed."""

    def __init__(self, message):
        """Log and raise."""
        LOG.exception(message)
        super().__init__(message)


class ApiResponseError(Exception):
    """REST API Request does not return code 200 in response."""

    def __init__(self, message):
        """Log and raise."""
        LOG.exception(message)
        super().__init__(message)


class UploadError(Exception):
    """Errors relating to file uploads."""


class S3KeyLengthExceeded(UploadError):
    """The name in bucket exceeded the allowed 1024 bytes."""

    def __init__(
        self,
        filename,
        message=" exceeds allowed limit for combined path and name length and can't be stored in the system.",
    ):
        super().__init__(f"{filename} {message}")


class NoDataError(Exception):
    """Errors when there is no data to do anything with."""


class APIError(Exception):
    """Error connecting to the dds web server."""
