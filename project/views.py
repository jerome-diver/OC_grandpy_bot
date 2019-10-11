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
        found = ANALYZE.find_something()
        print("| found value:", found, "\n| answer:", ANALYZE.answer)
        if found == 1:
            flash(u"j'ai trouvé quelque chose...", alert)
            return jsonify(dict(
                found=1,
                question=question,
                title=ANALYZE.title,
                answer=ANALYZE.answer,
                resume=ANALYZE.resume,
                latitude=ANALYZE.latitude,
                longitude=ANALYZE.longitude,
                address=ANALYZE.address,
                messages=render_template('messages.html', alert=alert)))
        elif found == 2:
            flash(u'Il y a plusieurs possibilités...', alert)
            return jsonify(dict(
                found=2,
                question=question,
                title=ANALYZE.title,
                answer=ANALYZE.answer,
                resume=ANALYZE.resume,
                latitude=ANALYZE.latitude,
                longitude=ANALYZE.longitude,
                address=ANALYZE.address,
                messages=render_template('messages.html', alert=alert)))
        else:
            alert = "alert-warning"
            flash(u'Hélas, ma mémoire me fait défaut, je suis trop vieux !',
                  alert)
            return jsonify(dict(
                found=0,
                answer=False,
                messages=render_template('messages.html', alert=alert)))
    else:
        alert="alert-danger"
        flash(u'Pas de question posée', alert)
        return jsonify({
            "ERROR": "missing question",
            "messages": render_template("messages.html", alert=alert)})


@app.route('/bot_said', methods=['POST'])
def bot_said():
    """Send an answer to AJAX call answer.js"""

    answer = ""
    return jsonify(dict(
        answer=render_template("bot_said.html",
                               answer=ANALYZE.answer)))


@app.route('/user_said', methods=['POST'])
def user_said():
    """Return question template to add"""

    question = request.form['question']
    return jsonify(dict(
        question=render_template('user_said.html',
                                 question=question)))
