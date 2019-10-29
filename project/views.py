"""View point file"""

from flask import Flask, render_template, jsonify, request, flash, Markup
from flask_assets import Environment, Bundle
from flask_bootstrap import Bootstrap
import re

from config import GOOGLE_KEY
from project.models import BotSpeach


app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)


from project.analyzer import Analyzer

ANALYZE = Analyzer()
EXTRACT_ID = re.compile(r".*\_(\d+)")
BOT = BotSpeach()


@app.route('/')
@app.route('/index/')
def index():
    """At start time, should call an index.html page"""

    global ANALYZE
    ANALYZE = Analyzer()
    return render_template('index.html',
                           logo_tag=BOT.presentation,
                           intro=BOT.ask("first"),
                           GOOGLE_KEY=GOOGLE_KEY)


@app.route('/submit', methods=['POST'])
def submit():
    """Send a question to AJAX call question.js"""

    question = request.form['question']
    type = request.form['type']
    index = request.form['index']
    alert = "alert-success"
    data = dict()
    if type == "answer":
        ANALYZE.last_answer(index)
    else:
        ANALYZE.clear()
    if question:
        ANALYZE.ask(question)
        found = ANALYZE.find_something()
        if found > 0:
            data = dict(
                question=question,
                title=ANALYZE.title,
                answer=ANALYZE.answer)
        if found == 1:
            flash(u"j'ai trouvé quelque chose...", alert)
            data.update( dict(
                resume=ANALYZE.resume,
                map_id=ANALYZE.map_id,
                latitude=ANALYZE.latitude,
                longitude=ANALYZE.longitude,
                address=ANALYZE.address))
        elif found == 2:
            flash(u'Il y a plusieurs possibilités...', alert)
        else:
            alert = "alert-warning"
            flash(u'Hélas, ma mémoire me fait défaut, je suis trop vieux !',
                  alert)
            data = dict(answer=False, result=BOT.answer('last', 'nothing'))
        data.update(dict(found=found))
    else:
        alert="alert-danger"
        flash(u'Pas de question posée', alert)
        data = dict(ERROR="missing question")
    data.update(dict(messages=render_template("messages.html",
                                              alert=alert)))
    print(data)
    return jsonify(data)


@app.route('/bot_said', methods=['POST'])
def bot_said():
    """Send an answer to AJAX call answer.js"""

    answer = Markup(request.form["answer"])
    time = request.form['time']
    location = request.form['location']
    map_id = f"map_{request.form['mapid']}"
    return jsonify(dict(
        answer=render_template("bot_said.html",
                               answer=answer,
                               time=time,
                               location=location,
                               map_id=map_id)))


@app.route('/user_said', methods=['POST'])
def user_said():
    """Return question template to add"""

    question = request.form['question']
    time = request.form['time']
    location = request.form['location']
    return jsonify(dict(
        question=render_template('user_said.html',
                                 question=question,
                                 time=time,
                                 location=location)))


@app.route('/map_coordinates', methods=['GET'])
def map_coordinates():
    """Get  map coordinates from AJAX bot request"""

    return jsonify(dict(
        map_id = ANALYZE.map_id,
        latitude = ANALYZE.latitude,
        longitude = ANALYZE.longitude,
        address = ANALYZE.address))
