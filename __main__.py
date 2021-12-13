import os.path
import pygame


THEMEPATH = os.getenv('THEMEPATH')
BYPASS = os.getenv('BYPASS')

def find(name):
    if os.path.exists(f"{THEMEPATH}{name}.mp3"):
        print("File exists.\n")
        pygame.mixer.init()
        pygame.mixer.music.load(f"{THEMEPATH}{name}.mp3")
        pygame.mixer.music.play()
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

        code = input()

        find(code)


main()
