"""Model of database data"""

import logging as lg
from flask_sqlalchemy import SQLAlchemy

from .views import app
from config import STOP_WORDS_FR

db = SQLAlchemy(app)


class Content(db.Model):
    """Content a SQL Alchemy ORM Model for Stop Words fr"""

    id = db.Column(db.Integer(), primary_key=True)
    word = db.Column(db.String(), nullable=False)

    def __init__(self, word):
        self.word = word


db.create_all()


def init_stop_words():
    """"Initialize database from stop words text file"""

    db.drop_all()
    db.create_all()
    try:
        with open(STOP_WORDS_FR, 'r') as sw_file:
            for word in sw_file:
                db.session.add(Content(word))
            db.session.commit()
    except FileNotFoundError as fnf_error:
        lg.error(f"{fnf_error}\nTry to check your file is in "
                 f"project/assets/stop_words-fr.txt and is readable")
    except Exception as Error:
        lg.error(f"Something gone wrong: {Error}")
    else:
        lg.warning("Database with stop words content initialized")
