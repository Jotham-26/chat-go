from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Entreprise


def rechercher_entreprises(
    db: Session,
    analyse: dict,
):

    query = db.query(Entreprise)

    if analyse["service"]:
        query = query.filter(
            Entreprise.service.ilike(f"%{analyse['service']}%")
        )

    if analyse["commune"]:
        query = query.filter(
            Entreprise.commune.ilike(f"%{analyse['commune']}%")
        )

    if analyse["quartier"]:
        query = query.filter(
            Entreprise.quartier.ilike(f"%{analyse['quartier']}%")
        )

    if analyse["categorie"]:
        query = query.filter(
            Entreprise.categorie.ilike(f"%{analyse['categorie']}%")
        )

    if analyse["trier_par"] == "note":
        query = query.order_by(
            Entreprise.note.desc()
        )

    return query.limit(analyse["nombre"]).all()


def enregistrer_entreprise(
    db: Session,
    p,
    service: str,
    categorie: str = "",
    commune: str | None = None,
    ville: str = "Abidjan"
    
):

    nom = p.get("displayName", {}).get("text")
    categorie = categorie.capitalize() if categorie else service.capitalize()
     
    photo = None
    
    if p.get("photos"):
    
        photo = p["photos"][0]["name"]
    

    existe = db.query(Entreprise).filter(
        Entreprise.nom == nom
    ).first()

    if existe:
        return

    entreprise = Entreprise(
       
        
        nom=nom,

        service=service.capitalize(),

        categorie=categorie,

        ville=ville,

        commune=commune if commune else "",

        quartier="",

        adresse=p.get("formattedAddress"),

       telephone=p.get("nationalPhoneNumber") or "Non renseigné",

       whatsapp=p.get("nationalPhoneNumber") or "Non renseigné",

        description="Entreprise importée depuis Google Places",

        latitude=p.get("location", {}).get("latitude"),

        longitude=p.get("location", {}).get("longitude"),

        note=p.get("rating"),

        nombre_avis=p.get("userRatingCount"),

        site_web=p.get("websiteUri"),
        photo=photo,

        verifie=True

    )
    print("PHOTO :", photo)
    db.add(entreprise)
    db.commit()