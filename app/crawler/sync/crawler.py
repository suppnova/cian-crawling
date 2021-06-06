from app.utils.config import REGION
from app.utils.districts import districts

from .CianCrawler import CianCrawler

regions = {"msk": 1, "spb": 2, "ekb": 4743}


def crawl():
    for district in districts[REGION]:
        CianCrawler(regions[REGION], district).crawl()
