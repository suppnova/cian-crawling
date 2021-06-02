import asyncio
from math import ceil

import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app.models.flat import Flat

regions = {"msk": 1, "spb": 2, "ekb": 4743}

districts = {
    "msk": [1, 151, 325] + list(range(4, 12)),
    "spb": range(133, 151),
    "ekb": range(286, 293),
}

URL = "https://cian.ru/cat.php"
REGION = "spb"
session = requests.Session()


class CianCrawler:
    """Class for crawling cian.ru."""

    def __init__(self, region: int, district: int):
        # def __init__(self, region: int, district: int, page=1, flats=[], session=None):
        """
        Constructor.

        :param region: given region (1 - Moscow, 2 - Saint-Petersburg, 3 - Ekaterinburg)
        :param district: given district (for example 1 - Northwestern Administrative District (Moscow))
        """
        self.region = region
        self.district = district
        self.page = 1
        self.flats = []
        self.session = None

    @staticmethod
    def get_pages_amount(soup) -> int:
        """
        Get amount of pages to parse.

        Amount of ads on one page: 28
        :param soup: BeautifulSoup from the first page (contains amount of ads in h5 block)
        :return: amount of pages to parse
        """
        ads = int("".join([char for char in soup.find("h5").text if char.isdigit()]))
        return ceil(ads / 28)

    async def get_response(self, page: int) -> aiohttp.request:
        """Get response from cian server.

        Creates url from parameters and gets response.
        :return: response from cian server
        """
        response = await self.session.request(
            "GET",
            URL,
            params={
                "deal_type": "sale",
                "engine_version": 2,
                "offer_type": "flat",
                "p": page,
                "district[0]": self.district,
                "region": self.region,
            },
        )
        text = await response.text()
        print(text)
        return text

    async def parse_page(self, page: int) -> None:
        """Parse a given page.

        Creates BeautifulSoup for html parsing.
        For every flat gets container for parsing, then adds Flat instance to flats list.
        :return: None
        """
        print("Parse", self.region, self.district, page)
        soup = BeautifulSoup(await self.get_response(page), features="html.parser")
        containers = soup.find_all("div", {"data-name": "LinkArea"})
        print(containers)
        for container in containers:
            self.flats.append(Flat(container))

    async def crawl(self):
        # soup = BeautifulSoup(self.get_response().text, features="html.parser")
        # pages = self.get_pages_amount()
        page = 1
        pages = 1
        tasks = []
        self.session = aiohttp.ClientSession()
        while page <= pages:
            tasks.append(self.parse_page(page))
            await asyncio.sleep(1)
            page += 1
        self.flats = await asyncio.gather(*tasks, return_exceptions=True)
        await self.session.close()
        return self.flats


async def main():
    vyborgsky_flats = await crawler.crawl()
    print(vyborgsky_flats)


crawler = CianCrawler(regions[REGION], districts[REGION][0])
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
