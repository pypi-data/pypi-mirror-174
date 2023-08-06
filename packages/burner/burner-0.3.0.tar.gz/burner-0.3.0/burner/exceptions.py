class BurnerException(Exception):
    """Base exception class."""

    pass


class EmptyAuthorisationException(BurnerException):
    """No authorisation was given, but it is necessary for this action."""

    pass


class ScraperException(BurnerException):
    """An error occured while scraping data from the website."""

    pass
