from game import dp, screen
from scenes import Gameplay
from scenes import MainMenu

if __name__ == "__main__":
    gameplay = Gameplay()
    main_menu = MainMenu()
    # dp.add(gameplay=gameplay,
    #        main_menu=main_menu)
    dp.main(MainMenu)
