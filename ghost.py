import json
import random

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

config = load_config()

blacklist = config["blacklist"]
interval = config["interval"]
exit_message = config["exit"]

import psutil
import time

def check_apps(blacklist):
    for proc in psutil.process_iter(["name"]):
        try:
            app_name = proc.info["name"]
            if app_name is None:
                continue
            lower_name = app_name.lower()

            for blocked in blacklist:
                if blocked.lower() in lower_name:
                    print(f"Haunt 👻: {app_name}")
        except:
            pass

# infinite loop
while True:
    try:
        check_apps(blacklist)
        time.sleep(interval) 
    except KeyboardInterrupt:
        print("\n")
        num = random.randint(1, 25)
        print(exit_message[num])        
        break
