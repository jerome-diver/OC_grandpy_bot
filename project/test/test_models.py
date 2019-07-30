"""Test of module models.py from package project
- function 'init_stop_words'
    will be used as a flask command through imported Click lib
- class 'StopWord'
    used for handle data content through SQLAlchemy ORM to
    sqlite database
"""

from flask_sqlalchemy import SQLAlchemy
from logging import INFO, ERROR

from project.views import app
from project.models import StopWord, init_stopwords
from project import models
from config import STOP_WORDS_FR


class TestStopWord:
    """Test class StopWord"""

    @classmethod
    def setup_class(cls):
        db = SQLAlchemy(app)
        cls.id = db.Column(db.Integer(), primary_key=True)
        cls.word = db.Column(db.String(), nullable=False)

    def setup_method(self):
            self.content = StopWord("test")

    def test_init(self):
        """Test of initialization of StopWord object instance"""

        assert self.content.word == "test"


def test_init_stop_words(caplog, monkeypatch):
    """Test of function init_stop_words"""

    original_open = open

    def monkey_open(*args, **kwargs):
        return original_open('fake', 'r')

    def monkey_db():
        return None

    init_stopwords()
    monkeypatch.setitem(__builtins__, 'open', monkey_open)
    init_stopwords()
    monkeypatch.setattr(models, 'db', monkey_db)
    init_stopwords()
    captured = caplog.record_tuples
    assert captured[0][0] == "project.models"
    assert captured[0][1] == INFO
    assert captured[0][2] == "Database with stop words content initialized"
    assert captured[1][0] == "project.models"
    assert captured[1][1] == ERROR
    assert captured[1][2] == f"[Errno 2] No such file or directory: 'fake'\n" \
                             f"Try to check your file is in " \
                             f"{STOP_WORDS_FR} and is readable"


def test_db(capsys):
    """Test type of global module scope  variable db"""

    from project.models import db
    print(type(db))
    captured = capsys.readouterr()
    assert captured.out == "<class 'flask_sqlalchemy.SQLAlchemy'>\n"