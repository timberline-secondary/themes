import os.path
import pygame
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

THEMEPATH = os.getenv('THEMEPATH')
BYPASS = os.getenv('BYPASS')

bypass = {"state": False}
latest = {}

def find(name):
    if name == BYPASS:
        bypass["state"] = not bypass["state"]
        print(f"Spam block is now {'off' if bypass['state'] else 'on'}")
        return
    if os.path.exists(f"{THEMEPATH}{name}.mp3"):
        print("File exists.\n")
        if not bypass["state"] and name in latest and latest[name] + timedelta(minutes=2) > datetime.now():
            print(f"{name} is too recent.")
            return
        pygame.mixer.init()
        pygame.mixer.music.load(f"{THEMEPATH}{name}.mp3")
        pygame.mixer.music.play()
        latest[name] = datetime.now()
        # !! Need to test how loud, if too loud use pygame.mixer.set_volume(float)
        while pygame.mixer.music.get_busy():
            continue
        return
    else:
        print(f"File '{name}.mp3' not found.\n")
        return


def main():
    while True:
        print("Please enter the code:")

        code = input("> ")

        find(code)


main()
