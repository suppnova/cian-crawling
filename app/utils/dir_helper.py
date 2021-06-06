from os import makedirs
from os.path import exists


def make_dir(path):
    if not exists(path):
        makedirs(path)
