INSERT INTO retail.hourly_sales_summary (date, hour, total_sales)
SELECT 
...
FROM retail.sales
WHERE transaction_time >= NOW() - INTERVAL '__HOURS_AGO__ HOURS'
...