import os
import requests
import json
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WeatherAPI:
    """
    A class for interacting with the OpenWeatherMap API to fetch weather data.
    """
    
    def __init__(self):
        """Initialize the WeatherAPI with configuration from environment variables."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variable
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            logger.error("API key not found. Please set OPENWEATHER_API_KEY in .env file.")
            raise ValueError("API key not found")
            
        self.base_url = os.getenv("OPENWEATHER_URL")
    
    def fetch_weather(self, city: str, units: str = "metric") -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data for a specified city.
        
        Args:
            city: The name of the city to get weather for
            units: The unit system to use (metric, imperial, standard)
            
        Returns:
            Dictionary containing weather data or None if request failed
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            logger.info(f"Fetching weather data for {city}")
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse and return the JSON response
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error occurred: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception occurred: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return None
    
    def process_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and extract relevant information from weather data.
        
        Args:
            data: Raw weather data from the API
            
        Returns:
            Dictionary containing processed weather information
        """
        if not data:
            return {"error": "No data available"}
        
        try:
            processed_data = {
                "location": data.get("name", "Unknown") + ", " + data.get("sys", {}).get("country", "Unknown"),
                "temperature": data.get("main", {}).get("temp"),
                "feels_like": data.get("main", {}).get("feels_like"),
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "weather": data.get("weather", [{}])[0].get("description", "Unknown"),
                "wind": {
                    "speed": data.get("wind", {}).get("speed"),
                    "direction": data.get("wind", {}).get("deg")
                },
                "timestamp": data.get("dt")
            }
            return processed_data
        except Exception as e:
            logger.error(f"Error processing weather data: {e}")
            return {"error": "Failed to process weather data"}

def save_to_file(data: Dict[str, Any], filename: str = "weather_data.json") -> bool:
    """
    Save processed weather data to a JSON file.
    
    Args:
        data: Processed weather data
        filename: Name of the file to save data to
        
    Returns:
        Boolean indicating success or failure
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Data successfully saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to file: {e}")
        return False

def display_weather(weather_data: Dict[str, Any]) -> None:
    """
    Display weather information in a user-friendly format.
    
    Args:
        weather_data: Processed weather data
    """
    if "error" in weather_data:
        print(f"Error: {weather_data['error']}")
        return
    
    print("\n========== WEATHER REPORT ==========")
    print(f"Location: {weather_data['location']}")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Feels like: {weather_data['feels_like']}°C")
    print(f"Weather: {weather_data['weather'].capitalize()}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Pressure: {weather_data['pressure']} hPa")
    print(f"Wind speed: {weather_data['wind']['speed']} m/s")
    print("====================================\n")

def main():
    """Main function to run the weather data fetcher."""
    try:
        # Initialize the WeatherAPI class
        weather_api = WeatherAPI()
        
        # Get city input from user
        city = input("Enter city name: ")
        
        # Fetch weather data
        raw_data = weather_api.fetch_weather(city)
        
        if raw_data:
            # Process the data
            processed_data = weather_api.process_weather_data(raw_data)
            
            # Display the weather information
            display_weather(processed_data)
            
            # Save data to file
            save_to_file(processed_data)
        else:
            print("Failed to fetch weather data. Check the logs for details.")
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print("An error occurred while running the program. Check the logs for details.")

if __name__ == "__main__":
    main()