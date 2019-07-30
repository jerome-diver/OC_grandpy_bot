# -- Grandpy Bot --
OpenClassRooms - projet 7 - GrandPy Bot, le papy robot.

Posez une question il vous répondra (mais on ne vous promet rien d'autre).

## Utiliser

- Python-3.7
- Flask
- javascript avec methodes AJAX (jQuery ok)
- API de Google Map
- API de Media Wiki

## Methode
TDD: TestDriven Development et de façon récursive pour chaque fonctionnalité
 implémentée (module, classe, méthode ou fonction):
 
- créer le test pour une fonctionnalité
- créer ensuite la fonctionnalité jusqu'à ce que le test passe
- améliorer le code une fois le test passé
- re-valider les tests pour confirmr que l'amélioration du code ne casse rien

## API utilisées pour récolter des réponses

### Google Maps

- [trouver une carte avec interaction](https://developers.google.com/maps/documentation/urls/guide?hl=fr)
- [API javascript Google Map v3](https://developers.google.com/maps/documentation/javascript/reference/?hl=fr#StreetViewPanorama)
- [afficher une carte statique](https://developers.google.com/maps/documentation/maps-static/intro?hl=fr)
- [Une vue de la ville](https://developers.google.com/maps/documentation/streetview/intro?hl=fr)

### Wikipedia (Media Wiki)

- [l'api de Media Wiki](https://www.mediawiki.org/wiki/API:Main_page/fr)

### Librairies Python existantes

- [pymediawiki](https://github.com/barrust/mediawiki)

## Dépendances

### Logiciels

- Python-3.7
- sqlite3

### Librairies Python

- pytest
- pytest-cov
- Flask
- Flask-Testing
- Flask-SQLAlchemy
- Flask-Bootstrap4
- Blinker
- ipykernel (pour jupyter)
- nltk (language learning toolkit)

## Installation

Allez là ou vous voulez tester ce projet et clonez ce repo github
(imaginons que vous allez dans ce répertoire: "~/OpenClassRooms/tests/)
```bash
cd ~/OpenClassRooms/test/
git clone git@github.com:jerome-diver/OC_grandpy_bot.git
```
Des dépendances sont requises.


## Initialisation

L'application utilise une mini base de donnée sqlite-3 pour enregistrer une 
iste de mots (stop words) permettant l'analyse de la question. Pour cela, il
 faut initialiser cette base de donnée avec la commande:
 ```bash
 export FLASK_APP=run.py 
 flask init_stopwords
 flesk run
 ```
