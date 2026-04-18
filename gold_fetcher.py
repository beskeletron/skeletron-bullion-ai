import requests


API_KEY = "goldapi-dl74xsmo3sy7r4-io"  


BASE_URL = "https://www.goldapi.io/api"

def get_gold_price():
    headers = {
        'x-access-token': API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{BASE_URL}/XAU/INR", headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data['price']
        currency = data['currency']
        timestamp = data['timestamp']
        return price, currency, timestamp
    else:
        return None, None, None

if __name__ == "__main__":
    price, curr, ts = get_gold_price()
    if price:
        print(f"Gold Price: ₹{price} per ounce")
    else:
        print("Failed to fetch gold price")