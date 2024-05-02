import pygame


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def _img(path: str):
        return pygame.image.load(path)
