"""Test module super_parser
- function remove_stop_words"""

from project.super_parser import remove_stop_words
from project.models import db, StopWord


def test_remove_stop_words():
    """Get sample of StopWords from database and try function
    result should be empty"""

    max = db.session.query(StopWord.id).count()
    stop_words = ""
    while max:
        max -= 1
        stop_words += " " + StopWord.query.filter_by(id=x).first().word
    assert remove_stop_words(stop_words) == ""
