SERVICES = [
    "plombier",
    "menuisier",
    "électricien",
    "restaurant",
    "hôtel",
    "garage",
    "coiffeur",
    "couturier",
    "pharmacie",
    "médecin",
    "dentiste",
    "maçon",
    "peintre",
    "climatisation",
    "informatique"
]


COMMUNES = [
    "cocody",
    "yopougon",
    "abingourou",
    "adjamé",
    "plateau",
    "treichville",
    "marcory",
    "koumassi",
    "port-bouët",
    "abobo",
    "bingerville"
]


def detect_service(message: str):

    message = message.lower()

    for service in SERVICES:
        if service in message:
            return service

    return None


def detect_commune(message: str):

    message = message.lower()

    for commune in COMMUNES:
        if commune in message:
            return commune

    return None