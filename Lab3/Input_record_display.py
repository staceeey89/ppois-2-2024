import pygame
import yaml

from Button import Button
from Input_field import Input_field


class Input_record_display:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.record_text = self.font.render(f"Введите имя:", True, "white")
        self.inp_field = Input_field()
        self.add_record_button = Button(100, 50, "Добавить", "white", 520, 350)

    def draw_record_field(self, sc, level_num, int_record_time, str_record_time):
        # Кнопка ввода рекорда
        empty_text = ""
        font = pygame.font.SysFont("Arial", 30)
        empty_input_text = font.render(empty_text, True, "white")
        while True:
            sc.fill((0, 0, 0))
            sc.blit(self.record_text, (500, 250))
            sc.blit(empty_input_text, (100, 100))
            self.add_record_button.draw_button(sc)
            self.inp_field.print_input(sc)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.inp_field.bg_block.collidepoint(event.pos):
                        self.inp_field.make_active()
                        self.inp_field.fill_input(sc)
                    elif (self.add_record_button.button.collidepoint(event.pos)
                          and len(self.inp_field.user_text) == 0):
                        empty_text = "Ник не может быть пустым!"
                        empty_input_text = font.render(empty_text, True, "white")
                    elif (self.add_record_button.button.collidepoint(event.pos)
                          and len(self.inp_field.user_text) > 0):
                        self.add_new_record(level_num, self.inp_field.user_text, int_record_time, str_record_time)
                        return

                self.inp_field.update_text(event, sc)

            pygame.display.flip()
            # clock.tick(60) means that for every second at most
            # 60 frames should be passed.
            self.clock.tick(60)

    def add_new_record(self, level_num, new_name, int_record_time, str_record_time):
        with open("configs/records.yaml", encoding="utf-8") as file:
            records_data = yaml.safe_load(file)

        prev_el = []
        temp_el = []

        prev_el.append(records_data["records"][level_num][1]["name"])
        prev_el.append(records_data["records"][level_num][1]["int_time"])
        prev_el.append(records_data["records"][level_num][1]["time"])

        records_data["records"][level_num][1]["int_time"] = int_record_time
        records_data["records"][level_num][1]["name"] = new_name
        records_data["records"][level_num][1]["time"] = str_record_time

        for i in range(2, 11):
            temp_el.append(records_data["records"][level_num][i]["name"])
            temp_el.append(records_data["records"][level_num][i]["int_time"])
            temp_el.append(records_data["records"][level_num][i]["time"])

            records_data["records"][level_num][i]["name"] = prev_el[0]
            records_data["records"][level_num][i]["int_time"] = prev_el[1]
            records_data["records"][level_num][i]["time"] = prev_el[2]

            prev_el = temp_el
            temp_el = []

        with open('configs/records.yaml', 'w') as file:
            yaml.dump(records_data, file)




