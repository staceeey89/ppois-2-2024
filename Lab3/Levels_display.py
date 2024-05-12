import pygame
import yaml
from Arkanoid_display import Arkanoid_display
from Mini_level import Mini_level
from Button import Button


class Levels_display:
    def __init__(self):
        pygame.init()

        with open("configs/levels.yaml") as levels:
            levels_data = yaml.safe_load(levels)

        self.level_buttons = []
        for i in range(1, 11):
            self.level_buttons.append(Mini_level(i,
                                                 levels_data["levels"][i - 1]["mini_img_x_pos"],
                                                 levels_data["levels"][i - 1]["mini_img_y_pos"]))

        self.home_button = Button(100, 25, "Домой", "white", 48, 700)

    def change_level(self, sc, WIDTH, HEIGHT):
        # Основной цикл игры
        running = True
        while running:
            # Обработать события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.button.collidepoint(event.pos):
                        return -1
                    for i, button in enumerate(self.level_buttons):
                        if button.button.collidepoint(event.pos):
                            arkanoid_display = Arkanoid_display(i)
                            result = arkanoid_display.start_game(sc, WIDTH, HEIGHT, i)
                            if result == 1:
                                return 1
                            else:
                                return 2

            # Отрисовать уровень
            self.print_mini_levels(sc)

            # Отобразить экран
            pygame.display.update()

    def print_mini_levels(self, sc):
        sc.fill((0, 0, 0))
        for i in range(1, 11):
            self.level_buttons[i-1].print_mini_level(sc)

        self.home_button.draw_button(sc)