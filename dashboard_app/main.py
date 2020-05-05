from flask import Flask, request, render_template
from waitress import serve
from flask_compress import Compress
import data

import utils
import logging
log = utils.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', countries=data.countries,  last_day=data.countries_calculated())


@app.route('/country')
def country():
    name = request.args.get('name')
    return render_template('country.html', graphJSON=data.country_chart(name), name=name)


@app.route('/countries_last_day')
def countries_last_day():
    countries_ids = request.args.get('countries')

    chart = data.countries_last_day_chart(countries_ids)
    return render_template('countries_last_day.html', graphJSON=chart, countries=data.countries)


@app.route('/countries')
def countries():
    countries_ids = request.args.get('countries')
    chart = data.countries_chart(countries_ids)
    return render_template('countries.html', graphJSON=chart)


@app.route('/countries_csv')
def countries_csv():
    countries_ids = request.args.get('countries')
    column = request.args.get('column')
    return data.countries_chart_csv(countries_ids, column)


@app.route('/set_debug_level')
def debug_level():
    level = request.args.get('level')

    l = logging.getLogger()
    old = logging.getLevelName(l.level)
    if level is None:
        return f'Logging level is {old}'
    level = level.upper()
    try:
        l.setLevel(level)
        return f'Logging level changed from {old} to {level}'
    except ValueError:
        return f'Unknown logging level {level}.'



if __name__ == '__main__':
    utils.init_logger()
    log.info("Starting App")
    data.init()
    Compress(app)
    serve(app, host="0.0.0.0", port=8080, threads=10)