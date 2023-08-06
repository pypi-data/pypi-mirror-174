import os
import shutil
import sqlite3
import time
from importlib import resources
from typing import List, Optional

import click
import peewee
import requests
from bs4 import BeautifulSoup, Tag
from peewee import SqliteDatabase

from . import database
from .database import Country, Price, Service
from .exceptions import EmptyAuthorisationException, ScraperException


class Client:
    def __init__(self, api_key: Optional[str] = None, database_path: str = "sms.db"):
        super().__init__()

        self._api_key = api_key
        self._session = requests.Session()

        self._database_path = database_path
        self._database = SqliteDatabase(self._database_path)

        database.proxy.initialize(self._database)
        self._database.create_tables([Country, Price, Service])

    def _initialize_database(self) -> sqlite3.Connection:
        countries: List[Country] = Country.select()

        if len(countries) == 0:
            for country in self.fetch_country_list():
                Country.create(
                    image=country["image"],
                    name=country["name"],
                    code=country["code"],
                )

        services: List[Service] = Service.select()

        if len(services) == 0:
            for service in self.fetch_service_list():
                Service.create(
                    image=service["image"],
                    name=service["name"],
                    code=service["code"],
                )

        countries: List[Country] = Country.select()

        for country in countries:
            prices: List[Price] = Price.select().where(Price.country == country)

            if len(prices) > 0:
                continue

            for price in self.fetch_prices_by_country(country.code):
                try:
                    service: Optional[Service] = Service.get(
                        Service.code == price["service_opt"]
                    )
                except peewee.DoesNotExist:
                    continue

                Price.create(
                    price=float(price["price"]),
                    enabled=price["enable"],
                    country=country,
                    service=service,
                )

            time.sleep(0.1)

    def reset_cache(self) -> None:
        """Deletes the old cache database and re-makes it."""
        self._database.close()

        os.remove(self._database_path)

        self._database = SqliteDatabase(self._database_path)

        database.proxy.initialize(self._database)
        self._database.create_tables([Country, Price, Service])

        self._initialize_database()

    def _fetch_table_data(self, table_id: int) -> List[dict]:
        """Fetch data from the tables listed on the API documentation. This is done as
        there is no officially exposed endpoint to crawl countries or services,
        only tables in the documentation.

        https://simsms.org/new_theme_api.html
        """
        resp = self._session.get("https://simsms.org/new_theme_api.html")
        soup = BeautifulSoup(resp.text, "html.parser")

        tables: List[Tag] = soup.find_all("table")

        if len(tables) == 0 or len(tables) < table_id + 1:
            raise ScraperException("The table with the given ID could not be found.")

        data: List[Country] = []
        rows: List[Tag] = tables[table_id].find_all("tr")

        for row in rows:
            row_data: List[Tag] = row.find_all("td")

            if len(row_data) < 4:
                continue

            # TODO: Maybe return something that _isn't_ a plain old `dict`.
            data.append(
                {
                    "id": int(row_data[0].get_text().strip()),
                    "image": row_data[1].find("img").get("src").strip(),
                    "name": row_data[2].get_text().strip(),
                    "code": row_data[3].get_text().strip(),
                }
            )

        return data

    def fetch_country_list(self) -> List[dict]:
        return self._fetch_table_data(0)

    def fetch_service_list(self) -> List[dict]:
        return self._fetch_table_data(1)

    def fetch_prices_by_country(self, country_code: str) -> dict:
        if self._api_key is None:
            raise EmptyAuthorisationException

        resp = self._session.get(
            "https://simsms.org/reg-sms.api.php",
            params={
                "type": "get_prices_by_country",
                "country_id": country_code,
                "apikey": self._api_key,
            },
        )

        resp.raise_for_status()

        return resp.json()

    def find_price_by_service(self, service_code: str) -> List[Price]:
        # TODO: Should be done automatically on __init__(?), but NOT if we are resetting
        # the cache.
        self._initialize_database()

        service: Optional[Service] = Service.get(Service.code == service_code)

        if not service:
            return

        return Price.select().where(Price.service == service).order_by(Price.price)


@click.group()
@click.option(
    "-a", "--authorization", help="Key to authorise against SimSMS's servers with."
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
    for country in client.fetch_country_list():
        click.echo(f"[{country['code']}] {country['name']}")


@cli.command()
@click.pass_obj
def services(client: Client):
    """List all of the available services and their codes."""
    for service in client.fetch_service_list():
        click.echo(f"[{service['code']}] {service['name']}")


@cli.command()
@click.argument("service")
@click.pass_obj
def prices(client: Client, service: str):
    """Find the cheapest prices for a given service."""
    for price in client.find_price_by_service(service):
        click.echo(
            "[{code}] {name:<16s} = ₽{price}".format(
                code=price.country.code,
                name=price.country.name,
                price=price.price,
            )
        )


@cli.command()
@click.pass_obj
def reset(client: Client):
    """Reset the cache with the latest information. Authorisation is needed."""
    client.reset_cache()


if __name__ == "__main__":
    cli()
