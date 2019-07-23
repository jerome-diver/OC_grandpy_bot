"""View point file"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from jac.contrib.flask import JAC
from flask import jsonify, request


app = Flask(__name__)
app.config.from_object('config')
app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_OUTPUT_DIR'] = './static/css'
app.config['COMPRESSOR_STATIC_PREFIX'] = '/project/static/css'
jac = JAC(app)
Bootstrap(app)


@app.route('/')
@app.route('/index/')
def index():
    """At start time, should call an index.html page"""

    return render_template('index.html')

@app.route('/question', method=['POST'])
def question():

    question = request.form['question']
    if question:
        return jsonify({'question': question})
    else:
        return jsonify({"ERROR": "missing question"})
