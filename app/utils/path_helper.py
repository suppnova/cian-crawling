from os.path import dirname
from sys import modules

from .config import STORAGE_PATH


def get_root_dirname():
    return dirname(modules["__main__"].__file__)


def get_flats_storage_dirname():
    return get_root_dirname() + f"/{STORAGE_PATH}/flats"


def get_coords_storage_dirname():
    return get_root_dirname() + f"/{STORAGE_PATH}/coords"


def get_histograms_storage_dir():
    return get_root_dirname() + f"/{STORAGE_PATH}/histograms"


def get_heatmaps_storage_dir():
    return get_root_dirname() + f"/{STORAGE_PATH}/heatmaps"
