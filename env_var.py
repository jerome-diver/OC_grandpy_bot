"""Package for environement global variables to share for all the
application when imported"""


from builtins import range
from pathlib import Path, PurePath
import random
import string
from os import environ


ORIGIN = PurePath(Path('.').absolute())
SECRET_KEY = "".join(
    [random.choice(string.printable) for _ in range(24)])
BASEDIR = Path.cwd()
STOP_WORDS_FR = str(PurePath(str(BASEDIR),
                             'project/assets/stopwords-fr.txt'))
STOP_VERBS_FR = str(PurePath(str(BASEDIR),
                             'project/assets/stop_verbs.json'))
GOOGLE_KEY = environ.get('GOOGLE_KEY')
