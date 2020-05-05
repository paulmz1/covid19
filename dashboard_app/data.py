import pandas as pd
import wget
import os
import threading
from datetime import datetime, timezone
from github import Github
import utils
import calculations
import charts
from objects import Countries
from utils import timer

log = utils.getLogger(__name__)
UPDATE_TIME = 20*60
data_dir = '../data'
# state_file = data_dir + '/state.json'
reports = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
population = 'https://raw.githubusercontent.com/datasets/population/master/data/population.csv'

reports_dl = data_dir + '/countries-aggregated.csv'
population_dl = data_dir + '/population.csv'
default_countries = 'config/default_countries.csv'

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
        countries.commit_date = commit_date
        new_data = True

    return new_data


def get_reports():
    df = pd.read_csv(reports_dl)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def get_default_countries(last_df):
    df_def_countries = pd.read_csv(default_countries)
    idx = [i for i, country in enumerate(last_df.index) if country in df_def_countries['Country'].tolist()]
    return idx


def load_data():
    reports_df = get_reports()
    last_day, last_date = calculations.get_last_day(reports_df)
    countries.load(reports_df, last_day, last_date,  get_default_countries(last_day))


def update_data():
    log.info("update_data()")

    if download_data_files() or not countries.loaded:
        load_data()

    threading.Timer(UPDATE_TIME, update_data).start()


def countries_calculated():
    return calculations.add_calculated_columns(countries.last_day)


def country_chart(name):
    country = calculations.get_country(countries.all_days, name)
    return charts.country_chart(calculations.add_calculated_columns(country))


def countries_last_day_chart(countries_ids: str) -> str:
    df = calculations.get_countries_by_ids(countries, countries_ids)
    return charts.country_last_day_chart(calculations.add_calculated_columns(df))


# @timer
def countries_chart(countries_ids):
    # @timer
    def calc():
        selected_countries = calculations.get_countries_by_ids(countries, countries_ids)
        selected_country_data = calculations.get_countries_by_name(countries, selected_countries)
        return calculations.add_calculated_columns(selected_country_data), selected_countries
    return charts.countries_charts(*calc())


@timer
def countries_chart_csv(countries_ids, column):

    selected_countries = calculations.get_countries_by_ids(countries, countries_ids)
    selected_country_data = calculations.get_countries_by_name(countries, selected_countries)
    selected_country_data = calculations.add_calculated_columns(selected_country_data)

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


