from math import cos, sin, pi

import pygame
import random

from engine.game_object import GameObject
from engine.sprite import Sprite
from game import PLAYER_WIDTH, PLAYER_HEIGHT, weapons, SCREEN_WIDTH, BULLET_WIDTH, ENEMY_WIDTH, ENEMY_HEIGHT, \
    player_img, screen, BRICK_WIDTH, BRICK_HEIGHT, brick_img, BULLET_HEIGHT, SPACING, SCREEN_HEIGHT, enemies, \
    font, BLACK, ENEMY_SHOT, sounds
from parser import EnemyData, WaveData, WeaponData


class Lives(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y)
        self.img = self._img(image)

        self.lives = 3

    def minus(self):
        self.lives -= 1

    def __call__(self, *args, **kwargs):
        self.draw()

    def draw(self):
        # Отображение счёта на экране
        if self.lives > 0:
            screen.blit(self.img, (SCREEN_WIDTH - self.x + 150, self.y - 12))
        if self.lives > 1:
            screen.blit(self.img, (SCREEN_WIDTH - self.x + 150 + PLAYER_WIDTH + 10, self.y - 12))
        if self.lives > 2:
            screen.blit(self.img, (SCREEN_WIDTH - self.x + 150 + 2 * (PLAYER_WIDTH + 10), self.y - 12))
        score_text = font.render("LIVES", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH - self.x, self.y))


# Класс игрока
class Player(GameObject):
    def __init__(self, x, y, weapon):
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.x = x
        self.y = y
        self.weapon = weapon
        self.img = self._img(player_img)

    def move_left(self):
        if self.x > 0:
            self.x -= 5

    def move_right(self):
        if self.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.x += 5

    def shoot(self):
        return Projectile(x=self.x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2,
                          y=self.y,
                          parent=self,
                          data=self.weapon)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


# Класс врага
class Enemy(GameObject):
    def __init__(self, x, y, data: EnemyData):
        super().__init__(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.x = x
        self.y = y
        self.weapon = weapons[data.weapon]
        self.img = self._img(data.sprite)
        self.score = data.score

    def shoot(self):
        return Projectile(x=self.x + ENEMY_WIDTH // 2 - BULLET_WIDTH // 2,
                          y=self.y,
                          parent=self,
                          data=self.weapon)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Flagship(Enemy):
    def __init__(self, x, y, data: EnemyData, speed: int, drop=True):
        super().__init__(x, y, data)
        self.x = x
        self.y = y
        self.speed = speed
        self.weapon = weapons[data.weapon]
        self.img = self._img(data.sprite)
        self.score = data.score
        self.drop = drop
        sound = pygame.mixer.Sound(sounds['flagship'])
        sound.play()

    def move(self):
        self.x += self.speed

    def shoot(self):
        pass
        # return Projectile(x=self.x + ENEMY_WIDTH // 2 - BULLET_WIDTH // 2,
        #                   y=self.y,
        #                   parent=self,
        #                   data=self.weapon)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Brick(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.bricks = [self._img(brick) for brick in brick_img]
        self.img = self.bricks[0]

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def ruin(self) -> bool:
        print("Ruin")
        new_img_index = self.bricks.index(self.img) + 1
        if new_img_index > len(brick_img) - 1:
            return True
        self.img = self.bricks[self.bricks.index(self.img)+1]
        return False


class WallBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bricks = [
            Brick(x, y), Brick(x + BRICK_WIDTH, y), Brick(x + BRICK_WIDTH * 2, y), Brick(x + BRICK_WIDTH * 3, y),
            Brick(x, y + BRICK_HEIGHT),
            Brick(x + BRICK_WIDTH, y + BRICK_HEIGHT),
            Brick(x + BRICK_WIDTH * 2, y + BRICK_HEIGHT),
            Brick(x + BRICK_WIDTH * 3, y + BRICK_HEIGHT),
            Brick(x, y + BRICK_HEIGHT * 2),
            Brick(x + BRICK_WIDTH, y + BRICK_HEIGHT * 2),
            Brick(x + BRICK_WIDTH * 2, y + BRICK_HEIGHT * 2),
            Brick(x + BRICK_WIDTH * 3, y + BRICK_HEIGHT * 2),
        ]

    def draw(self):
        for brick in self.bricks:
            brick.draw()


# Класс пули
class Projectile:
    def __new__(cls, x, y, parent, data: WeaponData):
        if data.advanced:
            return [AdvancedBullet(x, y, parent, data, 0),
                    AdvancedBullet(x, y, parent, data, pi/10),
                    AdvancedBullet(x, y, parent, data, -pi/10)
                    ]
        return [Bullet(x, y, parent, data)]


class Bullet(GameObject):
    def __init__(self, x, y, parent, data: WeaponData):
        super().__init__(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.parent = parent
        self.img = self._img(data.sprite)
        self.speed = data.speed
        if type(self.parent) is Player:
            sound = pygame.mixer.Sound(sounds[data.sound])
            sound.play()

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class AdvancedBullet(Bullet):
    @staticmethod
    def sign(x):
        return -1 if x < 0 else 1

    def __init__(self, x, y, parent, data: WeaponData, angle: float = 0):
        super().__init__(x, y, parent, data)
        self.angle = angle
        if parent is Player:
            sound = pygame.mixer.Sound(sounds[data.sound])
            sound.play()

    def move(self):
        self.y += self.speed * abs(cos(self.angle))

        self.x += self.speed * -1 * self.sign(self.y) * sin(self.angle)


# Класс блока врагов
class EnemyBox:
    def __init__(self, wave: WaveData):

        self.spacing = SPACING

        max_cols = len(max(wave.enemies, key=len))
        rows = len(wave.enemies)

        self.width = ENEMY_WIDTH * max_cols + SPACING * (max_cols - 1)
        self.height = ENEMY_HEIGHT * rows + SPACING * (rows - 1)
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y_limit = (SCREEN_HEIGHT - self.height) // 2 - 200
        self.y = 0 - self.y_limit

        self.enemies = []
        for i, row in enumerate(wave.enemies):
            row_x = self.x + ((self.width - (ENEMY_WIDTH * len(row) + SPACING * (len(row) - 1))) // 2)
            for j, enemy in enumerate(row):
                enemy_data = enemies[enemy]
                enemy = Enemy(row_x + j * (ENEMY_WIDTH + SPACING), self.y + i * (ENEMY_HEIGHT + SPACING), enemy_data)
                self.enemies.append(enemy)

        self.show_speed = 5
        self.show_flag = True
        self.direction = "right"

        self.move_speed = 1

        if len(self.enemies) < 4:
            pygame.time.set_timer(ENEMY_SHOT, 1600)
            self.move_speed = 2
        if len(self.enemies) == 1:
            self.move_speed = 3
        else:
            pygame.time.set_timer(ENEMY_SHOT, 800)

    def kill_enemy(self, enemy: Enemy):
        self.enemies.remove(enemy)
        if len(self.enemies) < 4:
            pygame.time.set_timer(ENEMY_SHOT, 1600)
            self.move_speed = 2
        if len(self.enemies) == 1:
            self.move_speed = 3
        pass

    def shoot(self):
        enemy = self.enemies[random.randint(1, len(self.enemies)) - 1]
        return enemy.shoot()

    def show(self):
        if self.y < self.y_limit and self.show_flag:
            self.y += self.show_speed
            for enemy in self.enemies:
                enemy.y += self.show_speed
            return True
        self.show_flag = False
        return False

    def move(self):
        if not self.show():
            limit_left = 0
            limit_right = SCREEN_WIDTH - self.width
            limit_top = 200
            limit_bottom = SCREEN_HEIGHT - self.height - 300
            if self.direction == "up":
                if self.y > limit_top:
                    for enemy in self.enemies:
                        enemy.y -= self.move_speed
                    self.y -= self.move_speed
                else:
                    self.direction = "right"
            elif self.direction == "right":
                if self.x < limit_right:
                    for enemy in self.enemies:
                        enemy.x += self.move_speed
                    self.x += self.move_speed
                else:
                    self.direction = "down"
            elif self.direction == "down":
                if self.y < limit_bottom:
                    for enemy in self.enemies:
                        enemy.y += self.move_speed
                    self.y += self.move_speed
                else:
                    self.direction = "left"
            elif self.direction == "left":
                if self.x > limit_left:
                    for enemy in self.enemies:
                        enemy.x -= self.move_speed
                    self.x -= self.move_speed
                else:
                    self.direction = "up"

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()


class DroppedWeapon(GameObject):
    def __init__(self, x, y, data: WeaponData, type_par):
        super().__init__(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.img = self._img(data.sprite)
        self.speed = data.speed
        self.type = type_par

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.img, (self.x, self.y))
