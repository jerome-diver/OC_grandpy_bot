"""Test module analyzer package methods for
 - Analyzer instance object
 - Properties mixin class
 - Parser mixin class
 - QueryWiki instance class
  """

from project.analyzer import *
from  env_var import STOP_WORDS_FR, STOP_VERBS_FR

import json
import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(scope="class")
def monkeypatch_for_class(request):
    """I use monkeypatch self fixture variable
    for class test methods API"""

    request.cls._monkeypatch = MonkeyPatch()


@pytest.fixture
def parser() -> Parser:
    """Need a parser"""

    return Parser()


@pytest.fixture
def analyzer() -> Analyzer:
    """Need an Analyzer instance fixture"""

    return Analyzer()


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


@pytest.mark.usefixtures("monkeypatch_for_class")
class TestQueryWiki():
    """Test for QueryWiki object instance"""

    def wiki_str(self, query):

        return query

    def wiki_kwargs(self, *args, **kwargs) -> str:

        return "OK"

    def test_define(self, query_wiki,
                    give_stop_words, give_stop_verbs):
        """Test define can get question and parser.remove_all"""

        question = " ".join(give_stop_verbs | give_stop_words)
        query_wiki.define(question)
        assert query_wiki._input == question
        assert query_wiki._query_analyzed == ""

    def test_page(self, query_wiki):
        """Test property page call mocked QueryWiki.WIKI.page"""

        self._monkeypatch.setattr(QueryWiki.WIKI, "page", self.wiki_str)
        assert query_wiki.page == None

    def test_resume(self, query_wiki):
        """Test QueryWiki.resume call mocked QueryWiki.WIKI.summary
        and return corect formed html"""

        self._monkeypatch.setattr(QueryWiki.WIKI, "summary",
                                  self.wiki_kwargs)
        assert query_wiki.resume == "<h2>None</h2><p>OK</p>"

    def test_searching(self, query_wiki):
        """TEst QueryWiki.searching return Boolean True value related to
        mocked QueryWiki.WIKI.search"""

        self._monkeypatch.setattr(QueryWiki.WIKI, "search",
                                  self.wiki_kwargs)
        assert query_wiki.searching is True


@pytest.mark.usefixtures("monkeypatch_for_class")
class TestAnalyzer():
    """Test for Analyzer class instance"""

    from project.models import BotSpeach
    BOT = BotSpeach()

    def wiki_str(self, query):

        return query

    def wiki_kwargs(self, *args, **kwargs) -> str:

        return "OK"

    def catch_coordinates(self, query):
        """Get mock coordinates"""

        pass

    def test_clear(self, analyzer):
        """Test if Analyzer.clear get good values initialization"""

        for id in range(2):
            analyzer.clear()
            assert isinstance(analyzer._query, QueryWiki)
            assert analyzer._get_last is False
            assert analyzer._index == 0
            assert analyzer._map_id == 1 + id

    @pytest.mark.parametrize('arg, last, index',
                             [(0, True, 0), (2, True, 2)])
    def test_last_answer(self, analyzer, arg, last, index):
        """Test last answer setup correctly"""

        analyzer.last_answer(arg)
        assert analyzer._get_last == last
        assert analyzer._index == index

    def test_ask(self, analyzer, give_stop_words, give_stop_verbs):
        """Test if can ask and get good _query (QueryWiki) defined"""

        full = " ".join(give_stop_words | give_stop_verbs)
        analyzer.ask(full)
        assert analyzer._query._query_analyzed == ''

    @pytest.mark.parametrize('possible, get_last, search, assertion',
                             [(dict(a=1, b=2), False, True, 2),
                              (dict(a=1, b=2), True, True, 1),
                              (dict(a=1), False, True, 1),
                              (dict(a=1), True, True, 1),
                              (dict(), False, True, 0),
                              (dict(), True, True, 1),
                              (dict(a=1, b=2), True, False, 0)])
    def test_find_something(self, analyzer, possible, get_last,
                            search, assertion):
        """Test correct setup what ever found from mocked QueryWiki"""

        self._monkeypatch.setattr(QueryWiki, "searching", search)
        self._monkeypatch.setattr(QueryWiki.WIKI, "page", self.wiki_str)
        self._monkeypatch.setattr(analyzer, "catch_coordinates",
                                  self.catch_coordinates)
        self._monkeypatch.setattr(QueryWiki, "possibilities",
                                  possible)
        analyzer._get_last = get_last
        assert analyzer.find_something() == assertion

    def test_collect_data(self, analyzer):
        """Test if self._result get result of method QueryWiki.page
        and function return Nothing"""

        self._monkeypatch.setattr(QueryWiki, "page", self.wiki_kwargs())
        self._monkeypatch.setattr(Analyzer, "catch_coordinates",
                                  self.catch_coordinates)
        assert analyzer.collect_data() == None
        assert analyzer.result == "OK"

    @pytest.mark.parametrize('result, assertion1, assertion2', [
                        (False, None, "<h2>None</h2><p>OK</p>"),
                        (True, BOT.answer("intro", "mono-choice"), "OK")])
    def test_form_answer_elements(self, analyzer, result,
                                  assertion1, assertion2):
        """Do something only if get a QueryWiki.result"""

        if result:
            self._monkeypatch.setattr(Analyzer, "result", self.wiki_kwargs())
            self._monkeypatch.setattr(QueryWiki, "resume", self.wiki_kwargs())
        analyzer.form_answer_elements()
        assert analyzer._introduction == assertion1
        assert analyzer.resume == assertion2
