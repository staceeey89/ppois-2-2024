import pygame
from pygame import Vector2

from model.entities.crashable import Crashable
from model.repository import load_sprite, load_sound, load_config
from model.entities.base_entity import BaseEntity
from view.graphics import rotate_image
from model.entities.bullet import Bullet


class Spaceship(BaseEntity, Crashable):

    def __init__(self, position, size, create_bullet_callback):
        self.config = load_config()

        self.create_bullet_callback = create_bullet_callback
        self.direction = Vector2((0, -1))
        self._original_sprite = load_sprite("spaceship", True, size)
        self._laser_sound = load_sound("laser")
        self._last_shoot = pygame.time.get_ticks()
        self.shoot_cooldown = self.config["spaceship_shoot_cooldown"]
        self.acceleration = self.config["spaceship_acceleration"]
        self.rotation_speed = self.config["spaceship_rotation_speed"]

        super().__init__(position, self._original_sprite, Vector2(0))
        super(BaseEntity, self).__init__()

    def accelerate(self):
        self.velocity += self.direction * self.acceleration

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.rotation_speed * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to((0, -1))
        self.sprite, rect = rotate_image(self._original_sprite,
                                         self.position,
                                         (self._original_sprite.get_width() / 2,
                                          self._original_sprite.get_height() / 2),
                                         angle)

        surface.blit(self.sprite, rect)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self._last_shoot >= self.shoot_cooldown:
            self._last_shoot = now
            bullet_velocity = self.direction * self.config["spaceship_bullet_speed"] + self.velocity
            bullet = Bullet(self.position, bullet_velocity)
            self.create_bullet_callback(bullet)
            self._laser_sound.play()
