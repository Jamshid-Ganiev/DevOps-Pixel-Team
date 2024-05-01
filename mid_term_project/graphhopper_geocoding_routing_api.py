import requests
import os
from dotenv import load_dotenv

# loads the environment variables from .env file
load_dotenv()


def format_time(minutes):
    # formats the time in hours and minutes
    if minutes < 60:
        return f"{minutes:.2f} minutes"
    else:
        hours = (minutes % 1440) // 60
        remaining_minutes = minutes % 60
        return f"{int(hours)} hours, and {int(remaining_minutes)} minutes"
    

def geocode_location(location, api_key):
    # gets the coordinates of the given locations and return lattitude and longtitude
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": location,
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['hits']) > 0:
            return data['hits'][0]['point']
        else:
            return None
    else:
        print(f"Geocoding error: {response.status_code}")
        return None

def get_route(start, end, mode, api_key):
    start_coords = geocode_location(start, api_key)
    end_coords = geocode_location(end, api_key)

    if start_coords is None or end_coords is None:
        print("Failed to geocode locations.")
        return

    url = "https://graphhopper.com/api/1/route"
    s_lat = start_coords['lat']
    s_lng = start_coords['lng']

    e_lat = end_coords['lat']
    e_lng = end_coords['lng']
    params = {
        "point": [f"{s_lat},{s_lng}", f"{e_lat},{e_lng}"],
        "vehicle": mode,
        "locale": "en",
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        distance = data['paths'][0]['distance'] / 1000  # converts meters to kilometers
        time_minutes = data['paths'][0]['time'] / 1000 / 60  # converts milliseconds to minutes
        print("1) API status: 200 (successful)")
        print(f"2) Distance between {start} and {end}: {distance:.2f} km")

        # formatted time
        formatted_time = format_time(time_minutes)
        print(f"3) Time it takes to reach the destination: {formatted_time}")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    start = input("Enter the starting point: ")
    end = input("Enter the destination: ")
    mode = input("Enter mode of transportation (car, foot, bike): ")

    api_key = os.environ.get("GRAPHHOPPER_API_KEY") # accessing the api key in the .env file

    get_route(start, end, mode, api_key)
