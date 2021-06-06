from csv import reader, writer

from app.utils.config import REGION
from app.utils.dir_helper import make_dir
from app.utils.path_helper import get_coords_storage_dirname, get_flats_storage_dirname

CSV_FLATS_HEADERS = ("address", "main_price", "price_per_m2", "area")
CSV_COORDS_HEADERS = ("lat", "lon", "price")


def write_flat_to_csv(row, distr):
    flats_path = get_flats_storage_dirname()
    make_dir(flats_path)
    with open(f"{flats_path}/flats{distr}.csv", "a+", encoding="utf-8") as fi:
        pen = writer(fi)
        pen.writerow(row)


def read_flats(distr):
    flats_path = get_flats_storage_dirname() + f"/flats{distr}.csv"
    rows = []
    with open(flats_path, "r", encoding="utf-8") as fi:
        csv_reader = reader(fi)
        for row in csv_reader:
            rows.append(row)
    return rows[1:] if len(rows) > 1 else []


def write_coords_to_csv(row, distr):
    coords_path = get_coords_storage_dirname() + f"/{REGION}"
    make_dir(coords_path)
    with open(
        f"{coords_path}/flats{distr}_coords_prices.csv", "a+", encoding="utf-8"
    ) as fi:
        pen = writer(fi)
        pen.writerow(row)
