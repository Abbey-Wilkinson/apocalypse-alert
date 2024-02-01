from concurrent.futures import ThreadPoolExecutor, as_completed
from os import environ
from time import perf_counter

from dotenv import load_dotenv
import pandas as pd
import polars as pl
from requests import Session

session = Session()


# World Cities

def get_capital_cities():
    """
    Loads the capital city of each country.
    """

    with open("worldcities.csv", "r") as file:
        cities = pd.read_csv(file)

        cities = cities[cities["capital"] == "primary"]

        city_names = cities["city"].values.tolist()

    return city_names


def get_capital_cities_pl():
    """
    Loads the capital city of each country.
    """
    cities = pl.read_csv("worldcities.csv", columns=[
                         'city', 'country', 'capital'])
    capital_cities = cities.filter(pl.col("capital") == "primary")['city']
    return capital_cities


# Air Pollution API

def get_pollution_api_request_response(city: str, key: str) -> dict:
    """
    Retrieve the response json data for an API request to the pollution api.
    """

    response = session.get(f'https://api.waqi.info/feed/{city}/?token={key}')
    json_data = response.json()
    return json_data


def get_pollution_info(pollution_data: dict) -> dict:
    """
    Gets the required data from all pollution data for that station.
    """

    if pollution_data["status"] == "ok":

        wanted_pollution = {
            "station_id": pollution_data['data']['idx'],
            "time": pollution_data['data']['time'].get('iso', "N/K"),
            "general_aqi": pollution_data['data']['aqi'],
            "city": pollution_data['data']['city']['name'],
            "lat": pollution_data['data']['city']['geo'][0],
            "lng": pollution_data['data']['city']['geo'][1],
            "individual_pollutant_data": pollution_data['data']['iaqi']
        }

        return wanted_pollution
    return "No data found."


def get_air_reading_data_for_all(capital_cities: pl.Series):
    """
    Retrieves all of the information on a capital city,
    if the endpoint is valid then the desired information is extracted.
    """
    with ThreadPoolExecutor() as executor:

        futures = [executor.submit(get_pollution_api_request_response,
                                   city, environ["POLLUTION_API_KEY"]) for city in capital_cities]

        wanted_city_data = []
        for future in as_completed(futures):
            all_city_data = future.result()
            city_data = get_pollution_info(all_city_data)

            if city_data != "No data found.":
                wanted_city_data.append(city_data)

    return wanted_city_data


# Earthquake API

def get_earthquake_api_request_response(lat: str, lng: str) -> dict:
    """
    Retrieve the response json data for an API request to the uv api.
    """

    response = session.get(
        f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude={lat}&longitude={lng}&maxradiuskm=1000')
    json_data = response.json()

    features = json_data.get("features", [])

    if features:
        feature = features[0]
        properties = feature.get('properties', {})

        return {
            "magnitude": properties['mag'],
            "country": properties['place'],
            "at": properties['time']
        }

    return None


def get_earthquake_data_for_all(cities: list[dict]) -> list[dict]:
    """
    Retrieves uv data for all capital cities.
    """

    with ThreadPoolExecutor() as executor:

        futures = [executor.submit(get_earthquake_api_request_response,
                                   city['lat'], city['lng']) for city in cities]

        all_earthquake_data = []
        for future in as_completed(futures):
            earthquake_detail = future.result()

            if earthquake_detail:
                all_earthquake_data.append(earthquake_detail)

        return all_earthquake_data


if __name__ == "__main__":

    load_dotenv()
    start = perf_counter()

    capital_cities = get_capital_cities_pl()
    wanted_city_data = get_air_reading_data_for_all(capital_cities)
    all_earthquake_index_data = get_earthquake_data_for_all(
        wanted_city_data)

    print(wanted_city_data)
    print(all_earthquake_index_data)

    end = perf_counter() - start
    print(f"Total time taken: {end}s")
