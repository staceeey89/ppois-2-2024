import pygame
import yaml


class Block:
    def __init__(self, x_pos, y_pos):
        with open("configs/levels.yaml") as levels:
            levels_data = yaml.safe_load(levels)

        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        self.width = settings_data["settings"]["block_width"]
        self.height = settings_data["settings"]["block_height"]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.block = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)