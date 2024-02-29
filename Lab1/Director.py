class Director:
    def __init__(self, name=""):
        self._name = str(name)
        self._experience = 0

    def change_experience(self, number, script):
        if (number == 0) and (number >= script.get_experience_director()):
            self._experience = number
            print("Опыт режиссера начальный.")
            return True
        elif (number == 1) and (number >= script.get_experience_director()):
            print("Опыт режиссера средний.")
            self._experience = number
            return True
        elif (number == 2) and (number >= script.get_experience_director()):
            print("Опыт режиссера профессиональный.")
            self._experience = number
            return True
        else:
            print("Некорректное значение!")
            return False

    def get_name(self):
        return self._name

    def get_experience(self):
        return self._experience
