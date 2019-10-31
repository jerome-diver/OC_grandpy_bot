"""Parse string to remove stop words"""

import re
from flask import render_template
from mediawiki import MediaWiki
from jinja2 import Markup, escape
import json

from env_var import STOP_WORDS_FR, STOP_VERBS_FR
from project.models import BotSpeach


class Properties:

    def __init__(self):

        self._question = None
        self._latitude = None
        self._longitude = None
        self._address = None
        self._result = None
        self._title = None
        self._resume = None
        self._introduction = None
        self._content = ""
        self._last = None
        self._get_last = False
        self._index = None
        self._map_id = 0
        self._query = None
        self._bot = BotSpeach()

    @property
    def question(self):
        """Property to get last question asked"""

        return self._question

    @property
    def latitude(self):
        """Property for self._latitude"""

        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set self._latitude"""

        self._latitude = value

    @property
    def longitude(self):
        """Property for self._latitude"""

        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set self._latitude"""

        self._longitude = value

    @property
    def address(self):
        """Property for self._address"""

        return self._address

    @address.setter
    def address(self, value):
        """Property setter for self._address"""

        self._address = value

    @property
    def answer(self):
        """Property for self._answer"""

        if self._get_last or len(self._query.possibilities) == 1:
            return Markup(
                f"<p>{escape(self._introduction)}</p>"
                f"<p>{self._content}</p>"
                f"<p>{escape(self._last)}</p>")
        elif len(self._query.possibilities) > 1:
            text = render_template("button_possibility.html",
                                   possibilities=self._query.possibilities)
            return Markup(text)
        else:
            return f'<p>{self._bot.answer("intro", "nothing")}</p>'

    @property
    def result(self):
        """Property for self._result"""

        return self._result

    @property
    def title(self):
        """Property for self._result"""

        return self._title

    @property
    def resume(self):
        """Property for self._result"""

        return self._query.resume

    @property
    def map_id(self):
        """Property for map id"""

        return self._map_id


class Parser():

    def __init__(self):
        self._input = None

    def remove_all(self, test=False) -> str:
        """Remove stop_words and conjugate verbs from input"""

        return self.remove_stop_words(self.remove_conjugate_verbs(self._input))

    def remove_stop_words(self, sentence) -> str:
        """Remove stop words"""

        # get set of stop_words
        with open(STOP_WORDS_FR, "r") as stop_words:
            sw = set(map(str.strip, set(stop_words)))
        clean = set(map(str.lower, sentence.split(" ")))
        # remove stop words and isolate chars
        nsw = set([x for x in clean if len(x) > 1]) - sw
        return " ".join(nsw) if nsw else ""

    def remove_conjugate_verbs(self, sentence) -> str:
        """Remove conjugate verbs"""

        cl = set(map(str.lower, sentence.split(" ")))
        with open(STOP_VERBS_FR, "r", encoding='utf-8') as stop_verbs:
            sv = set(map(str.strip, json.load(stop_verbs)))
        ncv = cl - sv
        return " ".join(ncv) if ncv else ""


class QueryWiki(Parser):
    """Create query to get result oriented searching form factory"""

    BOT = BotSpeach()
    WIKI = MediaWiki("https://fr.wikipedia.org/w/api.php", lang='fr')

    def __init__(self):

        super().__init__()
        self._possibilities = dict()
        self._query_analyzed = None

    def define(self, question: str):
        """Define query form and process other owned definition linked"""

        self._input = question
        self._query_analyzed = self.remove_all()
        print("RESULT ANALYZE:", self._query_analyzed)

    @property
    def page(self):
        """wiki property"""

        try:
            page = self.WIKI.page(self._query_analyzed)
        except:
            return None
        return page

    @property
    def resume(self):
        """Resume property"""

        try:
            text = self.WIKI.summary(title=self._query_analyzed,
                                     sentences=10)
        except:
            return QueryWiki.BOT.answer("last", "nothing")
        return f"<h2>{self._input}</h2><p>{text}</p>"

    @property
    def searching(self):
        """searching property from MEDIAWIKI"""

        import uuid
        possibilities = self.WIKI.search(self._query_analyzed,
                                         suggestion=False,
                                         results=5)
        if possibilities:
            print("POSSIBILITIES", possibilities)
            for possible in possibilities:
                self._possibilities[str(uuid.uuid4())] = possible
            return True
        self._possibilities = dict()
        return False

    @property
    def coordinates(self):
        """coordinates property from MEDIAWIKI"""

        if hasattr(self.page, "coordinates"):
            return self.page.coordinates
        return None

    @property
    def references(self):
        """references property from MEDIAWIKI"""

        if hasattr(self.page, "references"):
            return self.page.references
        return None

    @property
    def html(self):
        """html page property from MEDIAWIKI"""

        return self.page.html

    @property
    def possibilities(self, index=None):
        """Property for all possibilities of this queryWiki"""

        if index:
            return self._possibilities[index]
        return self._possibilities


class Analyzer(Properties):

    COORDINATES = re.compile(r'^https:\/\/.*maps\/.*\@(\d+\.\d+),(\d+.\d+).*')

    def __init__(self):

        super().__init__()
        self._query = QueryWiki()

    def clear(self):
        """Clear all class variables"""

        self._get_last = False
        self._index = 0
        self._query = QueryWiki()
        self._map_id += 1

    def last_answer(self, index):
        """Wash previous possibilities content and define one answer"""

        self._get_last = True
        self._index = index

    def ask(self, question: str):
        """Ask question"""

        if self._get_last:
            self._query.define(self._query.possibilities[self._index])
        else:
            self._query.define(question)

    def find_something(self) -> int:
        """Find possibilities or last answer and return code 0 1 or 2"""

        if self._query.searching:
            if len(self._query.possibilities) == 1 or self._get_last:
                self._last = self._bot.answer("last", "mono-choice")
                self.collect_data()
                self.form_answer_elements()
                return 1
            elif len(self._query.possibilities) > 1:
                self._introduction = self._bot.answer("intro", "multi-choice")
                for possible in self._query.possibilities.values():
                    self._content += f"{possible}\n"
                self._last = self._bot.answer("last", "multi-choice")
                return 2
        return 0

    def collect_data(self):
        """Provide analysis to get relevant MediaWiki data from query"""

        self.catch_coordinates(self._query)
        if not self.has_coordinates():
            self.catch_address(self._query)
        self._result = self._query.page

    def form_answer_elements(self):
        """Define answer elements for answer sentence"""

        if self.result:
            self._introduction = self._bot.answer("intro", "mono-choice")
            self._content = self.resume
        else:
            self._introduction = self._bot.answer("intro", "nothing")
            self._content = self._bot.answer("last", "nothing")

    def catch_coordinates(self, query):
        """Catch latitude and longitude coordinates from text page html"""

        coordinates = query.coordinates
        if coordinates:
            print('Find COORDINATES')
            self._latitude = float(coordinates[0])
            self._longitude = float(coordinates[1])
        else:
            references = query.references
            if references:
                print('Find REFERENCES')
                for ref in references:
                    found = self.COORDINATES.match(ref)
                    if found:
                        print('Find COORDINATES')
                        self.latitude = found.group(1)
                        self.longitude = found.group(2)

    def has_coordinates(self) -> bool:
        """Said if has coordinates ready"""

        return self._latitude is not None and self._longitude is not None

    def catch_address(self, query):
        """Catch an address from wiki text result"""

        self._address = ""
