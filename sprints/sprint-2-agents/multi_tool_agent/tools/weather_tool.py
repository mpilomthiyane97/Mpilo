import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> str:
    """
    Get current weather information for a specified city.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather description and temperature in Celsius
    """
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        return "OpenWeather API key is not set."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return f"Weather not found for {city}."

    weather_desc = response["weather"][0]["description"]
    temp = response["main"]["temp"]
    return f"Current weather in {city}: {weather_desc}, Temperature: {temp}°C."
