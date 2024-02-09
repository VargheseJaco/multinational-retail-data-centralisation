-- Updating the dim_card_details table
SELECT MAX(LENGTH(CAST(card_number AS TEXT)))
FROM dim_card_details; --longest entry is 22 characters

UPDATE dim_card_details
SET card_number = REPLACE(card_number, '?', '');

SELECT MAX(LENGTH(CAST(card_number AS TEXT)))
FROM dim_card_details; --longest entry is 19 characters

SELECT MAX(LENGTH(CAST(expiry_date AS TEXT)))
FROM dim_card_details; --longest entry is 5 characters

ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(19),
	ALTER COLUMN expiry_date TYPE VARCHAR(5),
	ALTER COLUMN date_payment_confirmed TYPE DATE;
