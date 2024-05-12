import random
import threading

import pygame

from controller.event_listener import EventListener
from controller.event_manager import *
from helpers.helpers import get_random_position, get_random_velocity
from model.entities.asteroid import Assteroid
from model.entities.asteroid_large import AssteroidLarge
from model.entities.asteroid_medium import AssteroidMedium
from model.entities.asteroid_small import AssteroidSmall
from model.entities.base_entity import BaseEntity
from model.entities.bullet import Bullet
from model.entities.spaceship import Spaceship
from model.entities.ufo import Ufo
from model.game_state_machine import STATE_MENU, StateMachine, STATE_PLAY, STATE_GAME_OVER, STATE_SAVE_RECORD
from model.physics import process_collisions
from model.repository import load_records, save_record, load_config


class GameModel(EventListener):
    SafeSpawnDistance = 200

    def __init__(self, event_manager):
        self.config = load_config()
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False
        self.state_stack = StateMachine()

        self.screen = pygame.display.get_surface()

        self.spaceship: Spaceship | None = None
        self.ufos: list[Ufo] = []
        self.bullets: list[Bullet] = []
        self.assteroids: list[Assteroid] = []
        self.lives: int = 0
        self.score: int = 0
        self.player_name: str = self.config["default_name"]

        self.ending_game: bool = False
        self.starting_new_level: bool = False
        self._last_ufo_spawn = pygame.time.get_ticks()
        self._spawn_menu_bg_objects()

    def notify(self, event):
        if isinstance(event, QuitEvent):
            pygame.quit()
            exit()

        elif isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                if not self.ending_game:
                    self.running = False
                    self._clear_game()
                    self._spawn_menu_bg_objects()

                    # false if no more states are left
                    if not self.state_stack.pop():
                        self.event_manager.post(QuitEvent())
            else:
                if event.state == STATE_PLAY:
                    self._start_new_game()
                else:
                    self.running = False
                    self._clear_game()

                self.state_stack.push(event.state)

    def run(self):
        self.event_manager.post(InitializeEvent())

        self.state_stack.push(STATE_MENU)
        while True:
            self._process_logic()
            self.event_manager.post(TickEvent())

    def save_record(self):
        save_record((self.player_name, self.score))

    def get_game_objects(self) -> list[BaseEntity]:
        game_objects = [*self.assteroids, *self.bullets, *self.ufos]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects


    def _spawn_menu_bg_objects(self):
        for _ in range(2):
            position = get_random_position(self.screen)
            self.assteroids.append(AssteroidLarge(position, get_random_velocity(3, 15) / 15,
                                                  None, None))

        for _ in range(4):
            position = get_random_position(self.screen)
            self.assteroids.append(AssteroidMedium(position, get_random_velocity(3, 15) / 15,
                                                   None, None))

        for _ in range(6):
            position = get_random_position(self.screen)
            self.assteroids.append(AssteroidSmall(position, get_random_velocity(3, 15) / 15,
                                                  None, None))

    def _clear_game(self):
        self._last_ufo_spawn = pygame.time.get_ticks()
        self.player_name = self.config["default_name"]
        self.assteroids = []
        self.ufos = []
        self.bullets = []
        self.spaceship = None

    def _game_over(self):
        self.ending_game = False
        self._clear_game()
        self.state_stack.pop()

        records = load_records()
        if len(records) == 0 or len(records) > 0 and records[0][1] < self.score:
            self.event_manager.post(StateChangeEvent(STATE_SAVE_RECORD))
            return

        self.event_manager.post(StateChangeEvent(STATE_GAME_OVER))

    def _die(self):
        self.lives -= 1
        self.spaceship = None
        for ufo in self.ufos:
            ufo.player_spaceship = None

        if self.lives == 0:
            self.ending_game = True
            pending_game_over = threading.Timer(1, self._game_over, args=[])
            pending_game_over.start()
            return

        t = threading.Timer(1.5, self._create_spaceship, args=[])
        t.start()

    def _process_logic(self):
        if self.running:
            if not self.starting_new_level and len(self.assteroids) == 0:
                self.starting_new_level = True
                t = threading.Timer(1.5, self._play_new_level, args=[])
                t.start()

            if len(self.ufos) < self.config["ufo_max_count"]:
                seconds = (pygame.time.get_ticks() - self._last_ufo_spawn) / 1000
                if seconds > self.config["ufo_spawn_cooldown"]:
                    self._last_ufo_spawn = pygame.time.get_ticks()
                    self._create_ufo()

            for bullet in self.bullets:
                if bullet.is_enemy:
                    if self.spaceship and self.spaceship.collides_with(bullet):
                        self._die()
                else:
                    for ufo in self.ufos:
                        if ufo.collides_with(bullet):
                            if self.bullets.__contains__(bullet):
                                self.bullets.remove(bullet)
                            ufo.crash()
                            self.ufos.remove(ufo)
                            break

                for asteroid in self.assteroids:
                    if asteroid.collides_with(bullet):
                        if self.bullets.__contains__(bullet):
                            self.bullets.remove(bullet)
                        asteroid.crash()
                        break

        for entity in self.get_game_objects():
            entity.move(self.screen)

        for bullet in self.bullets:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for ufo in self.ufos:
            if not self.screen.get_rect().collidepoint(ufo.position):
                self.ufos.remove(ufo)

        if self.spaceship:
            for crashable in [*self.assteroids, *self.ufos]:
                if crashable.collides_with(self.spaceship):
                    self.spaceship.crash()
                    crashable.crash()
                    self._die()
                    break

        process_collisions(self.assteroids)

    def _start_new_game(self):
        self._clear_game()
        self.lives = self.config["new_game_lives"]
        self.score = 0
        self.running = True
        self._create_spaceship()
        self._play_new_level()

    def _play_new_level(self):
        if not self.running or len(self.assteroids) != 0:
            return

        def assteroid_destroy_self_callback(assteroid: Assteroid) -> None:
            if self.assteroids.__contains__(assteroid):
                self.assteroids.remove(assteroid)
                self.score += assteroid.score

        assteroid_destroy_children_callback = self.assteroids.append

        for _ in range(int(self.config["new_level_asteroids_count"])):
            while True:
                position = get_random_position(self.screen)
                if not self.spaceship or position.distance_to(self.spaceship.position) > self.SafeSpawnDistance:
                    break

            self.assteroids.append(AssteroidLarge(position, get_random_velocity(3, 25) / 15,
                                                  assteroid_destroy_self_callback,
                                                  assteroid_destroy_children_callback))

        self.starting_new_level = False

    def _apply_random_modifier(self):
        modifiers = [
            (self._apply_better_cooldown, "Shoot more!"),
            (self._apply_slowed_assteroids, "Slower assteroids!"),
            (self._apply_one_more_live, "One more live!")
        ]

        if random.random() > 0.5:
            chosen_modifier = random.choice(modifiers)
            chosen_modifier[0]()
            self.event_manager.post(ModifierAppliedEvent(chosen_modifier[1]))

    def _apply_better_cooldown(self):
        if not self.spaceship:
            return

        preserved_spaceship = self.spaceship
        preserved_spaceship.shoot_cooldown = preserved_spaceship.shoot_cooldown / 2

        def return_cooldown():
            preserved_spaceship.shoot_cooldown = preserved_spaceship.shoot_cooldown * 2

        t = threading.Timer(10, return_cooldown, args=[])
        t.start()

    def _apply_slowed_assteroids(self):
        preserved_assteroid = self.assteroids.copy()

        for assteroid in self.assteroids:
            assteroid.velocity = assteroid.velocity / 2

        def return_speed():
            for assteroid in preserved_assteroid:
                assteroid.velocity = assteroid.velocity * 2

        t = threading.Timer(10, return_speed, args=[])
        t.start()

    def _apply_one_more_live(self):
        if self.lives < 5:
            self.lives += 1

    def _create_ufo(self):
        if self.ending_game or not self.running or not self.spaceship:
            return

        while True:
            position = get_random_position(self.screen)
            if position.distance_to(self.spaceship.position) > self.SafeSpawnDistance:
                break

        self.ufos.append(Ufo(position, (32, 32), self.bullets.append, self.spaceship, self._apply_random_modifier))

    def _create_spaceship(self):
        if self.ending_game or not self.running:
            return

        self.spaceship = Spaceship((self.screen.get_width() / 2, self.screen.get_height() / 2), (32, 32), self.bullets.append)

        for ufo in self.ufos:
            ufo.player_spaceship = self.spaceship
