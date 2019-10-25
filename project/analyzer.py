"""Parse string to remove stop words"""

import re
from flask import render_template
from mediawiki import MediaWiki
from jinja2 import Markup, escape
import json

from config import STOP_WORDS_FR, STOP_VERBS_FR

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

        print("Found latitude:", value)
        self._latitude = value

    @property
    def longitude(self):
        """Property for self._latitude"""

        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set self._latitude"""

        print("Found longitude:", value)
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
            return f'<p>Je ne sais rien à ce propos, je suis désolé.</p>'

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
        self._query_analyzed = None

    def remove_all(self):
        """Remove stop_words and conjugate verbs from input"""

        rsw = self.remove_stop_words(self._input)
        return self.remove_conjugate_verbs(rsw)

    def remove_stop_words(self, sentence) -> str:
        """Remove stop words"""

        # remove first and last spaces
        # replace ' - by <space> char
        # remove non alphabetic's chars
        clean = ["".join(c for c in word if c.isalpha())
                 for word in
                 sentence.strip()
                     .translate(str.maketrans("'-", "  "))
                     .split(" ")]
        # remove stop words and isolate chars
        nsw = [word for word in [x for x in clean if len(x) > 1]
               if not self.stop_words(word.lower())]
        return " ".join(nsw)

    def remove_conjugate_verbs(self, sentence) -> str:
        """Remove conjugate verbs"""

        ncv = [word for word in sentence.strip().split(" ")
               if not self.stop_verbs(word.lower())]
        return " ".join(ncv)

    @staticmethod
    def stop_words(word: str) -> bool:
        """is it in the stop word list ?"""

        with open(STOP_WORDS_FR, "r") as stop_words:
            for stop_word in stop_words:
                if word == stop_word.strip():
                    return True
        return False

    @staticmethod
    def stop_verbs(word: str) -> bool:
        """is it in the stop word list ?"""

        with open(STOP_VERBS_FR, "r", encoding='utf-8') as stop_verbs:
            for stop_verb in json.load(stop_verbs):
                if word == stop_verb.strip():
                    return True
        return False


class QueryWiki(Parser):
    """Create query to get result oriented searching form factory"""

    WIKI = MediaWiki("https://fr.wikipedia.org/w/api.php", lang='fr')

    def __init__(self):

        super().__init__()
        self._possibilities = list()

    def define(self, question: str):
        """Define query form and process other owned definition linked"""

        self._input = question
        self._query_analyzed = self.remove_all()
        print("After removed stop_words and conjugate verbs, query_parsed =",
              self._query_analyzed)

    @property
    def page(self):
        """wiki property"""

        return self.WIKI.page(self._query_analyzed)

    @property
    def resume(self):
        """Resume property"""

        text = self.WIKI.summary(title=self._query_analyzed,
                                 sentences=10)
        return f"<h2>{self._input}</h2><p>{text}</p>"

    @property
    def searching(self):
        """searching property from MEDIAWIKI"""

        self._possibilities = self.WIKI.search(self._query_analyzed,
                                               suggestion=False,
                                               results=5)
        if self._possibilities:
            return True
        return False

    @property
    def suggested_title(self):
        """suggested_title property from MEDIAWIKI"""

        return self.WIKI.suggest(self._query_analyzed)

    @property
    def coordinates(self):
        """coordinates property from MEDIAWIKI"""

        if hasattr(self.page, "coordinates"):
            return self.page.coordinates
        return None

    @property
    def references(self):
        """references property from MEDIAWIKI"""

        return self.page.references

    @property
    def html(self):
        """html page property from MEDIAWIKI"""

        return self.page.html

    @property
    def possibilities(self):
        """Property for all possibilities of this queryWiki"""

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

    def last_answer(self, index=0):
        """Wash previous possibilities content and define one answer"""

        self._get_last = True
        self._index = index - 1 if index != 0 else 0

    def ask(self, question: str):
        """Ask question"""

        if self._get_last:
            self._query.define(self._query.possibilities[self._index])
        else:
            self._query.define(question)

    def find_something(self) -> int:
        """Find possibilities or last answer and return code 0 1 or 2"""

        if self._query.searching:
            self._last = "J'espère que ça te convient bonhomme. As-tu une autre " \
                         "question ?"
            if self._get_last or len(self._query.possibilities) == 1:
                self.collect_data()
                self.form_answer_elements()
                return 1
            elif len(self._query.possibilities) > 1:
                self._introduction = "Cela me fait penser à plusieurs choses, " \
                                    "de quoi est-il question plus précisément ?"
                for index, possible in enumerate(self._query.possibilities):
                    self._content += f"{index}) {possible}\n"
                self._last = "Fais un choix dans cette liste mon grand..."
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

        if self._result:
            self._introduction = "Voilà ce que j'ai trouvé"
            self._content = self.resume

    def catch_coordinates(self, query):
        """Catch latitude and longitude coordinates from text page html"""

        coordinates = query.coordinates
        if coordinates:
            self._latitude = float(coordinates[0])
            self._longitude = float(coordinates[1])
        else:
            for ref in query.references:
                found = self.COORDINATES.match(ref)
                if found:
                    self.latitude = found.group(1)
                    self.longitude = found.group(2)
        if self.has_coordinates():
            print("COORDINATES :", self._latitude, self._longitude)
        else:
            print("NO COORDINATES FOUND")

    def has_coordinates(self) -> bool:
        """Said if has coordinates ready"""

        return self._latitude is not None and self._longitude is not None

    def catch_address(self, query):
        """Catch an address from wiki text result"""

        self._address = ""
