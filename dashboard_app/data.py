import pandas as pd
import plotly.graph_objects as go
import wget
import os
# https://datatables.net/
reports = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
population = 'https://raw.githubusercontent.com/datasets/population/master/data/population.csv'
reports_dl = 'data/countries-aggregated.csv'
population_dl = 'data/population.csv'
default_countries = 'config/default_countries.csv'
data_dir = 'data'

data = {}

# Download data files locally to speed up loading.
def download_data_files():
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        wget.download(reports, reports_dl)
        wget.download(population, population_dl)


def get_reports():
    df = pd.read_csv(reports_dl)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


# We are only interested in the last day of data
def get_last_report(reports_df):
    last_date = max(reports_df['Date'])

    last = reports_df[reports_df['Date'] == last_date]
    last = last.drop(labels='Date', axis=1)
    last.set_index('Country', inplace=True)
    return last


def get_default_countries(last_df):
    df_def_countries = pd.read_csv(default_countries)
    idx = [i for i, country in enumerate(last_df.index) if country in df_def_countries['Country'].tolist()]

    # idx = last_df[last_df.index.isin(df_def_countries['Country'])].index
    return idx


def get_country(name):
    reports_df = data['all']
    df = reports_df[reports_df['Country'].isin([name])].copy()

    df['Closed'] = df['Recovered'] + df['Deaths']
    df['Active'] = df['Confirmed'] - df['Closed']

    return df


def country_chart(name):
    df = get_country(name)
    traces = []

    def add_trace(column, color, fill=None):
        traces.append(go.Scatter(x=df['Date'], y=df[column], name=column, fill=fill, mode='lines', line_color=color))

    add_trace('Confirmed', 'blue')
    add_trace('Closed', 'indigo', 'tonexty')
    add_trace('Recovered', 'green')
    add_trace('Deaths', 'red')
    add_trace('Active', 'orange')

    return traces


def init():

    download_data_files()
    reports_df = get_reports()
    last_df = get_last_report(reports_df)
    data['all'] = reports_df
    data['last_date'] = last_df
    data['default_countries'] = get_default_countries(last_df)


