from flask import Flask, request, render_template
from waitress import serve
from dashboard_app import data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data=data.data)

if __name__ == '__main__':
    data.init()
    serve(app, host="0.0.0.0", port=8080)