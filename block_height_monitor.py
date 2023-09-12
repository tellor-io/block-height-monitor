import time
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

PRIMARY_NODE_ENDPOINT = os.getenv("PRIMARY_NODE_ENDPOINT")
SECONDARY_NODE_ENDPOINT = os.getenv("SECONDARY_NODE_ENDPOINT")
INTERVAL = os.getenv("INTERVAL")

primary = Web3(Web3.HTTPProvider(PRIMARY_NODE_ENDPOINT))
secondary = Web3(Web3.HTTPProvider(SECONDARY_NODE_ENDPOINT))

def block_height_monitor(primary, secondary):

        try:
            primary_block_number = primary.eth.block_number
            print(f"Primary node highest block: {primary_block_number}")
        except Exception as e:
            print("ERROR REACHING PRIMARY NODE: {e}")

        try:
            secondary_block_number = secondary.eth.block_number
            print(f"Secondary node highest block: {secondary_block_number}")
        except Exception as e:
            print("ERROR REACHING SECONDARY NODE: {e}")
        if abs(primary_block_number-secondary_block_number) < 2:
            print("Node is all good.")
            while True:
                time.sleep(30)
                block_height_monitor(primary, secondary)
        else:
            print("NODE IS OUT OF SYNC!")

block_height_monitor(primary, secondary)