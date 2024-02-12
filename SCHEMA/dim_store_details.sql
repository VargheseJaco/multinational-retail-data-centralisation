-- Updating the dim_store_details table
SELECT MAX(LENGTH(CAST(store_code AS TEXT)))
FROM dim_store_details; --longest entry is 12 characters

SELECT MAX(LENGTH(CAST(country_code AS TEXT)))
FROM dim_store_details; --longest entry is 2 characters

ALTER TABLE dim_store_details
	DROP level_0;
	
ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT,
	ALTER COLUMN locality TYPE VARCHAR(255),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN staff_numbers TYPE SMALLINT,
	ALTER COLUMN opening_date TYPE DATE,
	ALTER COLUMN store_type TYPE VARCHAR(255),
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN continent TYPE VARCHAR(255);

SELECT * FROM dim_store_details;