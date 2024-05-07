import pygame
import yaml
from Button import Button


class Reference_display:
    def __init__(self):
        self.home_button = Button(100, 25, "Домой", "white", 48, 700)

    def print_reference_display(self, sc):
        with open("configs/reference.yaml", encoding="utf-8") as reference:
            reference_data = yaml.safe_load(reference)

        # Инициализировать Pygame
        pygame.init()
        sc.fill((0, 0, 0))

        # Отобразить текст на экране
        for item in reference_data["reference"]:
            size = int(item["size"])
            font = pygame.font.SysFont("Arial", size)
            text = font.render(item["text"], True, (255, 255, 255))
            sc.blit(text, (item["x_pos"], item["y_pos"]))

        self.home_button.draw_button(sc)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.button.collidepoint(event.pos):
                        return True

            # Обновить экран
            pygame.display.update()


