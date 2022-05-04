"""Creates interactive and non-interactive plots using preprocessed data

Creates following plots in docs/interactive-plots folder:
cases-confirmed-global.html      -  Interactive map showing gloal confirmed cases
cases-std_confirmed-global.html  -  Interactive map showing global confirmed cases
                                    standardized by population
cases-deaths-global.html         -  Interactive map showing global deaths
cases-std_deaths-global.html     -  Interactive map showing global deaths
                                    standardized by population
cases-populous.html              -  Interactive bubble map showing
                                    cases for most populous countries
cases-populous-standardized.html -  Interactive bubble map showing cases for
                                    most populous countries standardized by
                                    population

confirmed-deaths-global.html      - Interactive dual axis plot showing deaths
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

def plot_metrics(df_all):
    """Creates metrics visualization

    Args:
      df: A dataframe containing continent data
    """
    today = pd.to_datetime(df_all['Date']).iloc[-1].strftime("%d %b %Y")
    total_confirmed_cases = df_all.groupby('Date')['Confirmed'].sum()[-2:]
    total_recovered_cases = df_all.groupby('Date')['Recovered'].sum()[-2:]
    total_deaths = df_all.groupby('Date')['Deaths'].sum()[-2:]

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        title = 'Confirmed',
        mode = "number+delta",
        value = total_confirmed_cases[1],
        number = {'valueformat': '2.4s'},
        delta = {'reference':total_confirmed_cases[0],'increasing':{'color':'red'}},
        domain = {'row': 0, 'column': 0}))


    fig.add_trace(go.Indicator(
        title = 'Deaths',
        mode = "number+delta",
        value = total_deaths[1],
        number = {"valueformat": '2.03s'},
        delta = {'reference':total_deaths[0],'increasing':{'color':'red'},
                 'valueformat': '2.03s'},
        domain = {'row': 0, 'column': 2}))

    fig.update_layout(grid = {'rows': 1, 'columns': 3, 'pattern': "coupled"},
        title='<i>Last update: </i>'+today,margin=dict(l=20,r=20)
        )
    fig.write_html(os.path.join(cc.INCLUDES_DIR,"metrics.html"),
                    include_plotlyjs = False, full_html = False)


def plot_scatter_map(df,map_style='open-street-map',cases='Confirmed'):
    """Creates map to show absolute covid19 metric over time

    Args:
      df: A dataframe containing continent data
      map_style: Style of the Mapbox basemap
                 e.g. carto-positron, carto-darkmatter, stamen-terrain etc
      cases: A metric e.g. Confirmed, Deaths, Recovered,
             std_confirmed, std_deaths, std_recovered
             (std_ shows that values are per 100K of population)
    """

    fig = px.scatter_mapbox(df, lat="latitude",lon="longitude",
        animation_frame='date_', animation_group='country', color='Continent',
        hover_name='country',size=cases, size_max=50,zoom=1, height=600,
        hover_data={cases:':.3s','latitude':False,'longitude':False})
    fig.update_layout(showlegend=True, mapbox_style=map_style)
    fig.write_html(os.path.join(cc.INTERACTIVE_PLOTS_DIR,'cases-'+ cases.lower()
                    + '-global.html'),include_plotlyjs = cc.PATH_TO_PLOTLY, auto_play=False)
    fig.write_html(os.path.join(cc.INCLUDES_DIR,'cases-'+ cases.lower() + '-global.html'),
                    include_plotlyjs = False, full_html = False, auto_play=False)

def plot_bubble_countries(df, countries, start_date='2020-03-11', filename='bubble_plot_countries.html'):
    """Creates animated bubble map to show standardized covid metrics for countries

    Args:
      df: A dataframe containing continent data
      countries: A list of countries to include
      filename: Name of the output file

      start_date: A str with the start date in YYYY-MM-DD format
    """
    df_subset = subset_countries(df, countries)
    df_subset['Date'] = df_subset['Date'].astype('datetime64')
    df_subset = df_subset[(df_subset['Date']>=pd.to_datetime(start_date))]
    fig = px.scatter(df_subset, x='std_confirmed', y='population',size='std_deaths',text='country',
                 size_max=100,animation_group='country',animation_frame='date_',
                 range_y=[1,df_subset['population'].max()+1e6],range_x=[1,df_subset['std_confirmed'].max()+1e6],
                 color='country',log_x=True,log_y=True,
                 hover_data={'std_confirmed':':.2f','population':':.2f','std_deaths':':.2f'})
    fig.update_xaxes(title_text='Confirmed Cases per 100 Thousand People')
    fig.update_yaxes(title_text='Population')
    fig.update_layout(height=450)
    fig.write_html(os.path.join(cc.INTERACTIVE_PLOTS_DIR,filename),
                include_plotlyjs = cc.PATH_TO_PLOTLY, auto_play=False)
    fig.write_html(os.path.join(cc.INCLUDES_DIR,filename),
                    include_plotlyjs = False, full_html = False, auto_play=False)

def plot_3d_scatter(df,countries=None,filename='3d-scatter.html',date=None):
    """Creates 3d scatter plot to show standardized covid metrics for countries

    Args:
      df: A dataframe containing continent data
      countries: A list of countries to include
      filename: Name of the output file
      date: A str with the date in YYYY-MM-DD format
           if not given uses the latest information
    """
    if countries is not None:
        df =  subset_countries(df, countries)

    if date is None:
        date = df['Date'].iloc[-1]

    df['Date'] = pd.to_datetime(df['Date'])

    df = df[(df['Date'] == pd.to_datetime(date))]


    fig = px.scatter_3d(df, x='std_confirmed', y='std_recovered', z='std_deaths', color='Continent',
                   hover_data={'Continent':False,'country':True,'std_confirmed':':.3s',
                   'std_recovered':':.3s','std_deaths':':.3s'})
    fig.update_layout(scene = dict(
                    xaxis_title='Confirmed Cases per 100 Thousand',
                    yaxis_title='Recovered Cases per 100 Thousand',
                    zaxis_title='Deaths per 100 Thousand'),
                    margin=dict(r=20, b=10, l=10, t=10))
    fig.write_html(os.path.join(cc.INTERACTIVE_PLOTS_DIR,filename),
                include_plotlyjs = cc.PATH_TO_PLOTLY, auto_play=False)
    fig.write_html(os.path.join(cc.INCLUDES_DIR,filename),
                    include_plotlyjs = False, full_html = False, auto_play=False)


def plot_populous_countries(df):
    """Creates animated bubble map to show standardized covid metrics for
       countries with high population

    Args:
      df: A dataframe containing continent data
    """
    countries = ['China','India','US','Indonesia','Pakistan','Brazil',
                        'Nigeria','Bangladesh','Russia','Mexico']
    filename = 'cases-populous-standardized.html'
    plot_bubble_countries(df,countries, start_date='2020-04-01', filename=filename)




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
        country = 'Global'
        date = df.groupby('Date')[['Confirmed']].sum().reset_index()['Date']
        confirmed = df.groupby('Date')[['Confirmed']].sum().reset_index()['Confirmed']
        deaths = df.groupby('Date')[['Deaths']].sum().reset_index()['Deaths']
        df_country = pd.DataFrame({'Date':date,'Confirmed':confirmed,'Deaths':deaths})
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace( go.Scatter(x=df_country.Date, y=df_country['Confirmed'], name="Confirmed Cases"), secondary_y=False, )
    fig.add_trace( go.Scatter(x=df_country.Date, y=df_country['Deaths'], name="Deaths"), secondary_y=True, )

    # Set axes titles
    fig.update_xaxes(title_text="Date") #
    fig.update_yaxes(title_text="<b>Confirmed</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Deaths</b>", secondary_y=True)
    fig.write_html(os.path.join(cc.INTERACTIVE_PLOTS_DIR,"confirmed-deaths-global.html"),
                    include_plotlyjs = cc.PATH_TO_PLOTLY)
    fig.write_html(os.path.join(cc.INCLUDES_DIR,"confirmed-deaths-global.html"),
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
    plot_metrics(df_data)
    plot_deaths_confirmed(df_data)
    plot_continents(df_continents)
    plot_scatter_map(df_data)
    plot_scatter_map(df_data, map_style='carto-darkmatter', cases='std_confirmed')
    plot_populous_countries(df_data)
    plot_3d_scatter(df_data,filename='cases-today-global.html')
if __name__ == "__main__":
    main()
