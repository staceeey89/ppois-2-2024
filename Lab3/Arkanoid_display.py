import os
from random import randrange as rnd

import pygame
import yaml
import time

from Blocks_level import Blocks_level
from Button import Button
from Paddle import Paddle
from Ball import Ball
from Modifictaion import Modification
from Input_record_display import Input_record_display


class Arkanoid_display:
    def __init__(self, level_num):
        with open("configs/settings.yaml") as settings:
            settings_data = yaml.safe_load(settings)

        pygame.init()  # Инициализировать Pygame в начале функции start_game
        pygame.mixer.init()
        self.input_record_display = Input_record_display()
        self.clock = pygame.time.Clock()  # Инициализировать часы Pygame
        self.paddle = Paddle()
        self.ball_list = []
        self.ball_list.append(Ball())
        self.level = Blocks_level(level_num)
        self.bg_img = pygame.transform.scale(pygame.image.load(os.path.join(
            "img/night_sky.jpg")).convert_alpha(), (settings_data["settings"]["WIDTH"],
                                                    settings_data["settings"]["HEIGHT"]))
        self.start_time = time.time()
        self.formatted_time = "-1"
        self.int_time = 0
        self.fps = settings_data["settings"]["fps"]
        self.modifications_list = []
        self.block_paddle_list = []
        self.home_button = Button(100, 25, "Домой", "white", 48, 700)
        self.game_over_sound = pygame.mixer.Sound('music/game_over_sound.mp3')
        self.win_sound = pygame.mixer.Sound('music/win_sound.mp3')
        self.paddle_mod_sound = pygame.mixer.Sound('music/achiv_sound.mp3')


    def start_game(self, sc, WIDTH, HEIGHT, level_num):
        pygame.mixer.music.load(f'music/level_music{level_num + 1}.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.display.update()

        running = True  # Флаг для запуска игрового цикла

        while running:

            # Обработать события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Отрисовка мира
            self.print_arkanoid_display(sc)

            # self.group.update(pygame.event.get())
            # self.group.draw(sc)

            # Движение мяча
            for ball in self.ball_list:
                ball.change_ball_x_pos()
                ball.change_ball_y_pos()

            for modification in self.modifications_list:
                modification.update_pos()

            # Отслеживание столкновений
            for ball in self.ball_list:
                self.check_ball_collisions(sc, WIDTH, ball)

            self.check_mod_paddle_collisions()

            # Победа, проигрыш
            if self.ball_list[0].ball.bottom > HEIGHT and len(self.ball_list) == 1:
                print('GAME OVER!')
                pygame.mixer.music.stop()
                self.game_over_sound.play()
                if self.game_over(sc):
                    return -1
            elif (len(self.level.green_block_list) == 0
                  and len(self.level.blue_block_list) == 0
                  and len(self.level.red_block_list) == 0
                  and len(self.ball_list) != 0):

                if self.check_record(level_num):
                    pygame.mixer.music.stop()
                    self.win_sound.play()
                    self.input_record_display.draw_record_field(sc, level_num, self.int_time, self.formatted_time)
                    print('WIN!!!')
                    return 1
                return 2
            elif len(self.ball_list) > 1:
                for i, ball in enumerate(self.ball_list):
                    if ball.ball.bottom > HEIGHT:
                        self.ball_list.pop(i)

            # Управление
            self.control_paddle(WIDTH)

            # Обновить экран
            pygame.display.flip()
            self.clock.tick(self.fps)

    def print_arkanoid_display(self, sc):
        sc.blit(self.bg_img, (0, 0))
        self.level.print_blocks_level(sc)
        self.paddle.print_paddle(sc)
        for ball in self.ball_list:
            ball.print_ball(sc)

        for modification in self.modifications_list:
            modification.draw_mod(sc)

        for block_paddle in self.block_paddle_list:
            pygame.draw.rect(sc, "purple", block_paddle)

        # Отображение времени
        font = pygame.font.SysFont("Arial", 15)
        self.int_time = int(self.calculate_record_time())
        text = font.render(self.formatted_time, True, (255, 255, 255))
        sc.blit(text, (1100, 700))

    def calculate_record_time(self):
        # Получить текущее время
        current_time = time.time()

        # Вычислить прошедшее время
        elapsed_time = current_time - self.start_time

        # Преобразовать прошедшее время в секунды, минуты и часы
        seconds = elapsed_time % 60
        minutes = (elapsed_time // 60) % 60
        hours = elapsed_time // 3600

        # Форматировать время
        self.formatted_time = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))
        return elapsed_time

    def check_ball_collisions(self, sc, WIDTH, ball):
        # Отслеживаем столкновение с элементами
        ball.check_hit_ball_elements(WIDTH, self.paddle.paddle)

        ball.check_hit_block_paddle(self.block_paddle_list)

        # Столкновение с блоками
        if ball.check_hit_ball_green_blocks(self.level.green_block_list):
            self.create_modification(ball.ball.left, ball.ball.top)
            self.fps += 1

        hit_rect = ball.check_hit_ball_blue_blocks(self.level.blue_block_list)
        if hit_rect is not None:
            self.level.recolor_hit_blue_block(sc, hit_rect.block)
            self.create_modification(ball.ball.left, ball.ball.top)
            self.fps += 1

        hit_rect = ball.check_hit_ball_red_blocks(self.level.red_block_list)
        if hit_rect is not None:
            self.level.recolor_hit_red_block(sc, hit_rect)
            self.create_modification(ball.ball.left, ball.ball.top)
            self.fps += 1

        ball.check_hit_ball_rock_blocks(self.level.rock_block_list)
        return -1

    def control_paddle(self, WIDTH):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.paddle.paddle.left > 0:
            self.paddle.left_speed()
        if key[pygame.K_RIGHT] and self.paddle.paddle.right < WIDTH:
            self.paddle.right_speed()

    def check_record(self, num):
        with open("configs/records.yaml", encoding="utf-8") as file:
            records_data = yaml.safe_load(file)

        current_record_time = records_data["records"][num][1]["int_time"]

        if self.int_time < current_record_time:
            return True
        else:
            return False

    def create_modification(self, x_pos, y_pos):
        random_number = rnd(1, 15)
        if random_number <= 5:
            self.modifications_list.append(Modification(x_pos, y_pos, random_number))

    def check_mod_paddle_collisions(self):
        rect_modifications_list = [modification.rect for modification in self.modifications_list]
        paddle_hit_index = self.paddle.paddle.collidelist(rect_modifications_list)
        if paddle_hit_index != -1:
            self.paddle_mod_sound.play()
            modification = self.modifications_list[paddle_hit_index]
            if modification.mod_idtf == 1:
                self.slow_fps(paddle_hit_index, rect_modifications_list)
                return
            elif modification.mod_idtf == 2:
                self.enlarge_paddle(paddle_hit_index, rect_modifications_list)
                return
            elif modification.mod_idtf == 3:
                self.reduce_paddle(paddle_hit_index, rect_modifications_list)
                return
            elif modification.mod_idtf == 4:
                self.create_new_ball(paddle_hit_index, rect_modifications_list)
                return
            elif modification.mod_idtf == 5:
                self.create_block_paddle(paddle_hit_index, rect_modifications_list)
                return

    def slow_fps(self, paddle_hit_index, rect_modifications_list):
        if self.fps > 15:
            self.fps -= 15
        self.modifications_list.pop(paddle_hit_index)
        rect_modifications_list.pop(paddle_hit_index)

    def reduce_paddle(self, paddle_hit_index, rect_modifications_list):
        if self.paddle.paddle_w > 35:
            self.paddle.paddle_w = self.paddle.paddle_w - 35
            self.paddle.paddle.width = self.paddle.paddle_w
        self.modifications_list.pop(paddle_hit_index)
        rect_modifications_list.pop(paddle_hit_index)

    def enlarge_paddle(self, paddle_hit_index, rect_modifications_list):
        if self.paddle.paddle_w < 1000 and self.paddle.paddle.centerx < 600:
            self.paddle.paddle_w = self.paddle.paddle_w + 20
            self.paddle.paddle.width = self.paddle.paddle_w
        elif self.paddle.paddle_w < 1000 and self.paddle.paddle.centerx >= 600:
            self.paddle.paddle.left -= 20
            self.paddle.paddle_w = self.paddle.paddle_w + 20
            self.paddle.paddle.width = self.paddle.paddle_w
        self.modifications_list.pop(paddle_hit_index)
        rect_modifications_list.pop(paddle_hit_index)

    def create_new_ball(self, paddle_hit_index, rect_modifications_list):
        new_ball = Ball()
        new_ball.ball.x = self.paddle.paddle.centerx
        self.ball_list.append(new_ball)
        self.modifications_list.pop(paddle_hit_index)
        rect_modifications_list.pop(paddle_hit_index)

    def create_block_paddle(self, paddle_hit_index, rect_modifications_list):
        with open("configs/modifications.yaml", encoding="utf-8") as modifications:
            mod_data = yaml.safe_load(modifications)
        if len(self.block_paddle_list) == 0:
            self.block_paddle_list.append(pygame.Rect(0, 740,
                                                      mod_data["modifications"]["block_paddle_width"],
                                                      mod_data["modifications"]["block_paddle_height"]))
        self.modifications_list.pop(paddle_hit_index)
        rect_modifications_list.pop(paddle_hit_index)

    def game_over(self, sc):
        while True:
            self.home_button.draw_button(sc)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.button.collidepoint(event.pos):
                        return True
            pygame.display.update()
