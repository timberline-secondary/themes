import os.path
import sys
import math
import pygame
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Every key on the number pad can be in a code (0-9 . + - * /), and a code plays <code>.mp3.
# But * and / can't be in a file name (/ is a folder, and USB sticks formatted for Windows
# don't allow *), so those themes' file names have letters in their place: typing 2*2 plays
# 2x2.mp3, and 3/4 plays 3d4.mp3. (The Hackerspace control panel names them this way.)
# Codes starting with * are still admin codes.
FILE_NAME_SWAPS = {"*": "x", "/": "d"}


# Every code typed is noted in keypad.log (next to this file), with the time and what
# happened, so it can be watched live (e.g. from the Hackerspace control panel's "Watch the
# keypad"). Admin codes are never written down: they're the passwords from .env.
KEYPAD_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keypad.log")
MAX_LOG_BYTES = 1_000_000  # then it's moved to keypad.log.1 and a new one is started


def file_name(code):
    """The theme file a code plays: '2+2' -> '2+2.mp3', '2*2' -> '2x2.mp3'."""
    return "".join(FILE_NAME_SWAPS.get(key, key) for key in code) + ".mp3"


class ThemePlayer:

    def __init__(self, spamblock_time, theme_path, spamblock_pw, error_sfx_pw, spamblock_time_remaining_pw):
        self.not_ssh_connection: bool = len(sys.argv) <= 1

        self.theme_path: str = theme_path
        self.spamblock_pw: str = spamblock_pw  # str as int
        self.error_sfx_pw: str = error_sfx_pw
        self.spamblock_time = spamblock_time
        self.spamblock_remaining_pw = spamblock_time_remaining_pw

        self.error_noise_on: bool = True
        self.last_played = {}  # dict containing {"code": time_last_played}
        # where codes come from, for keypad.log: the keypad, or a copy started over ssh
        self.source = "keypad" if self.not_ssh_connection else "ssh"

    def log(self, code, what):
        """Note a typed code, and what happened, in keypad.log. Never stops the player."""
        try:
            if os.path.exists(KEYPAD_LOG) and os.path.getsize(KEYPAD_LOG) > MAX_LOG_BYTES:
                os.replace(KEYPAD_LOG, KEYPAD_LOG + ".1")
            with open(KEYPAD_LOG, "a") as log_file:
                log_file.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {self.source:<6}  "
                               f"{code:<12}  {what}\n")
        except OSError:
            pass

    def execute_admin_code(self, code):
        """
        Handles the admin codes that are entered into the theme player.
        """
        if code == self.error_sfx_pw:
            self.error_noise_on = not self.error_noise_on
            self.log("(admin)", f"error sounds turned {'on' if self.error_noise_on else 'off'}")
            return
        elif code == self.spamblock_pw:  # if the code entered is the spamblock password
            print("Please the time in minutes:")

            time_inputted = input("> ")
            self.spamblock_time = time_inputted
            print(f"Spam block is now set to {time_inputted}")
            self.log("(admin)", f"spam block set to {time_inputted} minutes")
            return
        elif code == self.spamblock_remaining_pw:
            print("Please enter the song you wish to query:")

            song_queried = input("> ")
            self.log("(admin)", f"asked how long {song_queried} is spam-blocked for")
            spam_delta = timedelta(minutes=int(self.spamblock_time))

            try:
                spam_block_time_remaining = self.last_played[song_queried] + spam_delta - datetime.now()
                minutes = math.ceil(spam_block_time_remaining.total_seconds() / 60)
                if spam_block_time_remaining.days > -1:
                    os.system(
                        f"espeak -a 200 '{minutes if minutes > 0 else spam_block_time_remaining.seconds} {'minutes' if minutes > 0 else 'seconds'}' 2>/dev/null")
                    print(f"Spamblocker time remaining (hh:mm:ss): {spam_block_time_remaining}")
                    return
                else:
                    print("Not blocked.")
                    return
            except KeyError:  # Code has never been played before, so doesn't have a key in the last_played dictionary
                print("Never played.")
                return
        else:
            self.log("(admin)", "not an admin code")
            return

    def find(self, code):
        """ 
        Manages input values by first checking if the value is a special command, 
        if not, then check if the value matches the name of an mp3 file in self.theme_path
        """

        if code == "":
            return

        if code == "exit":
            self.log(code, "stopped the player")
            sys.exit()

        if code[0] == "*":
            self.execute_admin_code(code)
            return

        filepath = os.path.join(self.theme_path, file_name(code))
        if os.path.exists(filepath):  # if the file exists
            print(f"Found {filepath}")
            if not self.is_spamblocked(code):
                self.last_played[code] = datetime.now()
                self.log(code, f"played {file_name(code)}")
                self.play(filepath)

        else:
            self.log(code, f"not found (there's no {file_name(code)})")
            if self.error_noise_on:
                pygame.mixer.music.load('./media/not_found.mp3')
                pygame.mixer.music.play()

            print(f"File '{file_name(code)}' not found.\n")

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
                minutes = math.ceil(spam_block_time_remaining.total_seconds() / 60)
                self.log(code, f"spam-blocked ({minutes} more minute{'s' if minutes != 1 else ''})")
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
        if self.not_ssh_connection:
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
    CHECK_SPAM_TIME_PASSWORD = os.getenv('CHECK_SPAM_TIME_PASSWORD')

    player = ThemePlayer(DEFAULT_SPAMBLOCK, THEME_PATH, SPAMBLOCK_PASSWORD, ERROR_SFX_PASSWORD,
                         CHECK_SPAM_TIME_PASSWORD)
    player.run()
