import os.path
import pygame
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

THEME_PATH = os.getenv('THEME_PATH')
SPAMBLOCK_PASSWORD = os.getenv('SPAMBLOCK_PASSWORD')
DEFAULT_SPAMBLOCK = os.getenv('DEFAULT_SPAMBLOCK')

spamblock = {"time": DEFAULT_SPAMBLOCK, "waiting": False}
latest = {}


def find(name):
    if spamblock["waiting"]:  # if the spamblock is waiting for minute entry
        spamblock["time"] = name
        print(f"Spam block is now set to {spamblock['time']}")
        spamblock["waiting"] = False
        return
    if name == SPAMBLOCK_PASSWORD:  # if the code entered is the spamblock password
        spamblock["waiting"] = True
        return
    if os.path.exists(f"{THEME_PATH}{name}.mp3"):  # if the file exists
        print("File exists.\n")
        if not spamblock["time"] and name in latest and latest[name] + timedelta(
                minutes=int(spamblock["time"])) > datetime.now():
            print(f"{name} is too recent.")
            return
        pygame.mixer.music.load(f"{THEME_PATH}{name}.mp3")
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
    pygame.mixer.init()
    pygame.mixer.music.load("./start.mp3")
    pygame.mixer.music.play()
    while True:
        print("Please enter the code:")

        code = input("> ")

        find(code)


if __name__ == "__main__":
    main()
