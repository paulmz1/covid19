from flask import Flask, request, render_template
from waitress import serve
import data
import json
import plotly
import utils
log = utils.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data=data.data)


@app.route('/country')
def country():
    name = request.args.get('name')

    graphJSON = json.dumps(data.country_chart(name), cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('country.html', graphJSON=graphJSON, name=name)

@app.route('/countries_last_day')
def countries_last_day():
    countries = request.args.get('countries')
    print(countries)
    return render_template('countries_last_day.html', countries=countries)


if __name__ == '__main__':
    utils.init_logger()
    log.info("Starting App")
    data.init()
    serve(app, host="0.0.0.0", port=8080)