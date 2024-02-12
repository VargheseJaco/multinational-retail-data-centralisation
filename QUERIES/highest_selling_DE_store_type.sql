-- highest selling german store type

SELECT 
	SUM(dim_products.product_price * product_quantity) AS total_sales,
	dim_store_details.store_type,
	MAX(dim_store_details.country_code) AS country_code
FROM orders_table
	INNER JOIN dim_store_details on orders_table.store_code = dim_store_details.store_code
	INNER JOIN dim_products on orders_table.product_code = dim_products.product_code
WHERE dim_store_details.country_code = 'DE'
GROUP BY dim_store_details.store_type
ORDER BY total_sales;