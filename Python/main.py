import LV1, LV2
import start_menu
import importlib

levels = [LV1, LV2]
coin_count = 0


while True:
    selected_level = start_menu.main(coin_count)
    if selected_level == "exit":
        break
    print(selected_level)

    coin_count += levels[selected_level-1].main()
    importlib.reload(levels[selected_level-1])
    


