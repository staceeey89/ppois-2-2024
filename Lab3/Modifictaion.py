import pygame
import yaml

class Modification:
    def __init__(self, x_pos, y_pos, mod_idtf):
        with open("configs/modifications.yaml", encoding="utf-8") as modifications:
            mod_data = yaml.safe_load(modifications)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = mod_data["modifications"]["mod_width"]
        self.height = mod_data["modifications"]["mod_height"]
        self.animation_frames = []  # список изображений для анимации
        self.current_frame_index = 0
        self.mod_speed = mod_data["modifications"]["mod_speed"]  # скорость анимации
        self.mod_idtf = mod_idtf
        self.last_frame_update = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        # Загрузка изображений для анимации
        self.load_animation_frames()

    def load_animation_frames(self):
        with open("configs/modifications.yaml") as modifications:
            mod_data = yaml.safe_load(modifications)
            for frame_path in mod_data["modifications"][f"{self.mod_idtf}_bg_mod"]:
                frame = pygame.image.load(frame_path).convert_alpha()
                self.animation_frames.append(frame)

    def update_pos(self):
        # Двигаем анимацию вниз
        self.y_pos += self.mod_speed
        self.rect.y += self.mod_speed

    def draw_mod(self, sc):
        # Отрисовка анимации на экране
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update > 1000:  # Переключаем кадр раз в секунду (1000 мс)
            self.last_frame_update = current_time
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.animation_frames):
                self.current_frame_index = 0

        frame = self.animation_frames[self.current_frame_index]
        frame_rect = frame.get_rect(center=(self.x_pos, self.y_pos))
        sc.blit(frame, frame_rect)
