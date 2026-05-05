import json

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

config = load_config()

blacklist = config["blacklist"]
interval = config["interval"]
