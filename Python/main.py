import LV1
import start_menu
import pygame



selected_level = start_menu.main()
print(selected_level)

if selected_level == 1:
    LV1.main()

