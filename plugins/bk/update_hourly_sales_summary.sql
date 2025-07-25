INSERT INTO retail.hourly_sales_summary (date, hour, total_sales)
SELECT 
    DATE(transaction_time) AS date,
    EXTRACT(HOUR FROM transaction_time) AS hour,
    SUM(total_amount) AS total_sales
FROM retail.sales
WHERE transaction_time >= NOW() - INTERVAL '__HOURS_AGO__ HOURS'
GROUP BY date, hour
ON CONFLICT (date, hour) 
DO UPDATE SET total_sales = EXCLUDED.total_sales
WHERE hourly_sales_summary.total_sales <> EXCLUDED.total_sales