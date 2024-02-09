-- Updating the dim_date_times table
SELECT MAX(LENGTH(CAST(month AS TEXT)))
FROM dim_date_times; --longest entry is 2 characters

SELECT MAX(LENGTH(CAST(year AS TEXT)))
FROM dim_date_times; --longest entry is 4 characters

SELECT MAX(LENGTH(CAST(day AS TEXT)))
FROM dim_date_times; --longest entry is 2 characters

SELECT MAX(LENGTH(CAST(time_period AS TEXT)))
FROM dim_date_times; --longest entry is 10 characters

ALTER TABLE dim_date_times
	ALTER COLUMN month TYPE VARCHAR(2),
	ALTER COLUMN year TYPE VARCHAR(4),
	ALTER COLUMN day TYPE VARCHAR(2),
	ALTER COLUMN time_period TYPE VARCHAR(10),
	ALTER COLUMN date_uuid TYPE UUID USING CAST(date_uuid as UUID);
	