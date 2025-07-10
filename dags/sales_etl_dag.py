# Python
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from operators.check_sales_table_operator import CheckSalesTableOperator
from operators.generate_fake_sales_data_operator import GenerateFakeSalesDataOperator
from operators.update_hourly_sales_summary_operator import UpdateHourlySalesSummaryOperator

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
    tags=["etl", "sales"],
) as dag:

    sales_etl_start = DummyOperator(
        task_id='sales_etl_start'
    )

    check_and_create_table = CheckSalesTableOperator(
        task_id='check_and_create_table',
        conn_id='postgresql'
    )

    generate_fake_sales_data = GenerateFakeSalesDataOperator(
        task_id='generate_fake_sales_data',
        num_records=100
    )

    update_hourly_sales_summary = UpdateHourlySalesSummaryOperator(
        task_id='update_hourly_sales_summary',
        hours_ago=2
    )

    sales_etl_end = DummyOperator(
        task_id='sales_etl_end'
    )

    sales_etl_start >> check_and_create_table >> generate_fake_sales_data >> update_hourly_sales_summary >> sales_etl_end