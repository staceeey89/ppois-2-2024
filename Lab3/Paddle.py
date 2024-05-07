import pygame
import yaml


class Paddle:
    def __init__(self):
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)
        self.paddle_w = settings_data["settings"]["paddle_w"]
        self.paddle_h = settings_data["settings"]["paddle_h"]
        self.paddle_speed = settings_data["settings"]["paddle_speed"]
        self.paddle = pygame.Rect(settings_data["settings"]["WIDTH"] // 2 - self.paddle_w // 2,
                                  settings_data["settings"]["HEIGHT"] - self.paddle_h - 10,
                                  self.paddle_w, self.paddle_h)

    def left_speed(self):
        self.paddle.left -= self.paddle_speed

    def right_speed(self):
        self.paddle.right += self.paddle_speed

    def print_paddle(self, sc):
        pygame.draw.rect(sc, pygame.Color('darkorange'), self.paddle)

