import asyncio
import json
import urllib
from collections import namedtuple
from typing import NamedTuple

import geopy
import matplotlib.pyplot as plt
import pandas as pd
import requests
from config import API_KEY
from geopy import Nominatim

from districts import districts, districts_names

ReadDistricts = namedtuple("ReadDistricts", ["district", "datafr"])
column_names = {"main_price": "Средняя цена, млн", "area": "Средняя площадь, м2"}


def import_flats():
    storage = {"msk": [], "spb": [], "ekb": []}

    for city in storage:
        for district in districts[city]:
            df = pd.read_csv(f"../flats/flats{district}.csv")
            storage[city].append(ReadDistricts(district, df))

    return storage


def calc_mean_values(dataframe):
    return dataframe[["main_price", "area"]].mean()


def get_mean_values(data) -> dict:
    mean_values = {}
    for city in data:
        for readdistrict in data[city]:
            mean_values[readdistrict.district] = calc_mean_values(readdistrict.datafr)
    return mean_values


def get_plot(mean_val_storage, city):
    prices = []
    areas = []
    indices = []
    for district in districts[city]:
        prices.append(mean_val_storage[district]["main_price"] / 10 ** 6)
        areas.append(mean_val_storage[district]["area"])
        indices.append(districts_names[district])

    df_price = pd.DataFrame({"Средняя цена, млн": prices}, index=indices)
    df_price.plot.bar(rot=30)
    plt.savefig(f"{city}_mean_prices.png")

    df_area = pd.DataFrame({"Средняя площадь, м2": areas}, index=indices)
    df_area.plot.bar(rot=30)
    plt.savefig(f"{city}_mean_areas.png")
    # values = []
    # indices = []
    # for district in districts[city]:
    #     values.append(round(mean_val_storage[district][column] / 10**6, 2))
    #     indices.append(districts_names[district])
    # print(values)
    # datafr = pd.DataFrame({f"{column_names[column]}": values}, index=indices)
    # print(datafr)
    # ax = datafr.plot.bar(rot=30)
    # plt.savefig(f"{city}_mean_{column}s.png")


data_storage = import_flats()


mean_values = get_mean_values(data_storage)

for city in data_storage:
    get_plot(mean_values, city)
