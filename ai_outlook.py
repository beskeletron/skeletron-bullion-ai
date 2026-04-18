import subprocess

def get_ai_outlook(price):
    prompt = f"Gold is currently trading at ₹{price} per ounce in India. Based on general market knowledge, give a 2-3 sentence professional market outlook for an Indian investor. Mention possible factors affecting price. Keep it concise and neutral."
    
    # 'ollama' command ko try karenge
    command = f'ollama run llama3.2 "{prompt}"'
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        outlook = result.stdout.strip()
        return outlook
    except Exception as e:
        return "AI outlook temporarily unavailable."

if __name__ == "__main__":
    test_price = 62000  # Dummy price for testing
    outlook = get_ai_outlook(test_price)
    print("AI Outlook:")
    print(outlook)