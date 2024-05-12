import random

import pygame
from pygame import Vector2, Surface

from model.entities.crashable import Crashable
from model.repository import load_sprite, load_sound, load_config
from model.entities.base_entity import BaseEntity
from model.entities.bullet import Bullet
from model.entities.spaceship import Spaceship


class Ufo(BaseEntity, Crashable):

    def __init__(self, position, size, create_bullet_callback, player_spaceship: Spaceship, crash_callback=None):
        super().__init__(position, load_sprite("ufo", True, size), Vector2(0))

        self.config = load_config()

        self.create_bullet_callback = create_bullet_callback
        self.player_spaceship = player_spaceship
        if player_spaceship is None:
            self.velocity = Vector2((0, -1))
        else:
            self.velocity = (self.player_spaceship.position - self.position).normalize() * self.config["ufo_speed"]
        self._laser_sound = load_sound("laser")
        self._last_shoot = pygame.time.get_ticks()
        self._last_direction_change = pygame.time.get_ticks()

        super(BaseEntity, self).__init__(crash_callback=crash_callback)

    def move(self, surface: Surface):
        self.shoot()

        now = pygame.time.get_ticks()
        if now - self._last_direction_change >= self.config["ufo_direction_change_interval"]:
            self._last_direction_change = now
            self.velocity.rotate_ip(45 * random.randint(-2, 2))

        self.position += self.velocity

    def shoot(self):
        if self.player_spaceship is None:
            return

        now = pygame.time.get_ticks()
        if now - self._last_shoot >= self.config["ufo_shoot_cooldown"]:
            self._last_shoot = now
            bullet_velocity = (self.player_spaceship.position - self.position).normalize() * self.config["ufo_bullet_speed"]
            bullet = Bullet(self.position, bullet_velocity, is_enemy=True)
            self.create_bullet_callback(bullet)
            self._laser_sound.play()
