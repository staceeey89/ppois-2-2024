import random

from pygame import Surface

from model.entities.crashable import Crashable
from model.repository import load_sound
from view.graphics import rotate_image
from model.entities.base_entity import BaseEntity


class Assteroid(BaseEntity, Crashable):
    def __init__(self, position, sprite: Surface, velocity, destroy_assteroid_callback, create_assteroid_callback):
        self.mass = 200
        self.score = 50
        self.destroy_assteroid_callback = destroy_assteroid_callback
        self.create_assteroid_callback = create_assteroid_callback

        self.sprite, self.rect = rotate_image(sprite,
                                              position,
                                              (sprite.get_width() / 2,
                                               sprite.get_height() / 2),
                                              random.randrange(0, 360))

        super().__init__(position, self.sprite, velocity)
        super(BaseEntity, self).__init__(random.choice(["explosion1", "explosion2"]))

    def crash(self):
        self.crash_sound.play()
