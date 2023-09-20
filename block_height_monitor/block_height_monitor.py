import logging
import os
import time
from typing import Union

from discordwebhook import Discord
from dotenv import load_dotenv
from eth_typing.evm import BlockNumber
from web3 import Web3

from block_height_monitor import config

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="logs.log", filemode="a"
)

# Create a logger object
logger = logging.getLogger("block_height_monitor")
logger.setLevel(logging.INFO)  # Set the minimum log level

# Create a file handler to save logs to a file
file_handler = logging.FileHandler("logs.log", mode="a")
file_handler.setLevel(logging.INFO)  # Set the minimum log level for the file handler

# Create a console handler to print logs to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the minimum log level for the console handler

# Create a formatter to define the log message format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Set the formatter for both handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
# add the handler to the root logger
logging.getLogger("").addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# read variables from .env
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
PRIMARY_NODE_ENDPOINT = os.getenv("PRIMARY_NODE_ENDPOINT")
SECONDARY_NODE_ENDPOINT = os.getenv("SECONDARY_NODE_ENDPOINT")

# read variables from config.py
interval = config.interval

# set variables
alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
primary = Web3(Web3.HTTPProvider(PRIMARY_NODE_ENDPOINT))
secondary = Web3(Web3.HTTPProvider(SECONDARY_NODE_ENDPOINT))


def get_primary_block(primary: Web3) -> Union[BlockNumber, None]:
    try:
        primary_block_number = primary.eth.block_number
        logging.info(f"Primary node highest block: {primary_block_number}")
        return primary_block_number
    except Exception:
        return None


def get_secondary_block(secondary: Web3) -> Union[BlockNumber, None]:
    try:
        secondary_block_number = secondary.eth.block_number
        logging.info(f"Secondary node highest block: {secondary_block_number}")
        return secondary_block_number
    except Exception:
        return None


alarms = 0


def main() -> int:
    while True:
        if get_primary_block(primary) == get_secondary_block(secondary):
            alarms = 0
            logging.info("Node is all good. \U0001F60E")
            time.sleep(interval)
        elif get_primary_block(primary) == None:
            logging.info("Primary node could not be reached. Trying again in 60s...")
            alert_bot.post(content="Primary node could not be reached.")
            time.sleep(60)
        elif get_secondary_block(secondary) == None:
            logging.info("Secondary node could not be reached. Trying again in 60s...")
            alert_bot.post(content="Secondary node could not be reached.")
            time.sleep(60)
        else:
            alarms = alarms + 1
            alert_bot.post(content="\U0001F6A8 NODE IS OUT OF SYNC! \U0001F6A8")
            logging.info("NODES MAY BE OUT OF SYNC! \U0001F6A8 ALERT SENT!")
            if alarms > 5:
                logging.info("node is drunk send shutdown signal")
                # alert_bot.post(content="Node shutdown signal sent. Switch to backup nodes now!")
                time.sleep(3600)
            else:
                time.sleep(60)
