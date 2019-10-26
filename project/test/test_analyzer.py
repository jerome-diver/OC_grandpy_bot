"""Test module analyzer package methods for
 - Analyzer instance object
 - Properties mixin class
 - Parser mixin class
 - QueryWiki instance class
  """

from project.analyzer import *
from config import STOP_WORDS_FR, STOP_VERBS_FR
import json
import pytest

SENTENCES = [
    "Sais-tu où se trouve le Musée du Louvre ?"
    "Connaissez-vous Napoléon ?"
]

TESTS = []
for sentence in SENTENCES:
    TESTS.append(Analyzer())
    TESTS[-1].ask(sentence)


@pytest.fixture
def parser() -> Parser:
    """Need a parser"""

    return Parser()


@pytest.fixture
def query_wiki() -> QueryWiki:
    """Need a QueryWiki"""

    return QueryWiki()

@pytest.fixture
def give_stop_words() -> set:
    """Give a stop words set"""

    with open(STOP_WORDS_FR, 'r') as sw:
        return set(map(str.strip, sw))

@pytest.fixture
def give_stop_verbs() -> set:
    """Give a stop verbs set"""

    with open(STOP_VERBS_FR, 'r', encoding='utf-8') as sv:
        return set(map(str.strip, json.load(sv)))


class TestParser():
    """Test for Parser tools instance"""

    def test_remove_stop_words(self, parser, give_stop_words):
        """Test if all stop words to be removed"""

        full = " ".join(give_stop_words)
        assert parser.remove_stop_words(full) == ""

    def test_remove_conjugate_verbs(self, parser, give_stop_verbs):
        """Test if all stop words to be removed"""

        full = " ".join(give_stop_verbs)
        assert parser.remove_conjugate_verbs(full) == ""

    def test_remove_all(self, parser, give_stop_words, give_stop_verbs):
        """Test if can remove all full lists give empty string"""

        parser._input = " ".join(give_stop_words | give_stop_verbs)
        assert parser.remove_all() == ""


class TestQueryWiki():
    """Test for QueryWiki object instance"""

    def test_define(self, query_wiki,
                    give_stop_words, give_stop_verbs):
        """Test define can get question and parser.remove_all"""

        question = " ".join(give_stop_verbs | give_stop_words)
        query_wiki.define(question)
        assert query_wiki._input == question
        assert query_wiki._query_analyzed == ""


class TestAnalyzer():
    """Test for Analyzer class instance"""

    pass

