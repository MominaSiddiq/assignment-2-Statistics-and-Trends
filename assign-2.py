#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:14:45 2023

@author: macbook
"""

import pandas as pd
import stats as stats
import matplotlib.pyplot as plt

# giving the filenames path of choosen indicators
"""
elec_access = "electricity_access.csv"
elec_power = "electric_power.csv"
energy_use = "energy_use.csv"
co2_emission = "CO2_emission.csv"
"""
filenames = {
    "electricity_access.csv" : "elec_access",
    "electric_power.csv" :  "elec_power",
    "energy_use.csv" : "energy_use",
    "CO2_emission.csv" : "co2_emission"
    }
    
# Creating global variables
selected_countries = {}
start_year = 2000
end_year = 2014
selected_years = {}
selected_data = {}


def read_data(filename):
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
    data = pd.read_csv(filename, skiprows = 4, index_col=False)
    
    
    # cleaning the data(removing empty rows etc.)
    data.dropna(axis = 0, how = 'all', inplace = True)
    
    # remove emty columns
    data.dropna(axis = 1, how = 'all', inplace = True)
    
    
    # Drop the unnecessary columns in the data 
    data.drop(columns = ['Country Code', 'Indicator Name', 'Indicator Code'], inplace=True)
    
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
    
    # removing empty columns
    transposed_data.dropna(axis = 1, how = 'all', inplace = True)
    
    # Removeing any unnecessary columns in the transpose of data
    transposed_data = transposed_data.loc[:, ~transposed_data.columns.duplicated()]

    # Removing any duplicated rows
    transposed_data = transposed_data[~transposed_data.index.duplicated(keep='first')]
   
    return data, transposed_data



# Obtaining the summary statistics of data by the describe method    
def summary_statistics(data):
    """
    applies describe method on different indicators.

    Parameters
    ----------
    data : pandas dataframe
       The numerical data to analyze

    Returns
    -------
    summary_stats
        summary of selected data.

    """
    
    summary_stats = data.describe()
    
    return summary_stats 



def stats_methods(data):
    """
    applies skewness and kurtosis methods on different indicators.

    Parameters
    ----------
    data : pandas dataframe
        The numerical data to analyze
    Returns
    -------
    skewness & kurtosis of selected data.

    """
    
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data)
    
    return skewness, kurtosis


# Visualization of data by plotting different graphs on it
def line_plot(data, title):
    """
    plots a line plot on different data sets for selective countries and years. 

    Parameters
    ----------
    data : csv
        world bank data of different indicators.
    title : str
        title of different line-plot graphs.    

    Returns
    -------
    None.

    """
   
    # Filter the data for selective countries and years 2000 to 2014
    filtered_data = data.loc[data['Country Name'].isin(selected_countries)]
    filtered_data = filtered_data.set_index('Country Name').loc[:, str(start_year) : str(end_year)]
    
    # line-plot
    plt.figure(figsize=(8, 6))
    
    for country in selected_countries: 
        plt.plot(filtered_data.columns, filtered_data.loc[country], label = country)
        
    plt.xlabel('Years')
    plt.title(title)
    plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')  
    plt.show()
    
    

def bar_plot(data, title):    
    """
    plots a bar plot on different data sets for selective countries and years.

    Parameters
    ----------
    data : csv
        world bank data of different indicators.
    title : str
        title of different line-plot graphs.

    Returns
    -------
    None.

    """
   
    # Filter the data for selective countries and years 
    filtered_data = data[data['Country Name'].isin(selected_countries)][['Country Name'] + selected_years]
    filtered_data.set_index('Country Name', inplace = True)
    
    # Bar plot
    plt.figure(figsize=(10, 6))
    
   # x-axis ticks for the countries
    x = range(len(selected_countries))  
    bar_width = 0.1  # Width of each bar
    
    for i, year in enumerate(selected_years):
        plt.bar([pos + i * bar_width for pos in x], filtered_data[year], width=bar_width, label=year, edgecolor = 'black')

        
    plt.xlabel('Countries')
    plt.title(title)
    plt.xticks([pos + (len(selected_years) - 1) * bar_width / 2 for pos in x], selected_countries, rotation = 45, ha = 'right')
    plt.legend(loc='upper left')  
    plt.show()
    
    
    
def main():
    """
    A main function calling other functions.

    Returns
    -------
    None.

    """
    """
    elec_access_data, elec_access_trans = read_data(elec_access)
    elp_consume_data, elp_consume_trans = read_data(elec_power)
    energy_use_data, energy_use_trans = read_data(energy_use)
    co2_emission_data, co2_emission_trans = read_data(co2_emission)
    """
    # Creating dictionaries for original and transposed dataframes
    country_col_df = {}
    year_col_df = {}
    
    # Iterate through dataframes and store in dictionaries
    for file, df_name in filenames.items():
        original_df, transposed_df = read_data(file)
        country_col_df[df_name] = original_df
        year_col_df[df_name] = transposed_df
        
        # Printing each dataframe and its transpose 
        print(f"Original DataFrame of '{df_name}':")
        print(original_df)
        print(f"Transposed DataFrame of '{df_name}':")
        print(transposed_df)
        
        # Saving each of them into new dataframes 
        globals()[f"{df_name}_orig"] = original_df
        globals()[f"{df_name}_trans"] = transposed_df
    
    
    # selecting countries 
    global selected_countries 
    selected_countries = ['Bangladesh', 'China', 'United Kingdom', 'Pakistan', 
                          'Netherlands', 'United States', 'Portugal', 'South Asia', 'Qatar', 
                          'South Africa', 'Zimbabwe']
    
    # Selecting years
    global selected_years
    selected_years = [str(year) for year in range(start_year , end_year + 1, 2)] 
    
    """
    # Creating a list of all the dataframes
    dataframes = {
        "Electricity_access" : elec_access_trans, 
        "Electric_power_consume" : elp_consume_trans, 
        "Energy_use" : energy_use_trans, 
        "CO2_emission" : co2_emission_trans
    }
    
    """
    # Iterate through each dataframe to obtain the results of each method and store in dictionaries
    summary_resullts = {}
    stats_results ={}
    
    for name, df in transposed_df.items():
        # Selecting the data from each dataframe
        selected_data = df.loc[selected_years, selected_countries]
        
        # Giving the variable numeric values to apply metjods on it as it is an object 
        selected_data = selected_data.apply(pd.to_numeric, errors='coerce')
        
        # Calling the function for obtaining summary of each indicators 
        summary_of_data = summary_statistics(selected_data)
        summary_resullts[name] = {"Summary" : summary_of_data}
        
        # Calling the function to get the skewness and kurtosis 
        skewness, kurtosis = stats_methods(selected_data)
        stats_results[name] = {"Skewness" : skewness, "Kurtosis" : kurtosis}
    
    # Printing the results of each indicator:
    for name, values in summary_resullts.items():
        print(f"{name} Summary: {values['Summary']}")
        print("\n")

    for name, values in stats_results.items():
       print(f"{name} Skewness: {values['Skewness']}")
       print("\n")
       print(f"{name} Kurtosis: {values['Kurtosis']}")
       print("\n")
        
    """ 
    # titles for the line plot
    epc_title = "Electric Power Consumption(KWh per capita)"
    ela_title = "Access to Electricity(% of population)"
    
    # calling the function for line-plots and passing arguments
    line_plot(elp_consume_data, epc_title)
    line_plot(elec_access_data, ela_title)
    
    # titles for the bar plot
    egu_title = "Overall Energy Use(Kg)"
    co2_title = "CO2 Emission(kt)"
    
    # calling the function for bar plots and passing arguments
    bar_plot(energy_use_data, egu_title)
    bar_plot(co2_emission_data, co2_title)
    """




if __name__ == "__main__":
    main()
    