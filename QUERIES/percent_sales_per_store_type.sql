-- percent of sales through type of store

SELECT 
	dim_store_details.store_type AS store_type,
	SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales,
	SUM(orders_table.product_quantity * dim_products.product_price)	/ 
	(SELECT SUM(orders_table.product_quantity * dim_products.product_price) FROM orders_table
	 	INNER JOIN dim_products ON orders_table.product_code = dim_products.product_code)*100 AS "percentage_total(%)"
FROM orders_table
	INNER JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
	INNER JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY store_type
ORDER BY total_sales DESC;