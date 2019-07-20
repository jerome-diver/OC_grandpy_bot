"""View point file"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)


@app.route('/')
@app.route('/index/')
def index():
    """At start time, should call an index.html page"""

    return render_template('index.html')

