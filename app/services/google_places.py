import requests
import os
import json

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
print("Clé API :", API_KEY)

def rechercher_lieux(recherche):

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": (
        "places.id,"
        "places.displayName,"
        "places.formattedAddress,"
        "places.location,"
        "places.rating,"
        "places.userRatingCount,"
        "places.nationalPhoneNumber,"
        "places.websiteUri,"
        "places.businessStatus,"
        "places.photos"
    )
}

    body = {
        "textQuery": recherche
    }

    response = requests.post(url, json=body, headers=headers)

    data = response.json()

    print(json.dumps(data, indent=2, ensure_ascii=False))

    return data


    print(json.dumps(data, indent=2, ensure_ascii=False))

    return data
def extraire_places(resultat):

    return resultat.get("places", [])