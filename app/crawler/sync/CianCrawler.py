import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app.models.flat import Flat
from app.utils.config import PROXY_TYPE, URL
from app.utils.csv_helper import CSV_FLATS_HEADERS, write_flat_to_csv
from app.utils.proxy_helper import proxy_generator

get_proxy = proxy_generator()


class CianCrawler:
    """Class for crawling cian.ru."""

    def __init__(self, region: int, district: int):
        self.session = None
        self.region = region
        self.district = district
        self.page = 1
        self.flats = []
        self.proxies_dict = None
        self.update_proxy()

    def update_proxy(self):
        proxy = next(get_proxy)
        self.proxies_dict = {
            "http": f"{PROXY_TYPE}://{proxy}",
            "https": f"{PROXY_TYPE}://{proxy}",
        }
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,ka;q=0.7",
            "User-Agent": UserAgent().random,
            "Referer": "http://www.cian.ru/",
            "Cookie": "",
        }
        self.session.proxy = self.proxies_dict
        print(self.proxies_dict)

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
                proxies=self.proxies_dict,
            )
            return response.text
        except Exception as exc:
            print("Failed", self.proxies_dict, exc)
            self.update_proxy()
            return ""

    def parse_page(self) -> bool:
        print(
            "Parsing region:",
            self.region,
            "district:",
            self.district,
            "page:",
            self.page,
        )
        soup = BeautifulSoup(self.get_response(), features="html.parser")
        containers = soup.find_all("div", {"data-name": "LinkArea"})
        print("containers len: ", len(containers))
        if not containers:
            return False
        for container in containers:
            self.flats.append(Flat(container))
        return True

    def crawl(self):
        pages = 25
        write_flat_to_csv(CSV_FLATS_HEADERS, self.district)
        while self.page <= pages:
            time.sleep(1)
            if not self.parse_page():
                self.update_proxy()
                continue
            for flat in self.flats:
                write_flat_to_csv(flat.get_row(), self.district)
            self.page += 1
            self.flats = []
        return self.flats
