"""Test module analyzer package methods for
 - Analyzer instance object
 - Properties mixin class
 - Parser mixin class
 - QueryWiki instance class
  """

from project.analyzer import Analyzer

SENTENCES = [
    "Sais-tu où se trouve le Musée du Louvre ?"
    "Connaissez-vous Napoléon ?"
]

TESTS = []
for sentence in SENTENCES:
    TESTS.append(Analyzer())
    TESTS[-1].ask(sentence)


class TestProperties():
    """Test for properties for Analyzer"""

    def test_try(self):

        pass


class TestParser():
    """Test for Parser tools instance"""

    pass


class TestQueryWiki():
    """Test for QueryWiki object instance"""

    pass


class TestAnalyzer():
    """Test for Analyzer class instance"""

    def test_remove_stop_words():
        """Get sample of StopWords from database and try function
        result should be empty"""

        assert TESTS[0]._query == ""
        assert TESTS[1]._query == "Connaissez Napoléon"

    def test_extract_verbs():
        """Test function to extract principal verb in complicate sentence"""

        assert TESTS[1]._verbs == [("Connaissez", "VER:pres", "connaître")]

    def test_catch_coordinates():
        """Test extraction of searching words from sentence"""

    pass
