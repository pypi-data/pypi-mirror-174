class BurnerException(Exception):
    """Base exception class."""

    pass


class ScraperException(BurnerException):
    """An error occured while scraping data from the website."""

    pass


class InvalidServiceException(BurnerException):
    """The given service code was invalid."""

    pass


class APIException(BurnerException):
    """Base exception class for API requests."""


class EmptyAuthorisationException(APIException):
    """No authorisation was given, but it is necessary for this action."""

    pass


class InvalidAuthorisationException(APIException):
    """Authorisation was provided, but it was invalid."""

    pass


class NoFundsException(APIException):
    """The given account is out of funds."""

    pass


class NumbersBusyException(APIException):
    """The numbers are busy, try to get the number again in 30 seconds."""

    pass
