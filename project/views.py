"""View point file"""

from flask import Flask, render_template, jsonify, request, flash
from flask_bootstrap import Bootstrap
import wikipediaapi


app = Flask(__name__)
app.config.from_object('config')
app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_OUTPUT_DIR'] = './project/static/css'
app.config['COMPRESSOR_STATIC_PREFIX'] = '/project/static/css'
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
        if answer:
            flash(u"j'ai trouvé quelque chose...", "alert-success")
            alert = 'alert-success'
        else:
            flash(u'Hélas, ma mémoire me fait défaut, je suis trop vieux !',
                  "alert-warning")
            alert = "alert-waring"
        return jsonify({
            'question': question,
            'answer': answer.text,
            'messages': render_template('messages.html', alert=alert)})
    else:
        flash(u'Pas de question posée', 'alert-danger')
        return jsonify({
            "ERROR": "missing question",
            "messages": render_template("messages.html",
                                        alert="alert-danger")})
