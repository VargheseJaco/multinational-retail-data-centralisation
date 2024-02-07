#%%
from pathlib import Path
import pandas as pd
import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
import psycopg2

class DatabaseConnector:
    """
    A class for conecting to databases.

    Methods
    -------
    read_db_creds(creds_path):
        reads credentials from a yaml file

    init_db_engine(creds_path,dbtype='postgresql',dbapi='psycopg2'):
        initialises a connection engine 

    list_db_tables(engine):
       returns the names of all tables in connected database

    upload_to_db(df : pd.DataFrame,name,engine):
        uploads a pd.DataFrame to a database
    """
    def read_db_creds(creds_path):
        """
        reads database credentials from a yaml file to a dictionary

        Parameters
        ----------
        creds_path : str
            name of the yaml file containing the credentials

        Returns
        -------
        dictionary of credentials
        """
        credentials_dict = yaml.safe_load(Path(creds_path).read_text())

        return credentials_dict
    
    def init_db_engine(creds_path,dbtype='postgresql',dbapi='psycopg2'):
        """
        Initialises the engine attribute to connect to a database

        Parameters
        ----------
        creds_path : str
            name of the yaml file containing the credentials

        dbtype : str
            type of database (default is postgresql)

        dbapi : str
            API used for connection

        Returns
        -------
        an SQLAlchemy engine
        """
        credentials = DatabaseConnector.read_db_creds(creds_path)
        engine = create_engine(f"{dbtype}+{dbapi}://{credentials['USER']}:{credentials['PASSWORD']}@{credentials['HOST']}:{credentials['PORT']}/{credentials['DATABASE']}")

        return engine
    
    def list_db_tables(engine):
        """
        lists tables within a connected database

        Parameters
        ----------
        engine: SQLAlchemy engine
            an SQLAlchemy object that connects to a database

        Returns
        -------
        list of table names
        """
        inspector = inspect(engine)
        return inspector.get_table_names()
    
    def upload_to_db(df : pd.DataFrame,name,engine):
        """
        uploads a pd.DataFrame to a database

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to upload

        name : str
            name of the table once uploaded

        engine: SQLAlchemy engine
            an SQLAlchemy object that connects to a database

        """
        df.to_sql(name, engine, if_exists='replace')
    
