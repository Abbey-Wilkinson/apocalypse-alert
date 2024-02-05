'''Extract + make use of information from earthquakes API.'''
from geopythonukparliament import Countries

def get_lat_lon_from_country(country_name):
    countries = Countries()
    country_data = countries.get_country_by_name(country_name)
    
    if country_data:
        latitude, longitude = country_data['latitude'], country_data['longitude']
        return latitude, longitude
    else:
        print(f"Location information not found for {country_name}")
        return None

# Example usage
country_name = 'United States'
result = get_lat_lon_from_country(country_name)

if result:
    latitude, longitude = result
    print(f"Latitude: {latitude}, Longitude: {longitude}")