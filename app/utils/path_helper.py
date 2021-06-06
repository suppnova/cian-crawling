from os.path import abspath, dirname
from sys import modules


def get_root_dirname():
    return dirname(modules['__main__'].__file__)

def get_current_module_path(module):
    path = abspath(module)
    return dirname(path)

def get_flats_storage_dirname():
    return get_root_dirname() + '/flats'

def get_histograms_storage_dir():
    return get_root_dirname() + '/results/histograms'