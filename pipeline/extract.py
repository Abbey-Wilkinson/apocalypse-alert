from os import environ

from dotenv import load_dotenv
import requests

def get_request_response(url: str) -> dict:
    """Retrieve the response json data for an API request."""

    response = requests.get(url, headers={'x-access-token': environ['UV_API_KEY']})
    json_data = response.json()
    
    return json_data

if __name__ == "__main__":

    load_dotenv()

    print(get_request_response(
        'https://api.openuv.io/api/v1/uv?lat=-33.34&lng=115.342'))
    



