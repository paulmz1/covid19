import pandas as pd
import wget
import os
import threading
from datetime import datetime, timezone
from github import Github
import utils

import calculations as calc

import charts
from objects import Countries
from utils import timer

log = utils.getLogger(__name__)
UPDATE_TIME = 20*60
data_dir = '../data'
# state_file = data_dir + '/state.json'
reports_url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
population_url = 'https://raw.githubusercontent.com/datasets/population/master/data/population.csv'

reports_dl = data_dir + '/countries-aggregated.csv'
countries_url = 'config/countries.csv'
default_countries_url = 'config/default_countries.csv'

countries = Countries()


def is_newer(local_file, git_file, repo_name):

    local_file_date = datetime.fromtimestamp(os.path.getmtime(local_file), timezone.utc)

    if not countries.loaded: # Don't check Github on first load to limit API usage.
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
        wget.download(reports_url, reports_dl)
        countries.commit_date = commit_date
        new_data = True

    return new_data


def get_reports():
    df = pd.read_csv(reports_dl)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def get_population():
    df = pd.read_csv(countries_url)
    df.set_index('Country', inplace=True)
    return df


def get_default_countries(last_df):
    df_def_countries = pd.read_csv(default_countries_url)
    idx = [i for i, country in enumerate(last_df.index) if country in df_def_countries['Country'].tolist()]
    return idx


def load_data():
    reports_df = get_reports()
    reports_last_day, last_date = calc.get_last_day(reports_df)
    population = get_population()
    countries.load(reports_df, reports_last_day, last_date,  get_default_countries(reports_last_day), population)


def update_data():
    log.info("update_data()")

    if download_data_files() or not countries.loaded:
        load_data()

    threading.Timer(UPDATE_TIME, update_data).start()


def countries_calculated():
    return calc.add_calculated_for_population_columns(
        calc.add_calculated_columns(
            calc.add_population_index(countries.last_day, countries.population)))


def country_chart(name):
    country = calc.get_country(countries.all_days, name)
    return charts.country_chart(calc.add_calculated_columns(country))


def countries_last_day_chart(countries_ids: str, per_million) -> str:
    df = calc.get_countries_by_ids(countries, countries_ids)
    df = calc.add_calculated_columns(df)
    if per_million:
        df = calc.add_population_index(df, countries.population)
        df = calc.by_population(df)
    return charts.country_last_day_chart(df)


'''
def countries_chart(countries_ids, per_million):
    # @timer
    def calculate():
        selected_countries = calc.get_countries_by_ids(countries, countries_ids)
        selected_country_data = calc.get_countries_by_name(countries, selected_countries)
        if per_million:
            selected_country_data = calc.add_population(selected_country_data, countries.population)
            selected_country_data = calc.by_population(selected_country_data)
        return calc.add_calculated_columns(selected_country_data), selected_countries
    return charts.countries_charts(*calculate())
'''

@timer
def countries_chart_csv(countries_ids, column, per_million):

    selected_countries = calc.get_countries_by_ids(countries, countries_ids)
    selected_country_data = calc.get_countries_by_name(countries, selected_countries)
    selected_country_data = calc.add_calculated_columns(selected_country_data)
    if per_million:
        selected_country_data = calc.add_population(selected_country_data, countries.population)
        selected_country_data = calc.by_population(selected_country_data)

    return selected_country_data.pivot(index='Date', columns='Country', values=column).to_csv()


def init():
    # load_config()
    update_data()


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


