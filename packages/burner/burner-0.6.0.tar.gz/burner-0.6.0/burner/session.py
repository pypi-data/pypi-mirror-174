from typing import List, Optional, TypedDict

import requests
from bs4 import BeautifulSoup, Tag

from .exceptions import (
    APIException,
    EmptyAuthorisationException,
    InvalidAuthorisationException,
    NoFundsException,
    ScraperException,
)


class CountryPriceResponse(TypedDict):
    id: str
    enable: str
    country_id: str
    service_opt: str
    price: str
    country_shortname: str


class Session:
    def __init__(self, api_key: str = None):
        self._api_key = api_key

        self._session = requests.Session()

    def request(self, method: str, params: Optional[dict] = None) -> dict:
        """Make a request to SimSMS's API."""
        if not self._api_key:
            raise EmptyAuthorisationException

        params.update(
            {
                "metod": method,  # This spelling mistake is on purpose.
                "apikey": self._api_key,
            }
        )

        resp = self._session.get("https://simsms.org/priemnik.php", params=params)
        resp.raise_for_status()

        # "Коды возвращаемых ошибок" subsection: https://simsms.org/new_theme_api.html
        if resp.text in ("API KEY не найден!", "API KEY не получен!"):
            raise InvalidAuthorisationException

        elif resp.text == "Недостаточно средств!":
            raise NoFundsException

        elif resp.text in (
            "Превышено количество попыток!",
            "Произошла неизвестная ошибка.",
            "Произошла внутренняя ошибка сервера.",
            "Неверный запрос.",
        ):
            raise APIException

        data = resp.json()

        # Mostly rate limits or bans.
        if data["response"] in ("5", "6", "7"):
            raise APIException

        return data

    def _fetch_table_data(self, table_id: int) -> List[dict]:
        """Fetch data from the tables listed on the API documentation. This is done as
        there is no officially exposed endpoint to crawl countries or services, only
        tables in the documentation.

        https://simsms.org/new_theme_api.html
        """
        resp = self._session.get("https://simsms.org/new_theme_api.html")
        soup = BeautifulSoup(resp.text, "html.parser")

        tables: List[Tag] = soup.find_all("table")

        if len(tables) == 0 or len(tables) < table_id + 1:
            raise ScraperException("The table with the given ID could not be found.")

        data: List[dict] = []
        rows: List[Tag] = tables[table_id].find_all("tr")

        for row in rows:
            row_data: List[Tag] = row.find_all("td")

            if len(row_data) < 4:
                continue

            # TODO: Maybe return something that _isn't_ a plain old `dict`.
            data.append(
                {
                    # "id": int(row_data[0].get_text().strip()),
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

    def fetch_prices_by_country(self, country_code: str) -> List[CountryPriceResponse]:
        """Fetches all of the available prices for a specific country. This does not
        require an API key to see."""
        params = {"type": "get_prices_by_country", "country_id": country_code}

        resp = self._session.get("https://simsms.org/reg-sms.api.php", params=params)
        resp.raise_for_status()

        return resp.json()
