from airflow.models.baseoperator import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from services.sales_data_service import SalesDataService


class UpdateHourlySalesSummaryOperator(BaseOperator):
    def __init__(self, hours_ago: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hours_ago = hours_ago

    def execute(self, context):
        self.log.info(f"Executing UpdateHourlySalesSummaryOperator")
        
        if self.hours_ago < 1:
            raise ValueError("hours_ago must be at least 1 to update hourly sales summary.")

        # Pull connection ID from XCom
        conn_id = context['ti'].xcom_pull(task_ids='check_and_create_table', key='pg_conn_id')
        if not conn_id:
            raise ValueError("Postgres connection ID not found in XCom. Ensure the previous task pushes the connection ID.")
        
        # Use PostgresHook to establish connection
        hook = PostgresHook(postgres_conn_id=conn_id)
        pg_engine = hook.get_sqlalchemy_engine()
        sales_data_service = SalesDataService(pg_engine=pg_engine)
        
        try:
            sales_data_service.update_hourly_sales_summary(hours_ago=self.hours_ago)
            self.log.info(f"Successfully updated hourly sales summary for the last {self.hours_ago} hour(s).")
        except Exception as e:
            self.log.error(f"An error occurred while updating hourly sales summary: {e}")
            raise
