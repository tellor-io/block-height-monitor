import pytest
from block_height_monitor.monitor import PRIMARY_NODE_ENDPOINT, SECONDARY_NODE_ENDPOINT, get_primary_block, get_secondary_block, main
from web3 import Web3

primary = Web3(Web3.HTTPProvider(PRIMARY_NODE_ENDPOINT))
secondary = Web3(Web3.HTTPProvider(SECONDARY_NODE_ENDPOINT))

#tests will be here

    

    


