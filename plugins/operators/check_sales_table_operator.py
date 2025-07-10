from airflow.models.baseoperator import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


class CheckSalesTableOperator(BaseOperator):
    def __init__(self, conn_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id

    def execute(self, context):
        self.log.info(f"Executing CheckSalesTableOperator")

        hook = PostgresHook(postgres_conn_id=self.conn_id)
        # Check if schema exists, create if not
        hook.run(f"CREATE SCHEMA IF NOT EXISTS retail;")
        self.log.info(f"Schema retail checked/created.")

        # Check if table exists, create if not
        hook.run(f"""
        CREATE TABLE IF NOT EXISTS retail.sales (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            product VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            total_amount NUMERIC NOT NULL,
            transaction_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
        );
        """)
        self.log.info(f"Table retail.sales checked/created.")

        hook.run(f"""
        CREATE TABLE IF NOT EXISTS retail.hourly_sales_summary (
            date DATE NOT NULL,
            hour INT NOT NULL,
            total_sales NUMERIC NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            PRIMARY KEY (date, hour)
        );
        """)
        self.log.info(f"Table retail.hourly_sales_summary checked/created.")

        # Push connection ID to XCom
        context['ti'].xcom_push(key='pg_conn_id', value=self.conn_id)
        self.log.info("Postgres connection ID pushed to XCom.")