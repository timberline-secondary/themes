import os.path
import sys
import pygame
from dotenv import load_dotenv
from datetime import datetime, timedelta


class ThemePlayer:

    def __init__(self, spamblock_time, theme_path, spamblock_pw, error_sfx_pw):
        self.theme_path: str = theme_path
        self.spamblock_pw: str = spamblock_pw  # str as int
        self.error_sfx_pw: str = error_sfx_pw
        self.spamblock_time = spamblock_time

        self.error_noise_on: bool = True
        self.last_played = {}  # dict containing {"code": time_last_played}

    def find(self, code):
        """ 
        Manages input values by first checking if the value is a special command, 
        if not, then check if the value matches the name of an mp3 file in self.theme_path
        """

        if code == "exit":
            sys.exit()

        if code == self.error_sfx_pw:
            self.error_noise_on = not self.error_noise_on
            return

        if code == self.spamblock_pw:  # if the code entered is the spamblock password
            print("Please the time in minutes:")

            time_inputted = input("> ")
            self.spamblock_time = time_inputted
            print(f"Spam block is now set to {time_inputted}")
            return

        filepath = f"{self.theme_path}/{code}.mp3"
        if os.path.exists(filepath):  # if the file exists
            print(f"Found {filepath}")
            if not self.is_spamblocked(code):
                self.last_played[code] = datetime.now()
                self.play(filepath)

        else:
            if self.error_noise_on:
                pygame.mixer.music.load('./media/not_found.mp3')
                pygame.mixer.music.play()

            print(f"File '{code}.mp3' not found.\n")

    def is_spamblocked(self, code):
        """ If the code was last played within the spamblock time, return True."""
        spam_delta = timedelta(minutes=int(self.spamblock_time))

        try:
            spam_block_time_remaining = self.last_played[code] + spam_delta - datetime.now()
            if spam_block_time_remaining.days > -1:
                if self.error_noise_on:
                    pygame.mixer.music.load('./media/spamblock.mp3')
                    pygame.mixer.music.play()
                print(f"Not gonna play! Spamblocker time remaining (hh:mm:ss): {spam_block_time_remaining}")
                return True
            else:
                return False
        except KeyError:  # Code has never been played before, so doesn't have a key in the last_played dictionary
            return False

    @staticmethod
    def play(filepath):
        """
        Play the song.  Don't return the method until the song is finished playing.
        Assumes the filepath exists as a playable mp3 file.
        """
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

        # !! Need to test how loud, if too loud use pygame.mixer.set_volume(float)
        while pygame.mixer.music.get_busy():
            continue

    def run(self):
        pygame.mixer.init(buffer=1024)
        pygame.mixer.music.load("./media/start.mp3")
        pygame.mixer.music.play()
        while True:
            print("Please enter a code:")

            code = input("> ")

            self.find(code)


if __name__ == "__main__":
    load_dotenv()

    THEME_PATH = os.getenv('THEME_PATH')
    SPAMBLOCK_PASSWORD = os.getenv('SPAMBLOCK_PASSWORD')
    ERROR_SFX_PASSWORD = os.getenv('ERROR_SFX_PASSWORD')
    DEFAULT_SPAMBLOCK = os.getenv('DEFAULT_SPAMBLOCK')

    player = ThemePlayer(DEFAULT_SPAMBLOCK, THEME_PATH, SPAMBLOCK_PASSWORD, ERROR_SFX_PASSWORD)
    player.run()
