import time
import os
import emoji
from web3 import Web3
from discordwebhook import Discord
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
PRIMARY_NODE_ENDPOINT = os.getenv("PRIMARY_NODE_ENDPOINT")
SECONDARY_NODE_ENDPOINT = os.getenv("SECONDARY_NODE_ENDPOINT")
INTERVAL = int(os.getenv("INTERVAL"))

alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
primary = Web3(Web3.HTTPProvider(PRIMARY_NODE_ENDPOINT))
secondary = Web3(Web3.HTTPProvider(SECONDARY_NODE_ENDPOINT))

def block_height_monitor(primary, secondary):
        try:
            primary_block_number = primary.eth.block_number
            print(f"Primary node highest block: {primary_block_number}")
        except Exception:
            print("ERROR REACHING PRIMARY NODE")
            alert_bot.post(content="Primary node could not be reached.")

        try:
            secondary_block_number = secondary.eth.block_number
            print(f"Secondary node highest block: {secondary_block_number}")
        except Exception:
            print("ERROR REACHING SECONDARY NODE")
            alert_bot.post(content="Secondary node could not be reached.")

        try: 
            confidence = abs(primary_block_number-secondary_block_number)
        except UnboundLocalError:
            print("Node cannot be reached. Trying again in 15s...")
            time.sleep(15)
            block_height_monitor(primary, secondary)

        if confidence < 2:
            print("Node is all good. \U0001F60E")
            time.sleep(INTERVAL)
            block_height_monitor(primary, secondary)
            
        elif confidence >= 2:
            alert_bot.post(content="\U0001F6A8 NODE IS OUT OF SYNC! \U0001F6A8")
            print("NODE IS OUT OF SYNC! \U0001F6A8 ALERT SENT!")
            time.sleep(60)
            block_height_monitor(primary, secondary)

block_height_monitor(primary, secondary)