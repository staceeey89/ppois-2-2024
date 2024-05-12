from model.repository import load_sprite
from model.entities.base_entity import BaseEntity


class Bullet(BaseEntity):
    def __init__(self, position, velocity, is_enemy=False):
        self.is_enemy = is_enemy
        super().__init__(position, load_sprite("bullet", True, (8, 8)), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
