import requests
import os
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI

"""
This is the main program we programmed as a team(Pixel team). 4 Four different APIs are used in this platform.
1) GPT-4 API
2) graphhopper API
3) OpenWeather API
4) Whisper API
"""

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("GPT_4_API_KEY"))

# Function to format time
def format_time(minutes):
    if minutes < 60:
        return f"{minutes:.2f} minutes"
    else:
        hours = (minutes % 1440) // 60
        remaining_minutes = minutes % 60
        return f"{int(hours)} hours, and {int(remaining_minutes)} minutes"

# Function to geocode location
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

# Function to transcribe voice to text using Whisper API
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

# Function to get weather data using OpenWeather API
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

# Function to handle routing via voice
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

def ask_question():
    question = input("What do you want to know?\nEnter your question: ")
    return question

def get_answer(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer the user's questions professionally."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion
        if response.choices:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't understand your question."
    except Exception as e:
        # handles exceptions, like API errors
        return f"An error occurred: {str(e)}"

def get_city_info(city_name):
    try:
        prompt = f"What are the best time to travel to {city_name}?,"\
                 f" available airlines to {city_name}, famous foods in {city_name},"\
                 f" tourist attractions in {city_name}, and population of {city_name}?"\
                 f" give the answer in bullet points."
        
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant. Answer the questions professionally and make your asnwers as compact as possbile by keeping the core meaning."},
                {"role": "user", "content": prompt}
            ]
        )

        response = completion
        if response.choices:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't understand your question."
    except Exception as e:
        return f"An error occurred while fetching city information: {str(e)}"

def main():
    while True:
        print("Welcome to the Pixel team's travel guide application\n")
        print("There is a menu with 3 features:\n")
        print("Menu:")
        print("    1) Manual routing")
        print("    2) Voice command routing and weather info")
        print("    3) GPT-4 chatbot\n")
        print("Choose one to continue:\n")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            start = input("Enter the starting point: ")
            end = input("Enter the destination: ")
            mode = input("Enter mode of transportation (car, foot, bike): ")

            api_key = os.environ.get("GRAPHHOPPER_API_KEY") # accessing the api key in the .env file

            get_route(start, end, mode, api_key)
        elif choice == "2":
            while True:
                print("\nVoice Control Menu:")
                print("1. Routing via voice")
                print("2. Get current weather of a city")
                print("Type 'quit' to exit.")

                voice_choice = input("Enter your choice: ")

                if voice_choice == "1":
                    handle_routing()
                elif voice_choice == "2":
                    handle_weather_inquiry()
                elif voice_choice.lower() == "quit" or voice_choice.lower() == "q":
                    print("Finishing the program...")
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == "3":
            while True:
                print("Choose an option:")
                print("1. City Information")
                print("2. Chat with ChatGPT")
                choice = input("Enter your choice (1/2): ")

                if choice == "1":
                    city_name = input("Enter the city name or country name: ")
                    city_info = get_city_info(city_name)
                    print(city_info)
                elif choice == "2":
                    while True:
                        question = ask_question()
                        choices = ["no", "n", "exit", "quit", "bye"]
                        if question.lower() in choices:
                            break
                        answer = get_answer(question)
                        print(answer)
                        print("\n")
                else:
                    print("Invalid choice. Please enter either 1 or 2.")

                user_input = input("Do you want to continue? (yes/no): ")
                if user_input.lower() not in ["yes", "y"]:
                    break
        else:
            print("Invalid choice. Please enter either 1, 2, or 3.\n")

        user_input = input("Do you want to continue? (yes/no): ")
        if user_input.lower() not in ["yes", "y"]:
            break

if __name__ == "__main__":
    main()
