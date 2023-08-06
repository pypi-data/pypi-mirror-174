# dotations-locales-back

## Installation

> Les étapes qui suivent supposent que Python est déjà installé dans votre environnement. 
La version de Python nécessaire est décrite dans le fichier `pyproject.toml` à la récine du dépôt. 

La configuration des dépendances est gérée avec [poetry](https://python-poetry.org).

> Pour gérer différentes versions de Python sur une machine, nous utilisons `pyenv` qui permet par exemple d'installer une version avec `pyenv install 3.8.9` et `poetry env use python3.8`.

Pour créer un environnement virtuel et installer les dépendances de l'application, exécuter la commande suivante dans un terminal :

```shell
poetry install
```

Cette commande doit s'achever sans erreur.

On peut voir les dépendances installées avec cette commande : 

```shell
poetry show
```
> De même avec `poetry run pip list` pour les nostalgiques de pip 🙂

## Démarrer l'API Web

L'API Web est bâtie sur le framework [FastAPI](https://fastapi.tiangolo.com). 

Pour la démarrer en local, après avoir suivi les étapes d'installation, exécuter la commande suivante dans un terminal :

```shell
poetry run uvicorn dotations_locales_back.web_api.main:app --reload
```

L'API Web est alors accessible à l'adresse suivante : `http://127.0.0.1:8000`

Elle peut être testée via l'interface Swagger UI à cette adresse : `http://127.0.0.1:8000/docs`

## Tests

Pour lancer les tests il faut exécuter la commande suivante dans un terminal :

```shell
poetry run pytest
```

Ou depuis un terminal avec l'environnement virtuel activé :

```shell
pytest
```


## Déploiement sur Scalingo

Pour déployer cette application sur Scalingo, il est nécessaire de créer 3 fichiers supplémentaires. En effet Scalingo n'est pas compatible avec les fichiers de gestion des dépendances créés par Poetry.

Voici les fichiers à créer : 
* `requirements.txt` : Scalingo se base sur ce fichier pour installer les dépendances.  
Pour le créer il faut éxécuter la commande suivante :
    ```shell
    poetry export -f requirements.txt --without-hashes --output requirements.txt
    ```
> **Attention** : Si des dépendances sont ajoutées via Poetry, il faudra regénérer le fichier `requirements.txt` à chaque fois également. En effet, Poetry gère automatiquement l'ajout de dépendances dans son propre fichier `pyproject.toml` mais pas dans le fichier `requirements.txt`.

* `runtime.txt` : Scalingo se base sur ce fichier pour définir la version de python à utiliser. Il s'agit donc de s'assurer de sa cohérence avec la version de Python indiquée dans `pyproject.toml`

* `Procfile` : Lors du déploiement Scalingo se base sur ce fichier pour éxécuter la commande qui lance l'application.
L'hôte requis est `0.0.0.0` et il faut également que le serveur écoute le port défini dans une variable d'environnement `PORT`. Il faut donc ajouter la ligne suivante au fichier `Procfile` :
    ```
    web: uvicorn web_api.main:app --host=0.0.0.0 --port=${PORT:-5000}
    ```
