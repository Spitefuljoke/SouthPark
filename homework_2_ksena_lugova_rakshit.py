!pip install vk_api

import os
import requests
import json
import vk_api


# Part 1: get quote

def get_random_quote():
    url = "https://southparkquotes.onrender.com/v1/quotes"
    try:
        response = requests.get(url)
        # Check for HTTP errors
        response.raise_for_status()
        data = response.json()
        # The API returns a list of dictionaries, we need the first element
        if isinstance(data, list) and len(data) > 0:
            # Quote from the dictionary
            return f'"{data[0]["quote"]}"\n\n- {data[0]["character"]}'
        else:
            return "Failed to get quote: incorrect API response"
    except requests.exceptions.RequestException as e:
        print(f"Error when requesting API: {e}")
        return "Failed to get quote"
    except KeyError as e:
        print(f"Error processing API data: missing key {e}")
        return "Failed to get quote: missing data"


# Part 2: send it to VK

# Get VK_TOKEN and PEER_ID from environment variables
VK_TOKEN = os.getenv('vk_token')
PEER_ID_STR = os.getenv('peer_id')

if not VK_TOKEN:
    print("Error: VK_TOKEN environment variable not set.")
    # For local testing in Colab, you might temporarily uncomment and use your token here:
    # VK_TOKEN = 'your_vk_token_here_for_local_testing'

if not PEER_ID_STR:
    print("Error: VK_PEER_ID environment variable not set.")
    # For local testing in Colab, you might temporarily uncomment and use your peer ID here:
    # PEER_ID = 9712850 # Example ID
    PEER_ID = None
else:
    try:
        PEER_ID = int(PEER_ID_STR)
    except ValueError:
        print(f"Error: VK_PEER_ID '{PEER_ID_STR}' is not a valid integer.")
        PEER_ID = None


def send_quote_via_group(quote_text):
    if not VK_TOKEN or PEER_ID is None:
        print("Cannot send quote: VK_TOKEN or VK_PEER_ID not properly configured.")
        return

    try:
        # Authenticate in VK
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()

        # Send the message
        vk.messages.send(
            peer_id=PEER_ID,
            message=quote_text,
            random_id=0  # Parameter for message identification
        )
        print("Quote sent successfully!")
    except vk_api.exceptions.ApiError as e:
        print(f"Error sending quote: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Get a random quote and send it via VK
quote_to_send = get_random_quote()
send_quote_via_group(quote_to_send)
