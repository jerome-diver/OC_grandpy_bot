""" est of module models.py from package project
- function 'init_stop_words'
    will be used as a flask command through imported Click lib
- class 'Content'
    used for handle data content through SQLAlchemy ORM to
    sqlite database
"""

class TestContent:
    """Test class Content"""
    from project.models import Content
    content = Content("test")

    def test_init(self):
        """Test of initialization of Content object instance"""

        assert self.content.word == "test"


def test_init_stop_words(caplog):
    """Test of function init_stop_words"""

    from project.models import init_stop_words
    import logging
    init_stop_words()
    captured = caplog.record_tuples
    assert captured[0][0] == "project.models"
    assert captured[0][1] == logging.INFO
    assert captured[0][2] == "Database with stop words content initialized"

def test_db(capsys):
    """Test type of global module scope  variable db"""

    from project.models import db
    print(type(db))
    captured = capsys.readouterr()
    assert  captured.out == "<class 'flask_sqlalchemy.SQLAlchemy'>\n"