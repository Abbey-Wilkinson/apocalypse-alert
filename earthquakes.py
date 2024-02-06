import requests
import pandas as pd
import polars as pl

countries_csv = pd.read_csv("worldcities.csv")

country_searched = "Japan"
lng = countries_csv.loc[countries_csv["country"] == country_searched, 'lng'].values[0]
lat = countries_csv.loc[countries_csv["country"] == country_searched, 'lat'].values[0]
#look into api query parameters, why min lat instead of max lat?
response = requests.get(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude={lat}&minlongitude={lng}")
json_data = response.json()
magnitude = json_data["features"][0]["properties"]["mag"]


eq_for_country = []

count_eq = len(json_data["features"][0])
for i in range (0, count_eq):
    eq_data = {
    "mag": json_data["features"][i]["properties"]["mag"],
    "lng": json_data["features"][i]["geometry"]["coordinates"][0],
    "lat": json_data["features"][i]["geometry"]["coordinates"][1]
    }
    eq_for_country.append(eq_data)

df = pd.DataFrame(eq_for_country)
print(df)
