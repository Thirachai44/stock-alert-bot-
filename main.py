import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def get_price(symbol):
    url = f"https://www.tradingview.com/symbols/{symbol}/"
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url, headers=headers)
    if symbol.upper() in response.text:
        import re
        match = re.search(r'"regularMarketPrice":\s*({[^}]+})', response.text)
        if match:
            import json
            price_data = json.loads(match.group(1))
            return float(price_data['raw'])
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = { "chat_id": TELEGRAM_CHAT_ID, "text": message }
    requests.post(url, data=payload)

def main():
    tracked = {
        "AAPL": 190.0,
        "TSLA": 600.0
    }

    for symbol, target in tracked.items():
        price = get_price(symbol)
        if price is not None:
            if price >= target:
                send_telegram_message(f"🚨 {symbol} ราคา {price} แตะเป้า {target} แล้ว!")
            else:
                print(f"{symbol}: {price} ยังไม่ถึง {target}")
        else:
            send_telegram_message(f"⚠️ ดึงราคาหุ้น {symbol} ไม่ได้")

if __name__ == "__main__":
    main()
