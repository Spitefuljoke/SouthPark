import os
import sys
import requests
import vk_api

def get_random_quote():
    url = "https://southparkquotes.onrender.com/v1/quotes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return f'"{data[0]["quote"]}"\n\n- {data[0]["character"]}'
        else:
            return "Failed to get quote: incorrect API response"
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Failed to get quote"

VK_TOKEN = os.getenv('VK_TOKEN')
PEER_ID_STR = os.getenv('PEER_ID')

if not VK_TOKEN:
    print("Error: VK_TOKEN not set")
    sys.exit(1)
if not PEER_ID_STR:
    print("Error: PEER_ID not set")
    sys.exit(1)

try:
    PEER_ID = int(PEER_ID_STR)
except ValueError:
    print(f"Error: PEER_ID '{PEER_ID_STR}' is not an integer")
    sys.exit(1)

def send_quote_via_group(quote_text):
    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()
        vk.messages.send(peer_id=PEER_ID, message=quote_text, random_id=0)
        print("Quote sent successfully!")
    except Exception as e:
        print(f"Error sending quote: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting South Park quote bot...")
    quote = get_random_quote()
    if not quote:
        print("No quote received, exiting.")
        sys.exit(1)
    send_quote_via_group(quote)