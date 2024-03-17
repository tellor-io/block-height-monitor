import logging
import os
import time
from typing import Union
import asyncio

from discordwebhook import Discord
from dotenv import load_dotenv
from eth_typing.evm import BlockNumber
from web3 import Web3

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="logs.log", filemode="a"
)

# Create a logger object
logger = logging.getLogger("block_height_check")
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

# set Web3 variables
primary = Web3(Web3.HTTPProvider(PRIMARY_NODE_ENDPOINT))
secondary = Web3(Web3.HTTPProvider(SECONDARY_NODE_ENDPOINT))


# get block number from Primary node
async def get_primary_block(primary: Web3) -> Union[BlockNumber, None]:
    try:
        primary_block_number = primary.eth.block_number
        logging.info(f"Primary node highest block: {primary_block_number}")
        return primary_block_number
    except Exception:
        return None


# get block number from Secondary node
async def get_secondary_block(secondary: Web3) -> Union[BlockNumber, None]:
    try:
        secondary_block_number = secondary.eth.block_number
        logging.info(f"Secondary node highest block: {secondary_block_number}")
        return secondary_block_number
    except Exception:
        return None


# the main script
async def main() -> None:
    primary_block_number = await get_primary_block(primary)
    secondary_block_number = await get_secondary_block(secondary)
    alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
    if primary_block_number == secondary_block_number and primary_block_number is not None:
            logging.info("Node is all good bro \U00002705")
    else:
            logging.info("\U0001F6A8 CHECK NODE SYNC STATUS! \U0001F6A8")
            alert_bot.post(content="\U0001F6A8 CHECK NODE SYNC STATUS! \U0001F6A8")

if __name__ == "__main__":
    asyncio.run(main())