import random
import logging
from datetime import datetime, timedelta


class SalesDataService:
    def __init__(self, pg_engine):
        self.pg_engine = pg_engine
        self.logger = logging.getLogger(__name__)

    def generate_fake_sales_data(self, num_records=10):
        try:
            self.logger.info(f"Starting to generate {num_records} fake sales records for retail.sales")
            with self.pg_engine.connect() as con:
            # Generate fake sales data
                products = ["Product A", "Product B", "Product C", "Product D"]
                sales_data = []
                for _ in range(num_records):
                    user_id = random.randint(1, 100)
                    product = random.choice(products)
                    quantity = random.randint(1, 10)
                    price = random.randint(10, 100)
                    total_amount = int(quantity * price)
                    transaction_time = (datetime.now() - timedelta(days=random.randint(0, 30))).astimezone()
                    sales_data.append((user_id, product, quantity, total_amount, transaction_time))
                    self.logger.debug(f"Generated record: user_id={user_id}, product={product}, quantity={quantity}, total_amount={total_amount}, transaction_time={transaction_time}")

                # Insert data into the table
                insert_query = f"""
                    INSERT INTO retail.sales (user_id, product, quantity, total_amount, transaction_time)
                    VALUES (%s, %s, %s, %s, %s)
                """
                try:
                    con.execute(insert_query, sales_data)
                    self.logger.info(f"Successfully inserted {num_records} records into retail.sales")
                except Exception as e:
                    self.logger.error(f"Failed to insert records into retail.sales: {e}")
                    raise
        except Exception as e:
            self.logger.error(f"An error occurred while generating or inserting sales data: {e}")
            raise