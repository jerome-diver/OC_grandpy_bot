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
    with open(STOP_WORDS_FR, 'r') as swfr:
        for word in swfr:
            db.session.add(Content(word))
        db.session.commit()
    lg.warning("Database with stop words content initialized")
