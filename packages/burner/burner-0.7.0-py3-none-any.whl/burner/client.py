import os
import re
import time
from typing import List, Optional, Tuple

import peewee
from peewee import SqliteDatabase

from .session import Session

from . import database
from .database import Country, Price, Service
from .exceptions import (
    APIException,
    InvalidCountryException,
    InvalidServiceException,
    NumbersBusyException,
)


def _service_provider(self):
    services: List[Service] = Service.select()

    if len(services) == 0:
        Service.insert_many(self._api.fetch_service_list()).execute()


def _country_provider(self):
    countries: List[Country] = Country.select()

    if len(countries) == 0:
        Country.insert_many(self._api.fetch_country_list()).execute()


def _price_provider(self):
    countries: List[Country] = Country.select()

    for country in countries:
        if Price.select().where(Price.country == country).count() > 0:
            continue

        data: List[dict] = []

        for price in self._api.fetch_prices_by_country(country.code):
            try:
                service = Service.get(Service.code == price["service_opt"])
            except peewee.DoesNotExist:
                continue

            data.append(
                {
                    "price": float(price["price"]),
                    "enabled": price["enable"],
                    "country": country,
                    "service": service,
                }
            )

        Price.insert_many(data).execute()

        time.sleep(0.1)


_cache_providers = {
    "service": _service_provider,
    "country": _country_provider,
    "price": _price_provider,
}


def requires_cache(required_features: List[str]):
    """
    Indicates that certain data is necessary to run the request.

    Args:
        required_features (List[str]): List of features that will be needed to run the
            given function. These are available in the `_cache_providers` variable.
    """
    # TODO: Thread lock?
    def decorator(f):
        def wrapper(self, *args, **kwargs):
            for feature in required_features:
                feature_func = _cache_providers.get(feature)

                if not feature_func:
                    raise Exception("Invalid feature requested.", feature)

                feature_func(self)

            return f(self, *args, **kwargs)

        return wrapper

    return decorator


class Client:
    """
    The client will be used to handle any requests to the API and interactions with the
    database in a  well formatted fashion.

    Args:
        api_key (str?): The user's API key for SimSMS. This is not always necessary,
            especially if the user only wishes to check already cached information
            without purchasing numbers.
        database_path (str?): Where to save the database file to. If no path is given,
            it will be saved as "sms.db" to the current working directory.
    """

    def __init__(
        self, api_key: Optional[str] = None, database_path: Optional[str] = None
    ):
        super().__init__()

        self._api = Session(api_key)

        self._database_path: str = database_path if database_path else "sms.db"
        self._database = SqliteDatabase(self._database_path)

        database.proxy.initialize(self._database)
        self._database.create_tables([Country, Price, Service])

    def reset_cache(self) -> None:
        """Deletes the old cache database and re-makes it."""
        self._database.close()

        os.remove(self._database_path)

        self._database = SqliteDatabase(self._database_path)

        database.proxy.initialize(self._database)
        self._database.create_tables([Country, Price, Service])

        for func in _cache_providers.values():
            func(self)

    @requires_cache(["service", "country", "price"])
    def get_prices_by_service(self, service_code: str) -> List[Price]:
        """
        Find all of the available prices for a given service.

        Args:
            service_code (str): Code for the requested service, as determined from the
                database's 'code' parameter.

        Returns:
            A list of available prices in each country.

        Raises:
            InvalidServiceException: The provided service code was not valid.
        """
        if not re.match(r"^opt\d{1,3}$", service_code):
            raise InvalidServiceException

        service: Optional[Service] = Service.get(Service.code == service_code)

        if not service:
            raise InvalidServiceException

        return Price.select().where(Price.service == service).order_by(Price.price)

    @requires_cache(["country"])
    def get_countries(self) -> List[Country]:
        """
        Get a list of every country from the database. If there are no countries stored
        in the database then they will be inserted from the website.

        Returns:
            A list of countries from the database.
        """
        return Country.select().order_by(Country.code)

    @requires_cache(["service"])
    def get_services(self) -> List[Service]:
        """
        Get a list of every service from the database. If there are no services stored
        in the database then they will be inserted from the website.

        Returns:
            A list of services from the database.
        """
        services: List[Service] = Service.select()

        if len(services) == 0:
            Service.insert_many(self._api.fetch_service_list()).execute()

        return Service.select().order_by(Service.name)

    def get_number(self, country_code: str, service_code: str) -> Tuple[int, str]:
        """
        Request a phone number to receive codes from. Keep in mind that the phone code
        for the number is not given, and so a library like `phonenumbers` should be used
        to find the phone code from the alpha-2 code.

        Args:
            country_code (str): Alpha-2 country code.
            service_code (str): Code for the requested service, as determined from the
                database's 'code' parameter.

        Returns:
            The ID of the requested phone number, alongside the phone number itself, as
            a tuple of type `Tuple[int, str]`.

        Raises:
            InvalidCountryException: The provided country code was not valid.
            InvalidServiceException: The provided service code was not valid.
            NumbersBusyException: The requested number is currently busy handling
                another request. Please try again later.
        """
        if not re.match(r"^\w\w$", country_code):
            raise InvalidCountryException

        if not re.match(r"^opt\d{1,3}$", service_code):
            raise InvalidServiceException

        data = self._api.request(
            "get_number",
            {
                "country": country_code,
                "service": service_code,
            },
        )

        # "The numbers are busy, try to get the number again in 30 seconds."
        if data["number"] == "":
            raise NumbersBusyException

        return data["id"], data["number"]

    def get_sms(
        self, country_code: str, service_code: str, number_id: int
    ) -> Optional[str]:
        """
        Try to get the SMS code for a specific number.

        Args:
            country_code (str): Alpha-2 country code.
            service_code (str): Code for the requested service, as determined from the
                database's 'code' parameter.
            number_id (int): Identifying ID for the number we are trying to get an SMS
                code from. This will be received alongside a new phone number from the
                `get_number(...)` method.

        Returns:
            The received verification code, or None if it is not ready.

        Raises:
            InvalidCountryException: The provided country code was not valid.
            InvalidServiceException: The provided service code was not valid.
            APIException: An error occured during the API request.
        """
        if not re.match(r"^\w\w$", country_code):
            raise InvalidCountryException

        if not re.match(r"^opt\d{1,3}$", service_code):
            raise InvalidServiceException

        data = self._api.request(
            "get_sms",
            {
                "id": number_id,
                "country": country_code,
                "service": service_code,
            },
        )

        # Code wasn't received yet.
        if data["response"] == "2":
            return None

        # Code was received.
        elif data["response"] in ("1", "4"):
            return data["sms"]

        # Unknown error occured.
        else:
            raise APIException
