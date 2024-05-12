import pygame

# Инициализировать модуль шрифтов Pygame
pygame.font.init()


class Button:
    def __init__(self, width, height, text, color, x, y):
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.button = pygame.Rect(x, y, width, height)

    def draw_button(self, sc):
        pygame.draw.rect(sc, "white", self.button)
        sc.blit(self.text_surface,
                (self.button.centerx - self.text_surface.get_width() / 2,
                 self.button.centery - self.text_surface.get_height() / 2))
