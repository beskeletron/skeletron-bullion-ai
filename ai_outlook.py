import os
import logging
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_ai_outlook(price):
    if not GEMINI_API_KEY:
        return "AI outlook unavailable (API key missing)."
        
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""Gold is currently trading at ₹{price} per ounce in India.
        Based on general market knowledge, give a 2-3 sentence professional market outlook for an Indian investor.
        Mention possible factors affecting price. Keep it concise and neutral."""
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        return response.text.strip()
        
    except ImportError as e:
        logging.error(f"Import error: {e}")
        return "AI outlook module not available."
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return "AI outlook temporarily unavailable."