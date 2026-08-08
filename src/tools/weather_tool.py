import os
import requests
from langchain.tools import tool


@tool("Weather Information Tool")
def get_weather(city: str) -> str:
    """
    Fetch weather information for the specified city.
    
    Args:
        city: Name of the city
        
    Returns:
        Formatted weather information string
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return "Error: OpenWeather API key not found. Please configure OPENWEATHER_API_KEY in .env file."
    
    try:
        # OpenWeather API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather information
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_desc = data["weather"][0]["description"]
        weather_main = data["weather"][0]["main"]
        
        # Format the response
        weather_info = f"""
Weather Information for {city.title()}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperature: {temperature}°C (Feels like: {feels_like}°C)
🌤️  Conditions: {weather_main} - {weather_desc.title()}
💧 Humidity: {humidity}%
🌬️  Wind Speed: {wind_speed} m/s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return weather_info.strip()
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return f"Error: City '{city}' not found. Please check the city name and try again."
        return f"Error fetching weather data: {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to weather service: {str(e)}"
    except KeyError as e:
        return f"Error parsing weather data: Missing field {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
