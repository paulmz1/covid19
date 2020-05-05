from flask import Flask, request, render_template
from waitress import serve
from flask_compress import Compress
import data

import utils
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
    return render_template('countries_last_day.html', graphJSON=chart)


@app.route('/countries')
def countries():
    countries_ids = request.args.get('countries')
    chart = data.countries_chart(countries_ids)
    return render_template('countries.html', graphJSON=chart)

if __name__ == '__main__':
    utils.init_logger()
    log.info("Starting App")
    data.init()
    Compress(app)
    serve(app, host="0.0.0.0", port=8080)