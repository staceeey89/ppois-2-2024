import pygame
import yaml
from Block import Block


class Blocks_level:
    def __init__(self, level_num):
        with open("configs/levels.yaml") as levels:
            levels_data = yaml.safe_load(levels)

        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        # Инициализация всех настроек из конфигов
        # paddle settings
        self.green_block_list = []
        for block_coordinates in levels_data["levels"][level_num]["green_blocks"]:
            if len(block_coordinates) == 2:
                x, y = block_coordinates
                self.green_block_list.append(pygame.Rect(x, y, settings_data["settings"]["block_width"],
                                                         settings_data["settings"]["block_height"]))

        self.blue_block_list = []
        for block_coordinates in levels_data["levels"][level_num]["blue_blocks"]:
            if len(block_coordinates) == 2:
                x, y = block_coordinates
                self.blue_block_list.append(pygame.Rect(x, y, settings_data["settings"]["block_width"],
                                                        settings_data["settings"]["block_height"]))

        self.red_block_list = []
        for block_coordinates in levels_data["levels"][level_num]["red_blocks"]:
            if len(block_coordinates) == 2:
                x, y = block_coordinates
                self.red_block_list.append(pygame.Rect(x, y, settings_data["settings"]["block_width"],
                                                       settings_data["settings"]["block_height"]))

        self.rock_block_list = []
        for block_coordinates in levels_data["levels"][level_num]["rock_blocks"]:
            if len(block_coordinates) == 4:
                x, y, width, height = block_coordinates
                self.rock_block_list.append(pygame.Rect(x, y, width, height))

    def print_blocks_level(self, sc):
        for block in self.green_block_list:
            pygame.draw.rect(sc, "green", block)
        for block in self.blue_block_list:
            pygame.draw.rect(sc, "blue", block)
        for block in self.red_block_list:
            pygame.draw.rect(sc, "red", block)
        for block in self.rock_block_list:
            pygame.draw.rect(sc, "gray", block)

    def recolor_hit_blue_block(self, sc, hit_rect):
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        self.green_block_list.append(pygame.Rect(hit_rect.left, hit_rect.top,
                                                 settings_data["settings"]["block_width"],
                                                 settings_data["settings"]["block_height"]))
        pygame.draw.rect(sc, "green", self.green_block_list[len(self.green_block_list) - 1])

    def recolor_hit_red_block(self, sc, hit_rect):
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        self.blue_block_list.append(pygame.Rect(hit_rect.block.left, hit_rect.block.top,
                                                settings_data["settings"]["block_width"],
                                                settings_data["settings"]["block_height"]))
        pygame.draw.rect(sc, "blue", self.blue_block_list[len(self.blue_block_list) - 1])
