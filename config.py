"""Config file"""
from builtins import range
from pathlib import Path, PurePath
from os import environ
import random
import string


SECRET_KEY = "".join(
    [random.choice(string.printable) for _ in range(24)])
SQLALCHEMY_TRACK_MODIFICATIONS=True

BASEDIR = Path.cwd()
STOP_WORDS_FR = str(
    PurePath(str(BASEDIR), 'project/assets/stopwords-fr.txt'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(
    PurePath(str(BASEDIR), 'stopwords_fr.db'))
TAGPARFILE = str(
    PurePath(str(BASEDIR), "project/static/language/french.par"))
TAGDIR = "/opt/TreeTagger/"
GOOGLE_KEY = environ.get('GOOGLE_KEY')
LOCATION_WORDS = [
    "rue", 'avenue', 'allée', 'boulevard', 'impasse', 'chemin',
    'cité', 'route nationale', 'route départementale', 'RN', 'RD' ]
POSSIBLE_ANSWER = ["Je ne sais plus, je ne me rapelle plus de tout ça.",
                   "J'ai des souvenirs, plein... il me faut plus de "
                   "précision. Voici ce dont je me rapelle :",
                   "Je me rapelle bien quand j'étais gamin...",
                   "Salut, de quoi veux-tu que je te parle ?"]
port = int(environ.get('PORT', 5000))
