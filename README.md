# Secure Data Fetching Script

A Python script that securely fetches weather data from the OpenWeatherMap API, processes it, and displays the results.

By Nkunja Denis as a test for Senior Developer role

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

## Running

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
