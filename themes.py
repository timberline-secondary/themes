import os.path
import pygame
from dotenv import load_dotenv
from datetime import datetime, timedelta


class ThemePlayer:

    def __init__(self, spamblock_time, theme_path, spamblock_pw):
        self.theme_path: str = theme_path
        self.spamblock_pw: str = spamblock_pw  # str as int
        self.spamblock_time = spamblock_time
        self.waiting_for_spamblock_minutes_entry: bool = False
        self.latest = {}  # dict containing {"code": time}

    def find(self, value):

        if self.waiting_for_spamblock_minutes_entry:
            self.spamblock_time = value
            print(f"Spam block is now set to {self.spamblock_time}")
            self.waiting_for_spamblock_minutes_entry = False
            return

        if value == self.spamblock_pw:  # if the code entered is the spamblock password
            self.waiting_for_spamblock_minutes_entry = True
            return

        if os.path.exists(f"{self.theme_path}{value}.mp3"):  # if the file exists
            print("File exists.\n")
            if value in self.latest and self.latest[value] + timedelta(
                    minutes=int(self.spamblock_time)) > datetime.now():
                print(f"{value} is too recent.")
                return
            pygame.mixer.music.load(f"{self.theme_path}{value}.mp3")
            pygame.mixer.music.play()
            self.latest[value] = datetime.now()
            print(self.latest)

            # !! Need to test how loud, if too loud use pygame.mixer.set_volume(float)
            while pygame.mixer.music.get_busy():
                continue
            return
        else:
            print(f"File '{value}.mp3' not found.\n")
            return

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./start.mp3")
        pygame.mixer.music.play()
        while True:
            print("Please enter the code:")

            code = input("> ")

            self.find(code)


if __name__ == "__main__":
    load_dotenv()

    THEME_PATH = os.getenv('THEME_PATH')
    SPAMBLOCK_PASSWORD = os.getenv('SPAMBLOCK_PASSWORD')
    DEFAULT_SPAMBLOCK = os.getenv('DEFAULT_SPAMBLOCK')

    player = ThemePlayer(DEFAULT_SPAMBLOCK, THEME_PATH, SPAMBLOCK_PASSWORD)
    player.run()
