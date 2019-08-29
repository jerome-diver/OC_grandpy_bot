"""Test module analyzer package
- methods of Analyzer instance object"""

from project.analyzer import Analyzer
from project.models import StopWord

SENTENCES = [
    " ".join(x.word for x in StopWord.query.all()) + "     , + 5 _ ' ` @ ) ( =",
    "Connaissez-vous Napoléon ?"
]
ANSWER_TAGS = [None,
               [('Connaissez', 'VER:pres', 'connaître'),
                ('-vous', 'PRO:PER', 'vous'),
                ('Napoléon', 'NAM', 'Napoléon'),
                ('?', 'SENT', '?')] ]
TESTS = []
for sentence in SENTENCES:
    TESTS.append(Analyzer())
    TESTS[-1].ask(sentence)


def test_get_tags():
    """Test tags content presence"""

    assert isinstance(TESTS[1]._tags, list)
    for tag in TESTS[1]._tags:
        assert len(tag) == 3
        assert isinstance(tag, tuple)


def test_remove_stop_words():
    """Get sample of StopWords from database and try function
    result should be empty"""

    assert TESTS[0]._query == ""
    assert TESTS[1]._query == "Connaissez Napoléon"


def test_extract_verbs():
    """Test function to extract principal verb in complicate sentence"""

    assert TESTS[1]._verbs == [("Connaissez", "VER:pres", "connaître")]


def test_extract_searching_words():
    """Test extraction of verbs"""

    assert TESTS[1]._searching == "Napoléon"


def test_catch_coordinates():
    """Test extraction of searching words from sentence"""

    pass
