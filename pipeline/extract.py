from os import environ

from dotenv import load_dotenv
import pandas as pd
import requests


def get_pollution_api_request_response(city: str, key: str) -> dict:
    """
    Retrieve the response json data for an API request to the pollution api.
    """

    response = requests.get(f'https://api.waqi.info/feed/{city}/?token={key}')
    json_data = response.json()

    return json_data


def get_uv_api_request_response(key: str, lat: str, lng: str) -> dict:
    """
    Retrieve the response json data for an API request to the uv api.
    """

    response = requests.get(
        f'https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}', headers={'x-access-token': key})
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
            "lng": pollution_data['data']['city']['geo'][1]
        }

        return wanted_pollution
    return "No data found."


def get_individual_pollutant_info(pollution_data: dict) -> dict:
    """
    Gets the required data for each individual pollutant.
    """

    if pollution_data["status"] == "ok":
        individual_pollutant_data = pollution_data['data']['iaqi']
        return individual_pollutant_data
    return "No data found."


def get_capital_cities():
    """
    Loads the capital city of each country.
    """

    with open("worldcities.csv", "r") as file:
       cities = pd.read_csv(file)

       cities = cities[cities["capital"] == "primary"]

       city_names = cities["city"].values.tolist()
    
    return city_names


def get_air_reading_data_for_all(capital_cities: str):
    """
    Retrieves all of the information on a capital city,
    if the endpoint is valid then the desired information is extracted.
    """
    
    wanted_city_data = []
    for city in capital_cities:
        print(f"Getting data for {city}...")
        all_city_data = get_pollution_api_request_response(city, environ["POLLUTION_API_KEY"])
        city_data = get_pollution_info(all_city_data)

        if city_data != "No data found.":
            wanted_city_data.append(city_data)

    return wanted_city_data

        
def get_uv_index_data_for_all(cities: list[dict]) -> list[dict]:
    """
    Retrieves uv data for all capital cities.
    """

    all_uv_data = []
    for city in cities:
        print(f"Getting data for {city['city']}...")
        uv_data = get_uv_api_request_response(environ['UV_API_KEY'], city['lat'], city['lng'])

        all_uv_data.append(uv_data)
    
    return all_uv_data


if __name__ == "__main__":

    load_dotenv()


    capital_cities = get_capital_cities()
    # print(capital_cities)

    # pollution_data = get_pollution_api_request_response( capital_cities[1], environ["POLLUTION_API_KEY"])

    # relevant_pollution_data = get_pollution_info(pollution_data)
    # individual_pollutant_data = get_individual_pollutant_info(
    #     pollution_data)

    # print(relevant_pollution_data)
    # print(individual_pollutant_data)

    # uv_data = get_uv_api_request_response(environ['UV_API_KEY'], relevant_pollution_data['lat'], relevant_pollution_data['lng'])

    # print(uv_data)


    wanted_city_data = get_air_reading_data_for_all(capital_cities)
    print(wanted_city_data)


    all_uv_index_data = get_uv_index_data_for_all(wanted_city_data)
    print(all_uv_index_data)
