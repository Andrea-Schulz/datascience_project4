# This module contains custom functions functions for data wrangling

import pandas as pd

def remove_column_substr(df, substr):
    '''
    remove substring from a column name in a pandas dataframe
    :param df: pandas dataframe
    :param substr: substring to remove
    :return: pandas dataframe with new column names
    '''
    df.columns = df.columns.str.replace(substr, '')
    return df