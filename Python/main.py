import LV1, LV2
import start_menu
import importlib

Options_prototype = [{
    "master volume":1,
    "jump volume":1,
    "shot volume":1,
}]

def main():
    levels = [LV1, LV2]
    coin_count = 0


    while True:
        selected_level, options = start_menu.main(coin_count,Options_prototype[0])
        Options_prototype[0] = options
        if selected_level == "exit":
            break
        print(selected_level)

        coin_count += levels[selected_level-1].main(Options_prototype)
        importlib.reload(levels[selected_level-1])
        

if __name__ == "__main__":
    main()
