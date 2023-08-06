import importlib
from importlib import resources
import os
import shutil
import sqlite3
import sys
import time
from typing import List, Optional, TypedDict

import click
from pkg_resources import resource_filename
import requests
from bs4 import BeautifulSoup


class Country(TypedDict):
    id: int
    image: str
    name: str
    code: str


class Service(TypedDict):
    id: int
    image: str
    name: str
    code: str


class ServicePrice(TypedDict):
    id: int
    price: float
    country: Country
    service: Service


class Client(requests.Session):
    def __init__(self, api_key: Optional[str] = None, database_path: str = "sms.db"):
        super().__init__()

        self._api_key = api_key
        self._sql_path = database_path

        self._sql_connection: Optional[sqlite3.Connection] = None

        self._initialise_connection(database_path)
        self._initialise_price_cache()

    def _initialise_connection(self, database_path: str) -> sqlite3.Connection:
        self._sql_connection = sqlite3.connect(database_path)

        self._sql_connection.execute(
            """
            CREATE TABLE IF NOT EXISTS COUNTRIES (
                ID INT PRIMARY KEY NOT NULL,
                IMAGE TEXT NOT NULL,
                NAME TEXT NOT NULL,
                CODE TEXT NOT NULL
            );
        """
        )

        self._sql_connection.execute(
            """
            CREATE TABLE IF NOT EXISTS SERVICES (
                ID INT PRIMARY KEY NOT NULL,
                IMAGE TEXT NOT NULL,
                NAME TEXT NOT NULL,
                CODE TEXT NOT NULL
            )
        """
        )

        self._sql_connection.execute(
            """
            CREATE TABLE IF NOT EXISTS PRICES (
                ID INT PRIMARY KEY NOT NULL,
                ENABLED INT NOT NULL,
                PRICE REAL NOT NULL,
                COUNTRY_ID INT NOT NULL,
                SERVICE_ID INT NOT NULL,
                FOREIGN KEY(COUNTRY_ID) REFERENCES COUNTRIES(ID),
                FOREIGN KEY(SERVICE_ID) REFERENCES SERVICES(CODE)
            )
        """
        )

        cursor = self._sql_connection.cursor()

        cursor.execute("SELECT * FROM COUNTRIES")
        result = cursor.fetchall()

        if len(result) == 0:
            for country in self.fetch_country_list():
                cursor.execute(
                    f"INSERT INTO COUNTRIES (ID, IMAGE, NAME, CODE) VALUES (?, ?, ?, ?)",
                    (
                        country["id"],
                        country["image"],
                        country["name"],
                        country["code"],
                    ),
                )

        cursor.execute("SELECT * FROM SERVICES")
        result = cursor.fetchall()

        if len(result) == 0:
            for service in self.fetch_service_list():
                cursor.execute(
                    f"INSERT INTO SERVICES (ID, IMAGE, NAME, CODE) VALUES (?, ?, ?, ?)",
                    (
                        service["id"],
                        service["image"],
                        service["name"],
                        service["code"],
                    ),
                )

        cursor.close()

        self._sql_connection.commit()

    def _initialise_price_cache(self) -> None:
        cursor = self._sql_connection.cursor()
        cursor.execute("SELECT * FROM COUNTRIES")

        for country in cursor.fetchall():
            cursor.execute("SELECT * FROM PRICES WHERE COUNTRY_ID = ?", (country[0],))
            result = cursor.fetchall()

            if len(result) > 0:
                continue

            for price in self.fetch_prices_by_country(country[3]):
                cursor.execute(
                    "SELECT ID FROM SERVICES WHERE CODE = ?", (price["service_opt"],)
                )
                result_service = cursor.fetchone()

                if not result_service:
                    continue

                cursor.execute(
                    "SELECT ID FROM COUNTRIES WHERE CODE = ?",
                    (price["country_shortname"],),
                )
                result_country = cursor.fetchone()

                cursor.execute(
                    "INSERT INTO PRICES (ID, ENABLED, PRICE, COUNTRY_ID, SERVICE_ID) VALUES (?, ?, ?, ?, ?)",
                    (
                        price["id"],
                        price["enable"],
                        float(price["price"]),
                        result_country[0],
                        result_service[0],
                    ),
                )

            time.sleep(0.1)

        cursor.close()
        self._sql_connection.commit()

    def reset_cache(self) -> None:
        """Re-initialise the cache."""
        self._sql_connection.close()

        os.remove(self._sql_path)

        self._initialise_connection(self._sql_path)
        self._initialise_price_cache()

    def fetch_country_list(self) -> List[Country]:
        if self._sql_connection:
            cursor = self._sql_connection.cursor()

            cursor.execute("SELECT * FROM COUNTRIES")
            result = cursor.fetchall()

            cursor.close()

            if len(result) > 0:
                return [
                    {
                        "id": r[0],
                        "image": r[1],
                        "name": r[2],
                        "code": r[3],
                    }
                    for r in result
                ]

        resp = self.get("https://simsms.org/new_theme_api.html")
        soup = BeautifulSoup(resp.text, "html.parser")

        table = soup.find_all("table")[0]
        rows = table.find_all("tr")

        data: List[Country] = []

        for row in rows:
            row_data = row.find_all("td")

            if len(row_data) < 4:
                continue

            data.append(
                {
                    "id": int(row_data[0].get_text().strip()),
                    "image": row_data[1].find("img").get("src").strip(),
                    "name": row_data[2].get_text().strip(),
                    "code": row_data[3].get_text().strip(),
                }
            )

        return data

    def fetch_service_list(self) -> List[Service]:
        if self._sql_connection:
            cursor = self._sql_connection.cursor()

            cursor.execute("SELECT * FROM SERVICES")
            result = cursor.fetchall()

            cursor.close()

            if len(result) > 0:
                return [
                    {
                        "id": r[0],
                        "image": r[1],
                        "name": r[2],
                        "code": r[3],
                    }
                    for r in result
                ]

        resp = self.get("https://simsms.org/new_theme_api.html")
        soup = BeautifulSoup(resp.text, "html.parser")

        table = soup.find_all("table")[1]
        rows = table.find_all("tr")

        data: List[Service] = []

        for row in rows:
            row_data = row.find_all("td")

            if len(row_data) < 4:
                continue

            data.append(
                {
                    "id": int(row_data[0].get_text().strip()),
                    "image": row_data[1].find("img").get("src").strip(),
                    "name": row_data[2].get_text().strip(),
                    "code": row_data[3].get_text().strip(),
                }
            )

        return data

    def fetch_prices_by_country(self, country_code: str) -> dict:
        if self._api_key is None:
            raise Exception("Authorisation is required.")

        resp = self.get(
            "https://simsms.org/reg-sms.api.php",
            params={
                "type": "get_prices_by_country",
                "country_id": country_code,
                "apikey": self._api_key,
            },
        )

        return resp.json()

    def find_price_by_service(self, service_code: str) -> List[ServicePrice]:
        cursor = self._sql_connection.cursor()

        cursor.execute("SELECT ID FROM SERVICES WHERE CODE = ?", (service_code,))
        result = cursor.fetchone()

        if not result:
            return

        query = """
            SELECT
                COUNTRIES.ID AS COUNTRY_ID,
                COUNTRIES.CODE AS COUNTRY_CODE,
                COUNTRIES.IMAGE AS COUNTRY_IMAGE,
                COUNTRIES.NAME AS COUNTRY_NAME,
                SERVICES.ID AS SERVICE_ID,
                SERVICES.CODE AS SERVICE_CODE,
                SERVICES.IMAGE AS SERVICE_IMAGE,
                SERVICES.NAME AS SERVICE_NAME,
                PRICES.PRICE,
                PRICES.ID 
            FROM
                PRICES 
                    LEFT JOIN
                        COUNTRIES 
                        ON COUNTRIES.ID = PRICES.COUNTRY_ID 
                    LEFT JOIN
                        SERVICES 
                        ON SERVICES.ID = PRICES.SERVICE_ID 
            WHERE
                SERVICE_ID = ? 
            ORDER BY
                PRICE
        """

        cursor.execute(query, (result[0],))
        result = cursor.fetchall()

        cursor.close()

        return [
            {
                "country": {"id": r[0], "code": r[1], "image": r[2], "name": r[3]},
                "service": {"id": r[4], "code": r[5], "image": r[6], "name": r[7]},
                "price": r[8],
                "id": r[9],
            }
            for r in result
        ]


@click.group()
@click.option("--authorization", help="Key to authorise against SimSMS's servers with.")
@click.pass_context
def cli(ctx, authorization: str):
    ctx.ensure_object(dict)

    path_db = os.path.join(os.path.expanduser("~"), ".ramadan", "burner")
    file_db = os.path.join(path_db, "sms.db")

    if not os.path.isdir(path_db):
        os.makedirs(path_db)

    if not os.path.isfile(file_db):
        with resources.path("burner.resources", "sms.db") as path:
            shutil.copy(path, file_db)

    ctx.obj["CLIENT"] = Client(authorization, file_db)


@cli.command()
@click.pass_context
def countries(ctx):
    """List all of the available countries and their country codes."""
    client: Client = ctx.obj["CLIENT"]

    for country in client.fetch_country_list():
        click.echo(f"[{country['code']}] {country['name']}")


@cli.command()
@click.pass_context
def services(ctx):
    """List all of the available services and their codes."""
    client: Client = ctx.obj["CLIENT"]

    for service in client.fetch_service_list():
        click.echo(f"[{service['code']}] {service['name']}")


@cli.command()
@click.argument("service")
@click.pass_context
def prices(ctx, service: str):
    """Find the cheapest prices for a given service."""
    client: Client = ctx.obj["CLIENT"]

    for price in client.find_price_by_service(service):
        print(
            f"[{price['country']['code']}] {price['country']['name']:<16s} = ₽{price['price']}"
        )


@cli.command()
@click.pass_context
def reset(ctx):
    """Reset the cache with the latest information. Authorisation is needed."""
    client: Client = ctx.obj["CLIENT"]
    client.reset_cache()


if __name__ == "__main__":
    cli()
