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
- pipenv
- tree-tagger [Tree-tagger is for tag french sentences](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/#parfiles)

### Librairies Python

- pytest
- pytest-cov
- Flask
- Flask-Testing
- Flask-SQLAlchemy
- Flask-Bootstrap4
- Blinker
- ipykernel (pour jupyter)
- treetaggerwrapper (paquet PyPi pour obtenir une indication de chaque mot 
d'une phrase en français)

## Installation

Allez là ou vous voulez tester ce projet et clonez ce repo github
(imaginons que vous allez dans ce répertoire: "~/OpenClassRooms/tests/)
```bash
cd ~/OpenClassRooms/test/
git clone git@github.com:jerome-diver/OC_grandpy_bot.git
pipenv install
pipenv shell

```
**Des dépendances sont requises:**
Il aut installer tree-tagger depuis ses sources comme indiqué sur la page du
 lien.
 Ce que j'ai fait (mais il est possible de fairte atrement):
 une fois télécharger:
  - [le fichier source (pour ma part, je suis sous windows, mais il existe 
  pour Apple - OSX et Windows)](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.2.tar.gz)
  - [le fichier de tag-script](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz)
  - [le script d'installation](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh)
  
  Le fichier de la langue utilisée (le français) est déjà décompressé dans le 
  projet, le code s'en sert déjà, mais voici le lien et les infos utiles:
  - [le fichier du langage utilisé (ici, le français)](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/french.par.gz)
  - [trouvez ici la documentation de la signification des tags](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/french-tagset.html)
 ```bash
 sudo mkdir opt/TreeTagger
 sudo mv ~/download/tree-tagger-linux-3.2.2.tar.gz /opt/TreeTagger/
 sudo mv ~/download/tagger-scripts.tar.gz /opt/TreeTagger/
 sudo mv ~/download/install-tagger.sh /opt/TreeTagger/ 
 su
 cd /opt
 chmod -755 install-tagger.sh
 ./install-tagger.sh
 exit
 ```

## Initialisation

L'application utilise une mini base de donnée sqlite-3 pour enregistrer une 
iste de mots (stop words) permettant l'analyse de la question. Pour cela, il
 faut initialiser cette base de donnée avec la commande:
 ```bash
 export FLASK_APP=run.py 
 flask init_stopwords
 flesk run
 ```
