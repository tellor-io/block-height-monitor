# Block Height Monitor

This is a simple script / bot that compares the web3 BlockNumber of two different nodes. The bot will send an alert (discord message) if the two nodes' block numbers don't match, or if one of the nodes is catching up. 

### Clone repo and cd
```sh
git clone https://github.com/tellor-io/block-height-monitor
```
```sh
cd block-height-monitor
```
```sh
mv .env.example .env
```

### Setup

```sh
python3 -m venv venv
```
```sh
source venv/bin/activate
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
