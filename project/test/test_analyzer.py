"""Test module analyzer package methods for
 - Analyzer instance object
 - Properties mixin class
 - Parser mixin class
 - QueryWiki instance class
  """

from project.analyzer import Analyzer
from project.analyzer import Parser
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
def parser():
    """Need a parser"""

    return Parser()

class TestParser():
    """Test for Parser tools instance"""

    def give_stop_words(self) -> set:
        """Give a stop words set"""

        with open(STOP_WORDS_FR, 'r') as sw:
            return set(map(str.strip, sw))

    def give_stop_verbs(self) -> set:
        """Give a stop verbs set"""

        with open(STOP_VERBS_FR, 'r', encoding='utf-8') as sv:
            stop_verbs = set(map(str.strip, json.load(sv)))
        return stop_verbs

    def test_remove_stop_words(self, parser):
        """Test if all stop words to be removed"""

        sw = self.give_stop_words()
        full = " ".join(sw)
        assert parser.remove_stop_words(full) == ""

    def test_remove_conjugate_verbs(self, parser):
        """Test if all stop words to be removed"""

        sv = self.give_stop_verbs()
        full = " ".join(sv)
        assert parser.remove_conjugate_verbs(full) == ""

    def test_remove_all(self, parser):
        """Test if can remove all full lists give empty string"""

        full_set = self.give_stop_words()
        full_set.update(self.give_stop_verbs())
        parser._input = " ".join(full_set)
        assert parser.remove_all()


class TestQueryWiki():
    """Test for QueryWiki object instance"""

    pass


class TestAnalyzer():
    """Test for Analyzer class instance"""

    pass

