"""View point file"""

from flask import Flask, render_template, jsonify, request, flash
from flask_bootstrap import Bootstrap
from mediawiki import MediaWiki
from config import GOOGLE_KEY


app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
wiki = MediaWiki("https://fr.wikipedia.org/w/api.php", lang='fr')


@app.route('/')
@app.route('/index/')
def index():
    """At start time, should call an index.html page"""

    return render_template('index.html', GOOGLE_KEY=GOOGLE_KEY)


@app.route('/question', methods=['POST'])
def question():

    from project.super_parser import Analyzer
    question = request.form['question']
    if question:
        analyze = Analyzer(question)
        answer = wiki.page(analyze.remove_stop_words())
        latitude, longitude = analyze.catch_coordinates(answer.references)
        if answer:
            flash(u"j'ai trouvé quelque chose...", "alert-success")
            alert = 'alert-success'
        else:
            flash(u'Hélas, ma mémoire me fait défaut, je suis trop vieux !',
                  "alert-warning")
            alert = "alert-warning"
        return jsonify(dict(
            question=question,
            answer=answer.html,
            latitude=latitude,
            longitude=longitude,
            messages=render_template('messages.html', alert=alert)))
    else:
        flash(u'Pas de question posée', 'alert-danger')
        return jsonify({
            "ERROR": "missing question",
            "messages": render_template("messages.html",
                                        alert="alert-danger")})
