import pygame
import yaml
from Levels_display import Levels_display
from Button import Button
from Reference_display import Reference_display
from Record_display import Record_display


class Main_display:
    def __init__(self):
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        self.font = pygame.font.SysFont("Arial", 30)
        self.WIDTH, self.HEIGHT = settings_data["settings"]["WIDTH"], settings_data["settings"]["HEIGHT"]
        self.fps = settings_data["settings"]["fps"]
        self.main_buttons_list = [Button(200, 50, "Играть", (0, 255, 0), 500, 200),
                                  Button(200, 50, "Рекорды", (255, 255, 0), 500, 300),
                                  Button(200, 50, "Справка", (255, 165, 0), 500, 400),
                                  Button(200, 50, "Выход", (255, 0, 0), 500, 500)]

        pygame.init()
        pygame.mixer.init()
        self.sc = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.levels_display = Levels_display()
        self.reference_display = Reference_display()
        self.record_display = Record_display()
        pygame.mixer.music.set_volume(0.5)
        self.congr_text = self.font.render(f"Рекорд добавлен!:", True, "white")
        self.congr = False
        self.bg_mus_flag = False

    def show_main_screen(self):
        self.sc.fill((0, 0, 0))
        for button in self.main_buttons_list:
            button.draw_button(self.sc)
        if self.congr:
            self.print_congr_text(self.sc)
        if not self.bg_mus_flag:
            pygame.mixer.music.load('music/main_display_music.mp3')
            pygame.mixer.music.play(loops=-1)
            pygame.display.update()
            self.bg_mus_flag = True

    def show_change_level_screen(self):
        self.congr = False
        change_num = self.levels_display.change_level(self.sc, self.WIDTH, self.HEIGHT)
        if change_num == -1:
            self.congr = False
            self.bg_mus_flag = True
        elif change_num == 1:
            self.congr = True
            self.bg_mus_flag = False
        elif change_num == 2:
            self.congr = False
            self.bg_mus_flag = False
        self.show_main_screen()

    def show_reference_display(self):
        self.congr = False
        if self.reference_display.print_reference_display(self.sc):
            self.show_main_screen()

    def show_record_display(self):
        self.congr = False
        if self.record_display.show_record_display(self.sc):
            self.show_main_screen()

    def print_congr_text(self, sc):
        sc.blit(self.congr_text, (400, 100))
        pygame.display.update()

    def start_main_display(self):
        flag = True
        running = True
        while running:

            if flag:
                self.show_main_screen()
                flag = False

            # Обработать события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_buttons_list[0].button.collidepoint(event.pos):
                        # Сделать что-то, когда нажата кнопка "Играть"
                        self.show_change_level_screen()
                        # pass
                    elif self.main_buttons_list[1].button.collidepoint(event.pos):
                        # Сделать что-то, когда нажата кнопка "Рекорды"
                        self.show_record_display()
                    elif self.main_buttons_list[2].button.collidepoint(event.pos):
                        # Сделать что-то, когда нажата кнопка "Справка"
                        self.show_reference_display()
                    elif self.main_buttons_list[3].button.collidepoint(event.pos):
                        # Сделать что-то, когда нажата кнопка "Выход"
                        running = False

            # Обновить экран
            pygame.display.flip()
            self.clock.tick(self.fps)

        # Завершить работу pygame
        pygame.quit()
        exit()
