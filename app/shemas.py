from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str


class EntrepriseSchema(BaseModel):
    id: int
    nom: str | None = None
    service: str | None = None
    ville: str | None = None
    commune: str | None = None
    quartier: str | None = None
    telephone: str | None = None
    whatsapp: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True