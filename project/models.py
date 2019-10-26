"""Models module contain xml model for bot_speach.xml file's handler"""

import xml.etree.ElementTree as ET

from config import ORIGIN


class BotSpeach:
    """XML model handler to get bot speach sentences"""

    XML_DIR = ORIGIN / "project/assets"
    XML_FILE = str()
    SCRIPTS = None

    def __init__(self):

        self.XML_FILE = self.XML_DIR / "bot_speach.xml"
        self.SCRIPTS = ET.parse(str(self.XML_FILE))
        self._root = self.SCRIPTS.getroot()

    def ask(self, clue) -> str:
        """Return sentence for ask something by provide the clue's word"""

        ask = self._root.find('ask')
        return ask.find(clue).text

    def answer(self, clue, type):
        """Return text correspond to answer-clue with type attribute"""

        answer = self._root.find("answer")
        for target in answer.findall(clue):
            if target.attrib["type"] == type:
                return target.text

    @property
    def presentation(self):
        """Return presentation sentence"""

        prez = self._root.find("presentation")
        return prez.text