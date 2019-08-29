"""Parse string to remove stop words"""

import re
from treetaggerwrapper import TreeTagger as tt
from mediawiki import MediaWiki
from jinja2 import Markup, escape

from .models import StopWord
from config import TAGPARFILE, TAGDIR


WIKI = MediaWiki("https://fr.wikipedia.org/w/api.php", lang='fr')


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
        self._content = None
        self._last = None

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

        if self._result:
            return Markup(
                f"<p>{escape(self._introduction)}</p>"
                f"<p>{self._content}</p>"
                f"<p>{escape(self._last)}</p>")
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

        if self._title:
            text = WIKI.summary(title=self._title, sentences=2)
            return f"<h2>{self._title}</h2><p>{text}</p>"
        return "Nothing found"


class Analyzer(Properties):

    COORDINATES = re.compile(r'^https:\/\/.*maps\/.*\@(\d+\.\d+),(\d+.\d+).*')
    VERB = re.compile(r'VER:.*')

    def __init__(self):

        super().__init__()
        self._tags = None
        self._verbs = []
        self._query = None
        self._searching = None
        self._titles = []
        self._wiki = None
        self._possibilities = []

    def ask(self, question: str):
        """Ask question, then provide analisis"""

        self._question = question
        self.collect_data()
        self.form_answer_elements()

    def collect_data(self):
        """Provide analysis to get relevant MediaWiki data from query"""

        self._tags = self.get_tags()
        self._verbs = self.extract_verbs()
        self._query = self.remove_stop_words()
        self._searching = self.extract_searching_words()
        if self._query:
            self._wiki = WIKI.page(self._query)
            self.catch_coordinates()
            if not self.has_coordinates():
                self.catch_address()
            self._result = self._wiki.html
            self._title = WIKI.suggest(self._query)
            self._titles.append(WIKI.suggest(self._question))
            self._titles.append(self.title)
            self._possibilities.append(WIKI.search(self._question))
            self._possibilities.append(WIKI.search(self._query))

    def form_answer_elements(self):
        """Define answer elements for answer sentence"""

        if self._result:
            self._introduction = "Laisse moi te dire ce que j'ai trouvé"
            self._content = self.resume

    def remove_stop_words(self) -> str:
        """Remove stop words"""

        # remove first and last spaces
        # replace ' - by <space> char
        # remove non alphabetic's chars
        clean = ["".join(c for c in word if c.isalpha())
                 for word in
                 self._question.strip()
                     .translate(str.maketrans("'-", "  "))
                     .split(" ")]
        # remove stop words and isolate chars
        nsw = [word for word in [x for x in clean if len(x) > 1]
               if not StopWord.query
                              .filter_by(word=word.lower())
                              .first()]
        return " ".join(nsw)

    def get_tags(self):
        """Get tags from TreeTagger"""

        tagger = tt(TAGDIR=TAGDIR, TAGPARFILE=TAGPARFILE, TAGLANG='fr')
        return [tuple(tag.split("\t"))
                for tag in tagger.tag_text(self._question)]

    def extract_verbs(self) -> list:
        """Extract principal verb"""

        return [tag for tag in self._tags
                if self.VERB.match(tag[1])]

    def extract_searching_words(self) -> str:
        """remove verbs from self._query"""

        without_verbs = [word for word in self._query.split(" ")
                         if word not in
                         [tag[0] for tag in self._verbs] ]
        return " ".join(without_verbs)

    def catch_coordinates(self):
        """Catch latitude and longitude coordinates from text page html"""

        coordinates = self._wiki.coordinates
        if coordinates:
            self._latitude = float(coordinates[0])
            self._longitude = float(coordinates[1])
        else:
            for ref in self._wiki.references:
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

    def catch_address(self):
        """Catch an address from wiki text result"""

        self._address = ""
