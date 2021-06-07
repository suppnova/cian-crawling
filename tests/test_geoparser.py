from collections import namedtuple

import pytest

from app.geoparsing.geoparser import geolocator, geoparse, get_coordinates


def test_bad_address(monkeypatch):
    monkeypatch.setattr(geolocator, "geocode", lambda x: None)
    result = get_coordinates("test address")
    assert result is None


def test_good_address(monkeypatch):
    Coordinates = namedtuple("Coordinates", ["latitude", "longitude"])
    monkeypatch.setattr(geolocator, "geocode", lambda x: Coordinates("lat", "lon"))
    result = get_coordinates("test address")
    assert result == ("lat", "lon")
