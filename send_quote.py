{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4bc918cc-21e6-4a7e-bbc8-176cbb8654e2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Error: VK_TOKEN not set\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[31mSystemExit\u001b[39m\u001b[31m:\u001b[39m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Professional\\anaconda3\\Lib\\site-packages\\IPython\\core\\interactiveshell.py:3707: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import sys\n",
    "import requests\n",
    "import vk_api\n",
    "\n",
    "# Part 1: get quote\n",
    "def get_random_quote():\n",
    "    url = \"https://southparkquotes.onrender.com/v1/quotes\"\n",
    "    try:\n",
    "        response = requests.get(url)\n",
    "        response.raise_for_status()\n",
    "        data = response.json()\n",
    "        if isinstance(data, list) and len(data) > 0:\n",
    "            return f'\"{data[0][\"quote\"]}\"\\n\\n- {data[0][\"character\"]}'\n",
    "        else:\n",
    "            return \"Failed to get quote: incorrect API response\"\n",
    "    except Exception as e:\n",
    "        print(f\"Error fetching quote: {e}\")\n",
    "        return \"Failed to get quote\"\n",
    "\n",
    "# Part 2: send to VK\n",
    "VK_TOKEN = os.getenv('VK_TOKEN')\n",
    "PEER_ID_STR = os.getenv('PEER_ID')\n",
    "\n",
    "if not VK_TOKEN:\n",
    "    print(\"Error: VK_TOKEN environment variable not set\")\n",
    "    sys.exit(1)\n",
    "if not PEER_ID_STR:\n",
    "    print(\"Error: PEER_ID environment variable not set\")\n",
    "    sys.exit(1)\n",
    "\n",
    "try:\n",
    "    PEER_ID = int(PEER_ID_STR)\n",
    "except ValueError:\n",
    "    print(f\"Error: PEER_ID '{PEER_ID_STR}' is not a valid integer\")\n",
    "    sys.exit(1)\n",
    "\n",
    "def send_quote_via_group(quote_text):\n",
    "    try:\n",
    "        vk_session = vk_api.VkApi(token=VK_TOKEN)\n",
    "        vk = vk_session.get_api()\n",
    "        vk.messages.send(\n",
    "            peer_id=PEER_ID,\n",
    "            message=quote_text,\n",
    "            random_id=0\n",
    "        )\n",
    "        print(\"Quote sent successfully!\")\n",
    "    except Exception as e:\n",
    "        print(f\"Error sending quote: {e}\")\n",
    "        sys.exit(1)\n",
    "\n",
    "# Main\n",
    "print(\"Starting South Park quote bot...\")\n",
    "quote_to_send = get_random_quote()\n",
    "if not quote_to_send:\n",
    "    print(\"No quote received, exiting.\")\n",
    "    sys.exit(1)\n",
    "send_quote_via_group(quote_to_send)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ae10346d-45eb-41d1-84af-73539b734ea4",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
