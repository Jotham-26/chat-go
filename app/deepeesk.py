import httpx
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def call_deepseek(messages: list, model: str = "deepseek-chat") -> str:
    """
    Appelle l'API DeepSeek avec l'historique des messages
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60.0
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

async def chat_with_deepseek(user_message: str, history: list = None) -> str:
    """
    Fonction simplifiée pour discuter avec DeepSeek
    """
    if history is None:
        history = []
    
    # Construire le format des messages pour DeepSeek
    messages = []
    
    # Ajouter l'historique
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Ajouter le message actuel
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    return await call_deepseek(messages)