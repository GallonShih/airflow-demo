from airflow.models.baseoperator import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


class CheckSalesTableOperator(BaseOperator):
    def __init__(self, schema_name: str, table_name: str, conn_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_name = schema_name
        self.table_name = table_name
        self.conn_id = conn_id

    def execute(self, context):
        self.log.info(f"Executing CheckSalesTableOperator")

        hook = PostgresHook(postgres_conn_id=self.conn_id)
        # Check if schema exists, create if not
        hook.run(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name};")
        self.log.info(f"Schema {self.schema_name} checked/created.")

        # Check if table exists, create if not
        hook.run(f"""
        CREATE TABLE IF NOT EXISTS {self.schema_name}.{self.table_name} (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            product VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            total_amount NUMERIC NOT NULL,
            transaction_time TIMESTAMP NOT NULL
        );
        """)
        self.log.info(f"Table {self.schema_name}.{self.table_name} checked/created.")