import requests
import json
import time

from config import (
    CLIENT_ID,
    CLIENT_SECRET,
    WEBHOOK_URL,
    SEARCH_KEYWORDS,
    SEARCH_DEPARTMENT,
    SEARCH_CONTRACT,
    SEARCH_FULL_TIME,
    SEARCH_PUBLISHED_SINCE
)


TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
SEEN_JOBS_FILE = "seen_jobs.json"


def initialize_seen_jobs(offres):
    seen_jobs = {offre.get("id") for offre in offres if offre.get("id")}
    save_seen_jobs(seen_jobs)
    print(f"{len(seen_jobs)} offres enregistrées comme déjà vues.")


def load_seen_jobs():
    try:
        with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_FILE, "w", encoding="utf-8") as file:
        json.dump(list(seen_jobs), file, indent=2)


def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "o2dsoffre api_offresdemploiv2"
        }
    )

    response.raise_for_status()

    return response.json()["access_token"]


def send_to_discord(offre):
    message = (
        f"🔔 **Nouvelle offre trouvée !**\n\n"
        f"**{offre.get('intitule', 'Sans titre')}**\n"
        f"🏢 {offre.get('entreprise', {}).get('nom', 'Entreprise inconnue')}\n"
        f"📍 {offre.get('lieuTravail', {}).get('libelle', 'Lieu inconnu')}\n"
        f"📅 {offre.get('dateCreation', 'Date inconnue')}\n"
        f"🔗 {offre.get('origineOffre', {}).get('urlOrigine', 'Pas de lien')}"
    )

    while True:
        response = requests.post(
            WEBHOOK_URL,
            json={"content": message}
        )

        print("Discord :", response.status_code)

        if response.status_code == 204:
            return True

        if response.status_code == 429:
            try:
                retry_after = response.json().get("retry_after", 2)
            except ValueError:
                retry_after = 2

            print(
                f"Limite Discord atteinte. "
                f"Attente de {retry_after} secondes..."
            )

            time.sleep(retry_after)
            continue

        response.raise_for_status()


def search_offres(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    toutes_les_offres = []
    debut = 0
    taille_page = 150

    while True:
        fin = debut + taille_page - 1

        params = {
            "motsCles": SEARCH_KEYWORDS,
            "range": f"{debut}-{fin}"
        }

        if SEARCH_DEPARTMENT:
            params["departement"] = SEARCH_DEPARTMENT

        if SEARCH_CONTRACT:
            params["typeContrat"] = SEARCH_CONTRACT

        if SEARCH_FULL_TIME:
            params["tempsPlein"] = SEARCH_FULL_TIME

        if SEARCH_PUBLISHED_SINCE:
            params["publieeDepuis"] = SEARCH_PUBLISHED_SINCE

        response = requests.get(
            SEARCH_URL,
            headers=headers,
            params=params
        )

        print(
            f"Recherche des offres {debut}-{fin} : "
            f"HTTP {response.status_code}"
        )

        if response.status_code == 204:
            print("  → Aucune offre trouvée.")
            break

        response.raise_for_status()

        data = response.json()
        offres = data.get("resultats", [])

        toutes_les_offres.extend(offres)

        print(f"  → {len(offres)} offres récupérées")

        if len(offres) < taille_page:
            break

        debut += taille_page

    return toutes_les_offres


if __name__ == "__main__":
    token = get_access_token()
    print("Token récupéré avec succès !\n")

    offres = search_offres(token)

    print(f"{len(offres)} offres trouvées.\n")


    seen_jobs = load_seen_jobs()

    for offre in offres:
        job_id = offre.get("id")

        if job_id not in seen_jobs:
            if send_to_discord(offre):
                seen_jobs.add(job_id)
                save_seen_jobs(seen_jobs)
