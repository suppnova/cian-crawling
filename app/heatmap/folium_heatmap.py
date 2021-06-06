from collections import defaultdict

import branca.colormap as cm
from folium import folium
from folium.plugins import HeatMap
from pandas import concat, read_csv
from pandas.core.frame import DataFrame

from app.utils.config import REGION
from app.utils.dir_helper import make_dir
from app.utils.districts import cities_coordinates, districts
from app.utils.path_helper import get_coords_storage_dirname, get_heatmaps_storage_dir


def init_city_dataframe():
    summary_df = DataFrame()
    for district in districts[REGION]:
        print(district)
        print(f"{get_coords_storage_dirname()}/{REGION}/flats{district}_coords_prices.csv")
        try:
            df = read_csv(
                f"{get_coords_storage_dirname()}/{REGION}/flats{district}_coords_prices.csv"
            )
            summary_df = concat([summary_df, df])
        except FileNotFoundError:
            continue

        print(df)
    return summary_df


def build_heatmap():
    map_path = f"{get_heatmaps_storage_dir()}/{REGION}"
    make_dir(map_path)

    map_hooray = folium.Map(
        location=cities_coordinates[REGION], zoom_start=13, min_zoom=12
    )

    df = init_city_dataframe()
    print(df)

    # Ensure you're handing it floats
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs
    heat_df = df[["lat", "lon", "price"]]
    # heat_df = heat_df.dropna(axis=0, subset=["lat", "lon"])

    max_price = heat_df["price"].max() / 10 ** 6
    min_price = heat_df["price"].min() / 10 ** 6

    # List comprehension to make out list of lists
    heat_data = [
        [row["lat"], row["lon"], row["price"] / max_price]
        for index, row in heat_df.iterrows()
    ]

    # add color bar at the top of the map
    colormap = cm.LinearColormap(
        colors=["blue", "green", "yellow", "orange", "red"],
        vmin=min_price,
        vmax=max_price,
    )

    colormap.add_to(map_hooray)

    # Plot it on the map
    HeatMap(heat_data, radius=25).add_to(map_hooray)

    # Display the map
    map_hooray.save(f"{map_path}/map.html")
