import configparser as cp

config = cp.ConfigParser()
config.read("config.ini")

API_KEY = config["ACCESS"]["API_KEY"]
