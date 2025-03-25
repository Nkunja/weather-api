import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys
import io
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import WeatherAPI, save_to_file, display_weather

class TestWeatherAPI(unittest.TestCase):
    """Test cases for the WeatherAPI class and related functions."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a mock environment variable for testing
        os.environ["OPENWEATHER_API_KEY"] = "fake_api_key_for_testing"
        self.weather_api = WeatherAPI()
        
        # Sample weather data for testing
        self.sample_data = {
            "name": "Nairobi",
            "sys": {"country": "KE"},
            "main": {
                "temp": 24.93,
                "feels_like": 24.63,
                "humidity": 44,
                "pressure": 1012
            },
            "weather": [{"description": "broken clouds"}],
            "wind": {"speed": 4.63, "deg": 70},
            "dt": 1742827568
        }
    
    @patch('os.getenv')
    def test_init_with_missing_api_key(self, mock_getenv):
        """Test initialization with missing API key."""
        # Configure os.getenv to return None for API key
        mock_getenv.return_value = None
        
        # Now test that WeatherAPI initialization raises ValueError
        with self.assertRaises(ValueError):
            WeatherAPI()
    
    @patch('requests.get')
    def test_fetch_weather_success(self, mock_get):
        """Test successful weather data fetching."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.sample_data
        mock_get.return_value = mock_response
        
        result = self.weather_api.fetch_weather("Nairobi")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_fetch_weather_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        # Mock an HTTP error
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error")
        
        result = self.weather_api.fetch_weather("NonExistentCity")
        self.assertIsNone(result)
    
    @patch('requests.get')
    def test_fetch_weather_connection_error(self, mock_get):
        """Test handling of connection errors."""
        # Mock a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        result = self.weather_api.fetch_weather("Nairobi")
        self.assertIsNone(result)
    
    def test_process_weather_data(self):
        """Test weather data processing."""
        processed = self.weather_api.process_weather_data(self.sample_data)
        
        self.assertEqual(processed["location"], "Nairobi, KE")
        self.assertEqual(processed["temperature"], 24.93)
        self.assertEqual(processed["humidity"], 44)
        self.assertEqual(processed["weather"], "broken clouds")
    
    def test_process_weather_data_empty(self):
        """Test processing with empty data."""
        processed = self.weather_api.process_weather_data(None)
        
        self.assertIn("error", processed)
    
    def test_process_weather_data_missing_fields(self):
        """Test processing with missing fields."""
        incomplete_data = {"name": "Nairobi"}
        processed = self.weather_api.process_weather_data(incomplete_data)
        
        self.assertEqual(processed["location"], "Nairobi, Unknown")
        self.assertIsNone(processed["temperature"])
        self.assertEqual(processed["weather"], "Unknown")
    
    def test_save_to_file(self):
        """Test saving data to file."""
        test_filename = "test_weather_data.json"
        processed_data = {"location": "Test City", "temperature": 20}
        
        print(f"Current working directory: {os.getcwd()}")
        print(f"__file__ location: {__file__}")
        print(f"main module location: {sys.modules.get('main').__file__ if 'main' in sys.modules else 'Not found'}")
        
        # Test saving
        success = save_to_file(processed_data, test_filename)
        self.assertTrue(success)
        
        # Verify file content
        with open(test_filename, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, processed_data)
        
        # Clean up
        os.remove(test_filename)
    
    def test_display_weather(self):
        """Test weather display function."""
        processed_data = {
            "location": "Nairobi, KE",
            "temperature": 24.93,
            "feels_like": 24.63,
            "humidity": 44,
            "pressure": 1012,
            "weather": "broken clouds",
            "wind": {"speed": 4.63, "direction": 70},
            "timestamp": 1742827568
        }
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        display_weather(processed_data)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Nairobi, KE", output)
        self.assertIn("24.93°C", output)
        self.assertIn("44%", output)
        self.assertIn("Broken clouds", output)
    
    def test_display_weather_error(self):
        """Test display function with error data."""
        error_data = {"error": "No data available"}
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        display_weather(error_data)
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Error: No data available", output)

if __name__ == "__main__":
    unittest.main()