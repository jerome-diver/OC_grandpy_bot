# OC_grandpy_bot
OpenClassRooms - projet 7 - GrandPy Bot, le papy robot.
Posez une question il vous répondra.

__Utiliser__
- Flask
- javascript avec methodes AJAX

## API utilisées pour récolter des réponses

### Google Maps



### Wikipedia


## Installation

Allez là ou vous voulez tester ce projet et lonez ce repo github
(imaginons que vous allez dans ce répertoire: "~/OpenClassRooms/tests/)
```bash
cd ~/OpenClassRooms/test/
git clone 
```
Des dépendances sont requises.


## Initialisation

L'application utilise une mini base de donnée sqlite-3 pour enregistrer une 
iste de mots (stop words) permettant l'analyse de la question. Pour cela, il
 faut initialiser cette base de donnée avec la commande:
 ```bash
 export FLASK_APP=run.py 
 flask init_stopwords
 ```
