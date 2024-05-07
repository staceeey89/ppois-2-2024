import pygame
import yaml
from random import randrange as rnd


class Ball:
    def __init__(self):
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)
        self.ball_radius = settings_data["settings"]["ball_radius"]
        self.ball_speed = settings_data["settings"]["ball_speed"]
        self.ball_rect = settings_data["settings"]["ball_rect"]
        self.ball = pygame.Rect(rnd(30, 1100), 700, self.ball_rect, self.ball_rect)
        self.dx = settings_data["settings"]["dx"]
        self.dy = settings_data["settings"]["dy"]
        self.hit_sound = pygame.mixer.Sound('music/hit_sound.mp3')

    def change_ball_x_pos(self):
        self.ball.x += self.ball_speed * self.dx

    def change_ball_y_pos(self):
        self.ball.y += self.ball_speed * self.dy

    def check_hit_ball_elements(self, WIDTH, paddle):
        # Столкновение слева и справа
        if self.ball.left <= 5 or self.ball.centerx > WIDTH - self.ball_radius - 5:
            self.hit_sound.play()
            self.dx = -self.dx

        # Столкновение сверху
        if self.ball.top <= 5:
            self.hit_sound.play()
            self.dy = -self.dy

        # Столкновение с платформой
        if self.ball.colliderect(paddle) and self.dy > 0:
            self.hit_sound.play()
            self.detect_collision(paddle)
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.ball.x - 7 > 0:
                self.ball.x -= 7
            if key[pygame.K_RIGHT] and self.ball.x + 7 < 1200:
                self.ball.x += 7

    def check_hit_block_paddle(self, block_paddle_list):
        hit_block_index = self.ball.collidelist(block_paddle_list)
        if hit_block_index != -1:
            self.hit_sound.play()
            hit_rect = block_paddle_list.pop(hit_block_index)
            self.detect_collision(hit_rect)
            return True
        return False

    def check_hit_ball_green_blocks(self, green_block_list):
        # Столкновение с блоками
        hit_green_index = self.ball.collidelist(green_block_list)
        if hit_green_index != -1:
            self.hit_sound.play()
            hit_rect = green_block_list.pop(hit_green_index)
            self.detect_collision(hit_rect)
            return True
        return False

    def check_hit_ball_blue_blocks(self, blue_block_list):
        hit_blue_index = self.ball.collidelist(blue_block_list)
        if hit_blue_index != -1:
            self.hit_sound.play()
            hit_rect = blue_block_list.pop(hit_blue_index)
            self.detect_collision(hit_rect)
            return hit_rect
        else:
            return None

    def check_hit_ball_red_blocks(self, red_block_list):
        hit_red_index = self.ball.collidelist(red_block_list)
        if hit_red_index != -1:
            self.hit_sound.play()
            hit_rect = red_block_list.pop(hit_red_index)
            self.detect_collision(hit_rect)
            return hit_rect
        else:
            return None

    def check_hit_ball_rock_blocks(self, rock_block_list):
        hit_rock_index = self.ball.collidelist(rock_block_list)
        if hit_rock_index != -1:
            self.hit_sound.play()
            hit_rect = rock_block_list[hit_rock_index]
            self.detect_collision(hit_rect)

    def detect_collision(self, rect):
        if self.dx > 0:
            delta_x = self.ball.right - rect.left
        else:
            delta_x = rect.right - self.ball.left
        if self.dy > 0:
            delta_y = self.ball.bottom - rect.top
        else:
            delta_y = rect.bottom - self.ball.top

        if abs(delta_x - delta_y) < 10:
            self.dx, self.dy = -self.dx, -self.dy
        elif delta_x > delta_y:
            self.dy = -self.dy
        elif delta_y > delta_x:
            self.dx = -self.dx

    def print_ball(self, sc):
        pygame.draw.circle(sc, pygame.Color('white'), self.ball.center, self.ball_radius)
