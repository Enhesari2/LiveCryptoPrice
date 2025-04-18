import requests
import time
import random
import json

# -------------------------
# ✏️ Fixed settings
# -------------------------
BOT_TOKEN = "7877804608:AAEei57Fmno0k9T6918pSRN5Kwj4pOluzPs"
CHAT_ID = "@Trump_Mania_bot"
INTERVAL = 60  # time between updates (in seconds)
LIMIT = 100     # number of cryptocurrencies to display

# -------------------------
# 🚀 Get list of top cryptos
# -------------------------
def get_top_cryptos(limit=LIMIT):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    return response.json()

# -------------------------
# 📬 Send initial message
# -------------------------
def send_to_telegram(bot_token, chat_id, message, bitcoin_price):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [{"text": f"💰 BTC: {bitcoin_price:,}", "callback_data": "bitcoin_price"}]
            ]
        })
    }
    response = requests.post(url, data=payload)
    print("🔍 Response JSON:", response.json())
    if response.ok:
        return response.json()["result"]["message_id"]
    return None

# -------------------------
# ✏️ Edit message
# -------------------------
def edit_message(bot_token, chat_id, message_id, new_message, bitcoin_price):
    url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_message,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [{"text": f"💰 BTC: {bitcoin_price:,}", "callback_data": "bitcoin_price"}]
            ]
        })
    }
    response = requests.post(url, data=payload)
    print("✏️ Edited message:", response.json())
    return response.ok

# -------------------------
# 🧾 Format message
# -------------------------
def format_crypto_message(cryptos):
    emojis = ["🚀", "🪙", "💰", "📈", "🔥", "✅", "🤑", "👑", "🔶", "🔷"]
    message = "*💸 Live Cryptocurrency Prices:*\n\n"
    for coin in cryptos:
        emoji = random.choice(emojis)
        symbol = coin['symbol'].upper()
        price = f"{coin['current_price']:,}"
        message += f"{emoji} {'$'}*{symbol}*: ${price}\n"
    return message

# -------------------------
# 🧠 Main program execution
# -------------------------
def main():
    print(f"\n🚀 Starting bot with interval {INTERVAL} seconds. Ctrl+C to stop.\n")

    cryptos = get_top_cryptos()
    message = format_crypto_message(cryptos)

    # Get BTC price for the button
    btc_price = next(coin['current_price'] for coin in cryptos if coin['symbol'] == 'btc')
    
    message_id = send_to_telegram(BOT_TOKEN, CHAT_ID, message, btc_price)
    print(f"📨 Sent initial message (ID: {message_id})")

    while True:
        try:
            time.sleep(INTERVAL)
            cryptos = get_top_cryptos()
            new_message = format_crypto_message(cryptos)
            btc_price = next(coin['current_price'] for coin in cryptos if coin['symbol'] == 'btc')
            if message_id:
                success = edit_message(BOT_TOKEN, CHAT_ID, message_id, new_message, btc_price)
                if success:
                    print("✅ Updated message.")
                else:
                    print("❌ Failed to update message.")
            else:
                print("⚠️ Message ID not found.")

        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(INTERVAL)

# -------------------------
# 🏁 Start
# -------------------------
if __name__ == "__main__":
    main()
