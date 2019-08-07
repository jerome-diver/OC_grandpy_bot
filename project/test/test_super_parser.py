"""Test module super_parser
- function remove_stop_words"""

from project.super_parser import remove_stop_words
from project.models import db, StopWord


def test_remove_stop_words():
    """Get sample of StopWords from database and try function
    result should be empty"""

    sentence = " ".join(x.word for x in StopWord.query.all())
    sentence += "     , + 5 _ ' ` @ ) ( ="
    assert remove_stop_words(sentence) == ""


def test_extract_principal_verb():
    """Test function to extract principal verb in complicate sentence"""

    pass


def test_extract_searching_words():
    """Test extraction of searching words from sentence"""

    pass
