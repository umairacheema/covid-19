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
import covid19_paths as cc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

__author__ = "Umair Cheema"
__license__ = "GPL"


def load_data():
    """Loads data as dataframes

    Returns:
       Dataframes with preprocessed data for countries and continents

    Raises:
      FileNotFoundError: If preprocessed data is not available
    """
    #Set up file paths
    country_data_path = os.path.join(cc.DATA_DIR,'covid-all.csv')
    continents_data_path = os.path.join(cc.DATA_DIR,'continents.csv')
    #Check if data is available
    if not os.path.isfile(country_data_path):
        raise FileNotFoundError(errno.ENOENT,
                                os.strerror(errno.ENOENT), cc.DATA_DIR + '/' + 'covid-all.csv')

    #Read preprocessed data
    df_all = pd.read_csv(country_data_path)
    df_continents = pd.read_csv(continents_data_path)
    return df_all, df_continents

def plot_continents(df, cases='Confirmed'):
    """Creates line chart to show continent trend

    Args:
      df: A dataframe containing continent data
      cases: Confirmed, Deaths or Recovered
    """

    columns = df.columns
    fig = go.Figure()
    for column in columns:
        if(column not in ['Date','datetime']):
            fig.add_trace(go.Scatter(x=df.Date, y=df[column], name=column, mode='lines+markers'))

    fig.update_layout(xaxis_title='Date', yaxis_title=cases, title='COVID19 Continent Trend')
    fig.write_html(os.path.join(cc.INTERACTIVE_PLOTS_DIR, cases.lower() + "-continents.html"),
                    include_plotlyjs = cc.PATH_TO_PLOTLY)
    fig.write_html(os.path.join(cc.INCLUDES_DIR,cases.lower() + "-continents.html"),
                    include_plotlyjs = False, full_html = False)

def plot_deaths_confirmed(df,country = None):
    """Creates dual axis line chart to show deaths and confirmed cases

    Args:
      df: A dataframe containing all data
      country: Name of the country - By default shows global data in plot

    """
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
    fig.update_layout( title_text=country )
    # Set x-axis title
    fig.update_xaxes(title_text="Date") # Set y-axes titles
    fig.update_yaxes(title_text="<b>Confirmed</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Deaths</b>", secondary_y=True)
    fig.write_html(os.path.join(cc.INTERACTIVE_PLOTS_DIR,"confirmed-deaths-world.html"),
                    include_plotlyjs = cc.PATH_TO_PLOTLY)
    fig.write_html(os.path.join(cc.INCLUDES_DIR,"confirmed-deaths-world.html"),
                    include_plotlyjs = False, full_html = False)

def subset_countries(df, countries):
    """Returns filtered data based on the list of countries

    Args:
      df: A dataframe containing all data
      countries: List containing countries for data inclusion
    Returns:
       Dataframe with data for selected countries
    """
    subset = df
    if(countries != None):
        mask = df['country'].isin(countries)
        subset = df.loc[mask]
    return subset



def main():
    df_data, df_continents = load_data()
    plot_deaths_confirmed(df_data)
    plot_continents(df_continents)

if __name__ == "__main__":
    main()
