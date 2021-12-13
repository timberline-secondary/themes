import os.path
import pygame


# import vlc

def find(name):
    if os.path.exists(f"./songs/{name}.mp3"):
        print("File exists.\n")
        pygame.mixer.init()
        pygame.mixer.music.load(f"./songs/{name}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        main()
    else:
        print(f"No file found @ ./songs/{name}.mp3\n")
        main()


def main():
    print("Please enter the code:")

    code = input()

    find(code)


main()
