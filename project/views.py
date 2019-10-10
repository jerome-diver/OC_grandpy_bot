"""View point file"""

from flask import Flask, render_template, jsonify, request, flash, Markup
from flask_assets import Environment, Bundle
from flask_bootstrap import Bootstrap

from config import GOOGLE_KEY


app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)


from project.analyzer import Analyzer

ANALYZE = Analyzer()

@app.route('/')
@app.route('/index/')
def index():
    """At start time, should call an index.html page"""

    return render_template('index.html', GOOGLE_KEY=GOOGLE_KEY)


@app.route('/question', methods=['POST'])
def question():
    """Send a question to AJAX call question.js"""

    question = request.form['question']
    alert = "alert-success"
    if question:
        ANALYZE.ask(question)
        if ANALYZE.find_something() == 1:
            flash(u"j'ai trouvé quelque chose...", alert)
            return jsonify(dict(
                question=question,
                title=ANALYZE.title,
                answer=ANALYZE.answer,
                resume=ANALYZE.resume,
                latitude=ANALYZE.latitude,
                longitude=ANALYZE.longitude,
                address=ANALYZE.address,
                messages=render_template('messages.html', alert=alert)))
        elif ANALYZE.find_something() == 2:
            flash(u'Il y a plusieurs possibilités...', alert)
        else:
            alert = "alert-warning"
            flash(u'Hélas, ma mémoire me fait défaut, je suis trop vieux !',
                  alert)
            return jsonify(dict(
                answer=False,
                messages=render_template('messages.html', alert=alert)))
    else:
        alert="alert-danger"
        flash(u'Pas de question posée', alert)
        return jsonify({
            "ERROR": "missing question",
            "messages": render_template("messages.html", alert=alert)})


@app.route('/answer', methods=['POST'])
def answer():
    """Send an answer to AJAX call answer.js"""

    return jsonify(dict(
        answer=render_template("answer.html",
                               answer=ANALYZE.answer)))


@app.route('/show_question', methods=['POST'])
def show_question():
    """Return question template to add"""

    return jsonify(dict(
        question=render_template('question.html',
                                 question=ANALYZE.question)))
