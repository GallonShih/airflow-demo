import random
from datetime import datetime, timedelta

# Python

class SalesDataService:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def generate_fake_sales_data(self, schema_name, table_name, num_records=10):
        with self.pg_conn.connect() as con:
            # Generate fake sales data
            products = ["Product A", "Product B", "Product C", "Product D"]
            sales_data = []
            for _ in range(num_records):
                user_id = random.randint(1, 1000)
                product = random.choice(products)
                quantity = random.randint(1, 10)
                price = random.randint(10, 100)
                total_amount = int(quantity * price)
                transaction_time = datetime.now() - timedelta(days=random.randint(0, 30))
                sales_data.append((user_id, product, quantity, total_amount, transaction_time))

            # Insert data into the table
            insert_query = f"""
                INSERT INTO {schema_name}.{table_name} (user_id, product, quantity, total_amount, transaction_time)
                VALUES (%s, %s, %s, %s, %s)
            """
            con.execute(insert_query, sales_data)