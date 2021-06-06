import time

from geopy.geocoders import Nominatim

from app.utils.address_helper import process_address
from app.utils.config import REGION
from app.utils.csv_helper import CSV_COORDS_HEADERS, read_flats, write_coords_to_csv
from app.utils.districts import districts

geolocator = Nominatim(user_agent="geocoder")


def get_coordinates(address):
    location = geolocator.geocode(address)
    if location is None:
        return None
    return location.latitude, location.longitude


def geoparse():
    for district in districts[REGION]:
        flats = read_flats(district)
        if not flats:
            continue

        write_coords_to_csv(CSV_COORDS_HEADERS, district)
        for flat in flats:
            print(flat)
            if not flat:
                continue
            coordinates = get_coordinates(process_address(flat[0]))
            if not coordinates:
                continue
            lat, lon = coordinates
            print(district, lat, lon, flat[1])
            write_coords_to_csv((lat, lon, flat[1]), district)
            time.sleep(0.1)
