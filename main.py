#%%
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning
from data_extraction import DataExtractor

#%%
# Extracting, cleaning and uploading user details

engine = DatabaseConnector.init_db_engine('db_creds.yaml')
table_names = DatabaseConnector.list_db_tables(engine)

user_data = DataExtractor.read_rds_table(engine,table_names[1])

user_date_dict = {'date_of_birth': '%Y-%m-%d',
                    'join_date': '%Y-%m-%d'}
user_data_cleaned = DataCleaning(user_data).clean_user_data(user_date_dict,
                                                            email_column='email_address',
                                                            phone_no_column='phone_number')

user_local_engine = DatabaseConnector.init_db_engine('db_creds_local.yaml')
DatabaseConnector.upload_to_db(user_data_cleaned,'dim_users',user_local_engine)

#%%
# Extracting, cleaning and uploading card details

card_details_link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
card_data = DataExtractor.retrieve_pdf_data(card_details_link)

card_date_dict = {'date_payment_confirmed': '%Y-%m-%d'}
card_data_cleaned = DataCleaning(card_data).clean_card_data(to_date_dict=card_date_dict)

card_local_engine = DatabaseConnector.init_db_engine('db_creds_local.yaml')
DatabaseConnector.upload_to_db(card_data_cleaned,'dim_card_details',card_local_engine)
# %%
# Extracting, cleaning and uploading store details

header_dict = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
num_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'

num_stores = DataExtractor.list_number_of_stores(num_stores_endpoint, header_dict)
store_data = DataExtractor.retrieve_stores_data(num_stores, store_endpoint, header_dict)

store_date_dict = {'opening_date': '%Y-%m-%d'}
numeric_list=['latitude', 'longitude', 'staff_numbers']
store_data_cleaned = DataCleaning(store_data).clean_store_data(to_date_dict=store_date_dict,
                                                               to_numeric_list=numeric_list)

store_local_engine = DatabaseConnector.init_db_engine('db_creds_local.yaml')
DatabaseConnector.upload_to_db(store_data_cleaned,'dim_store_details',store_local_engine)
# %%
# Extracting, cleaning and uploading product details

address = 's3://data-handling-public/products.csv'

product_data = DataExtractor.extract_from_s3(address)
product_data.dropna(subset=['weight'], inplace =True)

known_units = ['kg','ml','oz','L','l','g','lb']
units = DataCleaning(product_data).find_units('weight', known_units)
print(units)

product_date_dict = {'date_added': '%Y-%m-%d'}


product_data_cleaned = DataCleaning(product_data).clean_product_data(to_date_dict=product_date_dict,
                                                                     weight_column='weight',
                                                                     price_column= 'product_price')

product_local_engine = DatabaseConnector.init_db_engine('db_creds_local.yaml')
DatabaseConnector.upload_to_db(product_data_cleaned,'dim_products',product_local_engine)
# %%
# Extracting, cleaning and uploading order details

engine = DatabaseConnector.init_db_engine('db_creds.yaml')
table_names = DatabaseConnector.list_db_tables(engine)

order_data = DataExtractor.read_rds_table(engine,table_names[2])

drop_columns = ['level_0', 'first_name', 'last_name', '1']
order_data_cleaned = DataCleaning(order_data).clean_order_data(drop_columns)

order_local_engine = DatabaseConnector.init_db_engine('db_creds_local.yaml')
DatabaseConnector.upload_to_db(order_data_cleaned,'orders_table',order_local_engine)
# %%
# Extracting, cleaning and uploading date details
address = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'

date_data = DataExtractor.extract_from_s3_link(address)

date_date_dict = {'timestamp': '%H:%M:%S'}
date_to_num_list = ['month', 'year', 'day']

date_data_cleaned = DataCleaning(date_data).clean_date_data(num_cols = date_to_num_list,
                                                            to_date_dict = date_date_dict)
date_data_cleaned['month'] = date_data_cleaned['month'].astype('int64')

date_local_engine = DatabaseConnector.init_db_engine('db_creds_local.yaml')
DatabaseConnector.upload_to_db(date_data_cleaned,'dim_date_times',date_local_engine)
# %%
