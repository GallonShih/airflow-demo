import requests
import logging

class WeatherService:
    """
    Weather service class for handling weather-related logic.
    """
    def __init__(self, lat: float, lon: float):
        self.url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        self.lat = lat
        self.lon = lon
        self.headers = {
            "User-Agent": "airflow-weather-dag"
        }
        self.logger = logging.getLogger(__name__)

    def fetch_weather(self):
        """
        Fetch weather data from Met.no API.
        :return: Current temperature (°C)
        :raises: Exception if the request fails or no valid data is found
        """
        params = {
            "lat": self.lat,
            "lon": self.lon
        }

        try:
            self.logger.info(f"Starting to fetch weather data from Met.no API, coordinates: lat={self.lat}, lon={self.lon}")
            response = requests.get(self.url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Extract current temperature
            timeseries = data.get("properties", {}).get("timeseries", [])
            if timeseries:
                current_weather = timeseries[0]  # Data for the first time point
                temperature = current_weather.get("data", {}).get("instant", {}).get("details", {}).get("air_temperature")
                self.logger.info(f"Successfully fetched weather data, current temperature: {temperature}°C")
                return temperature
            else:
                self.logger.warning("No valid weather data found.")
                raise Exception("No valid weather data found.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch weather data, error: {e}")
            raise Exception(f"Failed to fetch weather data: {e}")