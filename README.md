# Secure Data Fetching API

This is a Python project by Nkunja Denis as a test for Senior Python Developer role at Shift Security. 
It contains a python script that securely fetches weather data from the OpenWeatherMap API, processes it, and displays the results as well as unit tests for the same.


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

2. Create a virtual environment :
   ```
   python -m venv venv
   source venv/bin/activate  # On unix platforms
   venv\Scripts\activate     # On Windows
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
or
python main.py
```

The script will:
1. Prompt you to enter a city name
2. Fetch the current weather data for that city
3. Display the weather information in a readable format
4. Save the data to a JSON file

## Files Created
After Running the script, these files will be created in your project folder
- `weather_data.json`: contains the current weather data for the city entered
- `app.log`: contains any error messages and logs from the application

## Running Tests

Run the unit tests with:

```
python -m unittest test_api.py
```


Thank you