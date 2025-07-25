# from airflow import DAG
# from airflow.operators.dummy import DummyOperator
# from datetime import datetime, timedelta
# from operators.weather_operator import WeatherOperator
# from operators.send_discord_operator import SendDiscordOperator

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1),
# }

# with DAG(
#     dag_id='taipei_weather_dag',
#     default_args=default_args,
#     description='取得台北天氣資料並記錄到日誌中',
#     schedule_interval='@hourly',  # 每小時執行一次
#     start_date=datetime(2025, 1, 1),
#     catchup=False,
#     tags=['weather', 'taipei'],
# ) as dag:

#     weather_start_task = DummyOperator(
#         task_id='weather_start_task'
#     )

#     log_weather_task = WeatherOperator(
#         task_id='log_weather_task',
#         city_name='台北市',
#         lat=25.0478,  # 台北市緯度
#         lon=121.5319  # 台北市經度
#     )

#     send_discord_task = SendDiscordOperator(
#         task_id='send_discord_task',
#         webhook_variable_key="discord_webhook_url"
#     )

#     weather_end_task = DummyOperator(
#         task_id='weather_end_task'
#     )

#     weather_start_task >> log_weather_task >> send_discord_task >> weather_end_task
