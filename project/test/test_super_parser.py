"""Test module super_parser
- function remove_stop_words"""

from project.super_parser import remove_stop_words
from project.models import db, StopWord


def test_remove_stop_words():
    """Get sample of StopWords from database and try function
    result should be empty"""

    sentence = " ".join(x.word for x in StopWord.query.all())
    assert remove_stop_words(sentence) == ""
