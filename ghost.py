import json
import platform
import random
import shutil
import subprocess
import time
from plyer import notification
import psutil


# load config (yeah, just a simple wrapper)
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()

blacklist = config["blacklist"]
interval = config["interval"]
exit_message = config["exit"]


def send_notification(title, message):
    # try the normal way first
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except Exception:
        # eh, whatever
        pass

    # macOS is always special, cause i have a mac and it’s the only platform i care about for this project, so here we are
    if platform.system() == "Darwin":
        notifier = shutil.which("terminal-notifier") or "/opt/homebrew/bin/terminal-notifier"

        if shutil.which(notifier):
            subprocess.run(
                [
                    notifier,
                    "-title", title,
                    "-message", message,
                    "-sound", "default"
                ],
                check=False
            )

        # fallback apple-script thing
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display alert {json.dumps(title)} message {json.dumps(message)} as warning giving up after 5'
            ],
            check=False
        )


def haunt(app):
    # spooky ascii (don’t ask)
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
    send_notification("Ghostly Warning", f"Stop using {app}, boss.")


def check_apps(blacklist):
    detected = set()

    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info.get("name")
            if not name:
                continue

            lower = name.lower()
            for blocked in blacklist:
                if blocked.lower() in lower:
                    detected.add(blocked)

        except Exception:
            # processes are weird sometimes
            pass

    for app in sorted(detected):
        print(f"Detected: {app}")
        haunt(app)

    print()  # spacing for sanity


# main loop (infinite, because discipline)
while True:
    try:
        check_apps(blacklist)
        time.sleep(interval)
    except KeyboardInterrupt:
        print("\n")
        print(random.choice(exit_message))
        break
