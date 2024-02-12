-- online vs offline purchases
SELECT *
FROM orders_table
WHERE store_code LIKE 'WEB%';

SELECT 
	COUNT(orders_table.product_quantity) AS total_sales,
	SUM(orders_table.product_quantity) AS product_quantity_count,
	CASE 
		WHEN orders_table.store_code LIKE 'WEB%' THEMN 'Web'
		ELSE 'Offline'
	END AS location
FROM orders_table
	INNER JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY location
ORDER BY product_quantity_count;

SELECT *
FROM dim_store_details
WHERE store_code LIKE 'WEB%';
