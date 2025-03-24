# Secure API for Data Fetching

A Python script that securely fetches weather data from the OpenWeatherMap API, processes it, and displays the results.

## Features

- Securely stores API key using environment variables
- Fetches current weather data for any city
- Processes and displays relevant weather information
- Implements comprehensive error handling
- Includes logging for debugging and monitoring
- Unit tests for all components

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Nkunja/weather-api.git
   cd weather-api
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API key:
   - Copy `.env.example` to a new file named `.env`
   - Set the Open weather url as below
   - Sign up for an API key at [OpenWeatherMap](https://openweathermap.org/api)
   - Add your API key to the `.env` file:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     OPENWEATHER_URL=https://api.openweathermap.org/data/2.5/weather
     ```

## Usage

Run the script from the command line:

```
python3 main.py
```

The script will:
1. Prompt you to enter a city name
2. Fetch the current weather data for that city
3. Display the weather information in a readable format
4. Save the data to a JSON file

## Running Tests

Run the unit tests with:

```
python -m unittest test_api.py
```

## Dependencies

- requests: For making HTTP requests
- python-dotenv: For loading environment variables from .env file
- logging: For logging events and errors
- unittest: For unit testing

## Security Considerations

- API keys are stored in a `.env` file which is not committed to version control
- Error handling prevents sensitive information from being exposed in error messages
- Input validation helps prevent potential injection attacks
- All external communications use HTTPS
- Error details are logged safely without exposing sensitive data

## Project Structure

- `main.py`: Main script containing the WeatherAPI class and utility functions
- `test_api.py`: Unit tests for all components
- `.env.example`: Template for environment variables
- `.gitignore`: Configured to ignore .env file and other sensitive/unnecessary files
- `requirements.txt`: List of Python package dependencies
