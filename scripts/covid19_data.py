"""Preprocesses Time Series data into simpler forms for downstream analytics tasks

Creates following files in csse_covid_19_data folder:
covid-all.csv  - Contains countrywise time series data with confirmed cases, recovered cases and
                 deaths standardized by population
aggregate.json - Contains total confirmed cases, recovered cases and deaths globally
continents.csv - Contains time series data per continent
"""

import os
import errno
import numpy as np
import pandas as pd
import pycountry_convert as pc
import covid19_paths as cc


__author__ = "Umair Cheema"
__license__ = "GPL"


def preprocess_data(remove_cruise=True):
    """Preprocesses covid-19 data.
    Args:
      remove_cruise: Removes the cruise specific data from January/February
    Returns:
      A dataframe with preprocesses data

    Raises:
      FileNotFoundError: If John Hopkins COVID-19 data is not available
    """


    #Check if data is available
    if not os.path.isdir(cc.DATA_DIR):
        raise FileNotFoundError(errno.ENOENT,
                                os.strerror(errno.ENOENT), cc.DATA_DIR)

    #Read population and iso code data
    df_pop = pd.read_csv(os.path.join(cc.DATA_DIR, 'UID_ISO_FIPS_LookUp_Table.csv'))
    df_pop = df_pop[df_pop['Province_State'].isnull()]
    df_pop = pd.DataFrame({'iso3':df_pop.iso3, 'country':df_pop.Combined_Key, 'latitude':df_pop.Lat,
                           'longitude':df_pop.Long_, 'population':df_pop.Population})

    df_confirmed = pd.read_csv(os.path.join(cc.DATA_DIR, 'csse_covid_19_time_series',
                                            'time_series_covid19_confirmed_global.csv'))
    df_cured = pd.read_csv(os.path.join(cc.DATA_DIR, 'csse_covid_19_time_series',
                                        'time_series_covid19_recovered_global.csv'))
    df_deaths = pd.read_csv(os.path.join(cc.DATA_DIR, 'csse_covid_19_time_series',
                                         'time_series_covid19_deaths_global.csv'))


    df_confirmed.drop(columns=['Province/State'], inplace=True)
    df_confirmed = df_confirmed.melt(id_vars=['Country/Region', 'Lat', 'Long'], var_name='Date',
                                     value_name='Confirmed')

    df_cured.drop(columns=['Province/State'], inplace=True)
    df_cured = df_cured.melt(id_vars=['Country/Region', 'Lat', 'Long'], var_name='Date',
                             value_name='Recovered')

    df_deaths.drop(columns=['Province/State'], inplace=True)
    df_deaths = df_deaths.melt(id_vars=['Country/Region', 'Lat', 'Long'], var_name='Date',
                               value_name='Deaths')

    df_all = pd.merge(pd.merge(df_confirmed, df_cured, on=['Country/Region', 'Date', 'Lat', 'Long'],
                               how='outer'),
                      df_deaths, on=['Country/Region', 'Date', 'Lat', 'Long'],
                      how='outer')

    def get_continents(country):
        country = country.strip()
        continent = 'None'

        cruises = ['Diamond Princess', 'MS Zaandam']
        africa = ['Congo (Brazzaville)', 'Congo (Kinshasa)', 'Cote d\'Ivoire', 'Western Sahara']
        asia = ['Korea, South', 'Taiwan*', 'Timor-Leste', 'West Bank and Gaza', 'Burma']
        europe = ['Holy See', 'Kosovo']
        north_america = ['US']


        if country in africa:
            continent = 'AF'
        elif country in cruises:
            continent = 'Cruise'
        elif country in europe:
            continent = 'EU'
        elif country in asia:
            continent = 'AS'
        elif country in north_america:
            continent = 'NA'
        else:
            continent = pc.country_alpha2_to_continent_code(
                                pc.country_name_to_country_alpha2(country,
                                        cn_name_format="default"))
        if continent != 'Cruise':
            continent = pc.convert_continent_code_to_continent_name(continent)
        return continent


    df_all['Continent'] = df_all['Country/Region'].apply(get_continents)
    df_all = df_all.fillna(0)
    df_all['Date'] = pd.to_datetime(df_all.Date)
    df_all['date_'] = pd.to_datetime(df_all.Date).dt.date.values.astype('str')
    #Remove Cruise data if required
    if(remove_cruise):
        cruise_indices = df_all[ df_all['Continent'] == 'Cruise' ].index
        df_all.drop(cruise_indices , inplace=True)
    #Remove negative values
    df_all['Confirmed'].mask(df_all['Confirmed'] < 0, 0, inplace=True)
    df_all['Recovered'].mask(df_all['Recovered'] < 0, 0, inplace=True)
    df_all['Deaths'].mask(df_all['Deaths'] < 0, 0, inplace=True)
    df_all = df_all.sort_values(['Date','Continent', 'Country/Region'])
    df_all = df_all.drop(columns=['Lat','Long'])
    df_all = df_all.merge(df_pop, left_on='Country/Region', right_on='country')
    df_all = df_all.drop(columns=['Country/Region'])
    df_all = df_all.fillna(0)
    df_all['std_confirmed'] = (df_all['Confirmed']/df_all['population'])*1e5
    df_all['std_recovered'] = (df_all['Recovered']/df_all['population'])*1e5
    df_all['std_deaths'] = (df_all['Deaths']/df_all['population'])*1e5
    df_all = df_all.replace([np.inf, -np.inf], np.nan)
    df_all = df_all.fillna(0)

    return df_all


def get_continent_data(df_all, item='Confirmed'):
    """Groups covid data by continent

    Args:
      df_all: A dataframe containing all data
      item: Confirmed, Recovered or Deaths

    Returns:
      A dataframe with the continent data
    """

    df_grouped = df_all.groupby(['Date','Continent'])[[item]].sum()
    df_grouped = df_grouped[item].unstack()
    
    return df_grouped


def get_countries_data(df_all, item='Confirmed'):
    """Groups covid data by country

    Args:
      df_all: A dataframe containing all data
      item: Confirmed, Recovered or Deaths

    Returns:
      A dataframe with the country data
    """
    df_countries = df_all.groupby(['Date','country'])[['Confirmed','Recovered','Deaths']].sum()
    return df_countries[item].unstack()


def get_countries_breakup(df_all):
    """Groups covid data by countries and saves in csv

    Args:
      df_all: A dataframe containing all data
    """
    confirmed = (get_countries_data(df_all).reset_index()
                 .set_index('Date'))
    recovered = (get_countries_data(df_all, 'Recovered').reset_index()
        .set_index('Date'))
    deaths = (get_countries_data(df_all, 'Deaths').reset_index()
        .set_index('Date'))

    df_countries = pd.concat([confirmed, recovered, deaths], axis=1)
    df_countries.to_csv(os.path.join(cc.DATA_DIR,'countries.csv'))

def get_aggregate(df_all):
    """Computes total recovered, confirmed and deaths for covid

    Args:
      df_all: A dataframe containing all the data
    """
    df_all['datetime'] = pd.to_datetime(df_all['Date'])
    today = df_all['datetime'].iloc[-1].strftime("%d %b %Y")
    total_confirmed_cases = df_all.groupby('Date')['Confirmed'].sum()[-1]
    total_recovered_cases = df_all.groupby('Date')['Recovered'].sum()[-1]
    total_deaths = df_all.groupby('Date')['Deaths'].sum()[-1]
    df_aggregate = pd.DataFrame({'date':[today],'total_confirmed':[total_confirmed_cases],
                         'total_recovered':[total_recovered_cases],'total_deaths':[total_deaths]})
    return df_aggregate

def main():
    df_data = preprocess_data()
    df_data.to_csv(os.path.join(cc.DATA_DIR, 'covid-all.csv'))
    df_aggregate = get_aggregate(df_data)
    df_aggregate.to_json(os.path.join(cc.DATA_DIR,'aggregate.json'), orient='records')
    df_continents = get_continent_data(df_data)
    df_continents.to_csv(os.path.join(cc.DATA_DIR,'continents.csv'))
if __name__ == "__main__":
    main()
