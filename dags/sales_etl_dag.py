# Python
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from operators.check_sales_table_operator import CheckSalesTableOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

with DAG(
    dag_id='sales_etl',
    default_args=default_args,
    schedule_interval='@hourly',  # 每小時執行一次
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    sales_etl_start = DummyOperator(
        task_id='sales_etl_start'
    )

    check_and_create_table = CheckSalesTableOperator(
        task_id='check_and_create_table',
        schema_name='retail',
        table_name='sales',
        conn_id='postgresql'
    )


    sales_etl_end = DummyOperator(
        task_id='sales_etl_end'
    )

    sales_etl_start >> check_and_create_table >> sales_etl_end