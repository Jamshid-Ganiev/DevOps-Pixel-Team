import requests
import os
from dotenv import load_dotenv
import speech_recognition as sr
import time

# Load environment variables from .env file
load_dotenv()

# function to format time
def format_time(minutes):
    if minutes < 60:
        return f"{minutes:.2f} minutes"
    else:
        hours = (minutes % 1440) // 60
        remaining_minutes = minutes % 60
        return f"{int(hours)} hours, and {int(remaining_minutes)} minutes"

# function to geocode location
def geocode_location(location, api_key):
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

# Function to get route
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
        formatted_time = format_time(time_minutes)
        print(f"3) Time it takes to reach the destination: {formatted_time}")
    else:
        print(f"Error: {response.status_code}")

# the following can also be used to transcribe voice to text but it is not used in this code due to a bit inaccuracy
# # Function to transcribe voice to text using SpeechRecognition
# def transcribe_voice(audio_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio_data)
#             print(f"TRANSCRIBE VOICE FUNCTION:{text}")
#             return text
#         except sr.UnknownValueError:
#             return "Could not understand audio"
#         except sr.RequestError as e:
#             return f"Error: {e}"
        

# function to transcribe voice to text using Whisper API
def transcribe_voice(audio_url):
    url = "https://transcribe.whisperapi.com"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHISPER_API_KEY')}"
    }
    data = {
        "url": audio_url,
        "language": "english"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(response.json())
        try:
            text = response.json()['text']
            print(f"Transcribed text: {text}")
            return text
        except KeyError:
            return "Could not transcribe audio"
    else:
        return f"Error: {response.status_code}"

# function to get weather data using OpenWeather API
def get_weather(city_name):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()

        if "main" in weather_data and "temp" in weather_data["main"]:
            temperature_kelvin = weather_data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            weather_data["main"]["temp"] = temperature_celsius  # updates temperature to Celsius

        return weather_data
    else:
        return None

# function to handle routing via voice
def handle_routing():
    recognizer = sr.Recognizer()
    voice_data_folder = "voice_data/routing"

    if not os.path.exists(voice_data_folder):
        os.makedirs(voice_data_folder)

    with sr.Microphone() as source:
        print("Speak the starting point (city and street):")
        audio_data = recognizer.record(source, duration=7)
        audio_file_start = os.path.join(voice_data_folder, "start_location.wav")

        with open(audio_file_start, "wb") as f:
            f.write(audio_data.get_wav_data())
        start_location = transcribe_voice(audio_file_start)
        print("Start Location:", start_location)

        print("Speak the destination:")
        audio_data = recognizer.record(source, duration=7)
        audio_file_end = os.path.join(voice_data_folder, "end_location.wav")
        with open(audio_file_end, "wb") as f:
            f.write(audio_data.get_wav_data())
        end_location = transcribe_voice(audio_file_end)
        print("End Location:", end_location)

    mode = input("Enter mode of transportation (car, foot, bike): ")
    get_route(start_location, end_location, mode, os.getenv("GRAPHHOPPER_API_KEY"))

# Function to handle weather inquiry
def handle_weather_inquiry():
    recognizer = sr.Recognizer()
    voice_data_folder = "voice_data/weather"

    with sr.Microphone() as source:
        print("Which city's weather do you want to know?")
        audio_data = recognizer.record(source, duration=6)
        audio_file = os.path.join(voice_data_folder, "weather.wav")

        with open(audio_file, "wb") as f:
            f.write(audio_data.get_wav_data())

        city_name = transcribe_voice(audio_file)
        print("City Name:", city_name)

    if city_name:
        weather_data = get_weather(city_name)
        if weather_data:
            temperature = weather_data["main"]["temp"]
            formatted_temperature = "{:.2f}".format(temperature)  # formats temperature to two decimal places
            print("Weather:", weather_data["weather"][0]["description"])
            print("Temperature:", formatted_temperature, "°C")  # displays temperature with units
        else:
            print("Failed to retrieve weather data.")
    else:
        print("City name not recognized. Please try again.")

# Main loop
if __name__ == "__main__":
    while True:
        print("\nVoice Control Menu:")
        print("1. Routing via voice")
        print("2. Get current weather of a city")
        print("Type 'quit' to exit.")

        choice = input("Enter your choice: ")

        if choice == "1":
            handle_routing()
        elif choice == "2":
            handle_weather_inquiry()
        elif choice.lower() == "quit" or choice.lower() == "q":
            print("Finishing the program...")
            break
        else:
            print("Invalid choice. Please try again.")
s