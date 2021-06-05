import pandas as pd
from folium import folium
from folium.plugins import HeatMap

district = 286

df = pd.read_csv(f"../coords/flats{district}_coords_prices.csv")
print(df)
