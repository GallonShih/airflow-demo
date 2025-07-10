from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from services.sales_data_service import SalesDataService


class GenerateFakeSalesDataOperator(BaseOperator):
    def __init__(self, num_records: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_records = num_records

    def execute(self, context):
        self.log.info(f"Generating {self.num_records} fake sales records")
        
        # Pull connection ID from XCom
        conn_id = context['ti'].xcom_pull(task_ids='check_and_create_table', key='pg_conn_id')
        if not conn_id:
            raise ValueError("Postgres connection ID not found in XCom. Ensure the previous task pushes the connection ID.")
        
        # Use PostgresHook to establish connection
        hook = PostgresHook(postgres_conn_id=conn_id)
        pg_engine = hook.get_sqlalchemy_engine()
        sales_data_service = SalesDataService(pg_engine=pg_engine)

        try:
            sales_data_service.generate_fake_sales_data(num_records=self.num_records)
            self.log.info(f"Successfully generated and inserted {self.num_records} fake sales records")
        except Exception as e:
            self.log.error(f"An error occurred while generating fake sales data: {e}")
            raise