from collections import namedtuple

import matplotlib.pyplot as plt
from pandas import read_csv
from pandas.core.frame import DataFrame

from app.utils.config import REGION
from app.utils.dir_helper import make_dir
from app.utils.path_helper import get_flats_storage_dirname, get_histograms_storage_dir
from districts import cities_names, districts, districts_names

ReadDistricts = namedtuple("ReadDistricts", ["district", "datafr"])
column_names = {"main_price": "Средняя цена, млн", "area": "Средняя площадь, м2"}
plt.rc("font", size=8)


def import_flats():
    storage = {"msk": [], "ekb": [], "spb": []}

    for city in storage:
        for district in districts[city]:
            try:
                df = read_csv(f"{get_flats_storage_dirname()}/flats{district}.csv")
                storage[city].append(ReadDistricts(district, df))
            except FileNotFoundError:
                continue

    return storage


def calc_mean_values(dataframe):
    return dataframe[["main_price", "area"]].mean()


def get_mean_values(data) -> dict:
    mean_values = {}
    for city in data:
        for readdistrict in data[city]:
            mean_values[readdistrict.district] = calc_mean_values(readdistrict.datafr)
    return mean_values


def save_plot(df: DataFrame, city: str, filename: str) -> None:
    df.plot.bar(rot=20)
    plt.title(cities_names[city], fontdict={"fontsize": 14})
    plt.savefig(f"{get_histograms_storage_dir()}/{city}_{filename}.png")


def get_plots(mean_val_storage, city):
    prices = []
    areas = []
    indices = []
    for district in districts[city]:
        if district not in mean_val_storage:
            continue

        prices.append(mean_val_storage[district]["main_price"] / 10 ** 6)
        areas.append(mean_val_storage[district]["area"])
        indices.append(districts_names[district])

    save_plot(
        DataFrame({"Средняя площадь, м2": areas}, index=indices), city, "mean_areas"
    )
    save_plot(
        DataFrame({"Средняя цена, млн": prices}, index=indices), city, "mean_prices"
    )


def build_histograms():
    data_storage = import_flats()
    print(data_storage)
    mean_values = get_mean_values(data_storage)

    make_dir(get_histograms_storage_dir())
    get_plots(mean_values, REGION)
