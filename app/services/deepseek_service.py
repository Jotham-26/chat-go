import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def analyser_requete(message: str):

    prompt = """
        Tu es un assistant IA de Chat&GO. Ton rôle est d'analyser la demande de l'utilisateur et de répondre UNIQUEMENT avec un JSON valide, sans texte, sans explication, sans balises Markdown.
        Tu dois identifier les informations suivantes :
        - service
        - categorie
        - ville
        - commune
        - quartier
        - urgence
        - budget
        - nombre
        - ouvert
        - trier_par

        Services possibles : restaurant, hôtel, garage, plombier, menuisier, électricien, pharmacie, médecin, dentiste, maçon, peintre, couturier, coiffeur, climatisation, informatique et tout autre métier ou service mentionné par l'utilisateur.
        Catégorie : préciser si l'utilisateur recherche un type particulier (africain, italien, chinois, libanais, fast-food, clinique, etc.). Sinon laisser "".
        Ville : si aucune ville n'est précisée, mettre "Abidjan".

        Commune : extraire la commune si elle est mentionnée, sinon "".

        Quartier : extraire le quartier si présent, sinon "".

        Urgence : mettre true si la demande contient des termes comme "urgence", "vite", "immédiatement", "maintenant". Sinon false.

        Budget : extraire le budget si indiqué, sinon "".

        Nombre : extraire le nombre demandé par l'utilisateur (exemple : 3 restaurants). Si aucun nombre n'est indiqué, mettre 5.

        Ouvert : mettre true si l'utilisateur demande un établissement ouvert actuellement ("ouvert", "ouvert maintenant", "ouvert actuellement", "24h"), sinon false.

        trier_par :
        - "note" si l'utilisateur demande le meilleur, le mieux noté ou le plus recommandé.
        - "distance" si l'utilisateur demande le plus proche.
        - "" sinon.

        Retourne uniquement un JSON sous ce format :

        {
            "service": "",
            "categorie": "",
            "ville": "Abidjan",
            "commune": "",
            "quartier": "",
            "urgence": false,
            "budget": "",
            "nombre": 5,
            "ouvert": false,
            "trier_par": ""
        }
        L'utilisateur peut exprimer un besoin sans citer directement le service.

Tu dois identifier le service correspondant.

Exemples :

- "Je veux manger" → restaurant
- "J'ai faim" → restaurant
- "Qui peut me faire à manger ?" → restaurant
- "Je veux une pizza" → restaurant
- "Je veux dormir" → hôtel
- "Je cherche où passer la nuit" → hôtel
- "Mon robinet fuit" → plombier
- "Je n'ai plus d'électricité" → électricien
- "Ma voiture est en panne" → garage
- "Je veux me faire coiffer" → coiffeur
- "Je veux me faire belle" → coiffeur
- "Je veux une nouvelle coupe" → coiffeur
- "J'ai mal aux dents" → dentiste
- "Je suis malade" → médecin
- "J'ai besoin de médicaments" → pharmacie
- "Je veux construire une maison" → maçon
- "Je veux fabriquer une armoire" → menuisier
- "Mon ordinateur est en panne" → informatique
- "Je veux faire une table" → menuisier
- "Qui peut fabriquer une porte ?" → menuisier

Tu dois toujours déduire le service le plus logique, même si le mot exact n'est jamais utilisé.
Ne laisse jamais le champ "service" vide si l'intention de l'utilisateur permet de déduire un métier ou un établissement.

Privilégie toujours l'interprétation de l'intention plutôt que la recherche de mots-clés.
    """

    response = client.chat.completions.create(

        model="deepseek-chat",

        messages=[
            {
                "role":"user",
                "content":prompt
            },
            {
            "role": "user",
            "content": message
            }
        ],

        temperature=0

    )

    texte = response.choices[0].message.content
    print(texte)

    return json.loads(texte)