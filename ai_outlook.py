import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
YOUR_SITE_URL = "https://skeletronindustries.in"
YOUR_SITE_NAME = "Skeletron Industries"

def get_ai_outlook(price):
    if not OPENROUTER_API_KEY:
        return "Error: OpenRouter API key missing."

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": YOUR_SITE_URL,
                "X-Title": YOUR_SITE_NAME,
            },
            data=json.dumps({
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Gold is currently trading at ₹{price} per ounce in India. Based on general market knowledge, give a 2-3 sentence professional market outlook for an Indian investor. Mention possible factors affecting price. Keep it concise and neutral."
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 150,
            })
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        return f"AI outlook error: {e}"