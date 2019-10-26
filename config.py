"""Config file"""
from builtins import range
from pathlib import Path, PurePath
from os import environ
import random
import string

ORIGIN = PurePath(Path('.').absolute())
SECRET_KEY = "".join(
    [random.choice(string.printable) for _ in range(24)])
BASEDIR = Path.cwd()
STOP_WORDS_FR = str(
    PurePath(str(BASEDIR), 'project/assets/stopwords-fr.txt'))
STOP_VERBS_FR = str(
    PurePath(str(BASEDIR), 'project/assets/stop_verbs.json'))
GOOGLE_KEY = environ.get('GOOGLE_KEY')
port = int(environ.get('PORT', 5000))
