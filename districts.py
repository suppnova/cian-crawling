districts = {
    "msk": [1, 151, 325] + list(range(4, 12)),
    "spb": range(135, 151),
    "ekb": range(286, 293),
}

districts_names = {
    1: "СЗАО",
    4: "ЦАО",
    5: "САО",
    6: "СВАО",
    7: "ВАО",
    8: "ЮВАО",
    9: "ЮАО",
    10: "ЮЗАО",
    11: "ЗАО",
    151: "ЗелАО",
    325: "НАО",
}

for district in districts["spb"]:
    districts_names[district] = district

for district in districts["ekb"]:
    districts_names[district] = district
