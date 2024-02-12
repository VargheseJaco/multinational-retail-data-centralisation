-- time taken for sales

WITH time_table(hour, minutes, seconds, day, month, year, date_uuid) AS (
	SELECT 
		EXTRACT(hour FROM timestamp) as hour,
		EXTRACT(minute FROM timestamp) as minute,
		EXTRACT(second FROM timestamp) AS seconds,
		day,
		month,
		year,
		date_uuid
	FROM dim_date_times),
	
	timestamps(timestamp, date_uuid, year) AS(
		SELECT MAKE_TIMESTAMP(CAST(time_table.year AS int), CAST(time_table.month AS int),
							  CAST(time_table.day AS int), CAST(time_table.hour AS int),	
							  CAST(time_table.minutes AS int), CAST(time_table.seconds AS int)) AS order_timestamp,
			time_table.date_uuid AS date_uuid, 
			time_table.year AS year
		FROM time_table),
	
	time_stamp_diffs(year, time_diff) AS (
		SELECT timestamps.year, timestamps.timestamp - LEAD(timestamps.timestamp) OVER (ORDER BY timestamps.timestamp DESC) AS time_diff
		FROM timestamps),

	year_diffs(year, average_diff) AS (
		SELECT year, AVG(time_diff) AS average_diff
		FROM time_stamp_diffs
		GROUP BY year
		ORDER BY average_diff DESC)
		
SELECT 
	year, 
	CONCAT('hours: ', EXTRACT(HOUR FROM average_diff),
					'  minutes: ', EXTRACT(MINUTE FROM average_diff),
				   '  seconds: ', ROUND(EXTRACT(SECOND FROM average_diff)),
				   '  milliseconds: ', ROUND(EXTRACT(MILLISECOND FROM average_diff))) AS actual_time_taken
FROM year_diffs;