"""Creates interactive and non-interactive plots using preprocessed data

Creates following plots in docs/interactive-plots folder:
cases-all-confirmed.html         -  Interactive map showing gloal confirmed cases
cases-all-confirmed-standardized - Interactive map showing global confirmed cases
                                   standardized by population
cases-all-deaths.html            -  Interactive map showing global deaths
cases-all-deaths-standardized    - Interactive map showing global deaths
                                   standardized by population
cases-populous.html              - Interactive bubble map showing
                                   cases for most populous countries
cases-populous-standardized.html - Interactive bubble map showing cases for
                                   most populous countries standardized by
                                   population

confirmed-deaths-world.html      - Interactive dual axis plot showing deaths
                                   and confirmed cases
"""
import os
import errno
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

__author__ = "Umair Cheema"
__license__ = "GPL"

DATA_DIR = '../csse_covid_19_data'
PLOTS_DIR = '../docs/plots'
INTERACTIVE_PLOTS_DIR = '../docs/interactive_plots'

def load_data():
    """Loads data as dataframes

    Returns:
       Dataframes with preprocessed data for countries and continents

    Raises:
      FileNotFoundError: If preprocessed data is not available
    """
    #Set up file paths
    country_data_path = os.path.join(DATA_DIR,'covid-all.csv')
    continents_data_path = os.path.join(DATA_DIR,'continents.csv')
    #Check if data is available
    if not os.path.isfile(country_data_path):
        raise FileNotFoundError(errno.ENOENT,
                                os.strerror(errno.ENOENT), DATA_DIR + '/' + 'covid-all.csv')

    #Read preprocessed data
    df_all = pd.read_csv(country_data_path)
    df_continents = pd.read_csv(continents_data_path)
    return df_all, df_continents


def plot_deaths_confirmed(df,country = None):
    """Creates dual axis line chart to show deaths and confirmed cases

    Args:
      df: A dataframe containing all data
      country: Name of the country - By default shows global data in plot

    """
    df['datetime'] = pd.to_datetime(df['Date'])
    today = df['datetime'].iloc[-1].strftime("%d %b %Y")
    if (country):
        df_country = df[df['country']== country]
    else:
        country = 'World'
        date = df.groupby('Date')[['Confirmed']].sum().reset_index()['Date']
        confirmed = df.groupby('Date')[['Confirmed']].sum().reset_index()['Confirmed']
        deaths = df.groupby('Date')[['Deaths']].sum().reset_index()['Deaths']
        df_country = pd.DataFrame({'Date':date,'Confirmed':confirmed,'Deaths':deaths})
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace( go.Scatter(x=df_country.Date, y=df_country['Confirmed'], name="Confirmed Cases"), secondary_y=False, )
    fig.add_trace( go.Scatter(x=df_country.Date, y=df_country['Deaths'], name="Deaths"), secondary_y=True, )
    # Add figure title
    fig.update_layout( title_text=country+"(COVID-19) - "+today )
    # Set x-axis title
    fig.update_xaxes(title_text="Date") # Set y-axes titles
    fig.update_yaxes(title_text="<b>Confirmed</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Deaths</b>", secondary_y=True)
    fig.write_html(os.path.join(INTERACTIVE_PLOTS_DIR,"confirmed-deaths-world.html"))


def get_continent_breakup(df_all):
    """Groups covid data by continent and saves in csv

    Args:
      df_all: A dataframe containing all data
    """

    confirmed = get_continent_data(df_all).reset_index().set_index('Date')
    recovered = get_continent_data(df_all, 'Recovered').reset_index().set_index('Date')
    deaths = get_continent_data(df_all, 'Deaths').reset_index().set_index('Date')
    df_continents = pd.concat([confirmed, recovered, deaths], axis=1)
    df_continents.to_csv(os.path.join(DATA_DIR,'continents.csv'))


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
    df_countries.to_csv(os.path.join(DATA_DIR,'countries.csv'))


def main():
    df_data, df_continents = load_data()
    plot_deaths_confirmed(df_data)


if __name__ == "__main__":
    main()
