from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.shemas import ChatRequest
from app.services.deepseek_service import analyser_requete
from fastapi.responses import Response
import requests
import os

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
        media_type=r.headers.get("Content-Type", "image/jpeg")
    )
    

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    analyse = analyser_requete(request.message)

    service = analyse.get("service")
    commune = analyse.get("commune")
    ville = analyse.get("ville")
    quartier = analyse.get("quartier")

    if service is None:
        return {
            "output": "Je n'ai pas compris le service recherché."
        }

    entreprises = rechercher_entreprises(
        db,
        analyse
    )

    if len(entreprises) == 0:

        recherche = service

        recherche = service

        if analyse["categorie"]:
            recherche += f" {analyse['categorie']}"

        if commune:
             recherche += f" {commune}"

        if quartier:
            recherche += f" {quartier}"

            recherche += " Côte d'Ivoire"

        resultat = rechercher_lieux(recherche)

        places = extraire_places(resultat)

        for p in places:

         enregistrer_entreprise(
         db=db,
         p=p,
         service=analyse["service"],
         categorie=analyse["categorie"],
         commune=analyse["commune"],
         ville=analyse["ville"]
        )
         
        entreprises = rechercher_entreprises(
            db,
            analyse
        )
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

    return {
    "entreprises": liste
    }