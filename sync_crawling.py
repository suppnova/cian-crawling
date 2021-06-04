import csv
import time
from math import ceil

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app.models.flat import Flat

regions = {"msk": 1, "spb": 2, "ekb": 4743}

districts = {
    "msk": [151, 325] + list(range(4, 12)),
    "spb": range(135, 151),
    "ekb": range(286, 293),
}

URL = "http://cian.ru/cat.php"
REGION = "msk"
# PROXY = "89.108.88.146:1080"


CSV_HEADERS = (
    "address",
    "main_price",
    "price_per_m2",
    "area"
)


def gen_proxy():
    with open('socks5.csv', newline='') as f:
        next(f)
        for line in csv.reader(f):
            yield line[0]


get_proxy = gen_proxy()


class CianCrawler:
    """Class for crawling cian.ru."""

    def __init__(self, region: int, district: int):
        """
        Constructor.

        :param region: given region (1 - Moscow, 2 - Saint-Petersburg, 3 - Ekaterinburg)
        :param district: given district (for example 1 - Northwestern Administrative District (Moscow))
        """
        self.session = None
        # self.session = requests.Session()
        # self.session.headers = {
        #     # "User-Agent": UserAgent().random
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,ka;q=0.7",
        #     "User-Agent": UserAgent().random,
        #     "Referer": "http://www.cian.ru/",
        #     "Cookie": ""
        # }
        self.region = region
        self.district = district
        self.page = 1
        self.flats = []
        self.proxies_dict = None
        self.update_proxy()
        # self.proxies_dict = {"http": f"socks5://{PROXIES[0]}"}
        # print(self.proxies_dict)
        # self.session.proxies.update(self.proxies_dict)

    def update_proxy(self):
        proxy = next(get_proxy)
        self.proxies_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
        self.session = requests.Session()
        self.session.headers = {
            # "User-Agent": UserAgent().random
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,ka;q=0.7",
            "User-Agent": UserAgent().random,
            "Referer": "http://www.cian.ru/",
            "Cookie": ""
        }
        self.session.proxy = self.proxies_dict
        # self.session.proxies.update(self.proxies_dict)
        print(self.proxies_dict)

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

    def get_response(self) -> str:
        """Get response from cian server.

        Creates url from parameters and gets response.
        :return: response from cian server
        """
        try:
            response = self.session.get(
                URL,
                params={
                    "deal_type": "sale",
                    "engine_version": 2,
                    "offer_type": "flat",
                    "p": self.page,
                    "district[0]": self.district,
                    "region": self.region,
                },
                timeout=10,
                proxies=self.proxies_dict
            )
            # print(response.text)
            return response.text
        # SOCKSHTTPConnectionPool
        except Exception as exc:
            print("Failed", self.proxies_dict, exc)
            self.update_proxy()
            return ''

    def parse_page(self) -> bool:
        """Parse a given page.

        Creates BeautifulSoup for html parsing.
        For every flat gets container for parsing, then adds Flat instance to flats list.
        :return: None
        """
        print("Parsing region:", self.region, "district:", self.district, "page:", self.page)
        soup = BeautifulSoup(self.get_response(), features="html.parser")
        containers = soup.find_all("div", {"data-name": "LinkArea"})
        print('containers len: ',len(containers))
        if not containers:
            return False
        for container in containers:
            self.flats.append(Flat(container))
        return True

    def crawl(self):
        # soup = BeautifulSoup(self.get_response(1).text, features="html.parser")
        # pages = self.get_pages_amount()
        pages = 25
        write_to_csv2(CSV_HEADERS, self.district)
        while self.page <= pages:
            time.sleep(5)

            if not self.parse_page():
                print("page for restart", self.page)
                self.update_proxy()
                continue
                # break
            write_to_csv2(self.flats[-1].get_row(), self.district)
            [write_to_csv2(flat.get_row(), self.district) for flat in self.flats]
            self.page += 1
            self.flats = []
        return self.flats


def write_to_csv2(row, distr):
    with open(f"../flats{distr}.csv", "a+", encoding="utf-8") as fi:
        pen = csv.writer(fi)
        pen.writerow(row)


def write_to_csv(crawler: CianCrawler, distr: int):
    flats = crawler.crawl()
    with open(f"../flats{distr}.csv", "w", encoding="utf-8") as fi:
        pen = csv.writer(fi)
        pen.writerow(
            (
                "address",
                "main_price",
                "price_per_m2",
                "area"
            )
        )
        for flat in flats:
            pen.writerow(
                (
                    flat.address,
                    flat.main_price,
                    flat.price_per_m2,
                    flat.area
                )
            )


for district in districts[REGION]:
    CianCrawler(regions[REGION], district).crawl()
    # write_to_csv(CianCrawler(regions[REGION], district), district)
# crawler = CianCrawler(regions[REGION], districts[REGION][0])
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
