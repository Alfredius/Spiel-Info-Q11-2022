import LV1, LV2
import start_menu
import importlib
import pygame
import sys
from sys import platform

pygame.mixer.init()
if platform == "linux" or platform == "linux2":
    print("ERROR: Linux ist aktuell nicht supported.")
    print("Bitte kontaktiere mich oder mach es selber, ist ja nicht soo kompliziert, ich kanns nur nicht testen.")
    sys.exit()
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



Options_prototype = [{
        "music volume":1,
        "master volume":1,
        "jump volume":1,
        "shot volume":1,
    }]


def sound_hit():
    is_hit_sound.play()

def sound_jump():
    jumping_sound.play()

def sound_reloading():
    reloading_sound.play()

def sound_shot():
    shot_sound.play()



def set_volumes(Options_prototype):
    is_hit_sound.set_volume(0.8*Options_prototype["master volume"])
    jumping_sound.set_volume(0.8*Options_prototype["master volume"]*Options_prototype["jump volume"])
    reloading_sound.set_volume(0.2*Options_prototype["master volume"]*Options_prototype["shot volume"])
    shot_sound.set_volume(0.8*Options_prototype["master volume"]*Options_prototype["shot volume"])


def main():
    pygame.init()

    is_hit_sound.set_volume(0.8*Options_prototype[0]["master volume"])
    jumping_sound.set_volume(0.8*Options_prototype[0]["master volume"]*Options_prototype[0]["jump volume"])
    reloading_sound.set_volume(0.2*Options_prototype[0]["master volume"]*Options_prototype[0]["shot volume"])
    levels = [LV1, LV2]
    coin_count = 0

    level_count = 0

    while True:
        selected_level, options = start_menu.main(coin_count,Options_prototype[0],level_count)
        Options_prototype[0] = options
        # set_volumes(Options_prototype)
        pygame.mixer.music.set_volume(float(options["master volume"])*float(options["music volume"]))
        is_hit_sound.set_volume(0.8*options["master volume"])
        jumping_sound.set_volume(0.8*options["master volume"]*options["jump volume"])
        reloading_sound.set_volume(0.2*options["master volume"]*options["shot volume"])
        shot_sound.set_volume(0.8*options["master volume"]*options["shot volume"])
        if selected_level == "exit":
            break
        print(selected_level)

        print(Options_prototype)
        result,end_of_game = levels[selected_level-1].main(Options_prototype)
        if selected_level-1 == level_count and end_of_game and level_count < len(levels):
            level_count += 1
        coin_count += result
        importlib.reload(levels[selected_level-1])
        
def set_master_volume(volume):
    pygame.mixer.music.set_volume(volume*Options_prototype[0]["master volume"])
    shot_sound.set_volume(0.8*volume*Options_prototype[0]["shot volume"])
    is_hit_sound.set_volume(0.8*volume*Options_prototype[0]["shot volume"])
    jumping_sound.set_volume(0.8*volume*Options_prototype[0]["shot volume"])
    Options_prototype[0]["music volume"] = volume

def set_shot_volume(volume):
    shot_sound.set_volume(0.8*volume*Options_prototype[0]["master volume"])
    Options_prototype[0]["shot volume"] = volume

def set_jump_volume(volume):
    jumping_sound.set_volume(0.8*volume*Options_prototype[0]["master volume"])
    Options_prototype[0]["jump volume"] = volume

if __name__ == "__main__":
    main()
