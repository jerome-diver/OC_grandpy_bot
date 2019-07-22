"""Model of database data"""

from flask_sqlalchemy import SQLAlchemy
import logging as lg
import sys

from project.views import app
from config import STOP_WORDS_FR

db = SQLAlchemy(app)


class Content(db.Model):
    """Content a SQL Alchemy ORM Model for Stop Words fr"""

    id = db.Column(db.Integer(), primary_key=True)
    word = db.Column(db.String(), nullable=False)

    def __init__(self, word):
        self.word = word


db.create_all()


def init_stopwords():
    """Initialization of stop words in database model"""

    format_handler = lg.Formatter('%(levelname)s :: %(message)s')
    handler = lg.StreamHandler(sys.stdout)
    handler.setFormatter(format_handler)
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.INFO)
    logger.addHandler(handler)
    try:
        db.drop_all()
        db.create_all()
        with open(STOP_WORDS_FR, 'r') as sw_file:
            for word in sw_file:
                db.session.add(Content(word))
            db.session.commit()
    except FileNotFoundError as error:
        logger.error(f"{error}\nTry to check your file is in "
                     f"{STOP_WORDS_FR} and is readable")
    except Exception as error:
        logger.error(f"Something gone wrong: {error}")
    else:
        logger.info("Database with stop words content initialized")
