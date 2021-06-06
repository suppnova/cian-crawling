import csv

from .config import PROXY_FILE


def proxy_generator():
    with open(PROXY_FILE, newline="") as f:
        next(f)
        for line in csv.reader(f):
            yield line[0]
