"""Test module analyzer package
- methods of Analyzer instance object"""

from project.analyzer import Analyzer
from project.models import StopWord

SENTENCES = [
    " ".join(x.word for x in StopWord.query.all()) + "     , + 5 _ ' ` @ ) ( =",
    "Connaissez-vous Napoléon ?"
]


def test_tags():
    """Test tags content presence"""

    analyzer = Analyzer(SENTENCES[1])



def test_remove_stop_words():
    """Get sample of StopWords from database and try function
    result should be empty"""

    analyzer = Analyzer(SENTENCES[0])
    assert analyzer.remove_stop_words() == ""


def test_extract_tags():
    """Test function to extract principal verb in complicate sentence"""

    analyzer = Analyzer(SENTENCES[1])

def test_extarct_verbs():
    """Test extraction of verbs"""

    pass

def test_extract_searching_words():
    """Test extraction of searching words from sentence"""

    pass