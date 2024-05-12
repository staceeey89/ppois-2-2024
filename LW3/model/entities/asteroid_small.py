import random

from model.entities.crashable import Crashable
from model.repository import load_sprite, load_config
from model.entities.asteroid import Assteroid


class AssteroidSmall(Assteroid):
    SmallAssteroidsNames = ["assteroid_small1", "assteroid_small2", "assteroid_small3"]

    def __init__(self, position, velocity, destroy_assteroid_callback, create_assteroid_callback):
        config = load_config()

        self.mass = config["assteroid_small_mass"]
        self.score = config["assteroid_small_score"]
        sprite_name = random.choice(self.SmallAssteroidsNames)
        self.original_sprite = load_sprite(sprite_name, True, (16, 16))

        super().__init__(position, self.original_sprite, velocity, destroy_assteroid_callback, create_assteroid_callback)

    def crash(self):
        self.destroy_assteroid_callback(self)
        super().crash()
