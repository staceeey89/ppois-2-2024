import pygame

from engine.sprite import Sprite


class GameObject(Sprite):
    def __init__(self, x, y, width=0, height=0):
        super().__init__(x, y)
        self.width = width
        self.height = height

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)