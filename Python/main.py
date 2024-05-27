import LV1, LV2
import start_menu
import importlib
import pygame
from sys import platform


def main():
    pygame.init()

    Options_prototype = {
        "master volume":1,
        "jump volume":1,
        "shot volume":1,
    }

    pygame.mixer.init()
    if platform == "linux" or platform == "linux2":
        pass
    elif platform == "darwin":
        pygame.mixer.music.load("Sounds/Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav")
    elif platform == "win32":
        pygame.mixer.music.load("Sounds\\Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav")
    pygame.mixer.music.play(-1,0.0)

    levels = [LV1, LV2]
    coin_count = 0


    while True:
        selected_level, options = start_menu.main(coin_count,Options_prototype)
        Options_prototype = options
        pygame.mixer.music.set_volume(float(options["master volume"]))
        if selected_level == "exit":
            break
        print(selected_level)

        result = levels[selected_level-1].main(Options_prototype)
        coin_count += result
        importlib.reload(levels[selected_level-1])
        
def set_master_volume(volume):
    pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    main()
