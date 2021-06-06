import configparser as cp

config = cp.ConfigParser()
config.read("config.ini")

REGION = config["APP"]["REGION"]

STORAGE_PATH = config["STORAGE"]["PATH"]

URL = config["CRAWL"]["URL"]
PROXY_TYPE = config["CRAWL"]["PROXY_TYPE"]
PROXY_FILE = config["CRAWL"]["PROXY_FILE"]
