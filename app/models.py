from sqlalchemy import Column, Integer, String, Text
from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Float, Boolean

class Entreprise(Base):
    __tablename__ = "entreprises"

    id = Column(Integer, primary_key=True, index=True)
    photo = Column(String(255))
    nom = Column(String(150))
    service = Column(String(150))
    categorie = Column(String(100))

    ville = Column(String(100))
    commune = Column(String(100))
    quartier = Column(String(100))
    adresse = Column(Text)

    telephone = Column(String(30))
    whatsapp = Column(String(30))

    description = Column(Text)

    latitude = Column(Float)
    longitude = Column(Float)

    note = Column(Float)
    nombre_avis = Column(Integer)

    site_web = Column(String(255))

    verifie = Column(Boolean, default=False)