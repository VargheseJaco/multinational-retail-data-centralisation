#%%
import numpy as np
import pandas as pd
import re

class DataCleaning:
    """
    A class for cleaning data.

    Attributes
    -----------
    df : pd.DataFrame

    Methods
    -------
    fix_date(self,columns: list):
        converts dates to standard format and drops invalid/null dates

    fix_email(self, email_column):
        drops email addresses which are incorrectly formatted

    fix_phone_no(self, phone_no_column):
        drops phone numbers which are incorrectly formatted

    clean_user_data(self, to_date_list: list, email_column, phone_no_column)
        cleans the user_data table with the specified methods

    nan_count(self):
        shows how many null entries are in each columns 
    """
    def __init__(self,dataframe: pd.DataFrame):
        """
        Initialises the object

        Parameters
        ----------
        dataframe: pd.DataFrame
            the dataframe to clean
        """
        self.df = dataframe
    
    def nan_count(self):
        """
        shows how many null values are in each column of a DataFrame

        Returns
        -------
        pd.Series
        """
        return self.df.isnull().sum()
    
    def to_numeric(self,columns: list):
        """
        Converts the datatype of selected columns to numeric

        Parameters
        ----------
        columns : list
            list of columns to convert to numeric

        Returns
        -------
        a Pandas dataframe
        """
        df = self.df.copy(deep=True)
        for i in columns:
            df[i] = pd.to_numeric(df[i], errors = 'coerce')
            df.dropna(subset = [i],inplace=True)
        return df
    
    def fix_date(self,columns: dict):
        """
        removes rows with invalid dates

        Parameters
        ----------
        columns: list
            list of columns with dates to clean

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        for i in columns:
            df[i] = pd.to_datetime(df[i], format=columns[i], errors = 'coerce')
            df.dropna(subset = [i],inplace=True)
        return df
    
    def fix_email(self, email_column):
        """
        removes rows with invalid emails

        Parameters
        ----------
        email_column:
            column with emails to clean

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for i, email in enumerate(df[email_column]):
            if not re.match(pattern, email):
                df.loc[i,email_column] = np.nan
        df = df.dropna(subset=[email_column])
        return df
    
    def fix_phone_no(self, phone_no_column):
        """
        removes rows with invalid phone numbers

        Parameters
        ----------
        phone_no_column:
            column with phone numbers to clean

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        pattern = r"(\+1)?\s?\(?(2\d{2}|[3-9]\d{2})\)?[\s.-]?\d{3}[\s.-]?\d{4}"
        for i, phone_no in enumerate(df[phone_no_column]):
            if re.match(pattern, phone_no):
                df.loc[i,phone_no_column] = np.nan
        df = df.dropna(subset=[phone_no_column])
        return df

    def clean_user_data(self, to_date_list: list, email_column, phone_no_column):
        """
        cleans user data using class methods

        Parameters
        ----------
        to_date_list: list
            list of columns with dates to clean

        email_column:
            column with emails to clean

        phone_no_column:
            column with phone numbers to clean
        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning dates...')
        df = DataCleaning(df).fix_date(to_date_list)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning email addresses...')
        df = DataCleaning(df).fix_email(email_column)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning phone numbers...')
        df = DataCleaning(df).fix_phone_no(phone_no_column)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        return df
    
    def clean_card_data(self,to_date_dict):
        """
        cleans card data using class methods

        Parameters
        ----------
        to_date_list: list
            list of columns with dates to clean

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning dates...')
        df = DataCleaning(df).fix_date(to_date_dict)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        return df
    
    def clean_store_data(self,to_date_dict,to_numeric_list):
        """
        cleans card data using class methods

        Parameters
        ----------
        to_date_list: list
            list of columns with dates to clean
        
        to_numeric_list: list
            list of columns with numbers to clean
        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning dates...')
        df = DataCleaning(df).fix_date(to_date_dict)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        numeric_str = str(to_numeric_list).strip("[]")
        print(f'Cleaning: {numeric_str}')
        df = DataCleaning(df).to_numeric(to_numeric_list)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nDropping lat column') 
        df = df.drop(columns=['lat'])
        return df

    def find_units(self, weight_column, known_units):
        """
        finds units of values in a column e.g. weight

        Parameters
        ----------
        weight_column: str
            column to search for units
        
        known_units: list
            list of units that are likely to be present e.g. kg

        Returns
        -------
        list of units
        """
        df = self.df.copy(deep=True)
        letters= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 
        units = []

        for weight in df[weight_column].unique():
            unit = ''
            for char in weight:
                if char in letters:
                    unit += char
            if unit in known_units:
                units.append(unit)

        units = list(set(units))
        return units

    def contains_x(self,value):
        """
        handles entries with a multiplier e.g. 12 x 100g becomes 1200

        Parameters
        ----------
        value:
            value to check for 'x'
        Returns
        -------
        value(corrected)
        """
        if 'x' in value:
            value.replace(' ','')
            factors = value.split('x')
            return str(float(factors[0])*float(factors[1]))
        else:
            return value
    
    def to_kilo(self,value:str):
        """
        converts weight values to float

        Parameters
        ----------
        value:
            value to convert
        Returns
        -------
        value
        """
        if value.endswith('kg'):
            value = value.replace('kg', '')
            value = self.contains_x(value)
            value = float(value)
        elif value.endswith('ml'):
            value = value.replace('ml', '')
            value = self.contains_x(value)
            value = float(value)/1000
        elif value.endswith('g'):
            value = value.replace('g', '')
            value = self.contains_x(value)
            value = float(value)/1000
        elif value.endswith('lb'):
            value = value.replace('lb', '')
            value = self.contains_x(value)
            value = float(value)*0.453592
        elif value.endswith('oz'):
            value = value.replace('oz', '')
            value = self.contains_x(value)
            value = float(value)*0.0283495
        else:
            value = np.nan
        return value
    
    def convert_product_weights(self,weight_column):
        """
        applies to_kilo and contains_x to clean the weights column

        Parameters
        ----------
        weight_column:
            name of column to transform

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        df[weight_column] = df[weight_column].apply(self.to_kilo)
        df = df.dropna(subset=weight_column)
        return df
    
    def convert_price(self,price_column):
        """
        removes £ from price and turns into float

        Parameters
        ----------
        price_column:
            name of column to transform
        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        df[price_column] = df[price_column].apply(str)
        df[price_column] = df[price_column].str.replace('£','')
        df[price_column] = pd.to_numeric(df[price_column], errors = 'coerce')
        return df
    
    def clean_product_data(self,to_date_dict,weight_column,price_column):
        """
        cleans product data

        Parameters
        ----------
        weight_column:
            name of weight column to transform

        price_column:
            name of price column to transform
        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning dates...')
        df = DataCleaning(df).fix_date(to_date_dict)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning weights...')
        df = DataCleaning(df).convert_product_weights(weight_column)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nCleaning prices') 
        df = DataCleaning(df).convert_price(price_column)
        print(f'NUMBER OF ROWS REMAINING: {len(df)}')
        print('\nReplacing "Still_avaliable" in removed column with "Available')
        df['removed'] = df['removed'].map({'Still_avaliable':'Available', 'Removed':'Removed'})
        return df
    
    def clean_order_data(self,cols_to_drop):
        """
        cleans order data

        Parameters
        ----------
        cols_to_drop: list
            list of columns to drop

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        df = df.drop(columns=cols_to_drop)
        return df
    
    def clean_date_data(self, num_cols, to_date_dict):
        """
        cleans date data

        Parameters
        ----------
        cols_to_drop: list
            list of columns to drop

        Returns
        -------
        pd.DataFrame
        """
        df = self.df.copy(deep=True)
        df = DataCleaning(df).to_numeric(num_cols)
        df= DataCleaning(df).fix_date(to_date_dict)
        df = df.dropna(how='any')
        return df