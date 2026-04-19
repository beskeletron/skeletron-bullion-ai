import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_ai_outlook(price):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return "Error: DeepSeek API key missing."

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
        )

        prompt = f"""Gold is currently trading at ₹{price} per ounce in India.
        Based on general market knowledge, give a 2-3 sentence professional market outlook for an Indian investor.
        Mention possible factors affecting price. Keep it concise and neutral."""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI outlook error: {e}"