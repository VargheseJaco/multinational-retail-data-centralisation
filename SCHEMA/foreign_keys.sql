-- Filling values that arent present

INSERT INTO dim_card_details (card_number)
SELECT DISTINCT orders_table.card_number
FROM orders_table
WHERE orders_table.card_number NOT IN 
	(SELECT dim_card_details.card_number
	FROM dim_card_details);

INSERT INTO dim_products (product_code)
SELECT DISTINCT orders_table.product_code
FROM orders_table
WHERE orders_table.product_code NOT IN 
	(SELECT dim_products.product_code
	FROM dim_products);

INSERT INTO dim_store_details (store_code)
SELECT DISTINCT orders_table.store_code
FROM orders_table
WHERE orders_table.store_code NOT IN 
	(SELECT dim_store_details.store_code
	FROM dim_store_details);
	
INSERT INTO dim_users (user_uuid)
SELECT DISTINCT orders_table.user_uuid
FROM orders_table
WHERE orders_table.user_uuid NOT IN 
	(SELECT dim_users.user_uuid
	FROM dim_users);

-- Setting foreign keys

ALTER TABLE orders_table
	ADD FOREIGN KEY (card_number)
	REFERENCES dim_card_details(card_number);
	
ALTER TABLE orders_table
	ADD FOREIGN KEY (date_uuid)
	REFERENCES dim_date_times(date_uuid);
	
ALTER TABLE orders_table
	ADD FOREIGN KEY (product_code)
	REFERENCES dim_products(product_code);
	
ALTER TABLE orders_table
	ADD FOREIGN KEY (store_code)
	REFERENCES dim_store_details(store_code);
	
ALTER TABLE orders_table
	ADD FOREIGN KEY (user_uuid)
	REFERENCES dim_users(user_uuid);