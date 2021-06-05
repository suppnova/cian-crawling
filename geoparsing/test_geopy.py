import csv
import time

from geopy.geocoders import Nominatim
from process_address_string import process_address

from districts import districts

REGION = "ekb"
geolocator = Nominatim(user_agent="geocoder")
# d = districts[REGION][2:]


def get_coordinates(address):
    location = geolocator.geocode(address)
    if location is None:
        return None
    return location.latitude, location.longitude


def csv_reader(file_obj):
    """
    Read a csv file.
    """
    reader = csv.reader(file_obj)
    rows = []
    for row in reader:
        rows.append(row)
    return rows


def write_to_csv(distr, lat, lon, price):
    with open(
        f"../coords/{REGION}/flats{distr}_coords_prices.csv", "a+", encoding="utf-8"
    ) as fi:
        pen = csv.writer(fi)
        pen.writerow((lat, lon, price))


if __name__ == "__main__":
    for district in districts[REGION][3:]:
        csv_path = f"../flats/flats{district}.csv"
        with open(csv_path, "r", encoding="utf-8") as f_obj:
            flats = csv_reader(f_obj)
            for flat in flats:
                print(flat)
                if not flat:
                    continue
                coordinates = get_coordinates(process_address(flat[0]))
                if not coordinates:
                    continue
                # lat, lon = coordinates
                print(district, *coordinates, flat[1])
                write_to_csv(district, *coordinates, flat[1])
                # print(get_coordinates(process_address(flat[0])))
                # time.sleep(0.1)

# geolocator = Nominatim(user_agent="geocoder")
# location = geolocator.geocode(
#     "Свердловская область, Екатеринбург, Верх-Исетский, Евгения Савкова"
#     # "Свердловская область, Екатеринбург, Верх-Исетский, Мичуринский, Мичуринский ЖК"
#     # "Свердловская область, Екатеринбург, Мичуринский, Мичуринский ЖК"
#     # Свердловская область, Екатеринбург, р-н Верх-Исетский, мкр. Академический, улица Очеретина, 6
#     # "Свердловская область, Екатеринбург, Верх-Исетский, Академический, Очеретина, 6"
#     # "Свердловская область, Екатеринбург, Верх-Исетский, Меридиан ЖК"
#     # "Свердловская область, Екатеринбург, Крауля, 89А"
#     # "Свердловская область, Екатеринбург, Центральный квартал"
#     # "Свердловская область, Екатеринбург, Верх-Исетский, Центральный"
#     # "Свердловская область, Екатеринбург, р-н Кировский, мкр. ЖБИ, м. Динамо, Парк Каменные Палатки ЖК"
#     # "Свердловская область, Екатеринбург, р-н Верх-Исетский, мкр. Академический, улица Очеретина, 5"
# )
# print(location.address)
# print((location.latitude, location.longitude))
# print(location.raw)


# print(csv_reader("..flats/flats288.csv"))
