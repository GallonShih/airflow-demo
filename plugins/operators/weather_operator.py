from airflow.models.baseoperator import BaseOperator
from services.weather_service import WeatherService

class WeatherOperator(BaseOperator):
    """
    Custom Operator for fetching weather data.
    """
    def __init__(self, city_name: str, lat: float, lon: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_name = city_name
        self.lat = lat
        self.lon = lon

    def execute(self, context):
        """
        Execution logic for the Operator.
        """
        self.log.info(f"Fetching weather data for {self.city_name} (lat: {self.lat}, lon: {self.lon})")
        weather_service = WeatherService(lat=self.lat, lon=self.lon)

        try:
            temperature = weather_service.fetch_weather()
            if temperature is None:
                error_message = f"Weather data for {self.city_name} could not be fetched. Temperature is None."
                self.log.error(error_message)
                raise ValueError(error_message)

            msg = f"Current temperature in {self.city_name}: {temperature}°C"
            self.log.info(msg)

            # Push temperature to XCom for downstream tasks
            context['ti'].xcom_push(key='temperature_msg', value=msg)
            self.log.info("temperature_msg pushed to XCom.")

        except Exception as e:
            error_message = f"An error occurred while fetching weather data for {self.city_name}: {e}"
            self.log.exception(error_message)  # Use log.exception to include traceback
            raise