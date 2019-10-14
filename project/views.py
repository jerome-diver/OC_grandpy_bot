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
    type = request.form['type']
    index = int(request.form['index'])
    alert = "alert-success"
    data = dict()
    if type == "answer":
        ANALYZE.last_answer(index)
    if question:
        ANALYZE.ask(question)
        found = ANALYZE.find_something()
        print("| found value:", found, "\n| answer:", ANALYZE.answer)
        if found > 0:
            data = dict(
                question=question,
                title=ANALYZE.title,
                answer=ANALYZE.answer)
        if found == 1:
            flash(u"j'ai trouvé quelque chose...", alert)
            data.update( dict(
                resume=ANALYZE.resume,
                latitude=ANALYZE.latitude,
                longitude=ANALYZE.longitude,
                address=ANALYZE.address))
        elif found == 2:
            flash(u'Il y a plusieurs possibilités...', alert)
        elif found == 3:
            alert = "alert-warning"
            flash(u"l m'est impossible de répondre.", alert)
        else:
            alert = "alert-warning"
            flash(u'Hélas, ma mémoire me fait défaut, je suis trop vieux !',
                  alert)
            data = dict(answer=False)
        data.update(dict(found=found))
    else:
        alert="alert-danger"
        flash(u'Pas de question posée', alert)
        data = dict(ERROR="missing question")
    data.update(dict(messages=render_template("messages.html",
                                              alert=alert)))
    return jsonify(data)


@app.route('/bot_said', methods=['POST'])
def bot_said():
    """Send an answer to AJAX call answer.js"""

    answer = Markup(request.form["answer"])
    return jsonify(dict(
        answer=render_template("bot_said.html",
                               answer=answer)))


@app.route('/user_said', methods=['POST'])
def user_said():
    """Return question template to add"""

    question = request.form['question']
    return jsonify(dict(
        question=render_template('user_said.html',
                                 question=question)))
