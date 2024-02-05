import requests
import pandas as pd
import polars as pl

countries_csv = pd.read_csv("worldcities.csv")

country_searched = "India"
lng = countries_csv.loc[countries_csv["country"] == country_searched, 'lng'].values[0]
lat = countries_csv.loc[countries_csv["country"] == country_searched, 'lat'].values[0]

response = requests.get(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude={lat}&minlongitude={lng}")
json_data = response.json()
# print(json_data["features"][0]["properties"].keys())
print(lng)
print(lat)
