import asyncio
import logging
import os
from typing import Union

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
async def get_primary_block(primary: Web3) -> Union[BlockNumber]:
    try:
        primary_block_number = primary.eth.block_number
        logging.info(f"Primary node highest block: {primary_block_number}")
        return primary_block_number
    except Exception as e:
        raise ValueError(f"Invalid response from primary node {e}")


# get block number from Secondary node
async def get_secondary_block(secondary: Web3) -> Union[BlockNumber]:
    try:
        secondary_block_number = secondary.eth.block_number
        logging.info(f"Secondary node highest block: {secondary_block_number}")
        return secondary_block_number
    except Exception as e:
        raise ValueError(f"Invalid response from secondary node {e}")


# the main script
async def main() -> None:
    primary_block_number = await get_primary_block(primary)
    secondary_block_number = await get_secondary_block(secondary)
    alert_bot = Discord(url=DISCORD_WEBHOOK_URL)

    if primary_block_number == secondary_block_number:
        logging.info("Node is all synced up \U00002705")
        alert_bot.post(content="Node is all synced up \U00002705")

    elif primary_block_number < secondary_block_number:
        sync_percentage = (primary_block_number / secondary_block_number) * 100
        truncated_sync_percentage = float(f"{sync_percentage:.2f}")
        logging.info("\U0001F6A8 NODE IS SYNCING? \U0001F6A8")
        logging.info(f"Node is {truncated_sync_percentage}% synced")
        alert_bot.post(content=f"\U0001F6A8 NODE IS SYNCING? {truncated_sync_percentage}% synced")

    else:
        logging.info("Broken :( Check nodes or setup.")
        alert_bot.post(content="Broken :( Check nodes or setup.")


if __name__ == "__main__":
    asyncio.run(main())
