-- Casting datatypes of orders_table
SELECT MAX(LENGTH(CAST(card_number AS TEXT)))
FROM orders_table; --longest entry is 19 characters

SELECT MAX(LENGTH(CAST(store_code AS TEXT)))
FROM orders_table; --longest entry is 12 characters

SELECT MAX(LENGTH(CAST(product_code AS TEXT)))
FROM orders_table; --longest entry is 11 characters

ALTER TABLE orders_table
	DROP level_0,
	ALTER COLUMN date_uuid TYPE UUID USING CAST(date_uuid AS UUID),
	ALTER COLUMN user_uuid TYPE UUID USING CAST(user_uuid AS UUID),
	ALTER COLUMN card_number TYPE VARCHAR(19),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN product_quantity TYPE SMALLINT;
	