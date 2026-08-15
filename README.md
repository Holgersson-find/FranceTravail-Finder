# FranceTravail Finder

FranceTravail Finder est un petit outil Python qui recherche
automatiquement des offres d’emploi sur l’API France Travail et envoie
les nouvelles offres sur un salon Discord.

## Fonctionnalités

-   Recherche d’offres via l’API Offres d'emploi de France Travail
-   Récupération de plusieurs pages de résultats
-   Envoi des nouvelles offres sur Discord
-   Mémorisation des offres déjà envoyées
-   Peut être exécuté automatiquement avec le Planificateur de tâches
    Windows

## Fonctionnement

Le programme :

1.  Se connecte à l’API Offres d'emploi de France Travail.
2.  Recherche les offres correspondant aux critères définis dans
    config.py.
3.  Compare les offres trouvées avec seen_jobs.json.
4.  Envoie uniquement les nouvelles offres sur Discord.
5.  Ajoute les nouvelles offres à seen_jobs.json.

## Installation

### Prérequis

-   Windows
-   Python 3.13 ou version compatible
-   Un compte développeur France Travail
-   Un webhook Discord


### Installation des dépendances

pip install -r requirements.txt


### Configuration

Copiez config.example.py et renommez la copie en :

config.py

Puis renseignez vos propres paramètres :

CLIENT_ID = “votre_client_id”, 
CLIENT_SECRET = “votre_client_secret", 
WEBHOOK_URL = “votre_webhook_discord"

SEARCH_KEYWORDS = “”, 
SEARCH_DEPARTMENT = “”, 
SEARCH_CONTRACT = “”, 
SEARCH_FULL_TIME = “” (true/false), 
SEARCH_PUBLISHED_SINCE = 30 (nombre de jours)


## Lancement

python searcher.py

Ou via :

start_finder.bat


## Historique des offres

Le fichier seen_jobs.json contient les identifiants des offres déjà
traitées.

Il est créé automatiquement lors de la première exécution.

Ce fichier n’est pas inclus dans le dépôt GitHub.


## API Offres d'emploi

FranceTravail Finder utilise l’API officielle Offres d'emploi pour
récupérer les offres d’emploi.

Pour utiliser l’API, vous devez disposer de vos propres identifiants
API.

## Licence

Projet personnel réalisé à des fins d’apprentissage et d’automatisation
de recherche d’emploi.
