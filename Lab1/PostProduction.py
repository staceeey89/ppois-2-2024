class PostProduction:
    def __init__(self):
        self._message = None

    # Удаляет кадр
    def del_shot(self, number_message, montage):
        if (number_message - 1 < len(montage.get_shot_list())) and (number_message - 1 >= 0):
            del montage.get_shot_list()[number_message - 1]
            print("Кадр удален.")
            return True
        else:
            print("Такого кадра не существует.")
            return False

    # Передвигает кадр на указанную новую позицию
    def change_shot_place(self, new_number, old_number, montage):
        if ((old_number - 1 < len(montage.get_shot_list())) and (old_number - 1 >= 0)
                and (new_number - 1 < len(montage.get_shot_list())) and (new_number - 1 >= 0)):
            self._message = montage.get_shot_list().pop(old_number - 1)
            montage.get_shot_list().insert(new_number - 1, self._message)
            print("Кадр передвинут с позиции ", old_number, " на позицию ", new_number)
            return True
        else:
            print("Позиции не должны выходить за пределы.")
            return False

    def print_list_shot(self, montage):
        print("Список кадров:")
        num_shot = 1
        for message in montage.get_shot_list():
            print(num_shot, ". ", message)
            num_shot += 1
        return True

    def make_realization(self, studio, script, director, montage):
        print("Фильм: ", script.get_name())
        print("Тип: ", script.get_film_type())
        print("Список участников: ")
        number = 1
        # Выводим список актеров
        for person in studio.get_list_young_persons():
            print(number, ". Имя: ", person.get_name(), ", Возраст: ", person.get_age())
            number += 1

        for person in studio.get_list_old_persons():
            print(number, ". Имя: ", person.get_name(), ", Возраст: ", person.get_age())
            number += 1

        if director.get_experience() == 0:
            print("Режиссер: ", director.get_name(), ". Опыт: начальный.")
        elif director.get_experience() == 1:
            print("Режиссер: ", director.get_name(), ". Опыт: средний.")
        elif director.get_experience() == 2:
            print("Режиссер: ", director.get_name(), ". Опыт: профессиональный.")
        else:
            print("Режиссера нет.")

        print("Описание:")
        print(script.get_plot())

        print("Список всех кадров:")
        for shot in montage.get_shot_list():
            print(shot)
        return True
