import asyncio
import logging
import os
import time
import tracemalloc
from typing import Optional, Union

import requests
from discordwebhook import Discord
from dotenv import load_dotenv
from eth_typing.evm import BlockNumber
from web3 import Web3


load_dotenv()

tracemalloc.start()

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
timeout = 10  # Timeout in seconds
# Get the interval from the .env file
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

# Create persistent HTTP sessions for connection reuse
primary_session = requests.Session()
primary_session.headers.update({'Content-Type': 'application/json'})
secondary_session = requests.Session()
secondary_session.headers.update({'Content-Type': 'application/json'})

# Create Web3 instances once and reuse them (with persistent sessions)
primary = Web3(Web3.HTTPProvider(
    PRIMARY_NODE_ENDPOINT, 
    request_kwargs={"timeout": timeout},
    session=primary_session
))
secondary = Web3(Web3.HTTPProvider(
    SECONDARY_NODE_ENDPOINT, 
    request_kwargs={"timeout": timeout},
    session=secondary_session
))

# get block number from Primary node
async def get_primary_block() -> Optional[BlockNumber]:
    try:
        start_time = time.time()
        primary_block_number = primary.eth.get_block_number()
        response_time = time.time() - start_time
        logging.info(f"Primary node highest block: {primary_block_number} (response time: {response_time:.3f}s)")
        return primary_block_number
    except Exception as e:
        logging.error(f"Failed to connect to Primary node: {e}")
        alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
        alert_bot.post(content=f"Failed to connect to Primary node: {e}")
        return None


# get block number from Secondary node
async def get_secondary_block() -> Optional[BlockNumber]:
    try:
        start_time = time.time()
        secondary_block_number = secondary.eth.get_block_number()
        response_time = time.time() - start_time
        logging.info(f"Secondary node highest block: {secondary_block_number} (response time: {response_time:.3f}s)")
        return secondary_block_number
    except Exception as e:
        logging.error(f"Failed to connect to Secondary node: {e}")
        alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
        alert_bot.post(content=f"Failed to connect to Secondary node: {e}")
        return None


# the main script
async def check_node() -> None:
    """queries the nodes and sends alerts if something is off"""
    try:
        alert_bot = Discord(url=DISCORD_WEBHOOK_URL)

        primary_block_number = await get_primary_block()
        if primary_block_number is None:
            return

        secondary_block_number = await get_secondary_block()
        if secondary_block_number is None:
            return

        block_diff = abs(primary_block_number - secondary_block_number)
        
        if block_diff <= 10:
            logging.info(f"Node is synced (block difference: {block_diff}) ✅")
            return

        elif block_diff > 10:
            logging.info(f"\U0001F6A8 Node heights are different \U0001F6A8")
            logging.info(f"Primary node: {primary_block_number}, Secondary node: {secondary_block_number}")
            alert_bot.post(content=f"\U0001F6A8 Node heights are different. Primary: {primary_block_number}, Secondary: {secondary_block_number}")
            return

        else:
            logging.info("Bot may be broken.\U0001FAE0")
            alert_bot.post(content="Bot may be broken.\U0001FAE0")
            return

    except Exception as e:
        logging.error(f"Bot is broken?(everything's broken?): {e}")
        alert_bot = Discord(url=DISCORD_WEBHOOK_URL)
        alert_bot.post(content=f"Bot is broken?(everything's broken? {e}")
        return None


async def main()-> None:
    while True:
        await check_node()
        await asyncio.sleep(CHECK_INTERVAL)


asyncio.run(main())
