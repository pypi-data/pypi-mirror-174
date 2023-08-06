import os
import shutil
import sqlite3
import time
from importlib import resources
from typing import List, Optional, Tuple

import click
import peewee
import phonenumbers
from peewee import SqliteDatabase

from .session import Session

from . import database
from .database import Country, Price, Service
from .exceptions import (
    APIException,
    InvalidServiceException,
    NumbersBusyException,
)


class Client:
    def __init__(self, api_key: Optional[str] = None, database_path: str = "sms.db"):
        super().__init__()

        self._api = Session(api_key)

        self._database_path = database_path
        self._database = SqliteDatabase(self._database_path)

        database.proxy.initialize(self._database)
        self._database.create_tables([Country, Price, Service])

    def _initialize_database(self) -> sqlite3.Connection:
        """Makes sure that the necessary data is present. This includes the service
        and country data, alongside the available prices for each country."""
        countries: List[Country] = Country.select()

        if len(countries) == 0:
            Country.insert_many(self._api.fetch_country_list()).execute()

        services: List[Service] = Service.select()

        if len(services) == 0:
            Service.insert_many(self._api.fetch_service_list()).execute()

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
                
                data.append({
                    "price": float(price["price"]),
                    "enabled": price["enable"],
                    "country": country,
                    "service": service,
                })
            
            Price.insert_many(data).execute()

            time.sleep(0.1)

    def reset_cache(self) -> None:
        """Deletes the old cache database and re-makes it."""
        self._database.close()

        os.remove(self._database_path)

        self._database = SqliteDatabase(self._database_path)

        database.proxy.initialize(self._database)
        self._database.create_tables([Country, Price, Service])

        self._initialize_database()

    def find_prices_by_service(
        self, service_code: str, order_by: any = Price.price
    ) -> List[Price]:
        """Get the prices for a service across all countries."""
        service: Optional[Service] = Service.get(Service.code == service_code)

        if not service:
            raise InvalidServiceException

        return Price.select().where(Price.service == service).order_by(order_by)

    def get_countries(self) -> List[Country]:
        """Get every available country."""
        countries: List[Country] = Country.select()

        if len(countries) == 0:
            Country.insert_many(self._api.fetch_country_list()).execute()

        return Country.select().order_by(Country.code)

    def get_services(self) -> List[Service]:
        """Get every available service."""
        services: List[Service] = Service.select()

        if len(services) == 0:
            Service.insert_many(self._api.fetch_service_list()).execute()

        return Service.select().order_by(Service.name)

    def get_number(self, country_code: str, service_code: str) -> Tuple[int, str]:
        """Get a phone number and its ID for later checking."""
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
        """Try to get the SMS code for a specific number."""
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


@click.group()
@click.option(
    "-a",
    "--authorization",
    help="Key to authorise against SimSMS's servers with.",
)
@click.pass_context
def cli(ctx: click.Context, authorization: str):
    path_db = os.path.join(os.path.expanduser("~"), ".ramadan", "burner")
    file_db = os.path.join(path_db, "sms.db")

    if not os.path.isdir(path_db):
        os.makedirs(path_db)

    if not os.path.isfile(file_db):
        with resources.path("burner.resources", "sms.db") as path:
            shutil.copy(path, file_db)

    ctx.obj = Client(authorization, file_db)


@cli.command()
@click.pass_obj
def countries(client: Client):
    """List all of the available countries and their country codes."""
    for country in client.get_countries():
        click.echo(f"{country.code} = {country.name}")


@cli.command()
@click.pass_obj
def services(client: Client):
    """List all of the available services and their codes."""
    for service in client.get_services():
        click.echo(f"{service.code:<8s} = {service.name}")


@cli.command()
@click.argument("service")
@click.pass_obj
def prices(client: Client, service: str):
    """Find the cheapest prices for a given service."""
    for price in client.find_prices_by_service(service):
        click.echo(
            "[{code}] {name:<16s} = ₽{price}".format(
                code=price.country.code,
                name=price.country.name,
                price=price.price,
            )
        )


@cli.command()
@click.argument("country")
@click.argument("service")
@click.pass_obj
def number(client: Client, country: str, service: str):
    """Buy a number for a service in a given country, and await an SMS code from it."""
    _id, number = client.get_number(country, service)

    number_data = phonenumbers.parse(number, country)
    click.echo(f"+{number_data.country_code} {number}")

    while True:
        code = client.get_sms(country, service, _id)

        if code is not None:
            click.echo(f"Code received: {code}")
            break

        click.echo("Waiting for a code...")

        time.sleep(30)


@cli.command()
@click.pass_obj
def reset(client: Client):
    """Reset the cache with the latest information. Authorisation is needed."""
    client.reset_cache()


def main():
    cli(auto_envvar_prefix="SMS")


if __name__ == "__main__":
    main()
