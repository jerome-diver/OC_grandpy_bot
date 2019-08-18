"""Parse string to remove stop words"""


import re
from treetaggerwrapper import TreeTagger as tt

from .models import StopWord
from config import TAGPARFILE, TAGDIR


class Analyzer:

    COORDINATES = re.compile(r'^https:\/\/.*maps\/.*\@(\d+\.\d+),(\d+.\d+).*')

    def __init__(self, question: str):

        self._question = question

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
        """Get tags from treetagger"""

        tagger = tt(tagdir=TAGDIR, tagparfile=TAGPARFILE, taglang='fr')
        self._tags = [tuple(tag.split("\t"))
                      for tag in tagger.tag_text(self._question)]

    def extract_verbs(self) -> str:
        """Extract principal verb"""

        pass

    def extract_searching_words(self) -> str:
        """Keep principal words only"""

        pass

    @staticmethod
    def catch_coordinates(urls) -> tuple:
        """Catch latitude and longitude coordinates from text page html"""

        for url in urls:
            found = Analyzer.COORDINATES.match(url)
            if found:
                latitude = found.group(1)
                longitude = found.group(2)
                print("FOUND", latitude, longitude)
                return latitude, longitude
        return 0, 0
