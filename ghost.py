import json
import random
from plyer import notification

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

def haunt(app):
    print("""
      ___
     /   \\
    / O O \\
   |   U   |
 , |       | ,
  \\/(     )\\/
   | )   ( |
   |(     )|
   ||   | |'
   `|   | |
    |   | |
    |   /-'
    |_.'       
          """)
    
    print(f"Stop using {app}, boss.")

def check_apps(blacklist):
    current_detected = set()

    for proc in psutil.process_iter(["name"]):
        try:
            app_name = proc.info["name"]
            if app_name is None:
                continue
            lower_name = app_name.lower()

            for blocked in blacklist:
                if blocked.lower() in lower_name:
                    current_detected.add(blocked)
                    
        except:
            pass

    for app in sorted(current_detected):
        print(f"Detected: {app}")

    print()

# infinite loop
while True:
    try:
        check_apps(blacklist)
        
        #print("\n")
        time.sleep(interval) 
    except KeyboardInterrupt:
        print("\n")
        print(random.choice(exit_message))
        break
