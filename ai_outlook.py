import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_outlook(price):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""Gold is currently trading at ₹{price} per ounce in India.
        Based on general market knowledge, give a 2-3 sentence professional market outlook for an Indian investor.
        Mention possible factors affecting price. Keep it concise and neutral."""
        
        response = model.generate_content(prompt)
        outlook = response.text.strip()
        return outlook
    except Exception as e:
        return "AI outlook temporarily unavailable."