# Multinational Retail Data Centralisation

## Description:
Key technologies used: Postgres, AWS (s3), boto3, rest-API, csv, Python (Pandas).

As part of a multinational company's initiative to become more data-driven, there's a need to consolidate sales data from various sources into one centralized location. The task is to develop a system that stores all sales data in a single database, serving as the primary source of truth. This centralized approach enables easy access and analysis of up-to-date metrics for informed decision-making and optimization of business processes.

## File Structure:
- **data_cleaning.py**: Python script containing the DataCleaning class
- **data_extraction.py**: Python script containing the DataExtraction class
- **database_utils.pu**: Python script containing the DatabaseConnector class
- **main.py**: Main script that extracts, cleans and uploads the data to a central source
- **SCHEMA**: folder containing all SQL scripts to produce the star-based schema

- **QUERIES**: folder containing all SQL scripts to extract relevant information from the database

## Python Classes:
- **DataExtractor**: A class for extracting data from various sources
- **DataCleaning**: A class for cleaning extracted data
- **DatabaseConnector**: A class for connecting to databases

## Schema Structure (star-based):
Identified within SCHEMA/primary_keys.sql and SCHEMA/foreign_keys.sql: orders_table is the single source of truth with a key link to each dimension table.





