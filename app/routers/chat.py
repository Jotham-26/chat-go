from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import Response

import requests
import os

from app.database import get_db
from app.shemas import ChatRequest
from app.services.deepseek_service import analyser_requete
from app.services.google_places import rechercher_lieux, extraire_places
from app.crud import (
    enregistrer_entreprise,
    rechercher_entreprises,
)

router = APIRouter()


@router.get("/photo/{photo_name:path}")
def get_photo(photo_name: str):

    api_key = os.getenv("GOOGLE_API_KEY")

    url = (
        f"https://places.googleapis.com/v1/{photo_name}/media"
        f"?maxHeightPx=400&key={api_key}"
    )

    r = requests.get(url)

    return Response(
        content=r.content,
        media_type=r.headers.get(
            "Content-Type",
            "image/jpeg"
        )
    )


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # 1. Analyse de la demande

    analyse = analyser_requete(request.message)

    print("ANALYSE :", analyse)

    service = analyse.get("service")
    commune = analyse.get("commune")
    quartier = analyse.get("quartier")
    categorie = analyse.get("categorie")

    # 2. Vérifier le service

    if not service:

        return {
            "entreprises": [],
            "output": "Je n'ai pas compris le service recherché."
        }

    
    # 3. Chercher d'abord dans MySQL

    entreprises = rechercher_entreprises(
        db,
        analyse
    )

    print(
        "Résultats MySQL :",
        len(entreprises)
    )

    # 4. Si MySQL est vide
    # → recherche Google Places

    if len(entreprises) == 0:

        recherche = service

        if categorie:
            recherche += f" {categorie}"

        if commune:
            recherche += f" {commune}"

        if quartier:
            recherche += f" {quartier}"

        recherche += " Abidjan Côte d'Ivoire"

        print(
            "Recherche Google Places :",
            recherche
        )

        # 5. Recherche Google
        

        resultat = rechercher_lieux(
            recherche
        )

        places = extraire_places(
            resultat
        )

        print(
            "Résultats Google Places :",
            len(places)
        )

        
        # 6. Enregistrer les résultats
        for p in places:

            enregistrer_entreprise(
                db=db,
                p=p,
                service=analyse["service"],
                categorie=analyse["categorie"],
                commune=analyse["commune"],
                ville=analyse["ville"]
            )

        # 7. Relire MySQL

        entreprises = rechercher_entreprises(
            db,
            analyse
        )

        print(
            "Résultats après sauvegarde :",
            len(entreprises)
        )
    # 8. Préparer la réponse Flutter

    liste = []

    for e in entreprises:

        liste.append({

            "photo": e.photo,

            "nom": e.nom,

            "service": e.service,

            "adresse": e.adresse,

            "telephone": e.telephone,

            "whatsapp": e.whatsapp,

            "note": e.note,

            "site_web": e.site_web,

            "latitude": e.latitude,

            "longitude": e.longitude,

        })

    
    # 9. Réponse

    return {
        "entreprises": liste
    }