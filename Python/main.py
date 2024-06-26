import LV1, LV2
import start_menu
import importlib
import pygame
from sys import platform

pygame.mixer.init()
if platform == "linux" or platform == "linux2":
    pass
elif platform == "darwin":
    shot_sound = pygame.mixer.Sound("Sounds/Player/170161__timgormly__8-bit-laser.aiff")
    reloading_sound = pygame.mixer.Sound("Sounds/Player/143610__dwoboyle__weapons-synth-blast-02.wav")
    jumping_sound = pygame.mixer.Sound("Sounds/Player/399095__plasterbrain__8bit-jump.flac")
    is_hit_sound = pygame.mixer.Sound("Sounds/Player/143610__dwoboyle__weapons-synth-blast-02.wav")
    pygame.mixer.music.load("Sounds/Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav")
elif platform == "win32":
    shot_sound = pygame.mixer.Sound("Sounds\\Player\\170161__timgormly__8-bit-laser.aiff")
    reloading_sound = pygame.mixer.Sound("Sounds\\Player\\143610__dwoboyle__weapons-synth-blast-02.wav")
    jumping_sound = pygame.mixer.Sound("Sounds\\Player\\399095__plasterbrain__8bit-jump.flac")
    is_hit_sound = pygame.mixer.Sound("Sounds\\Player/143610__dwoboyle__weapons-synth-blast-02.wav")
    pygame.mixer.music.load("Sounds\\Background/696485__gis_sweden__minimal-tech-background-music-mtbm02.wav")
pygame.mixer.music.play(-1,0.0)
shot_sound.set_volume(0.8)


def sound_hit():
    is_hit_sound.play()

def sound_jump():
    jumping_sound.play()

def sound_reloading():
    reloading_sound.play()

def sound_shot():
    shot_sound.play()





def main():
    pygame.init()

    Options_prototype = {
        "master volume":1,
        "jump volume":1,
        "shot volume":1,
    }
    is_hit_sound.set_volume(0.8*Options_prototype["master volume"])
    jumping_sound.set_volume(0.8*Options_prototype["master volume"]*Options_prototype["jump volume"])
    reloading_sound.set_volume(0.2*Options_prototype["master volume"]*Options_prototype["shot volume"])
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
