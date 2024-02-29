from Actor import Actor


class Studio:
    def __init__(self, name="", person_number=0):
        self._name = str(name)
        self._person_number = int(person_number)
        self._list_young_persons = []
        self._list_old_persons = []
        self._need_young_number = 0
        self._need_old_number = 0

    def get_name(self):
        return self._name

    def get_person_number(self):
        return self._person_number

    def get_list_young_persons(self):
        return self._list_young_persons

    def get_list_old_persons(self):
        return self._list_old_persons

    # Проверка на заполненность
    def compare_numbers_people(self):
        return len(self._list_old_persons)+len(self._list_young_persons) < self._person_number

    # Меняет кол-во актеров-молодых и актеров-стариков
    def set_young_old_numbers(self, new_young, new_old):
        if new_old + new_young == self._person_number:
            while new_young < len(self._list_young_persons):
                del self._list_young_persons[-1]

            while new_old < len(self._list_old_persons):
                del self._list_old_persons[-1]

            self._need_young_number = new_young
            self._need_old_number = new_old
            return True
        else:
            return False

    def set_young_old_numbers_for_post(self, new_young, new_old, full_number):
        if new_old + new_young == full_number:
            while new_young < len(self._list_young_persons):
                del self._list_young_persons[-1]

            while new_old < len(self._list_old_persons):
                del self._list_old_persons[-1]

            self._need_young_number = new_young
            self._need_old_number = new_old
            return True
        else:
            return False

    def set_number_actor_helper(self):
        while ((len(self._list_old_persons) < self._need_old_number) or
               (len(self._list_young_persons) < self._need_young_number)):
            while True:
                try:
                    actor_name = str(input("Имя актера: "))
                    actor_age = int(input("Возраст, до 40 - молодой, после 40 - взрослый "))
                    break
                except ValueError:
                    print("Введите целое число.")
            if (actor_age <= 40) and (len(self._list_young_persons) < self._need_young_number):
                self.add_person(Actor(actor_name, actor_age))
            elif (actor_age > 40) and (len(self._list_old_persons) < self._need_old_number):
                self.add_person(Actor(actor_name, actor_age))
            elif len(self._list_old_persons)+len(self._list_young_persons) == self._person_number:
                print("Заполнено")
                return False
            else:
                print("Невозможно добавить актера.")

        return True

    def set_number_people(self, number, script):
        if number >= 0:
            while True:
                try:
                    print("Введите новое кол-во старых актеров: ")
                    old_number = int(input())
                    print("Введите новое кол-во молодых актеров: ")
                    young_number = int(input())
                    break
                except ValueError:
                    print("Введите целое число.")

            if old_number + young_number == number:
                self.set_young_old_numbers_for_post(young_number, old_number, number)
                script.set_actors_number(number)
                self._person_number = number
                if self.set_number_actor_helper():
                    print("Количество человек изменено.")
                    return True
            else:
                print("Количество старых и молодых актеров не совпадает с общим.")
                return False
        else:
            print("Кол-во актеров не может быть отрицательным.")
            return False

    # Добавляет нового актера
    def add_person(self, actor):
        # Проверка на переполненность молодых
        if ((actor.get_age() > 1) and (actor.get_age() <= 40) and
                (len(self._list_young_persons) + 1 <= self._need_young_number)):
            self._list_young_persons.append(actor)
            print("Молодой актер добавлен.")
        # Проверка на переполненность старых
        elif ((actor.get_age() > 40) and (actor.get_age() <= 100) and
              (len(self._list_old_persons) + 1 <= self._need_old_number)):
            self._list_old_persons.append(actor)
            print("Взрослый актер добавлен.")
        else:
            print("Невозможно добавить актера.")
            return False

        if len(self._list_old_persons) == self._need_old_number:
            print("Список взрослых заполнен.")

        if len(self._list_young_persons) == self._need_young_number:
            print("Список молодых заполнен.")

        return True
