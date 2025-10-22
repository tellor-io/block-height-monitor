# Block Height Monitor

This is a simple script / bot that compares the web3 BlockNumber of two different nodes. The bot will send an alerts (discord messages) if various conditions are met relating to the health of the node and their RPCs.

### Setup
```sh
git clone https://github.com/tellor-io/block-height-monitor
```
```sh
cd block-height-monitor
```
```sh
mv .env.example .env
```
```sh
python3 -m venv env
```
```sh
source env/bin/activate
```
```sh
pip install -e .
```
### Usage
Add your rpc and webhook urls to `.env` file. Update the `INTERVAL` to your desired frequency.

**To begin monitoring block height**
```sh
monitor
```
