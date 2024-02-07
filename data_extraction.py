#%%
import boto3
import json
import pandas as pd
import requests
import tabula

class DataExtractor:
    """
    A class for extracting information from databases

    Methods
    -------
    read_rds_table(engine,table_name):
        produces a pd.DataFrame from a table within a database

    """
    def read_rds_table(engine,table_name):
        """
        produces a pd.DataFrame from a table within a database

        Parameters
        ----------
        table_name : str
            name of the table to extract

        engine: SQLAlchemy engine
            an SQLAlchemy object that connects to a database

        Returns
        -------
        pd.DataFrame    

        """
        return pd.read_sql_table(table_name, engine)

    def retrieve_pdf_data(link:str):
        """
        produces a pd.DataFrame from a table within a pdf

        Parameters
        ----------
        link: str
            link to the pdf file (local or remote)
        Returns
        -------
        pd.DataFrame    

        """
        df = pd.concat(tabula.read_pdf(link, pages='all'))
        return df
    
    def list_number_of_stores(endpoint: str, header_dict: dict):
        """
        returns number of stores

        Parameters
        ----------
        endpoint: str
            link to API endpoint

        header_dict: dict
            dict of header details

        Returns
        -------
        number of stores    

        """
        response = requests.get(endpoint,
                                headers = header_dict)
        return response.json()['number_stores']

    def retrieve_stores_data(num_stores, data_endpoint: str, header_dict: dict):
        """
        returns dataframe of store info

        Parameters
        ----------
        num_stores: int
            number of stores

        data_endpoint: str
            link to API endpoint

        header_dict: dict
            dict of header details
            
        Returns
        -------
        pd.Dataframe of store info   

        """
        dataframes = []
        for number in range(num_stores):
            response = requests.get(data_endpoint.format(store_number = number),
                                    headers = header_dict)
            dataframes.append(pd.json_normalize(response.json()))
        return pd.concat(dataframes)
    
    def extract_from_s3(address):
        """
        exctracts data from S3 bucket (csv)

        Parameters
        ----------
        address: str
            address of S3 bucket
            
        Returns
        -------
        pd.Dataframe 

        """
        s3 = boto3.client("s3")

        address_split = address.split('/')[-2:]
        response = s3.get_object(Bucket=address_split[0], Key=address_split[1])

        df = pd.read_csv(response.get("Body"))
        return df        
    
    def extract_from_s3_link(link):
        """
        exctracts data from S3 bucket by link (json)

        Parameters
        ----------
        link: str
            link to S3 bucket
            
        Returns
        -------
        pd.Dataframe 

        """
        s3 = boto3.client("s3")
        
        address = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
        
        address_split = address.split('/')[-2:]
        bucket = address_split[0].split('.')[0]
        file_name = address_split[-1]

        response = s3.get_object(Bucket=bucket, Key= file_name)
        df = pd.read_json(response.get("Body"))

        return df



# %%
