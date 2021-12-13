import os.path
import pygame


def find(name):
    if os.path.exists(f"./songs/{name}.mp3"):
        print("File exists.\n")
        pygame.mixer.init()
        pygame.mixer.music.load(f"./songs/{name}.mp3")
        pygame.mixer.music.play()
        # !! Need to test how loud, if too loud use pygame.mixer.set_volume(float)
        while pygame.mixer.music.get_busy():
            continue
        return
    else:
        print(f"No file found @ ./songs/{name}.mp3\n")
        return


def main():
    while True:
        print("Please enter the code:")

        code = input()

        find(code)


main()
