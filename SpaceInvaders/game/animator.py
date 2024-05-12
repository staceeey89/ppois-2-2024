from typing import List

import pygame
from pygame import Surface

from engine.sprite import Sprite
from game import screen
from game.parser import AnimationData


class Animation(Sprite):
    def __init__(self, x, y, width, height, data: AnimationData):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.img = self._img(data.sprite)
        self.duration = data.frame_duration

    def play(self) -> bool:
        if self.duration >= 0:
            self.duration -= 1
            return True
        else:
            return False

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Animator:
    def __init__(self):
        self.animations: List[Animation] = []

    def play(self, animation: Animation):
        self.animations.append(animation)

    def __call__(self, *args, **kwargs):
        new_animations = []
        for animation in self.animations:
            if animation.play():
                animation.draw()
                new_animations.append(animation)
        self.animations = new_animations


