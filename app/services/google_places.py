import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


def rechercher_lieux(recherche):

    url = (
        "https://places.googleapis.com/v1/places:searchText"
    )

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

    response = requests.post(
        url,
        json=body,
        headers=headers,
        timeout=30
    )

    print(
        "Google Places HTTP :",
        response.status_code
    )

    print(
        "Google Places réponse :",
        response.text
    )

    response.raise_for_status()

    return response.json()


def extraire_places(resultat):

    return resultat.get(
        "places",
        []
    )