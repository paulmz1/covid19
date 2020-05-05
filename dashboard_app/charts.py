import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json
columns = {'Confirmed': ['blue'], 'Closed': ['indigo', 'tonexty'], 'Recovered': ['green'], 'Deaths': ['red'], 'Active': ['orange']}


def country_last_day_chart(counties: pd.DataFrame):
    traces = []

    def add_trace(column, color, fill=None):
        traces.append(go.Bar(name=column, x=counties.index, y=counties[column], marker_color=color))

    for column, color in columns.items():
        add_trace(column, *color)

    return to_json(traces)


def countries_chart(scdata: pd.DataFrame, column) -> str:
    fig = px.line(scdata, x='Date', y=column, color='Country')
    return fig.to_json()


def countries_charts(selected_country_data: pd.DataFrame) -> dict:
    return {column: countries_chart(selected_country_data, column) for column, color in columns.items() }


def country_chart(country:pd.DataFrame) -> str:

    traces = []

    def add_trace(column, color, fill=None):
        traces.append(go.Scatter(x=country['Date'], y=country[column], name=column, fill=fill, mode='lines', line_color=color))

    for column, color in columns.items():
        add_trace(column, *color)

    return to_json(traces)


def to_json(traces) -> str:
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)
