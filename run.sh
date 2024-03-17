#!/bin/bash

# Kill the existing Python process
pkill -f block_height_monitor/check_node.py

# Wait for a few seconds to ensure the process has been terminated
sleep 5

# Restart the Python process
nohup python block_height_monitor/check_node.py &
