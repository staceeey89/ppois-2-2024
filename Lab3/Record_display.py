import pygame
import yaml
from Button import Button


class Record_display:
    def __init__(self):
        self.home_button = Button(100, 25, "Домой", "white", 48, 700)
        self.next_button = Button(100, 25, "След", "white", 650, 700)
        self.prev_button = Button(100, 25, "Пред", "white", 500, 700)

    def show_record_display(self, sc):
        with open("configs/records.yaml", encoding="utf-8") as file:
            records_data = yaml.safe_load(file)

        pygame.init()
        num = 0

        while True:
            sc.fill((0, 0, 0))
            self.draw_buttons(sc)

            # Создать поверхность для каждого элемента в списке `records`
            self.draw_records(records_data, num, sc)

            self.draw_name_level(records_data, num, sc)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.button.collidepoint(event.pos):
                        return True
                    elif self.next_button.button.collidepoint(event.pos):
                        num += 1
                        if num > 9:
                            num = 0
                    elif self.prev_button.button.collidepoint(event.pos):
                        num -= 1
                        if num < 0:
                            num = 9

                # Обновить экран
                pygame.display.update()

    def draw_buttons(self, sc):
        self.home_button.draw_button(sc)
        self.next_button.draw_button(sc)
        self.prev_button.draw_button(sc)

    def draw_name_level(self, records_data, num, sc):
        level = records_data["records"][num]
        font = pygame.font.SysFont("Arial", level["size"])
        level_name = font.render(str(level["text"]), True, "white")
        sc.blit(level_name, (level["x_pos"], level["y_pos"]))

    def draw_records(self, records_data, num, sc):
        for i in range(1, 11):
            level = records_data["records"][num]
            font = pygame.font.SysFont("Arial", level[i]["size"])

            # Отрисовываем имя и время рекордсмена
            name_record = font.render(str(level[i]["name"]), True, "white")
            time_record = font.render(str(level[i]["time"]), True, "white")
            # Создать новую поверхность для объединенного текста
            combined_text = pygame.Surface(
                (name_record.get_width() + time_record.get_width() + 10,
                 max(name_record.get_height(), time_record.get_height())))
            combined_text.fill((0, 0, 0))  # Заполнить поверхность черным цветом

            # Нарисовать два элемента на объединенной поверхности
            combined_text.blit(name_record, (0, 0))
            combined_text.blit(time_record, (name_record.get_width() + 10, 0))

            # Отобразить объединенную поверхность на экране
            sc.blit(combined_text, (level[i]["x_pos"], level[i]["y_pos"]))
