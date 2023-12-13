#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:14:45 2023

@author: macbook
"""

import pandas as pd
import stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# giving the filenames path of choosen indicators
elec_access = "electricity_access.csv"
elec_power = "electric_power.csv"
energy_use = "energy_use.csv"
co2_emission = "CO2_emission.csv"

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
    data = pd.read_csv(filename, skiprows = 4, index_col = False)

    # cleaning the data(removing empty rows etc.)
    data.dropna(axis = 0, how = 'all', inplace = True)

    # remove emty columns
    data.dropna(axis = 1, how = 'all', inplace = True)

    # Drop the unnecessary columns in the data
    data.drop(columns = ['Country Code', 'Indicator Name',
              'Indicator Code'], inplace = True)
    country_col_df = data

    print(country_col_df)
    print("=" * 50)

    # taking the transpose
    years_col_df = data.T

    # setting the header
    years_col_df.columns = years_col_df.iloc[0]
    years_col_df = years_col_df[1:]

    # reset index for making years as columns
    years_col_df = years_col_df.reset_index()
    years_col_df = years_col_df.rename(columns = {'index': 'Year'})

    # setting years as index
    years_col_df.set_index('Year', inplace = True)

    # removing empty rows
    years_col_df.dropna(axis = 0, how = 'all', inplace = True)

    # removing empty columns
    years_col_df.dropna(axis = 1, how = 'all', inplace = True)

    # Removeing any unnecessary columns in the transpose of data
    years_col_df = years_col_df.loc[:, ~years_col_df.columns.duplicated()]

    # Removing any duplicated rows
    years_col_df = years_col_df[~years_col_df.index.duplicated(keep='first')]

    print(years_col_df)
    print("=" * 50)

    return country_col_df, years_col_df


# Using a groupby() method to group the desired data
def groupby_selected_data(dataframes):
    """
    This function grouped the desired data of each indicators 

    Parameters
    ----------
    dataframes : python dataframe
        dataframes of each indicators.

    Returns
    -------
    grouped data: python dataframes.

    """

    # Iterate through each indicator dataframe and perform groupby
    for indicator_name, df in dataframes.items():
        # Filter the dataframe based on selected countries and years
        filtered_df = df.loc[selected_years, selected_countries]

        # Perform groupby operation on the filtered_df
        # Grouping by country name and finding mean
        grouped_data = filtered_df.groupby(level = 0, axis = 1).mean()

        # Display the grouped data
        print(f"Grouped {indicator_name} data for selected countries:")
        print(grouped_data)
        print("=" * 50)

    return grouped_data


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
    data : pandas dataframe
        world bank data of different indicators.
    title : str
        title of different line-plot graphs.    

    Returns
    -------
    None.

    """

    # Filter the data for selective countries and years 2000 to 2014
    filtered_data = data.loc[data['Country Name'].isin(selected_countries)]
    filtered_data = filtered_data.set_index(
        'Country Name').loc[:, str(start_year) : str(end_year)]

    # line-plot
    plt.figure(figsize = (10, 8))

    for country in selected_countries:
        plt.plot(filtered_data.columns,
                 filtered_data.loc[country], label = country)

    plt.xlabel('Years', fontsize = 16)
    plt.title(title, fontsize = 16)
    plt.legend(title = 'Countries', bbox_to_anchor = (
        1.05, 1), loc = 'upper left', fontsize = 'large')
    plt.show()


def bar_plot(data, title):
    """
    plots a bar plot on different data sets for selective countries and years.

    Parameters
    ----------
    data : pandas dataframe
        world bank data of different indicators.
    title : str
        title of different bar-plot graphs.

    Returns
    -------
    None.

    """

    # Filter the data for selective countries and years
    filtered_data = data[data['Country Name'].isin(selected_countries)][[
        'Country Name'] + selected_years]
    filtered_data.set_index('Country Name', inplace = True)

    # Bar plot
    plt.figure(figsize = (10, 8))

   # x-axis ticks for the countries
    x = range(len(selected_countries))
    bar_width = 0.1  # Width of each bar

    for i, year in enumerate(selected_years):
        plt.bar([pos + i * bar_width for pos in x], filtered_data[year],
                width = bar_width, label = year, edgecolor = 'black')

    plt.xlabel('Countries', fontsize = 16)
    plt.title(title, fontsize = 16)
    plt.xticks([pos + (len(selected_years) - 1) * bar_width /
               2 for pos in x], selected_countries, rotation = 45, ha = 'right')
    plt.legend(loc = 'upper left', fontsize = 'large')
    plt.show()


def heat_map(indicators, country_name):
    """
    generate a heat map for different countries to show the correlation between indicators

    Parameters
    ----------
    indicators : pandas dataframes
        world bank data of different indicators.
    country_name : str
        Name of the country on which heat map construct
        
    Returns
    -------
    None.

    """
    # Fetching data for the specified country from each indicator
    country_data = {}
    for indicator, df in indicators.items():
        country_df = df[df['Country Name'] == country_name].T
        country_df.columns = [indicator]
        country_data[indicator] = country_df.loc[str(
            start_year) : str(end_year)]

    # Combine data for all indicators
    country_combined_data = pd.concat(country_data.values(), axis = 1)
    print(country_combined_data)

    # calculating the correlation
    corr_data = country_combined_data.corr()
    print(corr_data)
    print("=" * 50)

    # Plotting the correlogram heatmap
    plt.figure(figsize = (10, 8))
    sns.heatmap(corr_data, annot = True, cmap = 'cubehelix',
                square = True, center = 0, vmax = 1, vmin = -1)
    plt.title(f'{country_name}', fontsize = 16)
    plt.show()


def main():
    """
    A main function calling other functions.

    Returns
    -------
    None.

    """
    # Callig the read function and saving each dataframes into variables
    elec_access_data, elec_access_trans = read_data(elec_access)
    elp_consume_data, elp_consume_trans = read_data(elec_power)
    energy_use_data, energy_use_trans = read_data(energy_use)
    co2_emission_data, co2_emission_trans = read_data(co2_emission)

    # selecting countries
    global selected_countries
    selected_countries = ['Qatar', 'China', 'United Kingdom', 'Pakistan',
        'Netherlands', 'Portugal', 'United States', 'South Asia', 'Bangladesh',
        'South Africa', 'Zimbabwe']

    # Selecting years
    global selected_years
    selected_years = [str(year) for year in range(start_year, end_year + 1, 2)]

    # Creating a list of all the transformed dataframes
    trans_dataframes = {
        "Electricity_access": elec_access_trans,
        "Electricity_consume": elp_consume_trans,
        "Energy_use": energy_use_trans,
        "CO2_emission": co2_emission_trans,
    }

    # Creating a list of all the original dataframes
    org_dataframes = {
        "Electricity_access": elec_access_data,
        "Electricity_consume": elp_consume_data,
        "Energy_use": energy_use_data,
        "CO2_emission": co2_emission_data,
    }

    # Calling the function to group selected data of all the indicators
    selected_data = groupby_selected_data(trans_dataframes)

    # Iterate through each dataframe to obtain the results of each method and store in dictionaries
    summary_resullts = {}
    stats_results = {}

    for name, df in trans_dataframes.items():

        # Giving the variable numeric values to apply metjods on it as it is an object
        selected_data = selected_data.apply(pd.to_numeric, errors = 'coerce')

        # Calling the function for obtaining summary of each indicators
        summary_of_data = summary_statistics(selected_data)
        summary_resullts[name] = {"Summary": summary_of_data}

        # Calling the function to get the skewness and kurtosis
        skewness, kurtosis = stats_methods(selected_data)
        stats_results[name] = {"Skewness": skewness, "Kurtosis": kurtosis}

    # Printing the results of each indicator:
    for name, values in summary_resullts.items():
        print(f"{name} Summary: {values['Summary']}")
        print("=" * 50)

    for name, values in stats_results.items():
        print(f"{name} Skewness: {values['Skewness']}")
        print("=" * 50)
        print(f"{name} Kurtosis: {values['Kurtosis']}")
        print("=" * 50)

    # titles for the plots
    epc_title = "Electric Power Consumption (KWh per capita)"
    ela_title = "Access to Electricity (% of population)"
    egu_title = "Overall Energy Use (Kg)"
    co2_title = "CO2 Emission (kt)"

    # calling the function for line-plots and passing arguments
    line_plot(elp_consume_data, epc_title)
    line_plot(elec_access_data, ela_title)
    line_plot(energy_use_data, egu_title)
    line_plot(co2_emission_data, co2_title)

    # calling the function for bar plots and passing arguments
    bar_plot(energy_use_data, egu_title)
    bar_plot(co2_emission_data, co2_title)
    bar_plot(elp_consume_data, epc_title)

    # Calling the function for generating heat map
    heat_map(org_dataframes, "Qatar")
    heat_map(org_dataframes, "South Africa")
    heat_map(org_dataframes, "Zimbabwe")


if __name__ == "__main__":
    main()
