"""View point file"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_bootstrap import Bootstrap
from os import path
from jac.contrib.flask import JAC
import wikipediaapi


app = Flask(__name__)
app.config.from_object('config')
app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_OUTPUT_DIR'] = './project/static/css'
app.config['COMPRESSOR_STATIC_PREFIX'] = '/project/static/css'
jac = JAC(app)
bootstrap = Bootstrap(app)
wiki = wikipediaapi.Wikipedia(language='fr',
                              extract_format=wikipediaapi.ExtractFormat.HTML)


@app.route('/')
@app.route('/index/')
def index():
    """At start time, should call an index.html page"""

    return render_template('index.html')


@app.route('/question', methods=['POST'])
def question():

    from project.super_parser import remove_stop_words
    question = request.form['question']
    if question:
        question = remove_stop_words(question)
        print("after parsed :", question)
        answer = wiki.page(question)
        return jsonify({
            'question': question,
            'answer': answer.text })
    else:
        return jsonify({"ERROR": "missing question"})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/img/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
