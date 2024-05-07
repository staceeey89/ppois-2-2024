import pygame
import os
import yaml


class Mini_level:
    def __init__(self, level_num, x_pos, y_pos):
        """Инициализация миниуровня"""
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        self.width = settings_data["settings"]["mini_img_width"]
        self.height = settings_data["settings"]["mini_img_height"]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.level_image = pygame.transform.scale(pygame.image.load(os.path.join(
            f"img/level_{level_num}.png")).convert_alpha(), (self.width, self.height))
        self.button = pygame.Rect(x_pos, y_pos, self.width, self.height)
        # Инициализация попдиси к картинке
        self.font = pygame.font.SysFont("Arial", 15)
        self.text = self.font.render(f"Уровень {level_num}", True, "white")


    def print_mini_level(self, sc):
        sc.blit(self.text, (self.x_pos, self.y_pos - 20))
        sc.blit(self.level_image, (self.x_pos, self.y_pos))
