""" est of module models.py from package project
- function 'init_stop_words'
    will be used as a flask command through imported Click lib
- class 'Content'
    used for handle data content through SQLAlchemy ORM to
    sqlite database
"""

def test_content():
    """TEst of class Content"""

    from project.models import Content
    content = Content("test")
    assert content.word == "test"

def test_init_stop_words(capsys):
    """Test of function init_stop_words"""

    from project.models import init_stop_words
    init_stop_words()
    captured = capsys.readouterr()
    assert captured.out == "INFO :: Database with stop words content " \
                                "initialized\n"
