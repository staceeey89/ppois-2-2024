from typing import Dict, Type

import pygame
from pygame import Surface

from engine.scene import Scene


class Dispatcher:
    def __init__(self, screen: Surface, fps: int):
        self.scenes = {}
        self.current_scene = None
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.fps = fps

    def add(self, **scenes: Dict[str, Scene]):
        self.scenes.update(scenes)

    def checkout(self, scene_class: Type[Scene], *args, **kwargs):
        self.current_scene = scene_class(args)

    def main(self, scene_class: Type[Scene]):
        self.current_scene = scene_class()

        running = True
        while running:

            self.current_scene.update()

            self.current_scene.render(self.screen)

            self.clock.tick(self.fps)
