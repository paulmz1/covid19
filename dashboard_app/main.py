from flask import Flask, request, render_template
from waitress import serve
import data
import json
import plotly

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data=data.data)


@app.route('/country')
def country():
    name = request.args.get('name')

    graphJSON = json.dumps(data.country_chart(name), cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('country.html', graphJSON=graphJSON, name=name)


if __name__ == '__main__':
    data.init()
    serve(app, host="0.0.0.0", port=8080)