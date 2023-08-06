import os
import shutil
import time
from importlib import resources

import click
import phonenumbers

from .client import Client


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
    for price in client.get_prices_by_service(service):
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
@click.option(
    "-d",
    "--delay",
    default=30,
    type=int,
    help="Time in seconds to wait between checks.",
)
@click.pass_obj
def number(client: Client, country: str, service: str, delay: int):
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
        time.sleep(delay)


@cli.command()
@click.pass_obj
def reset(client: Client):
    """Reset the cache with the latest information. Authorisation is needed."""
    client.reset_cache()


def main():
    cli(auto_envvar_prefix="SMS")


if __name__ == "__main__":
    main()
