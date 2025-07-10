from airflow.models.baseoperator import BaseOperator
from airflow.models import Variable
import requests

class SendDiscordOperator(BaseOperator):
    def __init__(self, webhook_variable_key="discord_webhook_url", **kwargs):
        super().__init__(**kwargs)
        self.webhook_variable_key = webhook_variable_key
        self.webhook_url=Variable.get(self.webhook_variable_key)

    def execute(self, context):
        # Pull connection ID from XCom
        temperature_msg = context['ti'].xcom_pull(task_ids='log_weather_task', key='temperature_msg')
        if not temperature_msg:
            raise ValueError("Temperature message not found in XCom. Ensure the WeatherOperator task has run successfully.")

        custom_msg = Variable.get("custom_message", default_var="")

        discord_msg = f"{custom_msg}\n{temperature_msg}" if custom_msg else temperature_msg
        self.log.info(f"Sending temperature message to Discord: {discord_msg}")
        payload = {"content": discord_msg}
        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code != 204 and response.status_code != 200:
                raise Exception(f"Failed to send Discord message: {response.status_code}, {response.text}")
            self.log.info("✅ Discord message sent successfully.")
        except Exception as e:
            self.log.error(f"Error sending message to Discord: {e}")
            raise
