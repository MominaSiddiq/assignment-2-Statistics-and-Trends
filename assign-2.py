#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:14:45 2023

@author: macbook
"""

import pandas as pd
#import matplotlib.pyplot as plt

def read_data(filename, skip):
    """
    This function reads data into a pandas dataframe take transpose and 
    clean the data.

    Parameters
    ----------
    filename : csv
       take the filenames as an argument.

    Returns
    -------
    two dataframes.

    """
    # read the data from the file
    data = pd.read_csv(filename, skiprows = skip)
    
    # cleaning the data(removing empty rows etc.)
    data.dropna(axis = 0, how = 'all', inplace = True)
    data.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'], inplace=True)
    
    print(data)
    
    # taking the transpose
    transposed_data = data.T
    
    # setting the header 
    transposed_data.columns = transposed_data.iloc[0]
    transposed_data = transposed_data[1:]
    
    
    # reset index for making years as columns
    transposed_data = transposed_data.reset_index()
    transposed_data = transposed_data.rename(columns={'index': 'Year'})
    
    # setting years as index
    transposed_data.set_index('Year', inplace = True)
    
    # removing empty rows
    transposed_data.dropna(axis = 0, how = 'all', inplace = True)
    
    # Removeing any unnecessary columns in the transpose of data
    transposed_data = transposed_data.loc[:, ~transposed_data.columns.duplicated()]

    # Removing any duplicated rows
    transposed_data = transposed_data[~transposed_data.index.duplicated(keep='first')]
    
    #seperate DataFrame fro countries as columns
    countries_columns = transposed_data.T
    
    print(transposed_data)
    print(countries_columns)
    
    return transposed_data, countries_columns
   

    
def main():
    """
    A main function calling other functions.

    Returns
    -------
    None.

    """
    
    # giving the filename path of data
    UBP_file = "/Users/macbook/Desktop/assignment-2-Statistics-and-Trends/urban_population.csv"
    
    read_data(UBP_file, 4)
    
    
if __name__ == "__main__":
    main()
    
    
