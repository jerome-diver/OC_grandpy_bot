"""Parse string to remove stop words"""

import re
from treetaggerwrapper import TreeTagger as tt
from mediawiki import MediaWiki

from .models import StopWord
from config import TAGPARFILE, TAGDIR


class Properties:

    def __init__(self):
        self._latitude = None
        self._longitude = None
        self._address = None
        self._result = None
        self._answer = None

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

        return self._answer

    @property
    def result(self):
        """Property for self._result"""

        return self._result


class Analyzer(Properties):
    COORDINATES = re.compile(r'^https:\/\/.*maps\/.*\@(\d+\.\d+),(\d+.\d+).*')
    WIKI = MediaWiki("https://fr.wikipedia.org/w/api.php", lang='fr')

    def __init__(self, question: str):

        super().__init__()
        self._question = question
        self._tags = self.get_tags()
        self._query = self.remove_stop_words()
        self._wiki = None
        self.analyze()

    def analyze(self):
        """Provide analysis to get relevant MediaWiki data from query"""

        self._wiki = self.WIKI.page(self._query)
        self.catch_coordinates()
        #self.catch_address()
        self._result = self._wiki.html
        print("Result:", self._result)

    def remove_stop_words(self) -> str:
        """Remove stop words"""

        # remove first and last spaces and replace ' by <space> char
        first_pass = self._question.strip().replace("'", " ")
        # remove non alphabetic's chars
        clean = []
        for word in first_pass.split(" "):
            clean.append("".join(c for c in word
                                 if (c.isalpha()
                                     or c == "-")))
        # remove isolated chars
        clean = [x for x in clean if len(x) > 1]
        # remove stop words
        no_stop_words = []
        for word in clean:
            c = StopWord.query.filter_by(word=word).first()
            if not c:
                no_stop_words.append(word)
        return " ".join(no_stop_words)

    def get_tags(self):
        """Get tags from TreeTagger"""

        print("tt Option:", TAGPARFILE, TAGDIR)
        tagger = tt(TAGDIR=TAGDIR, TAGPARFILE=TAGPARFILE, TAGLANG='fr')
        return [tuple(tag.split("\t"))
                for tag in tagger.tag_text(self._question)]

    def extract_verbs(self) -> str:
        """Extract principal verb"""

        pass

    def extract_searching_words(self) -> str:
        """Keep principal words only"""

        pass

    def catch_coordinates(self):
        """Catch latitude and longitude coordinates from text page html"""

        for ref in self._wiki.references:
            found = self.COORDINATES.match(ref)
            if found:
                self.latitude = found.group(1)
                self.longitude = found.group(2)

    def has_coordinates(self) -> bool:
        """Said if has coordinates ready"""

        return self._latitude is not None and self._longitude is not None

    def catch_address(self):
        """Catch an address from wiki text result"""

        text = self._wiki.text
        self._address = ""
