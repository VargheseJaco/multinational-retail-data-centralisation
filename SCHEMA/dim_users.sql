-- Casting datatypes of dim_users
SELECT MAX(LENGTH(CAST(country_code AS TEXT)))
FROM dim_users; --longest entry is 2 characters

UPDATE dim_users
SET country_code = REPLACE(country_code, 'GGB', 'GB');

ALTER TABLE dim_users
	ALTER COLUMN first_name TYPE VARCHAR(225),
	ALTER COLUMN last_name TYPE VARCHAR(255),
	ALTER COLUMN date_of_birth TYPE DATE,
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN user_uuid TYPE UUID USING CAST(user_uuid AS UUID),
	ALTER COLUMN join_date TYPE DATE;
	
