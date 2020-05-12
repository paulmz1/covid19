import pandas as pd
import utils
from utils import timer
from objects import Countries
# We are only interested in the last day of data
# @timer
columns = ['Confirmed', 'Closed', 'Recovered', 'Deaths', 'Active']

def get_last_day(reports_df):
    last_date = max(reports_df['Date'])

    last_day = reports_df[reports_df['Date'] == last_date]
    last_day = last_day.drop(labels='Date', axis=1)
    last_day.set_index('Country', inplace=True)
    return last_day, last_date


def get_country(all_days, name):
    reports_df = all_days
    df = reports_df[reports_df['Country'].isin([name])].copy()
    return df

def add_population_index(df, population):
    return pd.merge(df, population, how='inner', left_index=True, right_on='Alias')

@timer
def add_population(df, population):
    return pd.merge(df, population, how='inner', left_on='Country', right_on='Alias')




def add_calculated_columns(df_:pd.DataFrame):
    df = df_.copy()
    df['Closed'] = df['Recovered'] + df['Deaths']
    df['Active'] = df['Confirmed'] - df['Closed']
    return df

@timer
def add_calculated_for_population_columns(df_:pd.DataFrame):
    df = df_.copy()
    for column in columns:
        df[f'{column}_PM'] = (df[column].to_numpy() / df['Population'].to_numpy()) * 1000000

        # exp = f'{column}_PM = ({column} / Population) * 1000000'
        # df.eval(exp, inplace=True)

    return df

@timer
def by_population(df:pd.DataFrame):

    df = add_calculated_for_population_columns(df)
    df.drop(columns, axis=1, inplace=True)
    df.rename(columns={f'{c}_PM': c for c in columns}, inplace=True)
    return df

def get_countries_by_ids(countries: Countries, country_ids: str) -> pd.DataFrame:
    ids = utils.to_list(country_ids)
    return countries.last_day.iloc[ids]  # last_df[last_day.index.isin(df_def_countries['Country'])]


def get_countries_by_name(countries: Countries, selected_countries: pd.DataFrame) -> pd.DataFrame:
    all_days = countries.all_days
    return all_days[all_days['Country'].isin(selected_countries.index)]




if __name__ == '__main__':
    pass


