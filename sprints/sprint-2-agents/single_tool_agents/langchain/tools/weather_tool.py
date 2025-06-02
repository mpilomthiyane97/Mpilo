from langchain.tools import tool
import os
import requests

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        return "OpenWeather API key is not set in environment variables."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url).json()
    if response.get("cod") != 200:
        return "Weather not found."

    weather = response["weather"][0]["description"]
    temp = response["main"]["temp"]
    return f"The weather in {city} is {weather} with a temperature of {temp}°C."
