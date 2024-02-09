-- Updating the dim_products table
ALTER TABLE dim_products 
	ADD COLUMN weight_class VARCHAR;
	
UPDATE dim_products
SET weight_class =
	CASE 
		WHEN weight < 2.0 
			THEN 'Light'
		WHEN weight >= 2 AND weight < 40 
			THEN 'Mid_Sized'
		WHEN weight >= 40 AND weight <140 
			THEN 'Heavy'
		WHEN weight >= 140 
			THEN 'Truck_Required'
	END;

SELECT MAX(LENGTH(CAST("EAN" AS TEXT)))
FROM dim_products; --longest entry is 17 characters

SELECT MAX(LENGTH(CAST(product_code AS TEXT)))
FROM dim_products; --longest entry is 11 characters

SELECT MAX(LENGTH(CAST(weight_class AS TEXT)))
FROM dim_products; --longest entry is 14 characters

ALTER TABLE dim_products 
	RENAME COLUMN removed to available;

ALTER TABLE dim_products
	DROP "Unnamed: 0";
	
ALTER TABLE dim_products
	ALTER COLUMN product_price TYPE FLOAT,
	ALTER COLUMN weight TYPE FLOAT,
	ALTER COLUMN "EAN" TYPE VARCHAR(17),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN date_added TYPE DATE,
	ALTER COLUMN uuid TYPE UUID USING CAST(uuid as UUID),
	ALTER COLUMN available TYPE BOOLEAN USING (available ='Available'),
	ALTER COLUMN weight_class TYPE VARCHAR(14);
