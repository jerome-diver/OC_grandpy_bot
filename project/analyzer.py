"""Parse string to remove stop words"""

import re
from flask import render_template
from treetaggerwrapper import TreeTagger as tt
from mediawiki import MediaWiki
from jinja2 import Markup, escape
from enum import Enum

from .models import StopWord
from config import TAGPARFILE, TAGDIR


class Removed(Enum):

    NOTHING = 1
    STOP_WORDS = 2
    STOP_WORDS_VERBS = 3


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
        self._possibilities = list()
        self._can_not_answer = False
        self._queries = dict(
            N=QueryWiki(Removed.NOTHING),
            SW=QueryWiki(Removed.STOP_WORDS),
            SW_V=QueryWiki(Removed.STOP_WORDS_VERBS))
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

        if self._get_last or len(self._possibilities) == 1:
            return Markup(
                f"<p>{escape(self._introduction)}</p>"
                f"<p>{self._content}</p>"
                f"<p>{escape(self._last)}</p>")
        elif len(self._possibilities) > 1:
            text = render_template("button_possibility.html",
                                   possibilities=self._possibilities)
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


class Tools():

    VERB = re.compile(r'VER:.*')

    def __init__(self):
        self._input = None

    def remove_stop_words(self) -> str:
        """Remove stop words"""

        # remove first and last spaces
        # replace ' - by <space> char
        # remove non alphabetic's chars
        clean = ["".join(c for c in word if c.isalpha())
                 for word in
                 self._input.strip()
                     .translate(str.maketrans("'-", "  "))
                     .split(" ")]
        # remove stop words and isolate chars
        nsw = [word for word in [x for x in clean if len(x) > 1]
               if not StopWord.query
                              .filter_by(word=word.lower())
                              .first()]
        return " ".join(nsw)

    def remove_verbs(self) -> str:
        """remove verbs from self._query"""

        without_verbs = [word for word in self._input.split(" ")
                         if word not in
                         [tag[0] for tag in self.extract_verbs()] ]
        return " ".join(without_verbs)

    def get_tags(self):
        """Get tags from TreeTagger"""

        tagger = tt(TAGDIR=TAGDIR, TAGPARFILE=TAGPARFILE, TAGLANG='fr')
        return [tuple(tag.split("\t"))
                for tag in tagger.tag_text(self._input)]

    def extract_verbs(self) -> list:
        """Extract principal verb"""

        return [tag for tag in self.get_tags()
                if self.VERB.match(tag[1])]


class QueryWiki(Tools):
    """Create query to get result oriented searching form factory"""

    WIKI = MediaWiki("https://fr.wikipedia.org/w/api.php", lang='fr')

    def __init__(self, form: Removed):

        super().__init__()
        self._form = form
        self._query_analyzed = None
        self._possibilities = list()

    def define(self, question: str):
        """Define query form and process other owned definition linked"""

        self._input = question
        if self._form == Removed.STOP_WORDS:
            self._query_analyzed = self.remove_stop_words()
        elif self._form == Removed.STOP_WORDS_VERBS:
            self._input = self.remove_stop_words()
            self._query_analyzed = self.remove_verbs()
        else:
            self._query_analyzed = question
        print(f"ANALYZE QUERY FOR {self._form} IS:", self._query_analyzed)

    @property
    def page(self):
        """wiki property"""

        return self.WIKI.page(self._query_analyzed)

    @property
    def resume(self):
        """Resume property"""

        text = self.WIKI.summary(title=self._query_analyzed,
                                 sentences=2)
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
    def tags(self):
        """tags property from Tools tags words"""

        return self.get_tags()

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

    def last_answer(self, index=0):
        """Wash previous possibilities content and define one answer"""

        self._get_last = True
        self._index = index - 1 if index != 0 else 0

    def ask(self, question: str):
        """Ask question"""

        if self._get_last:
            self._queries["N"].define(self._possibilities[self._index])
        elif not self.can_search():
            pass
        else:
            for key, query in self._queries.items():
                query.define(question)
                if query.searching:
                    for possible in query.possibilities:
                        if possible not in self._possibilities:
                            self._possibilities.append(possible)

    def find_something(self) -> int:
        self._last = "J'espère que ça te convient bonhomme. As-tu une autre " \
                     "question ?"
        if self._get_last:
            self._query = self._queries['N']
            self.collect_data()
            self.form_answer_elements()
            return 1
        elif self._can_not_answer:
            self.form_answer_elements()
            return 3
        elif len(self._possibilities) == 1:
            self._query = self._queries['SW_V']
            self._query.define(self._possibilities.pop())
            self.collect_data()
            self.form_answer_elements()
            return 1
        elif len(self._possibilities) > 1:
            self._introduction = "Cela me fait penser à plusieurs choses, " \
                                "de quoi est-il question plus précisément ?"
            for index, possible in enumerate(self._possibilities):
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

    def can_search(self):
        """Detect if can search"""

        self._can_not_answer = self.detect_subjective_question() or \
                               self.detect_emotion_subject()
        return not self._can_not_answer

    def detect_emotion_subject(self) -> bool:
        """Find if question target on emotion subject"""

        pass

    def detect_subjective_question(self) -> bool:
        """Detect if question is subjective"""

        pass
