import pandas as pd
import plotly.graph_objects as go
import wget
import os
import time
import json
import threading
from datetime import datetime, timezone
from github import Github
import utils
from utils import timer
log = utils.getLogger(__name__)
UPDATE_TIME = 60*60
data_dir = '../data'
# state_file = data_dir + '/state.json'
reports = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
population = 'https://raw.githubusercontent.com/datasets/population/master/data/population.csv'

reports_dl = data_dir + '/countries-aggregated.csv'
population_dl = data_dir + '/population.csv'
default_countries = 'config/default_countries.csv'

data = {}


def is_newer(local_file, git_file, repo_name):

    local_file_date = datetime.fromtimestamp(os.path.getmtime(local_file), timezone.utc)

    if not 'all' in data: # Don't check Github on first load to limit API usage.
        return False

    g = Github()
    if g.get_rate_limit().core.remaining <= 0:
        log.warning("API limit exceeded", g.get_rate_limit())
        return local_file_date

    repo = g.get_repo(repo_name)
    commits = repo.get_commits(path=git_file, since=local_file_date)

    log.info(commits.totalCount)
    if commits.totalCount:
        return commits[0].commit.committer.date
    return False


# Download data files locally to speed up loading.
def download_data_files():
    new_data = False
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        wget.download(population, population_dl)
        new_data = True
    try:
        commit_date = is_newer(reports_dl, "data/countries-aggregated.csv","datasets/covid-19")
    except FileNotFoundError:
        commit_date = datetime(2020,1,1)
    if commit_date:
        log.info("Downloading new data file")
        try:
            os.remove(reports_dl)
        except FileNotFoundError:
            log.info("No old file to remove")
        wget.download(reports, reports_dl)
        data['commit_date'] = commit_date
        new_data = True

    return new_data


def get_reports():
    df = pd.read_csv(reports_dl)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


# We are only interested in the last day of data
@timer
def get_last_report(reports_df):
    last_date = max(reports_df['Date'])

    last = reports_df[reports_df['Date'] == last_date]
    last = last.drop(labels='Date', axis=1)
    last.set_index('Country', inplace=True)
    return last, last_date


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


def load_data():
    reports_df = get_reports()
    last_df, last_date = get_last_report(reports_df)

    data['all'] = reports_df
    # log.debug(reports_df.memory_usage())
    data['last_date'] = last_date
    data['last_day'] = last_df
    data['default_countries'] = get_default_countries(last_df)


def update_data():
    log.info("update_data()")

    if download_data_files() or (not 'all' in data):
        load_data()

    threading.Timer(UPDATE_TIME, update_data).start()


def init():
    # load_config()
    update_data()
    data['commit_date'] = "n/a"

'''
def load_config():
    try:
        with open(state_file, 'r') as f:
            data['state'] = json.load(f)
    except FileNotFoundError:
        data['state'] = {}


def save_config():
    with open(state_file, 'w') as f:
        json.dump(data['state'], f)

'''





