import pandas as pd
from folium import folium
from folium.plugins import HeatMap

district = 286

df = pd.read_csv(f"../coords/flats{district}_coords_prices.csv")
print(df)

map_hooray = folium.Map(location=[56.84972475, 60.5664], zoom_start=13)

# Ensure you're handing it floats
df["lat"] = df["lat"].astype(float)
df["lon"] = df["lon"].astype(float)

# Filter the DF for rows, then columns, then remove NaNs
# heat_df = df[df['Speed_limit']=='30'] # Reducing data size so it runs faster
# heat_df = heat_df[heat_df['Year']=='2007'] # Reducing data size so it runs faster
heat_df = df[["lat", "lon", "price"]]
heat_df = heat_df.dropna(axis=0, subset=["lat", "lon"])

# List comprehension to make out list of lists
heat_data = [[row["lat"], row["lon"]] for index, row in heat_df.iterrows()]

# Plot it on the map
HeatMap(heat_data).add_to(map_hooray)

# Display the map
map_hooray.save("map.html")
