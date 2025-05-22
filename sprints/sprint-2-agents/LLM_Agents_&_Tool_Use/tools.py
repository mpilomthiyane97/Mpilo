import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API keys from environment ---
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Tool 1: Get weather for a given location ---
def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"{description}, {temperature}°C"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather: {e}"

# --- Tool 2: Recommend clothing based on weather ---
def dress_recommendation(weather):
    prompt = f"What should I wear if the weather is {weather}?"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
