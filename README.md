# DevOps-Pixel-Team
A repository for the Pixel team in Software Engineering Course


### This Python-based application is designed to assist users with various travel-related tasks, including routing, weather inquiries, and obtaining information about cities. 

## Prerequisites
Before running the application, It is recommended to install the following prerequisites:

- python 3.x
- Virtual environment

Additionally, install the required packages listed in the `requirements.txt` file using the following command:
```bash
pip install -r requirements.txt
```

## Set up API keys and save them in a .env file in the project directory like the following format:

```
# GPT-4 API KEY:
GPT_4_API_KEY=sk-proj-l8evTb8wjYPvenK4K3MoT3BlbkFJTbJ5T3K7fKys2CADnzAa

# graphhopper API KEY:
GRAPHHOPPER_API_KEY=6b2435ab-f952-4fed-9754-a61d9bfff722

# OpenWeather API KEY:
OPENWEATHER_API_KEY=a9a88bc302e36a5d86e1e13f59366f76

# Whisper API KEY:
WHISPER_API_KEY=8xQ9m6ntVyKYH1xC3Slke26u8WtSHUQQ

```

## Usage

Once the prerequisites and API keys are set up, you can run the application. The main functionalities provided by the application include:

### Manual Routing
- For the input, you specify the starting point, destination, and mode of transportation for routing.
- For the result, you get the distance between two places in kms, and how much times it takes to reach the destination.

### Voice Command Routing and Weather Info
- Provides routing and weather inquiries via voice commands.
- Openweather and Whisper APIs are used in this feature.

### GPT-4 Chatbot
- GPT-4-turbo model is used to provide assistance and information regarding city-related inquiries.
- AI chatbot to ask questions about anyting. ( like simple Chat-GPT)

## For a demonstration of the application's features, refer to the [DEMO_VIDEO](https://github.com/Jamshid-Ganiev/DevOps-Pixel-Team/blob/main/mid_term_project/presentation_folder/DEMO_VIDEO.mp4) located in the project repository.

# Collaborators:

- [imdiora](https://github.com/imdiora)
- [alhammadimohamed](https://github.com/alhammadimohamed)
- [soumanzhang](https://github.com/soumanzhang)
